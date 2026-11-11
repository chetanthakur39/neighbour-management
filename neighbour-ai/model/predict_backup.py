import re

import torch

from tokenizer.tokenizer import SimpleTokenizer
from model.intent_model import IntentClassifier
from model.intent_mapping import (
    LABEL_TO_INTENT,
    INTENT_TO_LABEL,
)
from model.api_client import NeighbourManagementAPI

import model.config as config


# ============================================================
# LOAD TOKENIZER
# ============================================================

def load_tokenizer():

    return SimpleTokenizer.load(
        config.TOKENIZER_FILE
    )


# ============================================================
# LOAD TRAINED MODEL
# ============================================================

def load_model(device):

    checkpoint = torch.load(
        config.MODEL_FILE,
        map_location=device
    )

    # --------------------------------------------------------
    # Support both the current checkpoint format and older
    # checkpoint formats.
    # --------------------------------------------------------

    vocab_size = checkpoint.get(
        "vocab_size",
        len(
            SimpleTokenizer.load(
                config.TOKENIZER_FILE
            )
        )
    )

    num_intents = checkpoint.get(
        "num_intents",
        checkpoint.get(
            "num_classes",
            len(INTENT_TO_LABEL)
        )
    )

    embedding_dim = checkpoint.get(
        "embedding_dim",
        config.EMBEDDING_DIM
    )

    hidden_dim = checkpoint.get(
        "hidden_dim",
        config.HIDDEN_DIM
    )

    hidden_layers = checkpoint.get(
        "hidden_layers",
        checkpoint.get(
            "num_hidden_layers",
            config.NUM_HIDDEN_LAYERS
        )
    )

    dropout = checkpoint.get(
        "dropout",
        config.DROPOUT
    )

    model = IntentClassifier(
        vocab_size=vocab_size,
        num_intents=num_intents,
        embedding_dim=embedding_dim,
        hidden_dim=hidden_dim,
        hidden_layers=hidden_layers,
        dropout=dropout
    )

    state_dict = checkpoint.get(
        "model_state_dict",
        checkpoint
    )

    model.load_state_dict(
        state_dict
    )

    model.to(device)

    model.eval()

    return model


# ============================================================
# PREPARE INPUT
# ============================================================

def prepare_input(
    text,
    tokenizer
):

    token_ids = tokenizer.encode(
        text,
        add_special_tokens=True
    )

    token_ids = token_ids[
        :config.MAX_LENGTH
    ]

    pad_id = tokenizer.token_to_id[
        SimpleTokenizer.PAD_TOKEN
    ]

    while len(token_ids) < config.MAX_LENGTH:

        token_ids.append(
            pad_id
        )

    return torch.tensor(
        [token_ids],
        dtype=torch.long
    )


# ============================================================
# PREDICT INTENT
# ============================================================

def predict_intent(
    text,
    model,
    tokenizer,
    device
):

    input_ids = prepare_input(
        text,
        tokenizer
    )

    input_ids = input_ids.to(device)

    with torch.no_grad():

        outputs = model(
            input_ids
        )

        probabilities = torch.softmax(
            outputs,
            dim=1
        )

        confidence, predicted_id = torch.max(
            probabilities,
            dim=1
        )

    intent_id = predicted_id.item()

    if intent_id not in LABEL_TO_INTENT:

        raise ValueError(
            f"Model predicted invalid intent ID: "
            f"{intent_id}"
        )

    intent = LABEL_TO_INTENT[
        intent_id
    ]

    confidence_value = (
        confidence.item()
    )

    return (
        intent,
        confidence_value,
        probabilities[0]
    )


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    if text is None:

        return ""

    text = str(text).strip()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


# ============================================================
# EXTRACT NUMBER
# ============================================================

