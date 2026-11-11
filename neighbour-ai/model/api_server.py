import json
import os
import traceback
import threading
import uuid

from http.server import (
    BaseHTTPRequestHandler,
    ThreadingHTTPServer
)

import torch

from model.predict import (
    load_tokenizer,
    load_model,
    analyze_command
)

from model.api_client import (
    NeighbourManagementAPI
)

from model.router import (
    CommandRouter
)


# ============================================================
# SERVER
# ============================================================

HOST = "0.0.0.0"

PORT = int(os.environ.get("PORT", "8000"))


# ============================================================
# GLOBALS
# ============================================================

DEVICE = None

TOKENIZER = None

MODEL = None

API = None

ROUTER = None


# ============================================================
# CONVERSATIONAL CONFIRMATION MEMORY
# ============================================================

PENDING_CONFIRMATIONS = {}

PENDING_CONFIRMATIONS_LOCK = threading.Lock()


# ============================================================
# CONVERSATION HISTORY MEMORY
#
# Separate from pending confirmations.
# This only records session conversation information.
# It does not change NLP, fuzzy matching, confidence,
# routing, validation, cleanup, or safety behavior.
# ============================================================

SESSION_CONVERSATIONS = {}

SESSION_CONVERSATIONS_LOCK = threading.Lock()

MAX_CONVERSATION_HISTORY = 20


def record_conversation(
    session_id,
    command,
    analysis=None,
    execution=None,
    message=None
):

    if not session_id:

        return


    analysis = (
        analysis
        if isinstance(analysis, dict)
        else {}
    )


    execution = (
        execution
        if isinstance(execution, dict)
        else {}
    )


    entities = analysis.get(
        "entities",
        {}
    )


    if not isinstance(
        entities,
        dict
    ):

        entities = {}


    record = {

        "command":
            command,

        "intent":
            analysis.get(
                "intent"
            ),

        "state":
            entities.get(
                "state"
            ),

        "jc":
            entities.get(
                "jc"
            ),

        "confidence":
            analysis.get(
                "confidence"
            ),

        "result_status":
            execution.get(
                "status"
            ),

        "message":
            message
    }


    with SESSION_CONVERSATIONS_LOCK:

        conversation = (
            SESSION_CONVERSATIONS
            .setdefault(
                session_id,
                {

                    "history":
                        [],

                    "last_command":
                        None,

                    "last_intent":
                        None,

                    "last_state":
                        None,

                    "last_jc":
                        None,

                    "last_result":
                        None
                }
            )
        )


        conversation[
            "history"
        ].append(
            record
        )


        if len(
            conversation["history"]
        ) > MAX_CONVERSATION_HISTORY:

            conversation[
                "history"
            ] = conversation[
                "history"
            ][
                -MAX_CONVERSATION_HISTORY:
            ]


        conversation[
            "last_command"
        ] = command


        conversation[
            "last_intent"
        ] = record[
            "intent"
        ]


        if record["state"]:

            conversation[
                "last_state"
            ] = record[
                "state"
            ]


        if record["jc"]:

            conversation[
                "last_jc"
            ] = record[
                "jc"
            ]


        conversation[
            "last_result"
        ] = {

            "status":
                record[
                    "result_status"
                ],

            "message":
                message
        }

# ============================================================
# CONVERSATION CONTEXT
#
# Uses existing per-session conversation history.
# Only fills missing State/JC values.
# Explicit State/JC in the current command always wins.
# ============================================================

def get_session_context(
    session_id
):

    if not session_id:

        return {}


    with SESSION_CONVERSATIONS_LOCK:

        conversation = (
            SESSION_CONVERSATIONS.get(
                session_id,
                {}
            )
        )


        if not isinstance(
            conversation,
            dict
        ):

            return {}


        return {

            "state":
                conversation.get(
                    "last_state"
                ),

            "jc":
                conversation.get(
                    "last_jc"
                )
        }


