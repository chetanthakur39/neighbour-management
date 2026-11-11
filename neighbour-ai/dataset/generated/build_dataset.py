import json
import random
from pathlib import Path
from collections import defaultdict, Counter


# ============================================================
# INPUT FILES
# ============================================================

GENERATED_FILE = Path(
    "dataset/generated/generated_dataset.json"
)

SPECIAL_FILE = Path(
    "dataset/generated/special_examples.json"
)

BALANCED_FILE = Path(
    "dataset/generated/balanced_examples.json"
)

SEED_FILE = Path(
    "dataset/raw/seed_dataset.json"
)


# ============================================================
# OUTPUT FILES
# ============================================================

TRAIN_FILE = Path(
    "dataset/train.json"
)

VALIDATION_FILE = Path(
    "dataset/validation.json"
)

TEST_FILE = Path(
    "dataset/test.json"
)


# ============================================================
# STATE / JC VALIDATION MAP
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
# IMPORTANT INTENTS
# ============================================================

REQUIRED_INTENTS = [
    "MISSING_INFORMATION",
    "START_CLEANUP",
    "CREATE_AUTOMATION"
]


# ============================================================
# LOAD JSON
# ============================================================

def load_json(path):

    if not path.exists():

        raise FileNotFoundError(
            f"\nFile not found: {path}\n"
            f"Please create this file before running the builder."
        )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ============================================================
# CREATE UNIQUE KEY
# ============================================================

def create_key(example):

    return (
        example.get(
            "text",
            ""
        ).strip().lower(),

        example.get(
            "intent",
            ""
        ),

        json.dumps(
            example.get(
                "entities",
                {}
            ),
            sort_keys=True
        ),

        json.dumps(
            example.get(
                "missing",
                []
            ),
            sort_keys=True
        )
    )


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicates(dataset):

    unique = {}

    for example in dataset:

        key = create_key(
            example
        )

        if key not in unique:

            unique[key] = example

    return list(
        unique.values()
    )


# ============================================================
# VALIDATE STATE + JC
# ============================================================

def validate_state_jc(
    state,
    jc
):

    # Both missing is allowed for
    # MISSING_INFORMATION examples.

    if state is None or jc is None:

        return True

    if state not in STATE_JC_MAP:

        return False

    return jc in STATE_JC_MAP[state]


# ============================================================
# VALIDATE MISSING INFORMATION
# ============================================================

def validate_missing_information(
    index,
    example,
    errors
):

    entities = example.get(
        "entities",
        {}
    )

    missing = example.get(
        "missing",
        []
    )

    requested_intent = entities.get(
        "requested_intent"
    )

    # --------------------------------------------------------
    # requested_intent required
    # --------------------------------------------------------

    if not requested_intent:

        errors.append(
            f"Example {index}: "
            "MISSING_INFORMATION has no "
            "requested_intent."
        )

        return

    # --------------------------------------------------------
    # Missing fields required
    # --------------------------------------------------------

    if not missing:

        errors.append(
            f"Example {index}: "
            "MISSING_INFORMATION has no "
            "missing fields."
        )

        return

    # --------------------------------------------------------
    # Requested intent validation
    # --------------------------------------------------------

    allowed_requested_intents = [
        "START_CLEANUP",
        "CREATE_AUTOMATION"
    ]

    if requested_intent not in (
        allowed_requested_intents
    ):

        errors.append(
            f"Example {index}: "
            f"unsupported requested_intent "
            f"'{requested_intent}'."
        )

    # --------------------------------------------------------
    # Every missing field must exist
    # in entities and be None
    # --------------------------------------------------------

    for field in missing:

        if field not in entities:

            errors.append(
                f"Example {index}: "
                f"missing field '{field}' "
                "is not present in entities."
            )

            continue

        if entities[field] is not None:

            errors.append(
                f"Example {index}: "
                f"field '{field}' is listed "
                "as missing but has a value."
            )

    # --------------------------------------------------------
    # Cleanup-specific validation
    # --------------------------------------------------------

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
                    f"START_CLEANUP missing "
                    f"entity field '{field}'."
                )

    # --------------------------------------------------------
    # Automation-specific validation
    # --------------------------------------------------------

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
                    f"CREATE_AUTOMATION missing "
                    f"entity field '{field}'."
                )

    # --------------------------------------------------------
    # State + JC combination
    # --------------------------------------------------------

    state = entities.get(
        "state"
    )

    jc = entities.get(
        "jc"
    )

    if not validate_state_jc(
        state,
        jc
    ):

        errors.append(
            f"Example {index}: "
            f"MISSING_INFORMATION contains "
            f"invalid State + JC combination: "
            f"{state} + {jc}"
        )