def extract_number(text):

    """
    Extract a retention/minimum-neighbour number.

    Supported examples:

        retain 10 neighbours
        retain at least 10 neighbours
        minimum retention of 10 neighbours
        minimum of 10 neighbours
        keep 10 neighbours
        keep at least 10 neighbours
        10 neighbours
    """

    # --------------------------------------------------------
    # Most specific retention patterns first.
    # --------------------------------------------------------

    priority_patterns = [

        # "minimum retention of 10 neighbours"
        r"\bminimum\s+retention\s+(?:of\s+)?(\d+)\b",

        # "minimum retention 10"
        r"\bminimum\s+retention\s+(\d+)\b",

        # "minimum of 10 neighbours"
        r"\bminimum\s+(?:of\s+)?(\d+)\b",

        # "retain at least 10"
        r"\bretain\s+at\s+least\s+(\d+)\b",

        # "retain 10"
        r"\bretain\s+(\d+)\b",

        # "retention of 10"
        r"\bretention\s+(?:of\s+)?(\d+)\b",

        # "keep at least 10"
        r"\bkeep\s+at\s+least\s+(\d+)\b",

        # "keep 10"
        r"\bkeep\s+(\d+)\b",

        # "at least 10 neighbours"
        r"\bat\s+least\s+(\d+)\s+"
        r"(?:neighbours?|neighbors?)\b",

        # "10 neighbours"
        r"\b(\d+)\s+"
        r"(?:neighbours?|neighbors?)\b",
    ]

    for pattern in priority_patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:

            return int(
                match.group(1)
            )

    # --------------------------------------------------------
    # Generic number fallback.
    #
    # This remains useful for existing behaviour, but the
    # retention-specific patterns above always get priority.
    # --------------------------------------------------------

    match = re.search(
        r"\b(\d+)\b",
        text
    )

    if match:

        return int(
            match.group(1)
        )

    return None


# ============================================================
# EXTRACT STATE FROM LIVE DATABASE
# ============================================================

def extract_state(
    text,
    api
):

    """
    Extract State using the live database.

    No State names are hard-coded.
    """

    states = api.get_states()

    normalized_text = text.lower()

    states = sorted(
        states,
        key=lambda value: len(
            str(value)
        ),
        reverse=True
    )

    for state in states:

        state_text = str(
            state
        ).strip()

        if not state_text:

            continue

        # ----------------------------------------------------
        # Exact phrase / word-aware matching.
        #
        # This prevents accidental partial matches.
        # ----------------------------------------------------

        pattern = (
            r"(?<![a-z])"
            + re.escape(
                state_text.lower()
            )
            + r"(?![a-z])"
        )

        if re.search(
            pattern,
            normalized_text
        ):

            return state

    return None


# ============================================================
# EXTRACT JC
# ============================================================

def extract_jc(text):

    """
    Extract JC from user command.

    Supported examples:

        JC_Lucknow
        JC_Mumbai
        JC_Jaipur_North
    """

    jc_pattern = re.compile(
        r"\bJC_[A-Za-z0-9_]+\b",
        re.IGNORECASE
    )

    match = jc_pattern.search(
        text
    )

    if match:

        return match.group(0)

    return None


# ============================================================
# EXTRACT ENTITIES
# ============================================================

def extract_entities(
    text,
    intent,
    api
):

    entities = {
        "state": None,
        "jc": None,
        "minimum_neighbours": None
    }

    # --------------------------------------------------------
    # STATE
    # --------------------------------------------------------

    entities["state"] = extract_state(
        text,
        api
    )

    # --------------------------------------------------------
    # JC
    # --------------------------------------------------------

    entities["jc"] = extract_jc(
        text
    )

    # --------------------------------------------------------
    # MINIMUM NEIGHBOURS
    #
    # IMPORTANT:
    # CREATE_AUTOMATION is included because automation
    # commands can contain their own retention requirement.
    # --------------------------------------------------------

    if intent in [
        "START_CLEANUP",
        "PREVIEW_CLEANUP",
        "CREATE_AUTOMATION"
    ]:

        entities[
            "minimum_neighbours"
        ] = extract_number(
            text
        )

    return entities


# ============================================================
# RULE-BASED INTENT REFINEMENT
# ============================================================