def resolve_conversation_context(
    session_id,
    analysis
):

    if not isinstance(
        analysis,
        dict
    ):

        return analysis


    entities = analysis.get(
        "entities"
    )


    if not isinstance(
        entities,
        dict
    ):

        entities = {}

        analysis["entities"] = entities


    state = entities.get(
        "state"
    )

    jc = entities.get(
        "jc"
    )


    # --------------------------------------------------------
    # Never overwrite State + JC explicitly supplied
    # in the current command.
    # --------------------------------------------------------

    if state and jc:

        return analysis


    context = get_session_context(
        session_id
    )


    context_used = False


    # --------------------------------------------------------
    # Fill only missing State
    # --------------------------------------------------------

    if not state and context.get(
        "state"
    ):

        entities["state"] = (
            context["state"]
        )

        context_used = True


    # --------------------------------------------------------
    # Fill only missing JC
    # --------------------------------------------------------

    if not jc and context.get(
        "jc"
    ):

        entities["jc"] = (
            context["jc"]
        )

        context_used = True


    # --------------------------------------------------------
    # Update analysis
    # --------------------------------------------------------

    if context_used:

        analysis["entities"] = entities

        analysis["context_used"] = True


        missing = analysis.get(
            "missing"
        )


        if isinstance(
            missing,
            list
        ):

            analysis["missing"] = [

                item

                for item in missing

                if str(item).strip().lower()

                not in (

                    "state",

                    "jc"
                )
            ]


    return analysis






# ============================================================
# ENTITY CONFIDENCE SETTINGS
# ============================================================

ENTITY_CONFIRMATION_THRESHOLD = 0.78


# ============================================================
# SESSION ID
# ============================================================

def get_session_id(
    payload
):

    session_id = payload.get(
        "session_id"
    )


    if isinstance(
        session_id,
        str
    ):

        session_id = session_id.strip()


        if session_id:

            return session_id


    return str(
        uuid.uuid4()
    )


# ============================================================
# YES / NO DETECTION
# ============================================================

def get_confirmation_reply(
    command
):

    normalized = command.strip().lower()


    yes_values = {

        "yes",
        "y",
        "yeah",
        "yep",
        "confirm",
        "confirmed",
        "correct",
        "proceed"
    }


    no_values = {

        "no",
        "n",
        "nope",
        "cancel",
        "incorrect",
        "wrong"
    }


    if normalized in yes_values:

        return "YES"


    if normalized in no_values:

        return "NO"


    return None


# ============================================================
# ENTITY CLARIFICATION CHECK
# ============================================================

def get_low_confidence_entities(
    analysis
):

    entities = analysis.get(
        "entities",
        {}
    )


    entity_confidence = analysis.get(
        "entity_confidence",
        {}
    )


    low_confidence = {}


    for key in (

        "state",

        "jc"
    ):

        entity = entities.get(
            key
        )


        confidence = entity_confidence.get(
            key
        )


        if not entity:

            continue


        if confidence is None:

            continue


        try:

            confidence = float(
                confidence
            )

        except (
            TypeError,
            ValueError
        ):

            continue


        if confidence < ENTITY_CONFIRMATION_THRESHOLD:

            low_confidence[key] = {

                "value":
                    entity,

                "confidence":
                    confidence
            }


    return low_confidence


# ============================================================
# CLARIFICATION MESSAGE
# ============================================================

def build_confirmation_message(
    analysis,
    low_confidence
):

    entities = analysis.get(
        "entities",
        {}
    )


    suggestions = []


    if entities.get(
        "state"
    ):

        suggestions.append(

            f"State: "
            f"{entities['state']}"
        )


    if entities.get(
        "jc"
    ):

        suggestions.append(

            f"JC: "
            f"{entities['jc']}"
        )


    if not suggestions:

        return (

            "I am not fully confident about "
            "the location. Please provide the "
            "correct State and JC."
        )


    return (

        "I am not fully confident about the "
        "location you entered. Did you mean:\n\n"

        + "\n".join(
            suggestions
        )

        + "\n\nPlease reply Yes to continue "
        "or No to cancel."
    )


# ============================================================
# PENDING CONFIRMATION RESPONSE
# ============================================================

