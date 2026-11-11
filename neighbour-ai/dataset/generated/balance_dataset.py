import json
from pathlib import Path


OUTPUT = Path(
    "dataset/generated/balanced_examples.json"
)


# ============================================================
# STATE / JC DATA
# ============================================================

STATE_JC_MAP = {
    "Andhra Pradesh": ["JC_Vijayawada"],
    "Assam": ["JC_Guwahati"],
    "Bihar": ["JC_Patna"],
    "Chandigarh": ["JC_Chandigarh"],
    "Delhi": ["JC_Central_Delhi"],
    "Goa": ["JC_Panaji"],
    "Gujarat": ["JC_Ahmedabad"],
    "Haryana": ["JC_Gurgaon"],
    "Himachal Pradesh": ["JC_Shimla"],
    "Jammu and Kashmir": ["JC_Srinagar"],
    "Jharkhand": ["JC_Ranchi"],
    "Karnataka": ["JC_Bangalore"],
    "Kerala": ["JC_Kochi"],
    "Madhya Pradesh": ["JC_Bhopal"],
    "Maharashtra": ["JC_Mumbai"],
    "Odisha": ["JC_Bhubaneswar"],
    "Punjab": ["JC_Chandigarh"],
    "Rajasthan": [
        "JC_Jaipur",
        "JC_Jaipur_North"
    ],
    "Tamil Nadu": ["JC_Chennai"],
    "Telangana": ["JC_Hyderabad"],
    "Uttar Pradesh": ["JC_Lucknow"],
    "Uttarakhand": ["JC_Dehradun"],
    "West Bengal": ["JC_Kolkata"]
}


# ============================================================
# BALANCED TEMPLATES
# ============================================================

