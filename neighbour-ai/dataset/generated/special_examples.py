import json
from pathlib import Path


OUTPUT_PATH = Path(
    "dataset/generated/special_examples.json"
)


def create_special_examples():

    examples = [

        # =========================================================
        # START_CLEANUP - MISSING INFORMATION
        # =========================================================

        {
            "text": "Delete the invalid neighbours",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "START_CLEANUP",
                "state": None,
                "jc": None,
                "minimum_neighbours": None
            },
            "missing": ["state", "jc"]
        },

        {
            "text": "Clean the invalid neighbours",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "START_CLEANUP",
                "state": None,
                "jc": None,
                "minimum_neighbours": None
            },
            "missing": ["state", "jc"]
        },

        {
            "text": "Remove all invalid neighbours",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "START_CLEANUP",
                "state": None,
                "jc": None,
                "minimum_neighbours": None
            },
            "missing": ["state", "jc"]
        },

        {
            "text": "Start the cleanup",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "START_CLEANUP",
                "state": None,
                "jc": None,
                "minimum_neighbours": None
            },
            "missing": ["state", "jc"]
        },

        {
            "text": "Run neighbour cleanup",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "START_CLEANUP",
                "state": None,
                "jc": None,
                "minimum_neighbours": None
            },
            "missing": ["state", "jc"]
        },

        {
            "text": "Delete invalid neighbour records",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "START_CLEANUP",
                "state": None,
                "jc": None,
                "minimum_neighbours": None
            },
            "missing": ["state", "jc"]
        },

        # ---------------------------------------------------------
        # STATE PRESENT, JC MISSING
        # ---------------------------------------------------------

        {
            "text": "Delete invalid neighbours in Uttar Pradesh",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "START_CLEANUP",
                "state": "Uttar Pradesh",
                "jc": None,
                "minimum_neighbours": None
            },
            "missing": ["jc"]
        },

        {
            "text": "Clean the invalid neighbours in Maharashtra",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "START_CLEANUP",
                "state": "Maharashtra",
                "jc": None,
                "minimum_neighbours": None
            },
            "missing": ["jc"]
        },

        {
            "text": "Remove invalid neighbours from Rajasthan",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "START_CLEANUP",
                "state": "Rajasthan",
                "jc": None,
                "minimum_neighbours": None
            },
            "missing": ["jc"]
        },

        {
            "text": "Start cleanup for Karnataka",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "START_CLEANUP",
                "state": "Karnataka",
                "jc": None,
                "minimum_neighbours": None
            },
            "missing": ["jc"]
        },

        {
            "text": "Remove bad neighbours in Punjab",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "START_CLEANUP",
                "state": "Punjab",
                "jc": None,
                "minimum_neighbours": None
            },
            "missing": ["jc"]
        },

        {
            "text": "Perform cleanup in Gujarat",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "START_CLEANUP",
                "state": "Gujarat",
                "jc": None,
                "minimum_neighbours": None
            },
            "missing": ["jc"]
        },

        {
            "text": "Delete invalid neighbour records in Kerala",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "START_CLEANUP",
                "state": "Kerala",
                "jc": None,
                "minimum_neighbours": None
            },
            "missing": ["jc"]
        },

        {
            "text": "Start deleting invalid neighbours in Telangana",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "START_CLEANUP",
                "state": "Telangana",
                "jc": None,
                "minimum_neighbours": None
            },
            "missing": ["jc"]
        },

        {
            "text": "Please remove invalid neighbours in West Bengal",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "START_CLEANUP",
                "state": "West Bengal",
                "jc": None,
                "minimum_neighbours": None
            },
            "missing": ["jc"]
        },

        # ---------------------------------------------------------
        # JC PRESENT, STATE MISSING
        # ---------------------------------------------------------

        {
            "text": "Clean the invalid neighbours for JC_Lucknow",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "START_CLEANUP",
                "state": None,
                "jc": "JC_Lucknow",
                "minimum_neighbours": None
            },
            "missing": ["state"]
        },

        {
            "text": "Delete the invalid neighbours for JC_Mumbai",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "START_CLEANUP",
                "state": None,
                "jc": "JC_Mumbai",
                "minimum_neighbours": None
            },
            "missing": ["state"]
        },

        {
            "text": "Clean JC_Jaipur",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "START_CLEANUP",
                "state": None,
                "jc": "JC_Jaipur",
                "minimum_neighbours": None
            },
            "missing": ["state"]
        },

        {
            "text": "Clean invalid neighbours for JC_Bangalore",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "START_CLEANUP",
                "state": None,
                "jc": "JC_Bangalore",
                "minimum_neighbours": None
            },
            "missing": ["state"]
        },

        {
            "text": "Run neighbour cleanup for JC_Ahmedabad",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "START_CLEANUP",
                "state": None,
                "jc": "JC_Ahmedabad",
                "minimum_neighbours": None
            },
            "missing": ["state"]
        },


        # =========================================================
        # CREATE_AUTOMATION - MISSING INFORMATION
        # =========================================================

        # ---------------------------------------------------------
        # BOTH STATE + JC MISSING
        # ---------------------------------------------------------

        {
            "text": "Create an automation",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "CREATE_AUTOMATION",
                "state": None,
                "jc": None,
                "minimum_neighbours": None,
                "execution_time": None,
                "frequency": None,
                "rules": None,
                "technology_flow": None
            },
            "missing": ["state", "jc"]
        },

        {
            "text": "Set up a daily automation",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "CREATE_AUTOMATION",
                "state": None,
                "jc": None,
                "minimum_neighbours": None,
                "execution_time": None,
                "frequency": "DAILY",
                "rules": None,
                "technology_flow": None
            },
            "missing": ["state", "jc"]
        },

        {
            "text": "Schedule an automation",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "CREATE_AUTOMATION",
                "state": None,
                "jc": None,
                "minimum_neighbours": None,
                "execution_time": None,
                "frequency": None,
                "rules": None,
                "technology_flow": None
            },
            "missing": ["state", "jc"]
        },

        {
            "text": "Create a cleanup automation",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "CREATE_AUTOMATION",
                "state": None,
                "jc": None,
                "minimum_neighbours": None,
                "execution_time": None,
                "frequency": None,
                "rules": None,
                "technology_flow": None
            },
            "missing": ["state", "jc"]
        },

        {
            "text": "Schedule daily neighbour validation",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "CREATE_AUTOMATION",
                "state": None,
                "jc": None,
                "minimum_neighbours": None,
                "execution_time": None,
                "frequency": "DAILY",
                "rules": None,
                "technology_flow": None
            },
            "missing": ["state", "jc"]
        },

        # ---------------------------------------------------------
        # STATE PRESENT, JC MISSING
        # ---------------------------------------------------------

        {
            "text": "Create an automation for Uttar Pradesh",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "CREATE_AUTOMATION",
                "state": "Uttar Pradesh",
                "jc": None,
                "minimum_neighbours": None,
                "execution_time": None,
                "frequency": None,
                "rules": None,
                "technology_flow": None
            },
            "missing": ["jc"]
        },

        {
            "text": "Set up an automation for Maharashtra",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "CREATE_AUTOMATION",
                "state": "Maharashtra",
                "jc": None,
                "minimum_neighbours": None,
                "execution_time": None,
                "frequency": None,
                "rules": None,
                "technology_flow": None
            },
            "missing": ["jc"]
        },

        {
            "text": "Schedule cleanup for Rajasthan",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "CREATE_AUTOMATION",
                "state": "Rajasthan",
                "jc": None,
                "minimum_neighbours": None,
                "execution_time": None,
                "frequency": None,
                "rules": None,
                "technology_flow": None
            },
            "missing": ["jc"]
        },

        {
            "text": "Create a daily automation for Karnataka",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "CREATE_AUTOMATION",
                "state": "Karnataka",
                "jc": None,
                "minimum_neighbours": None,
                "execution_time": None,
                "frequency": "DAILY",
                "rules": None,
                "technology_flow": None
            },
            "missing": ["jc"]
        },

        {
            "text": "Schedule daily validation for Gujarat",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "CREATE_AUTOMATION",
                "state": "Gujarat",
                "jc": None,
                "minimum_neighbours": None,
                "execution_time": None,
                "frequency": "DAILY",
                "rules": None,
                "technology_flow": None
            },
            "missing": ["jc"]
        },

        {
            "text": "Set up PCI and TAC automation for Uttar Pradesh",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "CREATE_AUTOMATION",
                "state": "Uttar Pradesh",
                "jc": None,
                "minimum_neighbours": None,
                "execution_time": None,
                "frequency": None,
                "rules": ["PCI", "TAC"],
                "technology_flow": None
            },
            "missing": ["jc"]
        },

        {
            "text": "Create a daily cleanup automation for Maharashtra at 9 PM",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "CREATE_AUTOMATION",
                "state": "Maharashtra",
                "jc": None,
                "minimum_neighbours": None,
                "execution_time": "21:00",
                "frequency": "DAILY",
                "rules": None,
                "technology_flow": None
            },
            "missing": ["jc"]
        },

        {
            "text": "Schedule validation for Rajasthan at 10 AM",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "CREATE_AUTOMATION",
                "state": "Rajasthan",
                "jc": None,
                "minimum_neighbours": None,
                "execution_time": "10:00",
                "frequency": None,
                "rules": None,
                "technology_flow": None
            },
            "missing": ["jc"]
        },

        # ---------------------------------------------------------
        # JC PRESENT, STATE MISSING
        # ---------------------------------------------------------

        {
            "text": "Create an automation for JC_Lucknow",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "CREATE_AUTOMATION",
                "state": None,
                "jc": "JC_Lucknow",
                "minimum_neighbours": None,
                "execution_time": None,
                "frequency": None,
                "rules": None,
                "technology_flow": None
            },
            "missing": ["state"]
        },

        {
            "text": "Schedule cleanup for JC_Mumbai",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "CREATE_AUTOMATION",
                "state": None,
                "jc": "JC_Mumbai",
                "minimum_neighbours": None,
                "execution_time": None,
                "frequency": None,
                "rules": None,
                "technology_flow": None
            },
            "missing": ["state"]
        },

        {
            "text": "Create daily validation for JC_Bangalore",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "CREATE_AUTOMATION",
                "state": None,
                "jc": "JC_Bangalore",
                "minimum_neighbours": None,
                "execution_time": None,
                "frequency": "DAILY",
                "rules": None,
                "technology_flow": None
            },
            "missing": ["state"]
        },

        {
            "text": "Create an automation for JC_Jaipur and retain 10 neighbours",
            "intent": "MISSING_INFORMATION",
            "entities": {
                "requested_intent": "CREATE_AUTOMATION",
                "state": None,
                "jc": "JC_Jaipur",
                "minimum_neighbours": 10,
                "execution_time": None,
                "frequency": None,
                "rules": None,
                "technology_flow": None
            },
            "missing": ["state"]
        },


        # =========================================================
        # AMBIGUOUS REQUESTS
        # =========================================================

        {
            "text": "Check Lucknow",
            "intent": "AMBIGUOUS_REQUEST",
            "entities": {
                "jc": "JC_Lucknow"
            }
        },

        {
            "text": "Check JC_Lucknow",
            "intent": "AMBIGUOUS_REQUEST",
            "entities": {
                "jc": "JC_Lucknow"
            }
        },

        {
            "text": "Check Maharashtra",
            "intent": "AMBIGUOUS_REQUEST",
            "entities": {
                "state": "Maharashtra"
            }
        },

        {
            "text": "Do something about Uttar Pradesh",
            "intent": "AMBIGUOUS_REQUEST",
            "entities": {
                "state": "Uttar Pradesh"
            }
        },

        {
            "text": "Do something about JC_Mumbai",
            "intent": "AMBIGUOUS_REQUEST",
            "entities": {
                "jc": "JC_Mumbai"
            }
        },

        {
            "text": "Check the neighbours",
            "intent": "AMBIGUOUS_REQUEST",
            "entities": {}
        },

        {
            "text": "Look at the neighbours",
            "intent": "AMBIGUOUS_REQUEST",
            "entities": {}
        },

        {
            "text": "Clean Lucknow",
            "intent": "AMBIGUOUS_REQUEST",
            "entities": {
                "jc": "JC_Lucknow"
            }
        },


        # =========================================================
        # OUT OF SCOPE
        # =========================================================

        {
            "text": "Book a flight to Delhi",
            "intent": "OUT_OF_SCOPE",
            "entities": {}
        },

        {
            "text": "Send an email to my manager",
            "intent": "OUT_OF_SCOPE",
            "entities": {}
        },

        {
            "text": "Play some music",
            "intent": "OUT_OF_SCOPE",
            "entities": {}
        },

        {
            "text": "Tell me today's weather",
            "intent": "OUT_OF_SCOPE",
            "entities": {}
        },

        {
            "text": "Order a laptop for me",
            "intent": "OUT_OF_SCOPE",
            "entities": {}
        },

        {
            "text": "Book a hotel for me",
            "intent": "OUT_OF_SCOPE",
            "entities": {}
        }

    ]

    return examples