def build_confirmation_response(
    command,
    session_id,
    analysis,
    low_confidence
):

    message = build_confirmation_message(

        analysis,

        low_confidence
    )


    return {

        "status":
            "CONFIRMATION_REQUIRED",

        "message":
            message,

        "command":
            command,

        "session_id":
            session_id,

        "intent":
            analysis.get(
                "intent"
            ),

        "confidence":
            analysis.get(
                "confidence"
            ),

        "entities":
            analysis.get(
                "entities"
            ),

        "entity_confidence":
            analysis.get(
                "entity_confidence"
            ),

        "low_confidence_entities":
            low_confidence,

        "missing":
            analysis.get(
                "missing"
            ),

        "entity_validation":
            analysis.get(
                "entity_validation"
            ),

        "entity_errors":
            analysis.get(
                "entity_errors"
            ),

        "analysis":
            analysis,

        "execution":
            {

                "status":
                    "CONFIRMATION_REQUIRED"
            }
    }


# ============================================================
# INITIALIZE
# ============================================================

def initialize_ai():

    global DEVICE
    global TOKENIZER
    global MODEL
    global API
    global ROUTER


    print(
        "=" * 60
    )

    print(
        "NEIGHBOUR MANAGEMENT AI HTTP SERVER"
    )

    print(
        "=" * 60
    )


    DEVICE = (

        torch.device(
            "cuda"
        )

        if torch.cuda.is_available()

        else

        torch.device(
            "cpu"
        )
    )


    print()

    print(
        "Device:",
        DEVICE
    )


    TOKENIZER = load_tokenizer()

    print(
        "Tokenizer loaded."
    )

    print(
        "Vocabulary:",
        len(TOKENIZER)
    )


    MODEL = load_model(
        DEVICE
    )

    print(
        "Trained model loaded."
    )


    API = NeighbourManagementAPI()

    print(
        "Live database API client created."
    )


    try:

        states = API.get_states()

        print(
            "Live database connected."
        )

        print(
            "Available states:",
            len(states)
        )

    except Exception as error:

        print(
            "WARNING: Could not connect "
            "to Spring Boot API."
        )

        print(
            "Make sure Spring Boot is running "
            "on http://localhost:8080"
        )

        print(
            "Details:",
            error
        )


    ROUTER = CommandRouter(
        API
    )


    print(
        "Command router loaded."
    )


    print()

    print(
        "=" * 60
    )

    print(
        "AI HTTP SERVER READY"
    )

    print(
        "=" * 60
    )

    print(
        f"Server: http://localhost:{PORT}"
    )

    print(
        f"Chat:   http://localhost:{PORT}/chat"
    )

    print(
        f"Health: http://localhost:{PORT}/health"
    )

    print(
        "=" * 60
    )


# ============================================================
# SEND JSON
# ============================================================

def send_json(
    handler,
    status_code,
    data
):

    response_body = json.dumps(
        data,
        indent=2,
        default=str
    ).encode(
        "utf-8"
    )


    handler.send_response(
        status_code
    )


    handler.send_header(
        "Content-Type",
        "application/json; charset=utf-8"
    )


    handler.send_header(
        "Content-Length",
        str(
            len(response_body)
        )
    )


    handler.send_header(
        "Access-Control-Allow-Origin",
        "*"
    )


    handler.send_header(
        "Access-Control-Allow-Methods",
        "GET, POST, OPTIONS"
    )


    handler.send_header(
        "Access-Control-Allow-Headers",
        "Content-Type"
    )


    handler.end_headers()


    handler.wfile.write(
        response_body
    )


# ============================================================
# BUILD MESSAGE
# ============================================================