BALANCED_TEMPLATES = {

    # ========================================================
    # GET_STATES
    # ========================================================

    "GET_STATES": [
        "Show all states",
        "List the available states",
        "Give me all states",
        "Display all states",
        "What states do we have",
        "Show available states",
        "List available states in the system",
        "Tell me all configured states",
        "Which states are configured",
        "What are the available states",
        "Show me the state list",
        "Give me the state list",
        "Display the state list",
        "I want to see all states",
        "Get all states",
        "Fetch all states",
        "Retrieve the available states",
        "Show the configured states",
        "List all configured states",
        "What states are present",

        # Stronger state-vs-JC boundary
        "I want to see every state",
        "Show me every state in the system",
        "Which states are present in the system",
        "Give me the complete list of states",
        "List every configured state",
        "What states are configured in the system",
        "Show every configured state",
        "Tell me which states are available",
        "Fetch the complete state list",
        "Display every available state"
    ],


    # ========================================================
    # GET_AUTOMATIONS
    # ========================================================

    "GET_AUTOMATIONS": [
        "Show my automations",
        "List my automations",
        "Show all automations",
        "List all automations",
        "Display the automations",
        "What automations are available",
        "What automations are configured",
        "Show configured automations",
        "List configured automations",
        "Give me the automation list",
        "Show the automation list",
        "Get all automations",
        "Fetch the automations",
        "Retrieve configured automations",
        "Which automations are active",
        "What automation jobs exist",
        "Show automation jobs",
        "List automation jobs",
        "Give me all configured automation jobs",
        "Display configured automation jobs"
    ],


    # ========================================================
    # CREATE_AUTOMATION
    # COMPLETE COMMANDS ONLY
    # ========================================================

    "CREATE_AUTOMATION": [

        "Create an automation for Uttar Pradesh JC_Lucknow",
        "Set up an automation for Maharashtra JC_Mumbai",
        "Create a cleanup automation for Rajasthan JC_Jaipur",
        "Schedule neighbour validation for Karnataka JC_Bangalore",
        "Schedule cleanup for Uttar Pradesh JC_Lucknow",
        "Set up automated neighbour validation for Maharashtra JC_Mumbai",
        "Create an automated cleanup job for Rajasthan JC_Jaipur_North",
        "Configure an automation for Delhi JC_Central_Delhi",
        "Create a scheduled job for Gujarat JC_Ahmedabad",
        "Set up scheduled cleanup for Punjab JC_Chandigarh",

        "Create a daily automation for Uttar Pradesh JC_Lucknow",
        "Schedule daily validation for Maharashtra JC_Mumbai",
        "Set up daily cleanup for Rajasthan JC_Jaipur",
        "Create a weekly automation for Karnataka JC_Bangalore",
        "Schedule weekly cleanup for Gujarat JC_Ahmedabad",
        "Create a monthly automation for Delhi JC_Central_Delhi",
        "Set up monthly validation for Punjab JC_Chandigarh",

        "Create an automation for Uttar Pradesh JC_Lucknow at 09:00",
        "Schedule cleanup for Maharashtra JC_Mumbai at 21:00",
        "Set up daily automation for Rajasthan JC_Jaipur at 20:00",
        "Schedule weekly validation for Karnataka JC_Bangalore at 18:00",
        "Create monthly cleanup for Gujarat JC_Ahmedabad at 10:00",

        "Create an automation for Uttar Pradesh JC_Lucknow and retain 10 neighbours",
        "Schedule cleanup for Maharashtra JC_Mumbai and retain 5 neighbours",
        "Create daily cleanup for Rajasthan JC_Jaipur and retain 15 neighbours",
        "Set up an automation for Karnataka JC_Bangalore with minimum retention of 20",
        "Create weekly cleanup for Gujarat JC_Ahmedabad and retain 10 neighbours",

        "Create PCI and TAC validation automation for Uttar Pradesh JC_Lucknow",
        "Schedule PCI and TAC validation for Maharashtra JC_Mumbai",
        "Create daily PCI and TAC validation for Rajasthan JC_Jaipur",
        "Schedule weekly PCI and TAC validation for Karnataka JC_Bangalore",
        "Create monthly PCI and TAC validation for Gujarat JC_Ahmedabad",

        "Create daily PCI and TAC validation for Uttar Pradesh JC_Lucknow at 21:00",
        "Schedule daily cleanup for Maharashtra JC_Mumbai at 20:00 and retain 10 neighbours",
        "Create weekly cleanup for Rajasthan JC_Jaipur at 09:00 and retain 5 neighbours",
        "Set up monthly validation for Karnataka JC_Bangalore at 18:00",
        "Create an automation for Gujarat JC_Ahmedabad at 10:00 and retain 15 neighbours",

        # Additional complete examples
        "Create daily cleanup for Bihar JC_Patna",
        "Create weekly validation for Assam JC_Guwahati",
        "Schedule monthly cleanup for Kerala JC_Kochi",
        "Create PCI validation automation for Telangana JC_Hyderabad",
        "Create TAC validation automation for Odisha JC_Bhubaneswar",
        "Schedule daily cleanup for Uttarakhand JC_Dehradun",
        "Create weekly automation for West Bengal JC_Kolkata"
    ],


    # ========================================================
    # GET_CLEANUP_PROGRESS
    # ========================================================

    "GET_CLEANUP_PROGRESS": [
        "Show cleanup progress",
        "Show the cleanup progress",
        "What is the cleanup progress",
        "How much cleanup is completed",
        "How much of the cleanup is complete",
        "Show cleanup completion",
        "Show cleanup status",
        "What is the current cleanup status",
        "How far has cleanup progressed",
        "Give me the cleanup progress",
        "Give me the current cleanup status",
        "How much work is completed",
        "What percentage of cleanup is complete",
        "Show the cleanup percentage",
        "Tell me the current cleanup percentage",
        "Check cleanup progress",
        "Check the cleanup status",
        "Is the cleanup completed",
        "How far is the cleanup",
        "What is happening with the cleanup"
    ],


    # ========================================================
    # GET_CLEANUP_RESULT
    # ========================================================

    "GET_CLEANUP_RESULT": [
        "Show the cleanup result",
        "Show the cleanup results",
        "Give me the cleanup result",
        "Show the final cleanup result",
        "What was the cleanup result",
        "What happened during cleanup",
        "Show the cleanup summary",
        "Give me the cleanup summary",
        "Show the final cleanup summary",
        "How many neighbours were deleted",
        "How many records were removed",
        "Tell me what was deleted",
        "Show what was deleted",
        "Give me the deletion result",
        "Show the deletion summary",
        "What did the cleanup remove",
        "Show the completed cleanup details",
        "Give me the completed cleanup details",
        "Get the latest cleanup result",
        "Show the last cleanup result"
    ],


    # ========================================================
    # START_CLEANUP
    # COMPLETE COMMANDS ONLY
    # ========================================================

    "START_CLEANUP": [

        "Delete invalid neighbours in Uttar Pradesh JC_Lucknow",
        "Clean invalid neighbours in Maharashtra JC_Mumbai",
        "Remove invalid neighbours from Rajasthan JC_Jaipur",
        "Start cleanup for Karnataka JC_Bangalore",
        "Run cleanup for Gujarat JC_Ahmedabad",
        "Delete invalid neighbour records in Delhi JC_Central_Delhi",
        "Clean the bad neighbours in Punjab JC_Chandigarh",
        "Run invalid neighbour cleanup for Kerala JC_Kochi",
        "Start deleting invalid neighbours in Telangana JC_Hyderabad",
        "Perform cleanup for Bihar JC_Patna",

        "Delete invalid neighbours in Uttar Pradesh JC_Lucknow retain 5",
        "Delete invalid neighbours in Maharashtra JC_Mumbai retain 10",
        "Clean invalid neighbours in Rajasthan JC_Jaipur retain 15",
        "Run cleanup for Karnataka JC_Bangalore retain 20",
        "Remove invalid neighbours in Gujarat JC_Ahmedabad retain 10",

        "Please clean the invalid neighbours in Uttar Pradesh JC_Lucknow",
        "Please remove invalid neighbour records in Maharashtra JC_Mumbai",
        "Start the cleanup for Rajasthan JC_Jaipur",
        "Run the cleanup for Karnataka JC_Bangalore",
        "Delete all eligible invalid neighbours in Gujarat JC_Ahmedabad"
    ],


    # ========================================================
    # AMBIGUOUS REQUESTS
    # ========================================================

    "AMBIGUOUS_REQUEST": [
        "Check Lucknow",
        "Check JC_Lucknow",
        "Look at Lucknow",
        "Show me Lucknow",
        "Do something about Lucknow",
        "Check Maharashtra",
        "Look at Maharashtra",
        "Do something about Maharashtra",
        "Check JC_Mumbai",
        "Look at JC_Mumbai",
        "Do something about JC_Mumbai",
        "Check the neighbours",
        "Look at the neighbours",
        "Do something with the neighbours",
        "Check this JC",
        "Look at this JC",
        "Check this state",
        "Do something about this state",
        "Can you check Lucknow",
        "Can you look at JC_Mumbai"
    ],


    # ========================================================
    # OUT OF SCOPE
    # ========================================================

    "OUT_OF_SCOPE": [
        "Book a flight",
        "Send an email",
        "Play some music",
        "Tell me the weather",
        "Order a laptop",
        "Book a hotel",
        "Send me an email",
        "Play a song",
        "What is today's weather",
        "Order something online",
        "Book a train ticket",
        "Set an alarm",
        "Open my social media",
        "Send a message to someone",
        "Buy something for me",
        "Translate this sentence",
        "Write an essay for me",
        "Show me a movie",
        "Find a restaurant",
        "Give me directions"
    ]
}