def refine_intent(
    text,
    predicted_intent
):

    """
    Safely refine high-value intents after the neural model.

    The neural model remains the primary classifier.

    These rules only handle highly deterministic language
    patterns where the intended operation is unambiguous.
    """

    normalized = text.lower().strip()

    # ========================================================
    # OUT OF SCOPE
    # ========================================================

    out_of_scope_patterns = [
        r"\brestaurant\b",
        r"\brestaurants\b",
        r"\btrain ticket\b",
        r"\bflight ticket\b",
        r"\bbook a flight\b",
        r"\bbook a train\b",
        r"\bhotel booking\b",
        r"\bplay music\b",
        r"\bsocial media\b",
        r"\bweather\b",
        r"\bbuy a laptop\b",
        r"\bbuy laptop\b",
    ]

    for pattern in out_of_scope_patterns:

        if re.search(
            pattern,
            normalized
        ):

            return "OUT_OF_SCOPE"

    # ========================================================
    # CLEANUP RESULT
    # ========================================================

    cleanup_result_patterns = [
        r"\bwhat was deleted\b",
        r"\bwhat was removed\b",
        r"\bshow what was deleted\b",
        r"\bshow what was removed\b",
        r"\bshow me what was deleted\b",
        r"\bshow me what was removed\b",
        r"\bcleanup result\b",
        r"\bcleanup results\b",
        r"\bdeletion result\b",
        r"\bdeletion results\b",
        r"\bwhat got deleted\b",
        r"\bwhat got removed\b",
        r"\bwhich neighbours were deleted\b",
        r"\bwhich neighbours were removed\b",
        r"\bwhich neighbors were deleted\b",
        r"\bwhich neighbors were removed\b",
    ]

    for pattern in cleanup_result_patterns:

        if re.search(
            pattern,
            normalized
        ):

            return "GET_CLEANUP_RESULT"

    # ========================================================
    # CLEANUP PROGRESS
    # ========================================================

    cleanup_progress_patterns = [
        r"\bhow much work is completed\b",
        r"\bhow much is completed\b",
        r"\bcleanup progress\b",
        r"\bcleanup status\b",
        r"\bhow far is the cleanup\b",
        r"\bhow far has the cleanup progressed\b",
        r"\bhow much cleanup is completed\b",
        r"\bcleanup completion\b",
        r"\bprogress of cleanup\b",
        r"\bstatus of cleanup\b",
    ]

    for pattern in cleanup_progress_patterns:

        if re.search(
            pattern,
            normalized
        ):

            return "GET_CLEANUP_PROGRESS"

    # ========================================================
    # AUTOMATION
    #
    # "automation" + create/setup/schedule/configure means
    # CREATE_AUTOMATION.
    #
    # This is intentionally checked before validation and
    # cleanup because phrases such as:
    #
    # "Create TAC validation automation..."
    #
    # must remain CREATE_AUTOMATION.
    # ========================================================

    automation_words = [
        "automation",
        "automated",
        "schedule",
        "scheduled",
        "configure automation",
        "configured automation",
        "set up automation",
        "set up an automation",
    ]

    create_words = [
        "create",
        "setup",
        "set up",
        "schedule",
        "scheduled",
        "configure",
        "automate",
        "automated",
    ]

    has_automation_word = any(
        word in normalized
        for word in automation_words
    )

    has_create_word = any(
        word in normalized
        for word in create_words
    )

    if (
        has_automation_word
        and has_create_word
    ):

        return "CREATE_AUTOMATION"

    # ========================================================
    # START CLEANUP
    #
    # IMPORTANT:
    # Destructive language must never be interpreted as
    # GET_NEIGHBOURS.
    #
    # These patterns only determine the INTENT.
    #
    # They do NOT execute deletion.
    #
    # Actual deletion must still pass the safety layer,
    # including minimum-retention protection.
    # ========================================================

    cleanup_action_patterns = [

        # Explicit cleanup
        r"\bstart cleanup\b",
        r"\brun cleanup\b",
        r"\bperform cleanup\b",
        r"\bexecute cleanup\b",

        # Invalid/bad neighbour cleanup
        r"\bclean invalid neighbours?\b",
        r"\bclean invalid neighbors?\b",

        r"\bclean bad neighbours?\b",
        r"\bclean bad neighbors?\b",

        r"\bremove invalid neighbours?\b",
        r"\bremove invalid neighbors?\b",

        r"\bdelete invalid neighbours?\b",
        r"\bdelete invalid neighbors?\b",

        # Eligible invalid neighbours
        r"\bdelete all eligible invalid neighbours?\b",
        r"\bdelete all eligible invalid neighbors?\b",

        r"\bremove all eligible invalid neighbours?\b",
        r"\bremove all eligible invalid neighbors?\b",

        # ----------------------------------------------------
        # Explicit destructive "all neighbours" commands.
        #
        # These are intentionally classified as START_CLEANUP
        # rather than GET_NEIGHBOURS.
        # ----------------------------------------------------

        r"\bdelete all neighbours?\b",
        r"\bdelete all neighbors?\b",

        r"\bremove all neighbours?\b",
        r"\bremove all neighbors?\b",

        r"\bdelete all eligible neighbours?\b",
        r"\bdelete all eligible neighbors?\b",

        r"\bremove all eligible neighbours?\b",
        r"\bremove all eligible neighbors?\b",

        # Direct destructive action
        r"\bdelete neighbours?\b",
        r"\bdelete neighbors?\b",

        r"\bremove neighbours?\b",
        r"\bremove neighbors?\b",
    ]

    for pattern in cleanup_action_patterns:

        if re.search(
            pattern,
            normalized
        ):

            return "START_CLEANUP"

    # ========================================================
    # VALIDATION
    #
    # Only classify as validation when the command is actually
    # asking to validate/check neighbours, rather than creating
    # an automation for validation.
    # ========================================================

    validation_patterns = [
        r"\bvalidate neighbours?\b",
        r"\bvalidate neighbors?\b",
        r"\bvalidation of neighbours?\b",
        r"\bvalidation of neighbors?\b",
        r"\bcheck neighbours?\b",
        r"\bcheck neighbors?\b",
        r"\brun neighbour validation\b",
        r"\brun neighbor validation\b",
    ]

    for pattern in validation_patterns:

        if re.search(
            pattern,
            normalized
        ):

            if not has_automation_word:

                return "VALIDATE_NEIGHBOURS"

    return predicted_intent


