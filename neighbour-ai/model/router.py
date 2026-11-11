from model.api_client import NeighbourManagementAPI
import model.config as config


class CommandRouter:

    def __init__(
        self,
        api=None
    ):

        self.api = (
            api
            if api is not None
            else NeighbourManagementAPI()
        )


    # ========================================================
    # MAIN ROUTER
    # ========================================================

    def route(
        self,
        analysis
    ):

        intent = analysis["intent"]

        entities = analysis["entities"]

        missing = analysis["missing"]

        entity_errors = analysis[
            "entity_errors"
        ]


        # ====================================================
        # OUT OF SCOPE
        # ====================================================

        if intent == "OUT_OF_SCOPE":

            return {
                "status":
                    "OUT_OF_SCOPE",

                "message":
                    "This request is outside "
                    "the Neighbour Management system."
            }


        # ====================================================
        # AMBIGUOUS
        # ====================================================

        if intent == "AMBIGUOUS_REQUEST":

            return {
                "status":
                    "AMBIGUOUS",

                "message":
                    "Please specify the operation "
                    "and the State/JC."
            }


        # ====================================================
        # MISSING INFORMATION
        # ====================================================

        # GET_INVALID_NEIGHBOURS is a read-only operation.
        # It must NOT require minimum_neighbours.
        #
        # minimum_neighbours is required only by cleanup
        # operations and automation creation.

        effective_missing = [

            item

            for item in (missing or [])

            if not (

                intent == "GET_INVALID_NEIGHBOURS"

                and

                item == "minimum_neighbours"
            )
        ]


        if effective_missing:

            return {
                "status":
                    "MISSING_INFORMATION",

                "missing":
                    effective_missing,

                "message":
                    self._missing_message(
                        effective_missing
                    )
            }


        # ====================================================
        # INVALID ENTITY
        # ====================================================

        if entity_errors:

            return {
                "status":
                    "INVALID_ENTITY",

                "errors":
                    entity_errors,

                "message":
                    "The requested State/JC "
                    "combination is invalid."
            }


        # ====================================================
        # STATES
        # ====================================================

        if intent == "GET_STATES":

            return self._get_states()


        # ====================================================
        # JCS
        # ====================================================

        if intent == "GET_JCS":

            return self._get_jcs(
                entities
            )


        # ====================================================
        # AUTOMATIONS
        # ====================================================

        if intent == "GET_AUTOMATIONS":

            return self._get_automations()


        # ====================================================
        # VALIDATION
        # ====================================================

        if intent == "VALIDATE_NEIGHBOURS":

            return self._validate(
                entities
            )


        # ====================================================
        # COUNTS
        #
        # GET_NEIGHBOURS is also accepted here as a safe
        # compatibility route.
        #
        # "How many neighbours..." is converted to GET_COUNTS
        # by predict.py.
        #
        # If the model nevertheless predicts GET_NEIGHBOURS,
        # we do not return "No route".
        # ====================================================

        if intent in (
            "GET_COUNTS",
            "GET_NEIGHBOURS"
        ):

            return self._counts(
                entities
            )


        # ====================================================
        # INVALID PERCENTAGE
        # ====================================================

        if intent == "GET_INVALID_PERCENTAGE":

            return self._invalid_percentage(
                entities
            )


        # ====================================================
        # INVALID NEIGHBOURS
        # ====================================================

        if intent == "GET_INVALID_NEIGHBOURS":

            return self._invalid_neighbours(
                entities
            )


        # ====================================================
        # PCI
        # ====================================================

        if intent == "GET_PCI_INVALID":

            return self._pci_invalid(
                entities
            )


        # ====================================================
        # TAC
        # ====================================================

        if intent == "GET_TAC_INVALID":

            return self._tac_invalid(
                entities
            )


        # ====================================================
        # PREVIEW
        # ====================================================

        if intent == "PREVIEW_CLEANUP":

            return self._preview_cleanup(
                entities
            )


        # ====================================================
        # DIRECT CLEANUP
        # ====================================================

        if intent == "START_CLEANUP":

            return self._start_cleanup(
                entities
            )


        # ====================================================
        # CREATE AUTOMATION
        # ====================================================

        if intent == "CREATE_AUTOMATION":

            return self._create_automation(
                entities
            )


        # ====================================================
        # CLEANUP RESULT
        # ====================================================

        if intent == "GET_CLEANUP_RESULT":

            return {
                "status":
                    "NOT_CONNECTED_YET",

                "message":
                    "Cleanup result retrieval "
                    "requires the backend result endpoint."
            }


        # ====================================================
        # CLEANUP PROGRESS
        # ====================================================

        if intent == "GET_CLEANUP_PROGRESS":

            return {
                "status":
                    "NOT_CONNECTED_YET",

                "message":
                    "Cleanup progress retrieval "
                    "requires the backend progress endpoint."
            }


        # ====================================================
        # UNKNOWN
        # ====================================================

        return {
            "status":
                "UNKNOWN_INTENT",

            "message":
                f"No route for intent: {intent}"
        }


    # ========================================================
    # GET STATES
    # ========================================================

    def _get_states(
        self
    ):

        states = self.api.get_states()

        return {

            "status":
                "SUCCESS",

            "intent":
                "GET_STATES",

            "states":
                states,

            "count":
                len(states)
        }


    # ========================================================
    # GET JCS
    # ========================================================

    def _get_jcs(
        self,
        entities
    ):

        state = entities.get(
            "state"
        )


        if state:

            jcs = self.api.get_jcs_by_state(
                state
            )

        else:

            jcs = self.api.get_all_jcs()


        return {

            "status":
                "SUCCESS",

            "intent":
                "GET_JCS",

            "state":
                state,

            "jcs":
                jcs,

            "count":
                len(jcs)
        }


    # ========================================================
    # VALIDATION
    # ========================================================

    def _validate(
        self,
        entities
    ):

        state = entities[
            "state"
        ]

        jc = entities[
            "jc"
        ]


        result = self.api.run_validation(
            state,
            jc,
            rules=[
                "PCI",
                "TAC"
            ]
        )


        return {

            "status":
                "SUCCESS",

            "intent":
                "VALIDATE_NEIGHBOURS",

            "state":
                state,

            "jc":
                jc,

            "validation":
                result
        }


    # ========================================================
    # COUNTS
    # ========================================================

    def _counts(
        self,
        entities
    ):

        result = self.api.run_validation(
            entities["state"],
            entities["jc"],
            rules=[
                "PCI",
                "TAC"
            ]
        )


        return {

            "status":
                "SUCCESS",

            "intent":
                "GET_COUNTS",

            "total":
                result.get(
                    "totalNeighbours",
                    0
                ),

            "valid":
                result.get(
                    "validNeighbours",
                    0
                ),

            "invalid":
                result.get(
                    "invalidNeighbours",
                    0
                ),

            "state":
                entities["state"],

            "jc":
                entities["jc"]
        }


    # ========================================================
    # INVALID PERCENTAGE
    # ========================================================

    def _invalid_percentage(
        self,
        entities
    ):

        result = self.api.run_validation(
            entities["state"],
            entities["jc"],
            rules=[
                "PCI",
                "TAC"
            ]
        )


        total = result.get(
            "totalNeighbours",
            0
        )

        invalid = result.get(
            "invalidNeighbours",
            0
        )


        percentage = (

            invalid / total * 100

            if total > 0

            else 0
        )


        return {

            "status":
                "SUCCESS",

            "intent":
                "GET_INVALID_PERCENTAGE",

            "state":
                entities["state"],

            "jc":
                entities["jc"],

            "total":
                total,

            "invalid":
                invalid,

            "invalid_percentage":
                round(
                    percentage,
                    2
                )
        }


    # ========================================================
    # INVALID NEIGHBOURS
    # ========================================================

    def _invalid_neighbours(
        self,
        entities
    ):

        result = self.api.run_validation(
            entities["state"],
            entities["jc"],
            rules=[
                "PCI",
                "TAC"
            ]
        )


        results = result.get(
            "results",
            []
        )


        invalid = [

            item

            for item in results

            if str(
                item.get(
                    "status",
                    ""
                )
            ).upper()
            == "INVALID"
        ]


        return {

            "status":
                "SUCCESS",

            "intent":
                "GET_INVALID_NEIGHBOURS",

            "state":
                entities["state"],

            "jc":
                entities["jc"],

            "invalidNeighbours":
                invalid,

            "count":
                len(invalid)
        }


    # ========================================================
    # PCI INVALID
    # ========================================================

    def _pci_invalid(
        self,
        entities
    ):

        result = self.api.run_validation(
            entities["state"],
            entities["jc"],
            rules=[
                "PCI"
            ]
        )


        return {

            "status":
                "SUCCESS",

            "intent":
                "GET_PCI_INVALID",

            "state":
                entities["state"],

            "jc":
                entities["jc"],

            "validation":
                result
        }


    # ========================================================
    # TAC INVALID
    # ========================================================

    def _tac_invalid(
        self,
        entities
    ):

        result = self.api.run_validation(
            entities["state"],
            entities["jc"],
            rules=[
                "TAC"
            ]
        )


        return {

            "status":
                "SUCCESS",

            "intent":
                "GET_TAC_INVALID",

            "state":
                entities["state"],

            "jc":
                entities["jc"],

            "validation":
                result
        }


    # ========================================================
    # PREVIEW CLEANUP
    # ========================================================

    def _preview_cleanup(
        self,
        entities
    ):

        minimum = entities.get(
            "minimum_neighbours"
        )


        if minimum is None:

            return {

                "status":
                    "MISSING_INFORMATION",

                "intent":
                    "PREVIEW_CLEANUP",

                "missing":
                    [
                        "minimum_neighbours"
                    ],

                "message":
                    "Minimum neighbours must be "
                    "provided for cleanup preview."
            }


        result = self.api.preview_cleanup(
            entities["state"],
            entities["jc"],
            minimum
        )


        return {

            "status":
                "SUCCESS",

            "intent":
                "PREVIEW_CLEANUP",

            "state":
                entities["state"],

            "jc":
                entities["jc"],

            "minimum_neighbours":
                minimum,

            "safety":
                result
        }


    # ========================================================
    # DIRECT CLEANUP
    # ========================================================

    def _start_cleanup(
        self,
        entities
    ):

        if not config.DIRECT_CLEANUP_ENABLED:

            return {

                "status":
                    "DIRECT_CLEANUP_DISABLED",

                "message":
                    "Direct cleanup is disabled "
                    "by configuration."
            }


        state = entities[
            "state"
        ]

        jc = entities[
            "jc"
        ]

        minimum = entities.get(
            "minimum_neighbours"
        )


        if minimum is None:

            return {

                "status":
                    "MISSING_INFORMATION",

                "intent":
                    "START_CLEANUP",

                "missing":
                    [
                        "minimum_neighbours"
                    ],

                "message":
                    "Minimum neighbours must be "
                    "provided for cleanup."
            }


        return self.api.direct_cleanup(
            state,
            jc,
            minimum
        )


    # ========================================================
    # CREATE AUTOMATION
    # ========================================================

    def _create_automation(
        self,
        entities
    ):

        state = entities.get(
            "state"
        )

        jc = entities.get(
            "jc"
        )


        if not state:

            return {

                "status":
                    "ERROR",

                "intent":
                    "CREATE_AUTOMATION",

                "message":
                    "State is required "
                    "to create automation."
            }


        if not jc:

            return {

                "status":
                    "ERROR",

                "intent":
                    "CREATE_AUTOMATION",

                "message":
                    "JC is required "
                    "to create automation."
            }


        frequency = (
            entities.get(
                "frequency"
            )
            or
            config.AUTOMATION_DEFAULT_FREQUENCY
        )


        if frequency not in (
            config.AUTOMATION_ALLOWED_FREQUENCIES
        ):

            return {

                "status":
                    "INVALID_AUTOMATION_CONFIGURATION",

                "intent":
                    "CREATE_AUTOMATION",

                "message":
                    f"Unsupported frequency: "
                    f"{frequency}"
            }


        execution_time = entities.get(
            "execution_time"
        )


        if execution_time is None:

            return {

                "status":
                    "MISSING_INFORMATION",

                "intent":
                    "CREATE_AUTOMATION",

                "missing":
                    [
                        "execution_time"
                    ],

                "message":
                    "Execution time is required."
            }


        rules = (
            entities.get(
                "rules"
            )
            or
            list(
                config.AUTOMATION_DEFAULT_RULES
            )
        )


        # ----------------------------------------------------
        # EXACT USER VALUE
        # ----------------------------------------------------

        minimum = entities.get(
            "minimum_neighbours"
        )


        if minimum is None:

            return {

                "status":
                    "MISSING_INFORMATION",

                "intent":
                    "CREATE_AUTOMATION",

                "missing":
                    [
                        "minimum_neighbours"
                    ],

                "message":
                    "Minimum neighbours must be "
                    "explicitly provided."
            }


        # ----------------------------------------------------
        # TECHNOLOGY FLOW
        # ----------------------------------------------------

        technology_flow = entities.get(
            "technology_flow"
        )


        if technology_flow is None:

            return {

                "status":
                    "MISSING_INFORMATION",

                "intent":
                    "CREATE_AUTOMATION",

                "missing":
                    [
                        "technology_flow"
                    ],

                "message":
                    "Technology flow must be provided. "
                    "Use FOUR_G_TO_FIVE_G or "
                    "FIVE_G_TO_FOUR_G."
            }


        allowed_flows = {

            "FOUR_G_TO_FIVE_G",

            "FIVE_G_TO_FOUR_G"
        }


        if technology_flow not in allowed_flows:

            return {

                "status":
                    "INVALID_AUTOMATION_CONFIGURATION",

                "intent":
                    "CREATE_AUTOMATION",

                "message":
                    "Invalid technology flow: "
                    f"{technology_flow}"
            }


        try:

            result = self.api.create_automation(

                state=state,

                jc=jc,

                frequency=frequency,

                execution_time=execution_time,

                rules=rules,

                minimum_neighbours=minimum,

                technology_flow=technology_flow
            )


        except Exception as error:

            return {

                "status":
                    "ERROR",

                "intent":
                    "CREATE_AUTOMATION",

                "state":
                    state,

                "jc":
                    jc,

                "minimum_neighbours":
                    minimum,

                "technology_flow":
                    technology_flow,

                "message":
                    str(error)
            }


        return {

            "status":
                "AUTOMATION_CREATED",

            "intent":
                "CREATE_AUTOMATION",

            "state":
                state,

            "jc":
                jc,

            "frequency":
                frequency,

            "execution_time":
                execution_time,

            "rules":
                rules,

            "minimum_neighbours":
                minimum,

            "technology_flow":
                technology_flow,

            "result":
                result
        }


    # ========================================================
    # GET AUTOMATIONS
    # ========================================================

    def _get_automations(
        self
    ):

        return {

            "status":
                "SUCCESS",

            "intent":
                "GET_AUTOMATIONS",

            "automations":
                self.api.get_automations()
        }


    # ========================================================
    # MISSING MESSAGE
    # ========================================================

    @staticmethod
    def _missing_message(
        missing
    ):

        if (
            "state" in missing
            and
            "jc" in missing
        ):

            return (
                "Please provide both "
                "the State and JC."
            )


        if "state" in missing:

            return (
                "Please provide the State."
            )


        if "jc" in missing:

            return (
                "Please provide the JC."
            )


        if "state_or_jc" in missing:

            return (
                "Please provide a State or JC."
            )


        if "minimum_neighbours" in missing:

            return (
                "Please provide the minimum "
                "number of neighbours to retain."
            )


        if "execution_time" in missing:

            return (
                "Please provide the automation "
                "execution time."
            )


        if "technology_flow" in missing:

            return (
                "Please provide the technology flow: "
                "FOUR_G_TO_FIVE_G or "
                "FIVE_G_TO_FOUR_G."
            )


        return (
            "Required information is missing."
        )