def remove_duplicates(examples):

    seen = set()
    unique_examples = []

    for example in examples:

        key = (
            example["text"].strip().lower(),
            example["intent"],
            json.dumps(
                example.get("entities", {}),
                sort_keys=True
            ),
            json.dumps(
                example.get("missing", []),
                sort_keys=True
            )
        )

        if key not in seen:

            seen.add(key)

            unique_examples.append(
                example
            )

    return unique_examples


def validate_examples(examples):

    errors = []

    for index, example in enumerate(examples):

        intent = example.get(
            "intent"
        )

        entities = example.get(
            "entities",
            {}
        )

        missing = example.get(
            "missing"
        )

        # -----------------------------------------------------
        # MISSING_INFORMATION validation
        # -----------------------------------------------------

        if intent == "MISSING_INFORMATION":

            if not missing:

                errors.append(
                    f"Example {index}: "
                    "MISSING_INFORMATION has no missing fields."
                )

            requested_intent = entities.get(
                "requested_intent"
            )

            if requested_intent not in (
                "START_CLEANUP",
                "CREATE_AUTOMATION"
            ):

                errors.append(
                    f"Example {index}: "
                    "MISSING_INFORMATION must have a valid "
                    "requested_intent."
                )

            # START_CLEANUP schema
            if requested_intent == "START_CLEANUP":

                required_fields = [
                    "state",
                    "jc",
                    "minimum_neighbours"
                ]

                for field in required_fields:

                    if field not in entities:

                        errors.append(
                            f"Example {index}: "
                            f"START_CLEANUP missing entity "
                            f"field '{field}'."
                        )

                if "state" in entities and (
                    "state" in missing
                    and entities["state"] is not None
                ):

                    errors.append(
                        f"Example {index}: "
                        "missing state must be None."
                    )

                if "jc" in entities and (
                    "jc" in missing
                    and entities["jc"] is not None
                ):

                    errors.append(
                        f"Example {index}: "
                        "missing jc must be None."
                    )

            # CREATE_AUTOMATION schema
            if requested_intent == "CREATE_AUTOMATION":

                required_fields = [
                    "state",
                    "jc",
                    "minimum_neighbours",
                    "execution_time",
                    "frequency",
                    "rules",
                    "technology_flow"
                ]

                for field in required_fields:

                    if field not in entities:

                        errors.append(
                            f"Example {index}: "
                            f"CREATE_AUTOMATION missing entity "
                            f"field '{field}'."
                        )

                if "state" in entities and (
                    "state" in missing
                    and entities["state"] is not None
                ):

                    errors.append(
                        f"Example {index}: "
                        "missing state must be None."
                    )

                if "jc" in entities and (
                    "jc" in missing
                    and entities["jc"] is not None
                ):

                    errors.append(
                        f"Example {index}: "
                        "missing jc must be None."
                    )

            for field in missing:

                if field not in entities:

                    errors.append(
                        f"Example {index}: "
                        f"missing field '{field}' "
                        "is absent from entities."
                    )

                elif entities[field] is not None:

                    errors.append(
                        f"Example {index}: "
                        f"missing field '{field}' "
                        "must be None."
                    )

        if intent == "MISSING_INFORMATION":

            requested_intent = entities.get(
                "requested_intent"
            )

            if requested_intent in (
                "START_CLEANUP",
                "CREATE_AUTOMATION"
            ):

                if (
                    entities.get("state") is not None
                    and entities.get("jc") is not None
                ):

                    errors.append(
                        f"Example {index}: "
                        "MISSING_INFORMATION cannot contain "
                        "both state and jc."
                    )

        # -----------------------------------------------------
        # Normal intent validation
        # -----------------------------------------------------

        if intent == "START_CLEANUP":

            if entities.get("state") is None:
                errors.append(
                    f"Example {index}: "
                    "START_CLEANUP requires state."
                )

            if entities.get("jc") is None:
                errors.append(
                    f"Example {index}: "
                    "START_CLEANUP requires jc."
                )

        if intent == "CREATE_AUTOMATION":

            if entities.get("state") is None:
                errors.append(
                    f"Example {index}: "
                    "CREATE_AUTOMATION requires state."
                )

            if entities.get("jc") is None:
                errors.append(
                    f"Example {index}: "
                    "CREATE_AUTOMATION requires jc."
                )

    return errors


def main():

    examples = create_special_examples()

    examples = remove_duplicates(
        examples
    )

    errors = validate_examples(
        examples
    )

    if errors:

        print(
            "\nSPECIAL DATASET VALIDATION FAILED"
        )

        for error in errors:

            print(
                "ERROR:",
                error
            )

        raise RuntimeError(
            "Special dataset validation failed."
        )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            examples,
            file,
            indent=4,
            ensure_ascii=False
        )

    from collections import Counter

    distribution = Counter(
        example["intent"]
        for example in examples
    )

    print(
        "Special dataset created."
    )

    print(
        "Examples:",
        len(examples)
    )

    print(
        "\nIntent distribution:"
    )

    for intent in sorted(
        distribution
    ):

        print(
            f"{intent}: "
            f"{distribution[intent]}"
        )

    print(
        "\nSpecial dataset validation PASSED."
    )

    print(
        "Schema validation: "
        "START_CLEANUP and CREATE_AUTOMATION "
        "require state + JC."
    )

    print(
        "Output:",
        OUTPUT_PATH
    )


if __name__ == "__main__":

    main()