# ============================================================
# VALIDATE ENTITIES AGAINST LIVE DATABASE
# ============================================================

def validate_entities(
    entities,
    intent,
    api
):

    state = entities["state"]

    jc = entities["jc"]

    validation = {
        "state_exists": None,
        "jc_exists": None,
        "state_jc_exists": None
    }

    # --------------------------------------------------------
    # STATE VALIDATION
    # --------------------------------------------------------

    if state is not None:

        validation[
            "state_exists"
        ] = api.state_exists(
            state
        )

    # --------------------------------------------------------
    # STATE + JC VALIDATION
    # --------------------------------------------------------

    if (
        state is not None
        and jc is not None
    ):

        validation[
            "state_jc_exists"
        ] = api.jc_exists(
            state,
            jc
        )

        validation[
            "jc_exists"
        ] = validation[
            "state_jc_exists"
        ]

    # --------------------------------------------------------
    # JC WITHOUT STATE
    # --------------------------------------------------------

    elif jc is not None:

        validation[
            "jc_exists"
        ] = None

        validation[
            "state_jc_exists"
        ] = None

    return validation


# ============================================================
# MISSING INFORMATION
# ============================================================

def get_missing_information(
    intent,
    entities
):

    missing = []

    state = entities["state"]

    jc = entities["jc"]

    # ========================================================
    # OPERATIONS THAT REQUIRE STATE + JC
    # ========================================================

    if intent in [
        "START_CLEANUP",
        "PREVIEW_CLEANUP",
        "VALIDATE_NEIGHBOURS"
    ]:

        if state is None:

            missing.append(
                "state"
            )

        if jc is None:

            missing.append(
                "jc"
            )

    # ========================================================
    # OPERATIONS THAT SUPPORT STATE OR JC
    # ========================================================

    elif intent in [
        "GET_NEIGHBOURS",
        "GET_INVALID_NEIGHBOURS",
        "GET_PCI_INVALID",
        "GET_TAC_INVALID",
        "GET_COUNTS",
        "GET_INVALID_PERCENTAGE"
    ]:

        if (
            state is None
            and jc is None
        ):

            missing.append(
                "state_or_jc"
            )

    # ========================================================
    # CREATE AUTOMATION
    #
    # Automation must identify the target State + JC.
    #
    # Minimum retention is extracted when supplied.
    #
    # We intentionally DO NOT require minimum_neighbours here.
    # The configured safety layer can supply/enforce the
    # minimum retention policy.
    # ========================================================

    elif intent == "CREATE_AUTOMATION":

        if state is None:

            missing.append(
                "state"
            )

        if jc is None:

            missing.append(
                "jc"
            )

    return missing