# ============================================================
# VALIDATE COMPLETE CLEANUP
# ============================================================

def validate_start_cleanup(
    index,
    example,
    errors
):

    entities = example.get(
        "entities",
        {}
    )

    state = entities.get(
        "state"
    )

    jc = entities.get(
        "jc"
    )

    # --------------------------------------------------------
    # State required
    # --------------------------------------------------------

    if state is None:

        errors.append(
            f"Example {index}: "
            "START_CLEANUP missing state."
        )

    # --------------------------------------------------------
    # JC required
    # --------------------------------------------------------

    if jc is None:

        errors.append(
            f"Example {index}: "
            "START_CLEANUP missing jc."
        )

    # --------------------------------------------------------
    # State + JC must be valid
    # --------------------------------------------------------

    if not validate_state_jc(
        state,
        jc
    ):

        errors.append(
            f"Example {index}: "
            "START_CLEANUP has invalid "
            f"State + JC combination: "
            f"{state} + {jc}"
        )

    # --------------------------------------------------------
    # Required cleanup fields
    # --------------------------------------------------------

    if (
        "minimum_neighbours"
        not in entities
    ):

        errors.append(
            f"Example {index}: "
            "START_CLEANUP missing "
            "minimum_neighbours field."
        )


# ============================================================
# VALIDATE COMPLETE AUTOMATION
# ============================================================

def validate_create_automation(
    index,
    example,
    errors
):

    entities = example.get(
        "entities",
        {}
    )

    state = entities.get(
        "state"
    )

    jc = entities.get(
        "jc"
    )

    # --------------------------------------------------------
    # Required fields
    # --------------------------------------------------------

    required_entity_keys = [
        "state",
        "jc",
        "minimum_neighbours",
        "execution_time",
        "frequency",
        "rules",
        "technology_flow"
    ]

    for key in required_entity_keys:

        if key not in entities:

            errors.append(
                f"Example {index}: "
                f"CREATE_AUTOMATION missing "
                f"entity field '{key}'."
            )

    # --------------------------------------------------------
    # State required
    # --------------------------------------------------------

    if state is None:

        errors.append(
            f"Example {index}: "
            "CREATE_AUTOMATION missing state."
        )

    # --------------------------------------------------------
    # JC required
    # --------------------------------------------------------

    if jc is None:

        errors.append(
            f"Example {index}: "
            "CREATE_AUTOMATION missing jc."
        )

    # --------------------------------------------------------
    # State + JC validation
    # --------------------------------------------------------

    if not validate_state_jc(
        state,
        jc
    ):

        errors.append(
            f"Example {index}: "
            "CREATE_AUTOMATION has invalid "
            f"State + JC combination: "
            f"{state} + {jc}"
        )


# ============================================================
# VALIDATE COMPLETE DATASET
# ============================================================

def validate_examples(dataset):

    errors = []

    intent_counts = Counter()

    for index, example in enumerate(
        dataset
    ):

        intent = example.get(
            "intent"
        )

        text = example.get(
            "text",
            ""
        )

        entities = example.get(
            "entities",
            {}
        )

        intent_counts[
            intent
        ] += 1

        # ----------------------------------------------------
        # Basic structure
        # ----------------------------------------------------

        if not text:

            errors.append(
                f"Example {index}: "
                "empty text."
            )

        if not intent:

            errors.append(
                f"Example {index}: "
                "missing intent."
            )

            continue

        if not isinstance(
            entities,
            dict
        ):

            errors.append(
                f"Example {index}: "
                "entities must be an object."
            )

            continue

        # ----------------------------------------------------
        # State / JC validation
        # ----------------------------------------------------

        state = entities.get(
            "state"
        )

        jc = entities.get(
            "jc"
        )

        if not validate_state_jc(
            state,
            jc
        ):

            errors.append(
                f"Example {index}: "
                f"invalid State + JC combination: "
                f"{state} + {jc}"
            )

        # ----------------------------------------------------
        # MISSING_INFORMATION
        # ----------------------------------------------------

        if intent == "MISSING_INFORMATION":

            validate_missing_information(
                index,
                example,
                errors
            )

        # ----------------------------------------------------
        # START_CLEANUP
        # ----------------------------------------------------

        elif intent == "START_CLEANUP":

            validate_start_cleanup(
                index,
                example,
                errors
            )

        # ----------------------------------------------------
        # CREATE_AUTOMATION
        # ----------------------------------------------------

        elif intent == "CREATE_AUTOMATION":

            validate_create_automation(
                index,
                example,
                errors
            )

    # --------------------------------------------------------
    # Required intents
    # --------------------------------------------------------

    for intent in REQUIRED_INTENTS:

        if intent_counts[
            intent
        ] == 0:

            errors.append(
                f"{intent} does not exist "
                "in the combined dataset."
            )

    return (
        errors,
        intent_counts
    )


