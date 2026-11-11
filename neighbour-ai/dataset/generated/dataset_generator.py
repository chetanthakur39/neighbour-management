import json
import random
from pathlib import Path


# ============================================================
# DATASET GENERATOR
# File name used by this project:
# dataset/generated/dataset_generator.py
#
# IMPORTANT SCHEMA RULE
# ---------------------
# Executable START_CLEANUP and CREATE_AUTOMATION examples
# require BOTH state and jc.
#
# Incomplete requests are labelled MISSING_INFORMATION and use:
#
# entities.requested_intent
# entities.state
# entities.jc
# entities.minimum_neighbours
# entities.execution_time
# entities.frequency
# entities.rules
# entities.technology_flow
#
# This schema is intentionally aligned with build_dataset.py,
# special_examples.py and seed_dataset.json.
# ============================================================


# ============================================================
# STATE -> JC MAPPING
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
# GENERAL INTENT TEMPLATES
# ============================================================

TEMPLATES = {

    "GET_STATES": [
        "Show me all available states",
        "List all states",
        "Which states are available",
        "What states are available in the system",
        "Give me the list of states",
        "Display all available states"
    ],

    "GET_JCS": [
        "Show the JCs in {state}",
        "Which JCs are available in {state}",
        "List the JCs for {state}",
        "Give me all JCs in {state}",
        "What JCs are available for {state}",
        "Show me the Jio Centers in {state}"
    ],

    "GET_NEIGHBOURS": [
        "Show neighbours in {state} for {jc}",
        "Show the neighbour relations for {jc}",
        "Give me the neighbours for {jc}",
        "List neighbours for {state} {jc}",
        "Display neighbour relations in {jc}",
        "Show me all neighbours for {jc}"
    ],

    "VALIDATE_NEIGHBOURS": [
        "Validate neighbours in {state} for {jc}",
        "Check neighbours in {state} for {jc}",
        "Run validation for {state} {jc}",
        "Validate the neighbour relations for {jc}",
        "Check PCI and TAC validity for {jc}",
        "Run PCI and TAC validation for {state} {jc}"
    ],

    "GET_INVALID_NEIGHBOURS": [
        "Show invalid neighbours in {state}",
        "Find invalid neighbours in {state}",
        "Which neighbour relations are invalid in {jc}",
        "Show the invalid neighbours for {jc}",
        "Find bad neighbour relations in {state}",
        "Show neighbours failing validation for {jc}"
    ],

    "GET_PCI_INVALID": [
        "Show PCI mismatches in {state}",
        "Find PCI problems in {jc}",
        "Which neighbours have a PCI mismatch in {state}",
        "Show neighbours with invalid PCI for {jc}",
        "Find PCI mismatch neighbours in {state}",
        "Which neighbour relations have PCI problems"
    ],

    "GET_TAC_INVALID": [
        "Show TAC mismatches in {state}",
        "Find TAC problems in {jc}",
        "Which neighbours have a TAC mismatch in {state}",
        "Show neighbours with invalid TAC for {jc}",
        "Find TAC mismatch neighbours in {state}",
        "Which neighbour relations have TAC problems"
    ],

    "GET_COUNTS": [
        "How many neighbours are valid and invalid in {state}",
        "Give me the valid and invalid count for {jc}",
        "How many invalid neighbours are there in {state}",
        "Show neighbour counts for {jc}",
        "Give me the neighbour statistics for {state}",
        "What are the valid and invalid totals for {jc}"
    ],

    "GET_INVALID_PERCENTAGE": [
        "What percentage of neighbours are invalid in {state}",
        "Show the invalid percentage for {jc}",
        "What is the invalid percentage in {state}",
        "Calculate the invalid neighbour percentage for {jc}",
        "How much of the neighbours are invalid in {state}"
    ],

    "PREVIEW_CLEANUP": [
        "Preview cleanup for {state} {jc}",
        "Show what cleanup would do for {state} {jc}",
        "How many neighbours would be deleted in {jc}",
        "Preview the invalid neighbour cleanup for {state}",
        "Show me the cleanup preview for {jc}",
        "What would happen if I cleaned {state} {jc}"
    ],

    # ========================================================
    # EXECUTABLE CLEANUP - COMPLETE COMMANDS ONLY
    # ========================================================

    "START_CLEANUP": [
        "Delete invalid neighbours in {state} {jc}",
        "Clean the invalid neighbours from {state} {jc}",
        "Remove invalid neighbour relations in {state} {jc}",
        "Start cleanup for {state} {jc}",
        "Please clean the invalid neighbours in {state} {jc}",
        "Run cleanup for {state} {jc}"
    ],

    # ========================================================
    # INCOMPLETE CLEANUP - ALWAYS MISSING_INFORMATION
    # ========================================================

    "START_CLEANUP_MISSING": [
        "Delete invalid neighbours in {state}",
        "Clean invalid neighbours for {jc}",
        "Start cleanup",
        "Run cleanup",
        "Delete invalid neighbours",
        "Clean neighbours in {state}",
        "Start cleanup for {jc}"
    ],

    "GET_CLEANUP_PROGRESS": [
        "Show cleanup progress",
        "How much of the cleanup is completed",
        "What is the current cleanup progress",
        "Show me the cleanup status",
        "How far has the cleanup progressed",
        "Give me the current cleanup percentage"
    ],

    "GET_CLEANUP_RESULT": [
        "Show the cleanup result",
        "How many neighbours were deleted",
        "Give me the result of the last cleanup",
        "Show the cleanup summary",
        "What happened during the cleanup",
        "Give me the final cleanup result"
    ],

    "GET_AUTOMATIONS": [
        "Show my automations",
        "List all configured automations",
        "Show available automations",
        "What automations are configured",
        "Give me the automation list"
    ],

    # ========================================================
    # EXECUTABLE AUTOMATION - COMPLETE COMMANDS ONLY
    # ========================================================

    "CREATE_AUTOMATION": [
        "Create an automation for {state} {jc}",
        "Set up an automation for {state} {jc}",
        "Create a cleanup automation for {state} {jc}",
        "Schedule neighbour validation for {state} {jc}",
        "Schedule cleanup for {state} {jc}",
        "Set up automated neighbour validation for {state} {jc}",
        "Create an automated cleanup job for {state} {jc}",
        "Configure an automation for {state} {jc}",
        "Create a scheduled job for {state} {jc}",
        "Set up scheduled cleanup for {state} {jc}",
        "Create a {frequency} automation for {state} {jc}",
        "Schedule {frequency} validation for {state} {jc}",
        "Set up {frequency} cleanup for {state} {jc}",
        "Create a {frequency} cleanup automation for {state} {jc}",
        "Schedule neighbour validation for {state} {jc} at {execution_time}",
        "Create an automation for {state} {jc} at {execution_time}",
        "Schedule cleanup for {state} {jc} at {execution_time}",
        "Set up {frequency} automation for {state} {jc} at {execution_time}",
        "Create {frequency} cleanup for {state} {jc} at {execution_time}",
        "Schedule {frequency} neighbour validation for {state} {jc} at {execution_time}",
        "Create an automation for {state} {jc} and retain {minimum_neighbours} neighbours",
        "Schedule cleanup for {state} {jc} and retain {minimum_neighbours} neighbours",
        "Create {frequency} cleanup for {state} {jc} and retain {minimum_neighbours} neighbours",
        "Set up an automation for {state} {jc} with minimum retention of {minimum_neighbours}",
        "Create PCI and TAC validation automation for {state} {jc}",
        "Schedule PCI and TAC validation for {state} {jc}",
        "Create {frequency} PCI and TAC validation for {state} {jc}",
        "Schedule {frequency} PCI and TAC validation for {state} {jc} at {execution_time}",
        "Create a {frequency} automation for {state} {jc} at {execution_time} and retain {minimum_neighbours} neighbours"
    ],

    # ========================================================
    # INCOMPLETE AUTOMATION - ALWAYS MISSING_INFORMATION
    # ========================================================

    "CREATE_AUTOMATION_MISSING": [
        "Create an automation for {state}",
        "Set up an automation for {jc}",
        "Create a cleanup automation",
        "Schedule neighbour validation",
        "Schedule cleanup",
        "Set up automated neighbour validation for {state}",
        "Create an automated cleanup job for {jc}",
        "Configure an automation",
        "Create a scheduled job",
        "Set up scheduled cleanup for {state}",
        "Create a {frequency} automation for {state}",
        "Schedule {frequency} validation for {jc}",
        "Set up {frequency} cleanup",
        "Create PCI and TAC validation automation",
        "Schedule PCI and TAC validation for {state}"
    ]
}


