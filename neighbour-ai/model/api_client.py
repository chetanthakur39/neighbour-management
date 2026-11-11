import os
import requests

import model.config as config


# ============================================================
# DEFAULT ENDPOINTS
# ============================================================

DEFAULT_API_BASE_URL = (
    os.environ.get("NEIGHBOUR_API_BASE_URL", "http://localhost:8080/api")
)

DEFAULT_VALIDATION_ENDPOINT = (
    "/validation/run"
)

DEFAULT_SAFETY_ENDPOINT = (
    "/safety/evaluate"
)

DEFAULT_AUTOMATION_ENDPOINT = (
    "/automations"
)


# ============================================================
# ALLOWED TECHNOLOGY FLOWS
# ============================================================

ALLOWED_TECHNOLOGY_FLOWS = {

    "FOUR_G_TO_FIVE_G",

    "FIVE_G_TO_FOUR_G"
}


class NeighbourManagementAPI:

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        base_url=None,
        timeout=15
    ):

        self.base_url = (

            base_url

            or

            getattr(
                config,
                "API_BASE_URL",
                DEFAULT_API_BASE_URL
            )

        ).rstrip("/")


        self.timeout = timeout


    # ========================================================
    # GET REQUEST
    # ========================================================

    def _get(
        self,
        endpoint,
        params=None
    ):

        url = (

            f"{self.base_url}"
            f"{endpoint}"
        )


        response = requests.get(

            url,

            params=params,

            timeout=self.timeout
        )


        response.raise_for_status()


        if not response.content:

            return {}


        return response.json()


    # ========================================================
    # POST REQUEST
    # ========================================================

    def _post(
        self,
        endpoint,
        body=None,
        params=None
    ):

        url = (

            f"{self.base_url}"
            f"{endpoint}"
        )


        response = requests.post(

            url,

            params=params,

            json=body,

            timeout=self.timeout
        )


        response.raise_for_status()


        if not response.content:

            return {}


        return response.json()


    # ========================================================
    # DELETE REQUEST
    # ========================================================

    def _delete(
        self,
        endpoint,
        body=None,
        params=None
    ):

        url = (

            f"{self.base_url}"
            f"{endpoint}"
        )


        response = requests.delete(

            url,

            params=params,

            json=body,

            timeout=self.timeout
        )


        response.raise_for_status()


        if not response.content:

            return {}


        return response.json()


    # ========================================================
    # STATES
    # ========================================================

    def get_states(
        self
    ):

        result = self._get(
            "/metadata/states"
        )


        if isinstance(
            result,
            dict
        ):

            return result.get(
                "states",
                []
            )


        if isinstance(
            result,
            list
        ):

            return result


        return []


    # ========================================================
    # ALL JCS
    # ========================================================

    def get_all_jcs(
        self
    ):

        result = self._get(
            "/metadata/jcs"
        )


        if isinstance(
            result,
            dict
        ):

            return result.get(
                "jcs",
                []
            )


        if isinstance(
            result,
            list
        ):

            return result


        return []


    # ========================================================
    # JCS BY STATE
    # ========================================================

    def get_jcs_by_state(
        self,
        state
    ):

        result = self._get(

            f"/metadata/jcs/{state}"
        )


        if isinstance(
            result,
            dict
        ):

            return result.get(
                "jcs",
                []
            )


        if isinstance(
            result,
            list
        ):

            return result


        return []


    # ========================================================
    # CHECK STATE + JC
    # ========================================================

    def check_state_jc(
        self,
        state,
        jc
    ):

        result = self._get(

            "/metadata/state-jc/exists",

            params={

                "state":
                    state,

                "jc":
                    jc
            }
        )


        if isinstance(
            result,
            dict
        ):

            return result


        return {

            "exists":
                False
        }


    # ========================================================
    # STATE EXISTS
    # ========================================================

    def state_exists(
        self,
        state
    ):

        if not state:

            return False


        states = self.get_states()


        for item in states:

            if not isinstance(
                item,
                str
            ):

                continue


            if item.lower() == state.lower():

                return True


        return False


    # ========================================================
    # JC EXISTS
    # ========================================================

    def jc_exists(
        self,
        state,
        jc
    ):

        if not state or not jc:

            return False


        result = self.check_state_jc(

            state,

            jc
        )


        return bool(

            result.get(
                "exists",
                False
            )
        )


    # ========================================================
    # VALIDATION
    # ========================================================

    def run_validation(
        self,
        state,
        jc,
        rules=None
    ):

        if not state:

            raise ValueError(
                "state is required."
            )


        if not jc:

            raise ValueError(
                "jc is required."
            )


        if rules is None:

            rules = [

                "PCI",

                "TAC"
            ]


        body = {

            "state":
                state,

            "jc":
                jc,

            "rules":
                rules
        }


        endpoint = getattr(

            config,

            "VALIDATION_ENDPOINT",

            DEFAULT_VALIDATION_ENDPOINT
        )


        return self._post(

            endpoint,

            body=body
        )


    # ========================================================
    # SAFETY EVALUATION
    # ========================================================

    def evaluate_safety(
        self,
        validation_response,
        minimum_neighbours
    ):

        if minimum_neighbours is None:

            raise ValueError(

                "minimum_neighbours "
                "is required."
            )


        try:

            minimum_neighbours = int(
                minimum_neighbours
            )

        except (
            TypeError,
            ValueError
        ):

            raise ValueError(

                "minimum_neighbours "
                "must be an integer."
            )


        endpoint = getattr(

            config,

            "SAFETY_EVALUATION_ENDPOINT",

            DEFAULT_SAFETY_ENDPOINT
        )


        return self._post(

            endpoint,

            body=validation_response,

            params={

                "minimumNeighbours":
                    minimum_neighbours
            }
        )


    # ========================================================
    # SAFETY DECISION
    # ========================================================

    @staticmethod
    def safety_is_explicitly_allowed(
        safety_response
    ):

        if not isinstance(
            safety_response,
            dict
        ):

            return False


        # ----------------------------------------------------
        # Direct boolean fields
        # ----------------------------------------------------

        for key in (

            "allowed",

            "deleteAllowed",

            "deletionAllowed",

            "safe",

            "canDelete"
        ):

            value = safety_response.get(
                key
            )


            if isinstance(
                value,
                bool
            ):

                return value


        # ----------------------------------------------------
        # Nested safety object
        # ----------------------------------------------------

        nested = safety_response.get(
            "safety"
        )


        if isinstance(
            nested,
            dict
        ):

            return (
                NeighbourManagementAPI
                .safety_is_explicitly_allowed(
                    nested
                )
            )


        return False


    # ========================================================
    # PREVIEW CLEANUP
    # ========================================================

    def preview_cleanup(
        self,
        state,
        jc,
        minimum_neighbours
    ):

        if minimum_neighbours is None:

            raise ValueError(

                "minimum_neighbours "
                "is required."
            )


        validation = self.run_validation(

            state,

            jc,

            rules=[

                "PCI",

                "TAC"
            ]
        )


        safety = self.evaluate_safety(

            validation,

            minimum_neighbours
        )


        return {

            "validation":
                validation,

            "safety":
                safety,

            "allowed":
                self.safety_is_explicitly_allowed(
                    safety
                )
        }


    # ========================================================
    # DIRECT CLEANUP
    # ========================================================

    def direct_cleanup(
        self,
        state,
        jc,
        minimum_neighbours
    ):

        if minimum_neighbours is None:

            raise ValueError(

                "minimum_neighbours "
                "is required."
            )


        try:

            minimum_neighbours = int(
                minimum_neighbours
            )

        except (
            TypeError,
            ValueError
        ):

            raise ValueError(

                "minimum_neighbours "
                "must be an integer."
            )


        validation = self.run_validation(

            state,

            jc,

            rules=[

                "PCI",

                "TAC"
            ]
        )


        safety = self.evaluate_safety(

            validation,

            minimum_neighbours
        )


        allowed = (
            self.safety_is_explicitly_allowed(
                safety
            )
        )


        # ----------------------------------------------------
        # FAIL CLOSED
        # ----------------------------------------------------

        requires_explicit = getattr(

            config,

            "DIRECT_CLEANUP_REQUIRES_EXPLICIT_SAFETY_APPROVAL",

            True
        )


        if (

            requires_explicit

            and

            not allowed
        ):

            return {

                "status":
                    "SAFETY_BLOCKED",

                "state":
                    state,

                "jc":
                    jc,

                "minimum_neighbours":
                    minimum_neighbours,

                "validation":
                    validation,

                "safety":
                    safety,

                "message":

                    "Backend safety evaluation "
                    "did not explicitly authorize "
                    "deletion. No records were deleted."
            }


        # ----------------------------------------------------
        # FIND IDS TO DELETE
        # ----------------------------------------------------

        safety_data = safety


        if (

            isinstance(
                safety_data,
                dict
            )

            and

            isinstance(
                safety_data.get(
                    "safety"
                ),
                dict
            )
        ):

            safety_data = safety_data[
                "safety"
            ]


        neighbour_ids = []


        if isinstance(
            safety_data,
            dict
        ):

            neighbour_ids = safety_data.get(

                "neighbourIdsToDelete",

                safety_data.get(

                    "neighbour_ids",

                    []
                )
            )


        if not isinstance(
            neighbour_ids,
            list
        ):

            neighbour_ids = []


        # ----------------------------------------------------
        # NOTHING TO DELETE
        # ----------------------------------------------------

        if not neighbour_ids:

            return {

                "status":
                    "NO_DELETION_REQUIRED",

                "state":
                    state,

                "jc":
                    jc,

                "minimum_neighbours":
                    minimum_neighbours,

                "validation":
                    validation,

                "safety":
                    safety,

                "message":

                    "Safety validation allowed "
                    "cleanup, but there are no "
                    "neighbour IDs to delete."
            }


        # ----------------------------------------------------
        # DELETE
        # ----------------------------------------------------

        body = {

            "state":
                state,

            "jc":
                jc,

            "minimumNeighbours":
                minimum_neighbours,

            "neighbourIds":
                neighbour_ids
        }


        result = self._delete(

            "/deletion/neighbours",

            body=body
        )


        return {

            "status":
                "CLEANUP_EXECUTED",

            "state":
                state,

            "jc":
                jc,

            "minimum_neighbours":
                minimum_neighbours,

            "validation":
                validation,

            "safety":
                safety,

            "deleted":
                result,

            "result":
                result
        }


    # ========================================================
    # AUTOMATIONS
    # ========================================================

    def get_automations(
        self
    ):

        result = self._get(
            "/automations"
        )


        if isinstance(
            result,
            dict
        ):

            return result.get(

                "automations",

                result
            )


        return result


    # ========================================================
    # GET SINGLE AUTOMATION
    # ========================================================

    def get_automation(
        self,
        automation_id
    ):

        return self._get(

            f"/automations/"
            f"{automation_id}"
        )


    # ========================================================
    # CREATE AUTOMATION
    # ========================================================
    #
    # IMPORTANT:
    #
    # This method uses:
    #
    # config.CREATE_AUTOMATION_ENDPOINT
    #
    # IF it exists.
    #
    # Otherwise it uses:
    #
    # /automations
    #
    # Therefore your current config.py does NOT need to
    # contain CREATE_AUTOMATION_ENDPOINT.
    #
    # ========================================================

    def create_automation(
        self,
        state,
        jc,
        frequency=None,
        execution_time=None,
        rules=None,
        minimum_neighbours=None,
        technology_flow=None
    ):

        # ----------------------------------------------------
        # STATE
        # ----------------------------------------------------

        if not state:

            raise ValueError(
                "state is required."
            )


        # ----------------------------------------------------
        # JC
        # ----------------------------------------------------

        if not jc:

            raise ValueError(
                "jc is required."
            )


        # ----------------------------------------------------
        # FREQUENCY
        # ----------------------------------------------------

        frequency = (

            frequency

            or

            getattr(

                config,

                "AUTOMATION_DEFAULT_FREQUENCY",

                "DAILY"
            )
        )


        # ----------------------------------------------------
        # RULES
        # ----------------------------------------------------

        if rules is None:

            rules = list(

                getattr(

                    config,

                    "AUTOMATION_DEFAULT_RULES",

                    [
                        "CELL_EXISTS",
                        "CELL_ACTIVE",
                        "NODE_ACTIVE",
                        "PCI_VALID",
                        "TAC_VALID",
                        "NOT_DUPLICATE"
                    ]
                )
            )


        # ----------------------------------------------------
        # EXECUTION TIME
        # ----------------------------------------------------

        if execution_time is None:

            raise ValueError(

                "execution_time is required."
            )


        execution_time = str(
            execution_time
        ).strip()


        if not execution_time:

            raise ValueError(

                "execution_time "
                "cannot be empty."
            )


        # ----------------------------------------------------
        # MINIMUM NEIGHBOURS
        #
        # NO DEFAULT VALUE.
        #
        # If chatbot says:
        #
        # minimum retention of 2
        #
        # then exactly 2 is sent.
        #
        # ----------------------------------------------------

        if minimum_neighbours is None:

            raise ValueError(

                "minimum_neighbours is required. "
                "The chatbot must explicitly "
                "provide the minimum number "
                "of neighbours."
            )


        try:

            minimum_neighbours = int(
                minimum_neighbours
            )

        except (
            TypeError,
            ValueError
        ):

            raise ValueError(

                "minimum_neighbours "
                "must be an integer."
            )


        if minimum_neighbours < 1:

            raise ValueError(

                "minimum_neighbours "
                "must be at least 1."
            )


        # ----------------------------------------------------
        # TECHNOLOGY FLOW
        # ----------------------------------------------------

        if technology_flow is None:

            raise ValueError(

                "technology_flow is required."
            )


        technology_flow = str(

            technology_flow

        ).strip().upper()


        if technology_flow not in (
            ALLOWED_TECHNOLOGY_FLOWS
        ):

            raise ValueError(

                "Invalid technology_flow: "

                f"{technology_flow}. "

                "Allowed values: "

                "FOUR_G_TO_FIVE_G, "

                "FIVE_G_TO_FOUR_G."
            )


        # ----------------------------------------------------
        # REQUEST BODY
        # ----------------------------------------------------
        #
        # This exactly matches:
        #
        # AutomationCreateRequest
        #
        # state
        # jc
        # technologyFlow
        # executionTime
        # minimumNeighbours
        # rules
        #
        # ----------------------------------------------------

        body = {

            "state":
                state,

            "jc":
                jc,

            "technologyFlow":
                technology_flow,

            "executionTime":
                execution_time,

            "minimumNeighbours":
                minimum_neighbours,

            "rules":
                rules
        }


        # ----------------------------------------------------
        # OPTIONAL NAME
        # ----------------------------------------------------
        #
        # Your Java DTO has a "name" field, but it is not
        # required by the chatbot command.
        #
        # We don't invent a name here unless the backend
        # requires one.
        #
        # ----------------------------------------------------


        # ----------------------------------------------------
        # AUTOMATION ENDPOINT
        # ----------------------------------------------------

        endpoint = getattr(

            config,

            "CREATE_AUTOMATION_ENDPOINT",

            DEFAULT_AUTOMATION_ENDPOINT
        )


        # ----------------------------------------------------
        # ACTUAL POST
        # ----------------------------------------------------

        return self._post(

            endpoint,

            body=body
        )


    # ========================================================
    # RUN AUTOMATION
    # ========================================================

    def run_automation(
        self,
        automation_id
    ):

        return self._post(

            f"/automations/"
            f"{automation_id}/run"
        )


    # ========================================================
    # AUTOMATION EXECUTIONS
    # ========================================================

    def get_automation_executions(
        self,
        automation_id
    ):

        return self._get(

            "/automation-executions/"
            f"automation/"
            f"{automation_id}"
        )


    # ========================================================
    # FIND AUTOMATION
    # ========================================================

    def find_automation(
        self,
        state,
        jc
    ):

        automations = (
            self.get_automations()
        )


        if not isinstance(
            automations,
            list
        ):

            return None


        for automation in automations:

            if not isinstance(
                automation,
                dict
            ):

                continue


            automation_state = (

                automation.get(
                    "state"
                )
            )


            automation_jc = (

                automation.get(
                    "jc"
                )
            )


            if (

                automation_state

                and

                automation_jc

                and

                automation_state.lower()
                ==
                state.lower()

                and

                automation_jc.lower()
                ==
                jc.lower()
            ):

                return automation


        return None