# ============================================================
# CHECK ENTITY VALIDATION ERRORS
# ============================================================

def get_entity_errors(
    entities,
    entity_validation
):

    errors = []

    state = entities["state"]

    jc = entities["jc"]

    state_exists = (
        entity_validation[
            "state_exists"
        ]
    )

    state_jc_exists = (
        entity_validation[
            "state_jc_exists"
        ]
    )

    # --------------------------------------------------------
    # INVALID STATE
    # --------------------------------------------------------

    if (
        state is not None
        and state_exists is False
    ):

        errors.append(
            f"State '{state}' "
            f"does not exist in the database."
        )

    # --------------------------------------------------------
    # INVALID STATE + JC
    # --------------------------------------------------------

    if (
        state is not None
        and jc is not None
        and state_jc_exists is False
    ):

        errors.append(
            f"JC '{jc}' does not belong "
            f"to State '{state}'."
        )

    return errors


# ============================================================
# COMPLETE COMMAND ANALYSIS
# ============================================================

def analyze_command(
    text,
    model,
    tokenizer,
    device,
    api
):

    text = normalize_text(
        text
    )

    if not text:

        return {
            "text": text,
            "intent": "AMBIGUOUS_REQUEST",
            "confidence": 1.0,
            "entities": {
                "state": None,
                "jc": None,
                "minimum_neighbours": None
            },
            "missing": [],
            "entity_validation": {
                "state_exists": None,
                "jc_exists": None,
                "state_jc_exists": None
            },
            "entity_errors": []
        }

    # --------------------------------------------------------
    # NEURAL MODEL PREDICTION
    # --------------------------------------------------------

    predicted_intent, confidence, _ = predict_intent(
        text,
        model,
        tokenizer,
        device
    )

    # --------------------------------------------------------
    # SAFE RULE REFINEMENT
    # --------------------------------------------------------

    intent = refine_intent(
        text,
        predicted_intent
    )

    # --------------------------------------------------------
    # ENTITIES
    # --------------------------------------------------------

    entities = extract_entities(
        text,
        intent,
        api
    )

    # --------------------------------------------------------
    # LIVE DATABASE VALIDATION
    # --------------------------------------------------------

    entity_validation = validate_entities(
        entities,
        intent,
        api
    )

    # --------------------------------------------------------
    # MISSING INFORMATION
    # --------------------------------------------------------

    missing = get_missing_information(
        intent,
        entities
    )

    # --------------------------------------------------------
    # ENTITY ERRORS
    # --------------------------------------------------------

    entity_errors = get_entity_errors(
        entities,
        entity_validation
    )

    return {
        "text": text,

        "intent": intent,

        "predicted_intent": predicted_intent,

        "confidence": confidence,

        "entities": entities,

        "missing": missing,

        "entity_validation":
            entity_validation,

        "entity_errors":
            entity_errors
    }


# ============================================================
# DISPLAY RESULT
# ============================================================