# ============================================================
# CREATE EXAMPLE
# ============================================================

def create_example(intent, text):

    # --------------------------------------------------------
    # START_CLEANUP
    #
    # IMPORTANT:
    # Every START_CLEANUP example generated here is COMPLETE.
    # Incomplete cleanup belongs to MISSING_INFORMATION and is
    # handled by special_examples.py / seed_dataset.json.
    # --------------------------------------------------------

    if intent == "START_CLEANUP":

        lower_text = text.lower()

        entities = {
            "state": None,
            "jc": None,
            "minimum_neighbours": None
        }

        # ----------------------------------------------------
        # State
        # ----------------------------------------------------

        for state in STATE_JC_MAP:

            if state.lower() in lower_text:

                entities["state"] = state

                break

        # ----------------------------------------------------
        # JC
        # ----------------------------------------------------

        for jcs in STATE_JC_MAP.values():

            for jc in jcs:

                if jc.lower() in lower_text:

                    entities["jc"] = jc

                    break

            if entities["jc"] is not None:

                break

        # ----------------------------------------------------
        # Minimum retention
        # ----------------------------------------------------

        for value in [
            5,
            10,
            15,
            20
        ]:

            patterns = [
                f"retain {value}",
                f"retention of {value}",
                f"minimum retention of {value}"
            ]

            if any(
                pattern in lower_text
                for pattern in patterns
            ):

                entities[
                    "minimum_neighbours"
                ] = value

                break

        # ----------------------------------------------------
        # Safety validation
        # ----------------------------------------------------

        if (
            entities["state"] is None
            or
            entities["jc"] is None
        ):

            raise ValueError(
                "START_CLEANUP example is incomplete: "
                f"{text}"
            )

        return {
            "text": text,
            "intent": "START_CLEANUP",
            "entities": entities
        }


    # --------------------------------------------------------
    # CREATE_AUTOMATION
    #
    # IMPORTANT:
    # Every CREATE_AUTOMATION example generated here is COMPLETE.
    # Incomplete automation belongs to MISSING_INFORMATION.
    # --------------------------------------------------------

    if intent == "CREATE_AUTOMATION":

        lower_text = text.lower()

        entities = {
            "state": None,
            "jc": None,
            "minimum_neighbours": None,
            "execution_time": None,
            "frequency": None,
            "rules": None,
            "technology_flow": None
        }

        # ----------------------------------------------------
        # State
        # ----------------------------------------------------

        for state in STATE_JC_MAP:

            if state.lower() in lower_text:

                entities["state"] = state

                break

        # ----------------------------------------------------
        # JC
        # ----------------------------------------------------

        for jcs in STATE_JC_MAP.values():

            for jc in jcs:

                if jc.lower() in lower_text:

                    entities["jc"] = jc

                    break

            if entities["jc"] is not None:

                break

        # ----------------------------------------------------
        # Frequency
        # ----------------------------------------------------

        if "daily" in lower_text:

            entities["frequency"] = "DAILY"

        elif "weekly" in lower_text:

            entities["frequency"] = "WEEKLY"

        elif "monthly" in lower_text:

            entities["frequency"] = "MONTHLY"

        # ----------------------------------------------------
        # Execution time
        # ----------------------------------------------------

        time_values = [
            "08:00",
            "09:00",
            "10:00",
            "18:00",
            "20:00",
            "21:00"
        ]

        for time_value in time_values:

            if time_value in text:

                entities[
                    "execution_time"
                ] = time_value

                break

        # ----------------------------------------------------
        # Minimum retention
        # ----------------------------------------------------

        for value in [
            5,
            10,
            15,
            20
        ]:

            patterns = [
                f"retain {value}",
                f"retention of {value}",
                f"minimum retention of {value}"
            ]

            if any(
                pattern in lower_text
                for pattern in patterns
            ):

                entities[
                    "minimum_neighbours"
                ] = value

                break

        # ----------------------------------------------------
        # Rules
        # ----------------------------------------------------

        has_pci = "pci" in lower_text
        has_tac = "tac" in lower_text

        if has_pci and has_tac:

            entities["rules"] = [
                "PCI",
                "TAC"
            ]

        elif has_pci:

            entities["rules"] = [
                "PCI"
            ]

        elif has_tac:

            entities["rules"] = [
                "TAC"
            ]

        # ----------------------------------------------------
        # Safety validation
        # ----------------------------------------------------

        if (
            entities["state"] is None
            or
            entities["jc"] is None
        ):

            raise ValueError(
                "CREATE_AUTOMATION example is incomplete: "
                f"{text}"
            )

        return {
            "text": text,
            "intent": "CREATE_AUTOMATION",
            "entities": entities
        }


    # --------------------------------------------------------
    # AMBIGUOUS REQUEST
    # --------------------------------------------------------

    if intent == "AMBIGUOUS_REQUEST":

        entities = {}

        lower_text = text.lower()

        if "lucknow" in lower_text:

            entities["jc"] = "JC_Lucknow"

        elif "mumbai" in lower_text:

            entities["jc"] = "JC_Mumbai"

        elif "maharashtra" in lower_text:

            entities["state"] = "Maharashtra"

        return {
            "text": text,
            "intent": "AMBIGUOUS_REQUEST",
            "entities": entities
        }


    # --------------------------------------------------------
    # NORMAL INTENTS
    # --------------------------------------------------------

    return {
        "text": text,
        "intent": intent,
        "entities": {}
    }