# ============================================================
# CALCULATE SPLIT COUNTS
# ============================================================

def calculate_split_counts(
    total
):

    if total < 3:

        return (
            total,
            0,
            0
        )

    # --------------------------------------------------------
    # Base 80 / 10 / 10
    # --------------------------------------------------------

    train_count = int(
        total * 0.80
    )

    validation_count = int(
        total * 0.10
    )

    test_count = (
        total
        - train_count
        - validation_count
    )

    # --------------------------------------------------------
    # Guarantee minimum 1 in each
    # --------------------------------------------------------

    train_count = max(
        train_count,
        1
    )

    validation_count = max(
        validation_count,
        1
    )

    test_count = max(
        test_count,
        1
    )

    # --------------------------------------------------------
    # Fix overflow
    # --------------------------------------------------------

    while (
        train_count
        + validation_count
        + test_count
        > total
    ):

        if train_count > 1:

            train_count -= 1

        elif validation_count > 1:

            validation_count -= 1

        elif test_count > 1:

            test_count -= 1

        else:

            break

    # --------------------------------------------------------
    # Fix underflow
    # --------------------------------------------------------

    while (
        train_count
        + validation_count
        + test_count
        < total
    ):

        train_count += 1

    return (
        train_count,
        validation_count,
        test_count
    )


# ============================================================
# STRATIFIED SPLIT
# ============================================================

def stratified_split(
    dataset
):

    """
    Split every intent independently.

    Target:
        ~80% TRAIN
        ~10% VALIDATION
        ~10% TEST

    Every intent with >= 3 examples is guaranteed
    to appear in all three splits.
    """

    grouped = defaultdict(
        list
    )

    for example in dataset:

        grouped[
            example["intent"]
        ].append(
            example
        )

    train = []
    validation = []
    test = []

    # --------------------------------------------------------
    # Process each intent
    # --------------------------------------------------------

    for intent, examples in (
        grouped.items()
    ):

        examples = list(
            examples
        )

        random.shuffle(
            examples
        )

        total = len(
            examples
        )

        # ----------------------------------------------------
        # Very small intent
        # ----------------------------------------------------

        if total < 3:

            train.extend(
                examples
            )

            continue

        (
            train_count,
            validation_count,
            test_count
        ) = calculate_split_counts(
            total
        )

        # ----------------------------------------------------
        # Slice
        # ----------------------------------------------------

        start = 0

        train.extend(
            examples[
                start:
                start + train_count
            ]
        )

        start += train_count

        validation.extend(
            examples[
                start:
                start + validation_count
            ]
        )

        start += validation_count

        test.extend(
            examples[
                start:
                start + test_count
            ]
        )

    # --------------------------------------------------------
    # Shuffle final datasets
    # --------------------------------------------------------

    random.shuffle(
        train
    )

    random.shuffle(
        validation
    )

    random.shuffle(
        test
    )

    return (
        train,
        validation,
        test
    )


# ============================================================
# VERIFY REQUIRED INTENTS IN SPLITS
# ============================================================

def verify_required_intents(
    train,
    validation,
    test
):

    train_counts = Counter(
        x["intent"]
        for x in train
    )

    validation_counts = Counter(
        x["intent"]
        for x in validation
    )

    test_counts = Counter(
        x["intent"]
        for x in test
    )

    errors = []

    # --------------------------------------------------------
    # Important intents
    # --------------------------------------------------------

    for intent in REQUIRED_INTENTS:

        if train_counts[
            intent
        ] == 0:

            errors.append(
                f"{intent} missing from TRAIN."
            )

        if validation_counts[
            intent
        ] == 0:

            errors.append(
                f"{intent} missing from VALIDATION."
            )

        if test_counts[
            intent
        ] == 0:

            errors.append(
                f"{intent} missing from TEST."
            )

    if errors:

        raise RuntimeError(
            "\n".join(errors)
        )