def display_result(result):

    print()
    print("=" * 60)
    print("COMMAND ANALYSIS")
    print("=" * 60)

    print()

    print(
        "Command:",
        result["text"]
    )

    print(
        "Intent:",
        result["intent"]
    )

    # --------------------------------------------------------
    # Show neural prediction separately when a rule refined it.
    # --------------------------------------------------------

    predicted_intent = result.get(
        "predicted_intent"
    )

    if (
        predicted_intent
        and predicted_intent
        != result["intent"]
    ):

        print(
            "Neural prediction:",
            predicted_intent
        )

        print(
            "Rule refinement:",
            result["intent"]
        )

    print(
        "Confidence:",
        f"{result['confidence'] * 100:.2f}%"
    )

    # --------------------------------------------------------
    # ENTITIES
    # --------------------------------------------------------

    print()
    print("Entities")
    print("-" * 60)

    print(
        "State:",
        result["entities"]["state"]
    )

    print(
        "JC:",
        result["entities"]["jc"]
    )

    print(
        "Minimum neighbours:",
        result["entities"][
            "minimum_neighbours"
        ]
    )

    # --------------------------------------------------------
    # MISSING INFORMATION
    # --------------------------------------------------------

    print()
    print("Missing information")
    print("-" * 60)

    if result["missing"]:

        print(
            ", ".join(
                result["missing"]
            )
        )

    else:

        print("None")

    # --------------------------------------------------------
    # LIVE DATABASE VALIDATION
    # --------------------------------------------------------

    print()
    print("Live Database Validation")
    print("-" * 60)

    validation = (
        result[
            "entity_validation"
        ]
    )

    print(
        "State exists:",
        validation[
            "state_exists"
        ]
    )

    print(
        "JC exists:",
        validation[
            "jc_exists"
        ]
    )

    print(
        "State + JC exists:",
        validation[
            "state_jc_exists"
        ]
    )

    # --------------------------------------------------------
    # ENTITY ERRORS
    # --------------------------------------------------------

    print()
    print("Entity Validation Errors")
    print("-" * 60)

    if result["entity_errors"]:

        for error in result[
            "entity_errors"
        ]:

            print(
                "ERROR:",
                error
            )

    else:

        print("None")

    # --------------------------------------------------------
    # EXECUTION STATUS
    # --------------------------------------------------------

    print()
    print("Execution Status")
    print("-" * 60)

    if result["entity_errors"]:

        print(
            "BLOCKED - invalid database entity."
        )

    elif result["missing"]:

        print(
            "BLOCKED - missing information."
        )

    else:

        print(
            "READY - command is structurally complete."
        )

    print("=" * 60)


# ============================================================
# INTERACTIVE MODE
# ============================================================

def main():

    print("=" * 60)
    print("NEIGHBOUR MANAGEMENT AI")
    print("PHASE 6B - LIVE DATABASE INTEGRATION")
    print("=" * 60)

    # --------------------------------------------------------
    # DEVICE
    # --------------------------------------------------------

    if torch.cuda.is_available():

        device = torch.device(
            "cuda"
        )

    else:

        device = torch.device(
            "cpu"
        )

    print()
    print(
        "Device:",
        device
    )

    # --------------------------------------------------------
    # TOKENIZER
    # --------------------------------------------------------

    tokenizer = load_tokenizer()

    print(
        "Tokenizer loaded."
    )

    print(
        "Vocabulary:",
        len(tokenizer)
    )

    # --------------------------------------------------------
    # MODEL
    # --------------------------------------------------------

    model = load_model(
        device
    )

    print(
        "Trained model loaded."
    )

    # --------------------------------------------------------
    # LIVE API
    # --------------------------------------------------------

    api = NeighbourManagementAPI()

    print(
        "Live database API client created."
    )

    # --------------------------------------------------------
    # VERIFY API CONNECTION
    # --------------------------------------------------------

    try:

        states = api.get_states()

        print(
            "Live database connected."
        )

        print(
            "Available states:",
            len(states)
        )

    except Exception as error:

        print()
        print(
            "ERROR: Could not connect "
            "to Spring Boot API."
        )

        print(
            "Make sure the backend is running "
            "on http://localhost:8080"
        )

        print(
            "Details:",
            error
        )

        return

    # --------------------------------------------------------
    # INTERACTIVE MODE
    # --------------------------------------------------------

    print()
    print(
        "Type a command."
    )

    print(
        "Type 'exit' to stop."
    )

    print("=" * 60)

    while True:

        try:

            text = input(
                "\nYou: "
            )

        except (
            KeyboardInterrupt,
            EOFError
        ):

            print()

            break

        text = text.strip()

        if not text:

            continue

        if text.lower() == "exit":

            print(
                "Exiting..."
            )

            break

        try:

            result = analyze_command(
                text,
                model,
                tokenizer,
                device,
                api
            )

            display_result(
                result
            )

        except Exception as error:

            print()
            print(
                "ERROR while processing command:"
            )

            print(
                error
            )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()