# ============================================================
# ENTITY SCHEMA
# ============================================================

START_CLEANUP_FIELDS = [
    "state",
    "jc",
    "minimum_neighbours"
]

CREATE_AUTOMATION_FIELDS = [
    "state",
    "jc",
    "minimum_neighbours",
    "execution_time",
    "frequency",
    "rules",
    "technology_flow"
]


# ============================================================
# VALIDATE BALANCED DATASET
# ============================================================


def validate_dataset(dataset):

    errors = []

    for index, example in enumerate(dataset):

        intent = example.get("intent")
        entities = example.get("entities")

        if not isinstance(entities, dict):
            errors.append(
                f"Example {index}: entities must be an object."
            )
            continue

        # ----------------------------------------------------
        # START_CLEANUP
        # ----------------------------------------------------

        if intent == "START_CLEANUP":

            for field in START_CLEANUP_FIELDS:

                if field not in entities:
                    errors.append(
                        f"Example {index}: "
                        f"START_CLEANUP missing entity field '{field}'."
                    )

            if entities.get("state") is None:
                errors.append(
                    f"Example {index}: "
                    "START_CLEANUP has no state."
                )

            if entities.get("jc") is None:
                errors.append(
                    f"Example {index}: "
                    "START_CLEANUP has no JC."
                )

        # ----------------------------------------------------
        # CREATE_AUTOMATION
        # ----------------------------------------------------

        if intent == "CREATE_AUTOMATION":

            for field in CREATE_AUTOMATION_FIELDS:

                if field not in entities:
                    errors.append(
                        f"Example {index}: "
                        f"CREATE_AUTOMATION missing entity field '{field}'."
                    )

            if entities.get("state") is None:
                errors.append(
                    f"Example {index}: "
                    "CREATE_AUTOMATION has no state."
                )

            if entities.get("jc") is None:
                errors.append(
                    f"Example {index}: "
                    "CREATE_AUTOMATION has no JC."
                )

    return errors


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicates(dataset):

    seen = set()

    unique_dataset = []

    for example in dataset:

        key = (
            example["text"].strip().lower(),
            example["intent"],
            json.dumps(
                example.get(
                    "entities",
                    {}
                ),
                sort_keys=True
            )
        )

        if key not in seen:

            seen.add(key)

            unique_dataset.append(
                example
            )

    return unique_dataset