def build_message(
    analysis,
    execution
):

    if not isinstance(
        execution,
        dict
    ):

        return (
            "Command processed."
        )


    status = execution.get(
        "status"
    )


    intent = analysis.get(
        "intent"
    )


    # ========================================================
    # ERROR
    # ========================================================

    if status in (

        "ERROR",

        "AMBIGUOUS",

        "MISSING_INFORMATION",

        "INVALID_ENTITY",

        "INVALID_AUTOMATION_CONFIGURATION",

        "SAFETY_BLOCKED",

        "DIRECT_CLEANUP_DISABLED",

        "OUT_OF_SCOPE",

        "UNKNOWN_INTENT"
    ):

        return execution.get(

            "message",

            "The command could not be executed."
        )


    # ========================================================
    # STATES
    # ========================================================

    if intent == "GET_STATES":

        states = execution.get(
            "states",
            []
        )


        if not states:

            return (
                "No states were found "
                "in the database."
            )


        lines = [

            "Available States:",

            ""
        ]


        for index, state in enumerate(
            states,
            start=1
        ):

            lines.append(
                f"{index}. {state}"
            )


        lines.append("")

        lines.append(

            f"Total states: "
            f"{len(states)}"
        )


        return "\n".join(
            lines
        )


    # ========================================================
    # JCS
    # ========================================================

    if intent == "GET_JCS":

        jcs = execution.get(
            "jcs",
            []
        )

        state = execution.get(
            "state"
        )


        if not jcs:

            if state:

                return (
                    f"No JCs were found "
                    f"for {state}."
                )

            return (
                "No JCs were found."
            )


        title = (

            f"JCs in {state}:"

            if state

            else

            "Available JCs:"
        )


        lines = [

            title,

            ""
        ]


        for index, jc in enumerate(
            jcs,
            start=1
        ):

            lines.append(
                f"{index}. {jc}"
            )


        lines.append("")

        lines.append(

            f"Total JCs: "
            f"{len(jcs)}"
        )


        return "\n".join(
            lines
        )


    # ========================================================
    # COUNTS
    # ========================================================

    if intent in (
        "GET_COUNTS",
        "GET_NEIGHBOURS"
    ):

        return (

            "Neighbour Statistics\n\n"

            f"State: "
            f"{execution.get('state', '')}\n"

            f"JC: "
            f"{execution.get('jc', '')}\n\n"

            f"Total neighbours: "
            f"{execution.get('total', 0)}\n"

            f"Valid neighbours: "
            f"{execution.get('valid', 0)}\n"

            f"Invalid neighbours: "
            f"{execution.get('invalid', 0)}"
        )


    # ========================================================
    # INVALID PERCENTAGE
    # ========================================================

    if intent == "GET_INVALID_PERCENTAGE":

        return (

            "Invalid Neighbour Percentage\n\n"

            f"State: "
            f"{execution.get('state', '')}\n"

            f"JC: "
            f"{execution.get('jc', '')}\n\n"

            f"Total neighbours: "
            f"{execution.get('total', 0)}\n"

            f"Invalid neighbours: "
            f"{execution.get('invalid', 0)}\n"

            f"Invalid percentage: "
            f"{execution.get('invalid_percentage', 0)}%"
        )


    # ========================================================
    # INVALID NEIGHBOURS
    # ========================================================

    if intent == "GET_INVALID_NEIGHBOURS":

        invalid = execution.get(
            "invalidNeighbours",
            []
        )


        if not invalid:

            return (

                f"No invalid neighbours found "
                f"for "
                f"{execution.get('state', '')} "
                f"{execution.get('jc', '')}."
            )


        lines = [

            "Invalid Neighbours:",

            ""
        ]


        for item in invalid:

            lines.append(

                "Neighbour ID: "
                +
                str(
                    item.get(
                        "neighbourId",
                        "N/A"
                    )
                )
            )


            lines.append(

                "Source Cell: "
                +
                str(
                    item.get(
                        "sourceCell",
                        "N/A"
                    )
                )
            )


            lines.append(

                "Target Cell: "
                +
                str(
                    item.get(
                        "targetCell",
                        "N/A"
                    )
                )
            )


            failed = item.get(
                "failedRules",
                []
            )


            lines.append(

                "Failed Rules: "
                +
                ", ".join(
                    map(
                        str,
                        failed
                    )
                )
            )


            lines.append("")


        lines.append(

            f"Total invalid neighbours: "
            f"{len(invalid)}"
        )


        return "\n".join(
            lines
        )


    # ========================================================
    # PCI
    # ========================================================

    if intent == "GET_PCI_INVALID":

        validation = execution.get(
            "validation",
            {}
        )


        results = validation.get(
            "results",
            []
        )


        pci_invalid = [

            item

            for item in results

            if "PCI" in item.get(
                "failedRules",
                []
            )
        ]


        if not pci_invalid:

            return (

                f"No PCI-invalid neighbours "
                f"found for "
                f"{execution.get('state', '')} "
                f"{execution.get('jc', '')}."
            )


        lines = [

            "PCI Invalid Neighbours:",

            ""
        ]


        for item in pci_invalid:

            lines.append(

                f"Neighbour ID: "
                f"{item.get('neighbourId', 'N/A')}"
            )

            lines.append(

                f"Source PCI: "
                f"{item.get('sourcePci', 'N/A')}"
            )

            lines.append(

                f"Target PCI: "
                f"{item.get('targetPci', 'N/A')}"
            )

            lines.append("")


        lines.append(

            f"Total PCI-invalid neighbours: "
            f"{len(pci_invalid)}"
        )


        return "\n".join(
            lines
        )


    # ========================================================
    # TAC
    # ========================================================

    if intent == "GET_TAC_INVALID":

        validation = execution.get(
            "validation",
            {}
        )


        results = validation.get(
            "results",
            []
        )


        tac_invalid = [

            item

            for item in results

            if "TAC" in item.get(
                "failedRules",
                []
            )
        ]


        if not tac_invalid:

            return (

                f"No TAC-invalid neighbours "
                f"found for "
                f"{execution.get('state', '')} "
                f"{execution.get('jc', '')}."
            )


        lines = [

            "TAC Invalid Neighbours:",

            ""
        ]


        for item in tac_invalid:

            lines.append(

                f"Neighbour ID: "
                f"{item.get('neighbourId', 'N/A')}"
            )

            lines.append(

                f"Source TAC: "
                f"{item.get('sourceTac', 'N/A')}"
            )

            lines.append(

                f"Target TAC: "
                f"{item.get('targetTac', 'N/A')}"
            )

            lines.append("")


        lines.append(

            f"Total TAC-invalid neighbours: "
            f"{len(tac_invalid)}"
        )


        return "\n".join(
            lines
        )


    # ========================================================
    # VALIDATION
    # ========================================================

    if intent == "VALIDATE_NEIGHBOURS":

        validation = execution.get(
            "validation",
            {}
        )


        return (

            f"Validation completed for "
            f"{execution.get('state', '')} "
            f"{execution.get('jc', '')}.\n\n"

            f"Total neighbours: "
            f"{validation.get('totalNeighbours', 0)}\n"

            f"Valid: "
            f"{validation.get('validNeighbours', 0)}\n"

            f"Invalid: "
            f"{validation.get('invalidNeighbours', 0)}"
        )


    # ========================================================
    # PREVIEW
    # ========================================================

    if intent == "PREVIEW_CLEANUP":

        safety = execution.get(
            "safety",
            {}
        )


        if (
            isinstance(
                safety,
                dict
            )
            and
            isinstance(
                safety.get(
                    "safety"
                ),
                dict
            )
        ):

            safety = safety[
                "safety"
            ]


        allowed = safety.get(
            "deletionAllowed",
            safety.get(
                "deleteAllowed",
                False
            )
        )


        if allowed:

            return (

                "Cleanup Preview\n\n"

                f"State: "
                f"{execution.get('state', '')}\n"

                f"JC: "
                f"{execution.get('jc', '')}\n"

                f"Minimum neighbours: "
                f"{execution.get('minimum_neighbours', '')}\n\n"

                f"Invalid neighbours: "
                f"{safety.get('invalidNeighbours', 0)}\n"

                f"Neighbours to delete: "
                f"{safety.get('neighboursToDelete', 0)}\n"

                f"Neighbours to retain: "
                f"{safety.get('neighboursToRetain', 0)}\n\n"

                "Deletion is allowed."
            )


        return (

            f"Cleanup is not allowed for "
            f"{execution.get('state', '')} "
            f"{execution.get('jc', '')}."
        )


    # ========================================================
    # CLEANUP
    # ========================================================

    if intent == "START_CLEANUP":

        if status == "CLEANUP_EXECUTED":

            deleted = execution.get(
                "deleted",
                {}
            )


            return (

                "Cleanup completed successfully.\n\n"

                f"State: "
                f"{execution.get('state', '')}\n"

                f"JC: "
                f"{execution.get('jc', '')}\n"

                f"Deleted neighbours: "
                f"{deleted.get('deletedCount', 0)}"
            )


        if status == "NO_DELETION_REQUIRED":

            return (

                f"No deletion was required for "
                f"{execution.get('state', '')} "
                f"{execution.get('jc', '')}."
            )


        return execution.get(
            "message",
            "Cleanup was not executed."
        )


    # ========================================================
    # AUTOMATION CREATED
    # ========================================================

    if status == "AUTOMATION_CREATED":

        return (

            "Automation created successfully.\n\n"

            f"State: "
            f"{execution.get('state', '')}\n"

            f"JC: "
            f"{execution.get('jc', '')}\n"

            f"Frequency: "
            f"{execution.get('frequency', '')}\n"

            f"Execution time: "
            f"{execution.get('execution_time', '')}\n"

            f"Minimum neighbours: "
            f"{execution.get('minimum_neighbours', '')}\n"

            f"Technology flow: "
            f"{execution.get('technology_flow', '')}"
        )


    # ========================================================
    # AUTOMATIONS
    # ========================================================

    if intent == "GET_AUTOMATIONS":

        automations = execution.get(
            "automations",
            []
        )


        if not automations:

            return (
                "No automations are currently configured."
            )


        lines = [

            "Configured Automations:",

            ""
        ]


        for index, automation in enumerate(
            automations,
            start=1
        ):

            if not isinstance(
                automation,
                dict
            ):

                lines.append(
                    f"{index}. {automation}"
                )

                continue


            name = automation.get(
                "name",
                "Unnamed automation"
            )


            state = automation.get(
                "state",
                "N/A"
            )


            jc = automation.get(
                "jc",
                "N/A"
            )


            frequency = automation.get(
                "frequency",
                "N/A"
            )


            execution_time = automation.get(

                "executionTime",

                automation.get(
                    "execution_time",
                    "N/A"
                )
            )


            minimum = automation.get(

                "minimumNeighbours",

                automation.get(
                    "minimum_neighbours",
                    "N/A"
                )
            )


            technology = automation.get(

                "technologyFlow",

                automation.get(
                    "technology_flow",
                    "N/A"
                )
            )


            status_value = automation.get(
                "status",
                "N/A"
            )


            lines.append(
                f"{index}. {name}"
            )

            lines.append(
                f"   State: {state}"
            )

            lines.append(
                f"   JC: {jc}"
            )

            lines.append(
                f"   Frequency: {frequency}"
            )

            lines.append(
                f"   Execution time: "
                f"{execution_time}"
            )

            lines.append(
                f"   Minimum neighbours: "
                f"{minimum}"
            )

            lines.append(
                f"   Technology flow: "
                f"{technology}"
            )

            lines.append(
                f"   Status: {status_value}"
            )

            lines.append("")


        lines.append(

            f"Total automations: "
            f"{len(automations)}"
        )


        return "\n".join(
            lines
        )


    # ========================================================
    # SUCCESS FALLBACK
    # ========================================================

    if status == "SUCCESS":

        return execution.get(

            "message",

            "Command completed successfully."
        )


    return execution.get(

        "message",

        f"Command completed with status: {status}"
    )