# ============================================================
# VERIFY MISSING INFORMATION BALANCE
# ============================================================

def verify_missing_information(
    train,
    validation,
    test
):

    train_count = sum(
        1
        for x in train
        if x["intent"]
        == "MISSING_INFORMATION"
    )

    validation_count = sum(
        1
        for x in validation
        if x["intent"]
        == "MISSING_INFORMATION"
    )

    test_count = sum(
        1
        for x in test
        if x["intent"]
        == "MISSING_INFORMATION"
    )

    print()
    print(
        "MISSING_INFORMATION SPLIT CHECK"
    )

    print(
        "-" * 55
    )

    print(
        "Train:",
        train_count
    )

    print(
        "Validation:",
        validation_count
    )

    print(
        "Test:",
        test_count
    )

    if (
        train_count == 0
        or validation_count == 0
        or test_count == 0
    ):

        raise RuntimeError(
            "MISSING_INFORMATION must appear "
            "in TRAIN, VALIDATION and TEST."
        )


# ============================================================
# SAVE JSON
# ============================================================

def save_json(
    path,
    data
):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


# ============================================================
# PRINT DISTRIBUTION
# ============================================================

def print_distribution(
    name,
    dataset
):

    counts = Counter(
        example["intent"]
        for example in dataset
    )

    print()
    print(
        "=" * 55
    )

    print(
        name
    )

    print(
        "=" * 55
    )

    print(
        "Total:",
        len(dataset)
    )

    for intent, count in sorted(
        counts.items()
    ):

        print(
            f"{intent}: {count}"
        )


# ============================================================
# VERIFY FINAL SPLITS
# ============================================================

