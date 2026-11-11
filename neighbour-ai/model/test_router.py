from model.api_client import NeighbourManagementAPI
from model.router import CommandRouter


def print_result(
    title,
    result
):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)

    print(result)


def main():

    print("=" * 70)
    print("PHASE 6C - COMMAND ROUTER TEST")
    print("=" * 70)

    api = NeighbourManagementAPI()

    router = CommandRouter(
        api
    )

    # ========================================================
    # TEST 1 - STATES
    # ========================================================

    result = router.route(
        {
            "intent":
                "GET_STATES",

            "entities": {
                "state": None,
                "jc": None,
                "minimum_neighbours": None
            },

            "missing": [],

            "entity_errors": []
        }
    )

    print_result(
        "TEST 1 - GET STATES",
        result
    )

    # ========================================================
    # TEST 2 - JCs
    # ========================================================

    result = router.route(
        {
            "intent":
                "GET_JCS",

            "entities": {
                "state":
                    "Uttar Pradesh",

                "jc": None,

                "minimum_neighbours":
                    None
            },

            "missing": [],

            "entity_errors": []
        }
    )

    print_result(
        "TEST 2 - GET JCs",
        result
    )

    # ========================================================
    # TEST 3 - VALIDATION
    # ========================================================

    result = router.route(
        {
            "intent":
                "VALIDATE_NEIGHBOURS",

            "entities": {
                "state":
                    "Uttar Pradesh",

                "jc":
                    "JC_Lucknow",

                "minimum_neighbours":
                    None
            },

            "missing": [],

            "entity_errors": []
        }
    )

    print_result(
        "TEST 3 - VALIDATE",
        result
    )

    # ========================================================
    # TEST 4 - COUNTS
    # ========================================================

    result = router.route(
        {
            "intent":
                "GET_COUNTS",

            "entities": {
                "state":
                    "Uttar Pradesh",

                "jc":
                    "JC_Lucknow",

                "minimum_neighbours":
                    None
            },

            "missing": [],

            "entity_errors": []
        }
    )

    print_result(
        "TEST 4 - COUNTS",
        result
    )

    # ========================================================
    # TEST 5 - INVALID PERCENTAGE
    # ========================================================

    result = router.route(
        {
            "intent":
                "GET_INVALID_PERCENTAGE",

            "entities": {
                "state":
                    "Uttar Pradesh",

                "jc":
                    "JC_Lucknow",

                "minimum_neighbours":
                    None
            },

            "missing": [],

            "entity_errors": []
        }
    )

    print_result(
        "TEST 5 - INVALID PERCENTAGE",
        result
    )

    # ========================================================
    # TEST 6 - PREVIEW
    # ========================================================

    result = router.route(
        {
            "intent":
                "PREVIEW_CLEANUP",

            "entities": {
                "state":
                    "Uttar Pradesh",

                "jc":
                    "JC_Lucknow",

                "minimum_neighbours":
                    5
            },

            "missing": [],

            "entity_errors": []
        }
    )

    print_result(
        "TEST 6 - PREVIEW CLEANUP",
        result
    )

    # ========================================================
    # TEST 7 - CLEANUP GUARD
    # ========================================================

    result = router.route(
        {
            "intent":
                "START_CLEANUP",

            "entities": {
                "state":
                    "Uttar Pradesh",

                "jc":
                    "JC_Lucknow",

                "minimum_neighbours":
                    5
            },

            "missing": [],

            "entity_errors": []
        }
    )

    print_result(
        "TEST 7 - CLEANUP SAFETY GUARD",
        result
    )

    # ========================================================
    # TEST 8 - MISSING INFORMATION
    # ========================================================

    result = router.route(
        {
            "intent":
                "START_CLEANUP",

            "entities": {
                "state": None,
                "jc": None,
                "minimum_neighbours": None
            },

            "missing": [
                "state",
                "jc"
            ],

            "entity_errors": []
        }
    )

    print_result(
        "TEST 8 - MISSING INFORMATION",
        result
    )

    # ========================================================
    # TEST 9 - INVALID ENTITY
    # ========================================================

    result = router.route(
        {
            "intent":
                "START_CLEANUP",

            "entities": {
                "state":
                    "Uttar Pradesh",

                "jc":
                    "JC_Mumbai",

                "minimum_neighbours":
                    5
            },

            "missing": [],

            "entity_errors": [
                "JC 'JC_Mumbai' does not belong "
                "to State 'Uttar Pradesh'."
            ]
        }
    )

    print_result(
        "TEST 9 - INVALID ENTITY",
        result
    )

    print()
    print("=" * 70)
    print("PHASE 6C ROUTER TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":

    main()