# ============================================================
# AUTOMATION VALUES
# ============================================================

FREQUENCIES = [
    "DAILY",
    "WEEKLY",
    "MONTHLY"
]

EXECUTION_TIMES = [
    "08:00",
    "09:00",
    "10:00",
    "11:00",
    "18:00",
    "19:00",
    "20:00",
    "21:00"
]

MINIMUM_NEIGHBOURS = [
    5,
    10,
    15,
    20
]

AUTOMATION_RULES = [
    ["PCI"],
    ["TAC"],
    ["PCI", "TAC"]
]

TECHNOLOGY_FLOWS = [
    "4G",
    "5G",
    "ALL"
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def choose_state_and_jc():
    state = random.choice(
        list(STATE_JC_MAP.keys())
    )

    jc = random.choice(
        STATE_JC_MAP[state]
    )

    return state, jc


# ============================================================
# CREATE AUTOMATION EXAMPLE
# ============================================================

def generate_automation_example(template):

    state, jc = choose_state_and_jc()

    frequency = None
    execution_time = None
    minimum_neighbours = None
    rules = None
    technology_flow = None

    if "{frequency}" in template:
        frequency = random.choice(FREQUENCIES)

    if "{execution_time}" in template:
        execution_time = random.choice(EXECUTION_TIMES)

    if "{minimum_neighbours}" in template:
        minimum_neighbours = random.choice(
            MINIMUM_NEIGHBOURS
        )

    if "PCI" in template and "TAC" in template:
        rules = ["PCI", "TAC"]
    elif "PCI" in template:
        rules = ["PCI"]
    elif "TAC" in template:
        rules = ["TAC"]

    text = template.format(
        state=state,
        jc=jc,
        frequency=(
            frequency.lower()
            if frequency
            else ""
        ),
        execution_time=(
            execution_time
            if execution_time
            else ""
        ),
        minimum_neighbours=(
            minimum_neighbours
            if minimum_neighbours is not None
            else ""
        )
    )

    entities = {
        "state": state,
        "jc": jc,
        "minimum_neighbours": minimum_neighbours,
        "execution_time": execution_time,
        "frequency": frequency,
        "rules": rules,
        "technology_flow": technology_flow
    }

    return {
        "text": text.strip(),
        "intent": "CREATE_AUTOMATION",
        "entities": entities
    }


# ============================================================
# MISSING INFORMATION EXAMPLE
# ============================================================

def generate_missing_information_example(
    requested_intent,
    template
):
    """
    Generate an incomplete command.

    IMPORTANT:
    The final schema uses entities.requested_intent.
    It does NOT use a top-level source_intent.
    """

    state, jc = choose_state_and_jc()

    needs_state = "{state}" in template
    needs_jc = "{jc}" in template

    include_state = (
        needs_state
        and random.choice([True, False])
    )

    include_jc = (
        needs_jc
        and random.choice([True, False])
    )

    # If the template can contain both, guarantee that at least
    # one required entity is missing.
    if (
        needs_state
        and needs_jc
        and include_state
        and include_jc
    ):
        if random.choice([True, False]):
            include_state = False
        else:
            include_jc = False

    frequency = (
        random.choice(FREQUENCIES)
        if "{frequency}" in template
        else None
    )

    execution_time = (
        random.choice(EXECUTION_TIMES)
        if "{execution_time}" in template
        else None
    )

    minimum_neighbours = (
        random.choice(MINIMUM_NEIGHBOURS)
        if "{minimum_neighbours}" in template
        else None
    )

    text = template.format(
        state=(
            state
            if include_state
            else ""
        ),
        jc=(
            jc
            if include_jc
            else ""
        ),
        frequency=(
            frequency.lower()
            if frequency
            else ""
        ),
        execution_time=(
            execution_time
            if execution_time
            else ""
        ),
        minimum_neighbours=(
            minimum_neighbours
            if minimum_neighbours is not None
            else ""
        )
    )

    text = " ".join(
        text.split()
    ).strip()

    rules = None

    if "PCI" in template and "TAC" in template:
        rules = ["PCI", "TAC"]
    elif "PCI" in template:
        rules = ["PCI"]
    elif "TAC" in template:
        rules = ["TAC"]

    entities = {
        "requested_intent": requested_intent,
        "state": (
            state
            if include_state
            else None
        ),
        "jc": (
            jc
            if include_jc
            else None
        ),
        "minimum_neighbours": minimum_neighbours,
        "execution_time": execution_time,
        "frequency": frequency,
        "rules": rules,
        "technology_flow": None
    }

    missing = []

    if entities["state"] is None:
        missing.append("state")

    if entities["jc"] is None:
        missing.append("jc")

    if not missing:
        raise ValueError(
            "MISSING_INFORMATION example accidentally "
            "contains both state and JC: "
            f"{text}"
        )

    return {
        "text": text,
        "intent": "MISSING_INFORMATION",
        "entities": entities,
        "missing": missing
    }


# ============================================================
# NORMAL EXAMPLE
# ============================================================

def generate_example(
    intent,
    template,
    state=None,
    jc=None
):

    text = template.format(
        state=state or "",
        jc=jc or ""
    )

    entities = {}

    if "{state}" in template:
        entities["state"] = state

    if "{jc}" in template:
        entities["jc"] = jc

    if intent in [
        "START_CLEANUP",
        "PREVIEW_CLEANUP"
    ]:
        entities["minimum_neighbours"] = None

    return {
        "text": text.strip(),
        "intent": intent,
        "entities": entities
    }


# ============================================================
# DATASET GENERATION
# ============================================================

def generate_dataset(
    examples_per_intent=100
):

    dataset = []

    for intent, templates in TEMPLATES.items():

        for _ in range(
            examples_per_intent
        ):

            template = random.choice(
                templates
            )

            # ------------------------------------------------
            # INCOMPLETE OPERATIONS
            # ------------------------------------------------

            if intent.endswith("_MISSING"):

                requested_intent = (
                    intent.replace(
                        "_MISSING",
                        ""
                    )
                )

                example = (
                    generate_missing_information_example(
                        requested_intent,
                        template
                    )
                )

            # ------------------------------------------------
            # CREATE_AUTOMATION
            # ------------------------------------------------

            elif intent == "CREATE_AUTOMATION":

                example = (
                    generate_automation_example(
                        template
                    )
                )

            # ------------------------------------------------
            # NORMAL INTENTS
            # ------------------------------------------------

            else:

                state, jc = (
                    choose_state_and_jc()
                )

                example = generate_example(
                    intent,
                    template,
                    state,
                    jc
                )

            dataset.append(
                example
            )

    return dataset


# ============================================================
# DUPLICATE REMOVAL
# ============================================================

def remove_duplicates(dataset):

    seen = set()
    unique_dataset = []

    for example in dataset:

        key = (
            example["text"].lower(),
            example["intent"],
            json.dumps(
                example["entities"],
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
# DATASET SUMMARY
# ============================================================

def print_intent_summary(dataset):

    counts = {}

    for example in dataset:

        intent = example["intent"]

        counts[intent] = (
            counts.get(intent, 0) + 1
        )

    print()
    print(
        "Intent distribution:"
    )

    for intent in sorted(counts):

        print(
            f"{intent}: {counts[intent]}"
        )


# ============================================================
# HARD VALIDATION
# ============================================================

def validate_required_entities(dataset):

    errors = []

    for index, example in enumerate(dataset):

        intent = example["intent"]
        entities = example.get(
            "entities",
            {}
        )

        # ----------------------------------------------------
        # EXECUTABLE CLEANUP / AUTOMATION
        # ----------------------------------------------------

        if intent in [
            "START_CLEANUP",
            "CREATE_AUTOMATION"
        ]:

            if not entities.get("state"):

                errors.append(
                    f"Example {index}: "
                    f"{intent} is missing state."
                )

            if not entities.get("jc"):

                errors.append(
                    f"Example {index}: "
                    f"{intent} is missing JC."
                )

        # ----------------------------------------------------
        # MISSING INFORMATION
        # ----------------------------------------------------

        elif intent == "MISSING_INFORMATION":

            requested_intent = entities.get(
                "requested_intent"
            )

            if requested_intent not in [
                "START_CLEANUP",
                "CREATE_AUTOMATION"
            ]:

                errors.append(
                    f"Example {index}: "
                    "MISSING_INFORMATION has invalid "
                    "requested_intent."
                )

                continue

            # Required schema fields
            required_fields = [
                "requested_intent",
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
                        f"MISSING_INFORMATION missing "
                        f"entity field '{field}'."
                    )

            missing = example.get(
                "missing"
            )

            if (
                not isinstance(missing, list)
                or not missing
            ):

                errors.append(
                    f"Example {index}: "
                    "MISSING_INFORMATION has no "
                    "missing fields."
                )

                continue

            expected_missing = []

            if not entities.get("state"):
                expected_missing.append(
                    "state"
                )

            if not entities.get("jc"):
                expected_missing.append(
                    "jc"
                )

            if sorted(missing) != sorted(
                expected_missing
            ):

                errors.append(
                    f"Example {index}: "
                    f"missing={missing} does not "
                    f"match actual missing fields="
                    f"{expected_missing}."
                )

            if (
                entities.get("state")
                and entities.get("jc")
            ):

                errors.append(
                    f"Example {index}: "
                    "MISSING_INFORMATION contains "
                    "both state and JC."
                )

    if errors:

        raise ValueError(
            "Required-entity validation failed:\n"
            + "\n".join(
                errors[:30]
            )
        )

    print()
    print(
        "Required entity validation: PASSED"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    random.seed(
        42
    )

    print()
    print(
        "=" * 55
    )
    print(
        "GENERATING DATASET"
    )
    print(
        "=" * 55
    )

    dataset = generate_dataset(
        examples_per_intent=100
    )

    print()
    print(
        "Before duplicate removal:",
        len(dataset)
    )

    dataset = remove_duplicates(
        dataset
    )

    print(
        "After duplicate removal:",
        len(dataset)
    )

    print_intent_summary(
        dataset
    )

    validate_required_entities(
        dataset
    )

    random.shuffle(
        dataset
    )

    output_path = Path(
        "dataset/generated/generated_dataset.json"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            dataset,
            file,
            indent=2,
            ensure_ascii=False
        )

    print()
    print(
        "Dataset generation completed."
    )

    print(
        "Total examples:",
        len(dataset)
    )

    print(
        "Output:",
        output_path
    )


if __name__ == "__main__":
    main()