def verify_final_splits(
    combined,
    train,
    validation,
    test
):

    # --------------------------------------------------------
    # Required intents
    # --------------------------------------------------------

    verify_required_intents(
        train,
        validation,
        test
    )

    # --------------------------------------------------------
    # Missing information
    # --------------------------------------------------------

    verify_missing_information(
        train,
        validation,
        test
    )

    # --------------------------------------------------------
    # Total
    # --------------------------------------------------------

    final_total = (
        len(train)
        + len(validation)
        + len(test)
    )

    if final_total != len(
        combined
    ):

        raise RuntimeError(
            "Final split total does not match "
            "combined dataset."
        )

    # --------------------------------------------------------
    # Duplicate check across splits
    # --------------------------------------------------------

    all_split_examples = (
        train
        + validation
        + test
    )

    keys = [
        create_key(
            example
        )
        for example in all_split_examples
    ]

    if len(keys) != len(
        set(keys)
    ):

        raise RuntimeError(
            "Duplicate examples found "
            "across final splits."
        )


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # Reproducibility
    # --------------------------------------------------------

    random.seed(
        42
    )

    print()
    print(
        "=" * 55
    )

    print(
        "BUILDING FINAL DATASET"
    )

    print(
        "=" * 55
    )

    # --------------------------------------------------------
    # Load sources
    # --------------------------------------------------------

    generated = load_json(
        GENERATED_FILE
    )

    special = load_json(
        SPECIAL_FILE
    )

    balanced = load_json(
        BALANCED_FILE
    )

    seed = load_json(
        SEED_FILE
    )

    # --------------------------------------------------------
    # Source information
    # --------------------------------------------------------

    print()
    print(
        "SOURCE DATASETS"
    )

    print(
        "-" * 55
    )

    print(
        "Generated examples:",
        len(generated)
    )

    print(
        "Special examples:",
        len(special)
    )

    print(
        "Balanced examples:",
        len(balanced)
    )

    print(
        "Seed examples:",
        len(seed)
    )

    # --------------------------------------------------------
    # Source intent distributions
    # --------------------------------------------------------

    print()
    print(
        "SOURCE INTENT COUNTS"
    )

    print(
        "-" * 55
    )

    for name, source in [
        ("Generated", generated),
        ("Special", special),
        ("Balanced", balanced),
        ("Seed", seed)
    ]:

        counts = Counter(
            x.get("intent")
            for x in source
        )

        print(
            f"\n{name}:"
        )

        for intent, count in sorted(
            counts.items()
        ):

            print(
                f"  {intent}: {count}"
            )

    # --------------------------------------------------------
    # Safety checks
    # --------------------------------------------------------

    if len(balanced) == 0:

        raise RuntimeError(
            "balanced_examples.json contains 0 examples."
        )

    if len(special) == 0:

        raise RuntimeError(
            "special_examples.json contains 0 examples."
        )

    if len(seed) == 0:

        raise RuntimeError(
            "seed_dataset.json contains 0 examples."
        )

    # --------------------------------------------------------
    # Combine
    # --------------------------------------------------------

    combined = (
        generated
        + special
        + balanced
        + seed
    )

    print()
    print(
        "Before duplicate removal:",
        len(combined)
    )

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    combined = remove_duplicates(
        combined
    )

    print(
        "After duplicate removal:",
        len(combined)
    )

    # --------------------------------------------------------
    # Validate combined
    # --------------------------------------------------------

    print()
    print(
        "VALIDATING COMBINED DATASET"
    )

    errors, intent_counts = (
        validate_examples(
            combined
        )
    )

    if errors:

        print()
        print(
            "DATASET VALIDATION FAILED"
        )

        print(
            "-" * 55
        )

        for error in errors:

            print(
                "ERROR:",
                error
            )

        raise RuntimeError(
            "Dataset validation failed "
            f"with {len(errors)} error(s)."
        )

    print(
        "Dataset validation PASSED."
    )

    print()
    print(
        "FINAL COMBINED INTENT COUNTS"
    )

    print(
        "-" * 55
    )

    for intent, count in sorted(
        intent_counts.items()
    ):

        print(
            f"{intent}: {count}"
        )

    # --------------------------------------------------------
    # Explicit important-intent counts
    # --------------------------------------------------------

    print()
    print(
        "IMPORTANT INTENTS"
    )

    print(
        "-" * 55
    )

    for intent in REQUIRED_INTENTS:

        print(
            f"{intent}: "
            f"{intent_counts[intent]}"
        )

    # --------------------------------------------------------
    # Stratified split
    # --------------------------------------------------------

    (
        train,
        validation,
        test
    ) = stratified_split(
        combined
    )

    # --------------------------------------------------------
    # Verify
    # --------------------------------------------------------

    verify_final_splits(
        combined,
        train,
        validation,
        test
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    save_json(
        TRAIN_FILE,
        train
    )

    save_json(
        VALIDATION_FILE,
        validation
    )

    save_json(
        TEST_FILE,
        test
    )

    # --------------------------------------------------------
    # Print distributions
    # --------------------------------------------------------

    print_distribution(
        "TRAIN DATASET",
        train
    )

    print_distribution(
        "VALIDATION DATASET",
        validation
    )

    print_distribution(
        "TEST DATASET",
        test
    )

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    final_total = (
        len(train)
        + len(validation)
        + len(test)
    )

    print()
    print(
        "=" * 55
    )

    print(
        "FINAL DATASET SUMMARY"
    )

    print(
        "=" * 55
    )

    print(
        "Combined dataset:",
        len(combined)
    )

    print(
        "Train:",
        len(train)
    )

    print(
        "Validation:",
        len(validation)
    )

    print(
        "Test:",
        len(test)
    )

    print(
        "Train + Validation + Test:",
        final_total
    )

    print()

    print(
        "MISSING_INFORMATION:"
    )

    print(
        "  Train:",
        sum(
            1
            for x in train
            if x["intent"]
            == "MISSING_INFORMATION"
        )
    )

    print(
        "  Validation:",
        sum(
            1
            for x in validation
            if x["intent"]
            == "MISSING_INFORMATION"
        )
    )

    print(
        "  Test:",
        sum(
            1
            for x in test
            if x["intent"]
            == "MISSING_INFORMATION"
        )
    )

    print()

    print(
        "Files created:"
    )

    print(
        " -",
        TRAIN_FILE
    )

    print(
        " -",
        VALIDATION_FILE
    )

    print(
        " -",
        TEST_FILE
    )

    print()
    print(
        "DATASET BUILD COMPLETED SUCCESSFULLY."
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()