# ============================================================
# HTTP HANDLER
# ============================================================

class AIRequestHandler(
    BaseHTTPRequestHandler
):


    def log_message(
        self,
        format,
        *args
    ):

        print(
            f"[AI SERVER] {format % args}"
        )


    # ========================================================
    # OPTIONS
    # ========================================================

    def do_OPTIONS(
        self
    ):

        self.send_response(
            204
        )


        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )


        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, POST, OPTIONS"
        )


        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )


        self.end_headers()


    # ========================================================
    # GET
    # ========================================================

    def do_GET(
        self
    ):

        if self.path == "/":

            send_json(

                self,

                200,

                {
                    "status":
                        "SUCCESS",

                    "service":
                        "Neighbour Management AI",

                    "message":
                        "AI HTTP server is running."
                }
            )

            return


        if self.path == "/health":

            send_json(

                self,

                200,

                {
                    "status":
                        "UP",

                    "ai":
                        MODEL is not None,

                    "router":
                        ROUTER is not None,

                    "springBootAPI":
                        API is not None
                }
            )

            return


        send_json(

            self,

            404,

            {
                "status":
                    "NOT_FOUND",

                "message":
                    "Endpoint not found."
            }
        )


    # ========================================================
    # POST CHAT
    # ========================================================

    def do_POST(
        self
    ):

        if self.path != "/chat":

            send_json(

                self,

                404,

                {
                    "status":
                        "NOT_FOUND",

                    "message":
                        "Endpoint not found."
                }
            )

            return


        try:

            content_length = int(

                self.headers.get(
                    "Content-Length",
                    "0"
                )
            )


            if content_length <= 0:

                send_json(

                    self,

                    400,

                    {
                        "status":
                            "ERROR",

                        "message":
                            "Request body is required."
                    }
                )

                return


            body = self.rfile.read(
                content_length
            )


            payload = json.loads(
                body.decode(
                    "utf-8"
                )
            )


            session_id = get_session_id(
                payload
            )


            command = payload.get(
                "command"
            )


            if not isinstance(
                command,
                str
            ):

                send_json(

                    self,

                    400,

                    {
                        "status":
                            "ERROR",

                        "message":
                            "Field 'command' is required."
                    }
                )

                return


            command = command.strip()


            if not command:

                send_json(

                    self,

                    400,

                    {
                        "status":
                            "ERROR",

                        "message":
                            "Command cannot be empty."
                    }
                )

                return


            # =================================================
            # PENDING CONVERSATIONAL CONFIRMATION
            # =================================================

            confirmation_reply = get_confirmation_reply(
                command
            )


            with PENDING_CONFIRMATIONS_LOCK:

                pending = PENDING_CONFIRMATIONS.get(
                    session_id
                )


            if pending is not None:

                if confirmation_reply == "YES":

                    with PENDING_CONFIRMATIONS_LOCK:

                        pending = (
                            PENDING_CONFIRMATIONS.pop(
                                session_id,
                                None
                            )
                        )


                    if pending is not None:

                        analysis = pending.get(
                            "analysis"
                        )


                        execution = ROUTER.route(
                            analysis
                        )


                        message = build_message(

                            analysis,

                            execution
                        )


                        record_conversation(

                            session_id,

                            pending.get(
                                "command"
                            ),

                            analysis=analysis,

                            execution=execution,

                            message=message
                        )


                        response = {

                            "status":
                                execution.get(
                                    "status",
                                    "SUCCESS"
                                ),

                            "message":
                                message,

                            "command":
                                pending.get(
                                    "command"
                                ),

                            "session_id":
                                session_id,

                            "intent":
                                analysis.get(
                                    "intent"
                                ),

                            "confidence":
                                analysis.get(
                                    "confidence"
                                ),

                            "entities":
                                analysis.get(
                                    "entities"
                                ),

                            "entity_confidence":
                                analysis.get(
                                    "entity_confidence"
                                ),

                            "missing":
                                analysis.get(
                                    "missing"
                                ),

                            "entity_validation":
                                analysis.get(
                                    "entity_validation"
                                ),

                            "entity_errors":
                                analysis.get(
                                    "entity_errors"
                                ),

                            "analysis":
                                analysis,

                            "execution":
                                execution
                        }


                        send_json(

                            self,

                            200,

                            response
                        )


                        return


                elif confirmation_reply == "NO":

                    with PENDING_CONFIRMATIONS_LOCK:

                        PENDING_CONFIRMATIONS.pop(

                            session_id,

                            None
                        )


                    record_conversation(

                        session_id,

                        command,

                        analysis=pending.get(
                            "analysis",
                            {}
                        ),

                        execution={
                            "status":
                                "CONFIRMATION_CANCELLED"
                        },

                        message=(
                            "Okay. The command was not executed. "
                            "Please enter the correct command."
                        )
                    )


                    send_json(

                        self,

                        200,

                        {

                            "status":
                                "CONFIRMATION_CANCELLED",

                            "message":
                                "Okay. The command was not executed. "
                                "Please enter the correct command.",

                            "command":
                                command,

                            "session_id":
                                session_id
                        }
                    )


                    return


                else:

                    send_json(

                        self,

                        200,

                        {

                            "status":
                                "CONFIRMATION_REQUIRED",

                            "message":
                                "Please reply Yes to continue with "
                                "the suggested State and JC, or No "
                                "to cancel.",

                            "command":
                                command,

                            "session_id":
                                session_id,

                            "entities":
                                pending.get(
                                    "analysis",
                                    {}
                                ).get(
                                    "entities"
                                )
                        }
                    )


                    return


            if (
                MODEL is None
                or
                TOKENIZER is None
                or
                API is None
                or
                ROUTER is None
            ):

                send_json(

                    self,

                    503,

                    {
                        "status":
                            "ERROR",

                        "message":
                            "AI service is not initialized."
                    }
                )

                return


            # =================================================
            # AI ANALYSIS
            # =================================================

            analysis = analyze_command(

                command,

                MODEL,

                TOKENIZER,

                DEVICE,

                API
            )

            # =================================================
            # CONVERSATION CONTEXT
            #
            # Fill missing State/JC from the same session before
            # confidence handling and routing.
            #
            # Explicit current command values always win.
            # =================================================

            analysis = resolve_conversation_context(

                session_id,

                analysis
            )




            # =================================================
            # ENTITY CONFIDENCE CLARIFICATION
            # =================================================

            low_confidence = (
                get_low_confidence_entities(
                    analysis
                )
            )


            if low_confidence:

                with PENDING_CONFIRMATIONS_LOCK:

                    PENDING_CONFIRMATIONS[
                        session_id
                    ] = {

                        "command":
                            command,

                        "analysis":
                            analysis,

                        "low_confidence":
                            low_confidence
                    }


                response = build_confirmation_response(

                    command,

                    session_id,

                    analysis,

                    low_confidence
                )


                send_json(

                    self,

                    200,

                    response
                )


                return


            # =================================================
            # ROUTER
            # =================================================

            execution = ROUTER.route(
                analysis
            )


            # =================================================
            # MESSAGE
            # =================================================

            message = build_message(

                analysis,

                execution
            )


            # =================================================
            # CONVERSATION HISTORY
            # =================================================

            record_conversation(

                session_id,

                command,

                analysis=analysis,

                execution=execution,

                message=message
            )


            # =================================================
            # FINAL RESPONSE
            # =================================================

            response = {

                "status":
                    execution.get(
                        "status",
                        "SUCCESS"
                    ),

                "message":
                    message,

                "command":
                    command,

                "session_id":
                    session_id,

                "intent":
                    analysis.get(
                        "intent"
                    ),

                "confidence":
                    analysis.get(
                        "confidence"
                    ),

                "entities":
                    analysis.get(
                        "entities"
                    ),

                "entity_confidence":
                    analysis.get(
                        "entity_confidence"
                    ),

                "missing":
                    analysis.get(
                        "missing"
                    ),

                "entity_validation":
                    analysis.get(
                        "entity_validation"
                    ),

                "entity_errors":
                    analysis.get(
                        "entity_errors"
                    ),

                "analysis":
                    analysis,

                "execution":
                    execution
            }


            send_json(

                self,

                200,

                response
            )


        except Exception as error:

            print()

            print(
                "ERROR WHILE PROCESSING "
                "CHAT REQUEST"
            )

            print(
                "Details:",
                error
            )

            traceback.print_exc()


            send_json(

                self,

                500,

                {
                    "status":
                        "ERROR",

                    "message":
                        str(error)
                }
            )


# ============================================================
# MAIN
# ============================================================

def main():

    initialize_ai()


    server = ThreadingHTTPServer(

        (
            HOST,
            PORT
        ),

        AIRequestHandler
    )


    print()

    print(
        "=" * 60
    )

    print(
        "NEIGHBOUR MANAGEMENT AI "
        "HTTP SERVER STARTED"
    )

    print(
        "=" * 60
    )

    print(
        f"Server: http://localhost:{PORT}"
    )

    print(
        f"Chat:   http://localhost:{PORT}/chat"
    )

    print(
        f"Health: http://localhost:{PORT}/health"
    )

    print()

    print(
        "Waiting for requests..."
    )

    print(
        "Press CTRL+C to stop."
    )

    print(
        "=" * 60
    )


    try:

        server.serve_forever()

    except KeyboardInterrupt:

        print()

        print(
            "Stopping AI server..."
        )

    finally:

        server.server_close()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()