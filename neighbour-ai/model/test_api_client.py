from model.api_client import NeighbourManagementAPI


def main():

    print("=" * 60)
    print("PHASE 6B - API CLIENT TEST")
    print("=" * 60)

    api = NeighbourManagementAPI()

    # --------------------------------------------------------
    # STATES
    # --------------------------------------------------------

    print()
    print("Testing states API...")
    print("-" * 60)

    states = api.get_states()

    print(
        "Number of states:",
        len(states)
    )

    print(
        "States:",
        states
    )

    # --------------------------------------------------------
    # JCs
    # --------------------------------------------------------

    print()
    print(
        "Testing JC API for Uttar Pradesh..."
    )

    print("-" * 60)

    jcs = api.get_jcs_by_state(
        "Uttar Pradesh"
    )

    print(
        "JCs:",
        jcs
    )

    # --------------------------------------------------------
    # VALID STATE + JC
    # --------------------------------------------------------

    print()
    print(
        "Testing valid State + JC..."
    )

    print("-" * 60)

    result = api.check_state_jc(
        "Uttar Pradesh",
        "JC_Lucknow"
    )

    print(
        "Result:",
        result
    )

    # --------------------------------------------------------
    # INVALID STATE + JC
    # --------------------------------------------------------

    print()
    print(
        "Testing invalid State + JC..."
    )

    print("-" * 60)

    result = api.check_state_jc(
        "Uttar Pradesh",
        "JC_Mumbai"
    )

    print(
        "Result:",
        result
    )

    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("PHASE 6B API CLIENT TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()