# ============================================================
# MAIN
# ============================================================

def main():

    dataset = []

    for intent, templates in BALANCED_TEMPLATES.items():

        for text in templates:

            dataset.append(
                create_example(
                    intent,
                    text
                )
            )

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    dataset = remove_duplicates(
        dataset
    )

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    errors = validate_dataset(
        dataset
    )

    # Hard safety rule for the training dataset:
    # executable cleanup/automation examples must always
    # contain both State and JC. Missing-information examples
    # are generated only by special_examples.py / seed data.
    for index, example in enumerate(dataset):

        if example["intent"] in (
            "START_CLEANUP",
            "CREATE_AUTOMATION"
        ):

            entities = example["entities"]

            if not entities.get("state") or not entities.get("jc"):

                errors.append(
                    f"Example {index}: executable "
                    f"{example['intent']} has incomplete scope."
                )

    if errors:

        print()
        print(
            "BALANCED DATASET VALIDATION FAILED"
        )
        print(
            "--------------------------------------------------------"
        )

        for error in errors:

            print(
                "ERROR:",
                error
            )

        raise RuntimeError(
            "Balanced dataset validation failed."
        )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            dataset,
            file,
            indent=2,
            ensure_ascii=False
        )

    # --------------------------------------------------------
    # Distribution
    # --------------------------------------------------------

    from collections import Counter

    distribution = Counter(
        example["intent"]
        for example in dataset
    )

    print()
    print(
        "Balanced examples created:",
        len(dataset)
    )

    print()
    print(
        "Intent distribution:"
    )

    for intent in sorted(
        distribution
    ):

        print(
            f"{intent}: "
            f"{distribution[intent]}"
        )

    print()
    print(
        "Balanced dataset validation PASSED."
    )

    print(
        "Output:",
        OUTPUT
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()