"""
Central intent definitions for the Neighbour Management AI.

IMPORTANT
---------
This file is the single source of truth for intent names and
numeric labels.

The order of INTENTS MUST NOT be changed after a model has been
trained, because the neural network output index depends on it.

Current model:
    18 intent classes
    labels: 0 - 17
"""

from typing import Dict, List


# ============================================================
# INTENTS
# ============================================================

INTENTS: List[str] = [
    "AMBIGUOUS_REQUEST",
    "CREATE_AUTOMATION",
    "GET_AUTOMATIONS",
    "GET_CLEANUP_PROGRESS",
    "GET_CLEANUP_RESULT",
    "GET_COUNTS",
    "GET_INVALID_NEIGHBOURS",
    "GET_INVALID_PERCENTAGE",
    "GET_JCS",
    "GET_NEIGHBOURS",
    "GET_PCI_INVALID",
    "GET_STATES",
    "GET_TAC_INVALID",
    "MISSING_INFORMATION",
    "OUT_OF_SCOPE",
    "PREVIEW_CLEANUP",
    "START_CLEANUP",
    "VALIDATE_NEIGHBOURS",
]


# ============================================================
# PRIMARY LABEL MAPPING
# ============================================================

# Intent -> numeric label

INTENT_TO_LABEL: Dict[str, int] = {
    intent: index
    for index, intent in enumerate(INTENTS)
}


# Numeric label -> intent

LABEL_TO_INTENT: Dict[int, str] = {
    index: intent
    for index, intent in enumerate(INTENTS)
}


# ============================================================
# STANDARD PROJECT ALIASES
# ============================================================

# New preferred naming.
#
# Use these names in new code.

INTENT_TO_ID: Dict[str, int] = dict(
    INTENT_TO_LABEL
)

ID_TO_INTENT: Dict[int, str] = dict(
    LABEL_TO_INTENT
)


# Backward-compatible aliases.

INTENT_TO_INDEX: Dict[str, int] = dict(
    INTENT_TO_LABEL
)

INDEX_TO_INTENT: Dict[int, str] = dict(
    LABEL_TO_INTENT
)


# ============================================================
# HELPERS
# ============================================================

def get_num_intents() -> int:
    """Return the number of supported intents."""

    return len(INTENTS)


def get_intent_label(intent: str) -> int:
    """
    Return the numeric label for an intent.

    Raises:
        ValueError: if the intent is unknown.
    """

    if not isinstance(intent, str):

        raise ValueError(
            "Intent must be a string."
        )

    normalized = intent.strip()

    if normalized not in INTENT_TO_LABEL:

        raise ValueError(
            f"Unknown intent: {intent}"
        )

    return INTENT_TO_LABEL[normalized]


def get_intent_id(intent: str) -> int:
    """
    Preferred alias for get_intent_label().
    """

    return get_intent_label(intent)


def get_intent_name(label: int) -> str:
    """
    Return the intent name for a numeric label.

    Raises:
        ValueError: if the label is invalid.
    """

    if not isinstance(label, int):

        raise ValueError(
            "Intent label must be an integer."
        )

    if label not in LABEL_TO_INTENT:

        raise ValueError(
            f"Invalid intent label: {label}"
        )

    return LABEL_TO_INTENT[label]


def get_intent_from_id(intent_id: int) -> str:
    """
    Preferred alias for get_intent_name().
    """

    return get_intent_name(intent_id)


def is_valid_intent(intent: str) -> bool:
    """Return True when the intent is supported."""

    if not isinstance(intent, str):

        return False

    return intent.strip() in INTENT_TO_LABEL


def is_valid_intent_id(intent_id: int) -> bool:
    """Return True when the numeric intent ID is supported."""

    return (
        isinstance(intent_id, int)
        and intent_id in ID_TO_INTENT
    )


def get_all_intents() -> List[str]:
    """Return a copy of the complete intent list."""

    return list(INTENTS)


def get_all_intent_ids() -> List[int]:
    """Return all valid intent IDs."""

    return list(range(len(INTENTS)))


# ============================================================
# SPECIAL INTENT HELPERS
# ============================================================

def is_operational_intent(intent: str) -> bool:
    """
    Return True for intents that can cause or request
    operational neighbour-management actions.
    """

    operational_intents = {
        "START_CLEANUP",
        "CREATE_AUTOMATION",
        "PREVIEW_CLEANUP",
        "VALIDATE_NEIGHBOURS",
    }

    return intent in operational_intents


def is_information_intent(intent: str) -> bool:
    """
    Return True for read-only information intents.
    """

    information_intents = {
        "GET_AUTOMATIONS",
        "GET_CLEANUP_PROGRESS",
        "GET_CLEANUP_RESULT",
        "GET_COUNTS",
        "GET_INVALID_NEIGHBOURS",
        "GET_INVALID_PERCENTAGE",
        "GET_JCS",
        "GET_NEIGHBOURS",
        "GET_PCI_INVALID",
        "GET_STATES",
        "GET_TAC_INVALID",
    }

    return intent in information_intents


def requires_missing_information_check(intent: str) -> bool:
    """
    Return True when the command may require entity
    completeness validation before execution.
    """

    return intent in {
        "START_CLEANUP",
        "CREATE_AUTOMATION",
        "PREVIEW_CLEANUP",
        "VALIDATE_NEIGHBOURS",
    }


# ============================================================
# VALIDATION
# ============================================================

def validate_intents() -> bool:
    """
    Validate the complete intent mapping.

    This function protects against:
        - duplicate intent names
        - missing mappings
        - non-continuous labels
        - inconsistent reverse mappings
        - invalid aliases
    """

    # --------------------------------------------------------
    # Basic checks
    # --------------------------------------------------------

    if not INTENTS:

        raise ValueError(
            "INTENTS cannot be empty."
        )

    # --------------------------------------------------------
    # Duplicate check
    # --------------------------------------------------------

    if len(INTENTS) != len(set(INTENTS)):

        duplicates = [
            intent
            for intent in INTENTS
            if INTENTS.count(intent) > 1
        ]

        duplicates = sorted(set(duplicates))

        raise ValueError(
            "Duplicate intents found: "
            f"{duplicates}"
        )

    # --------------------------------------------------------
    # Mapping sizes
    # --------------------------------------------------------

    if len(INTENT_TO_LABEL) != len(INTENTS):

        raise ValueError(
            "INTENT_TO_LABEL mapping is inconsistent."
        )

    if len(LABEL_TO_INTENT) != len(INTENTS):

        raise ValueError(
            "LABEL_TO_INTENT mapping is inconsistent."
        )

    if len(INTENT_TO_ID) != len(INTENTS):

        raise ValueError(
            "INTENT_TO_ID mapping is inconsistent."
        )

    if len(ID_TO_INTENT) != len(INTENTS):

        raise ValueError(
            "ID_TO_INTENT mapping is inconsistent."
        )

    # --------------------------------------------------------
    # Label continuity
    # --------------------------------------------------------

    labels = sorted(
        INTENT_TO_LABEL.values()
    )

    expected_labels = list(
        range(len(INTENTS))
    )

    if labels != expected_labels:

        raise ValueError(
            "Intent labels must be continuous "
            "starting from 0."
        )

    # --------------------------------------------------------
    # Forward/reverse mapping check
    # --------------------------------------------------------

    for intent in INTENTS:

        label = INTENT_TO_LABEL[intent]

        if LABEL_TO_INTENT.get(label) != intent:

            raise ValueError(
                "Intent mapping is inconsistent for: "
                f"{intent}"
            )

    # --------------------------------------------------------
    # Alias consistency
    # --------------------------------------------------------

    if INTENT_TO_ID != INTENT_TO_LABEL:

        raise ValueError(
            "INTENT_TO_ID must match "
            "INTENT_TO_LABEL."
        )

    if ID_TO_INTENT != LABEL_TO_INTENT:

        raise ValueError(
            "ID_TO_INTENT must match "
            "LABEL_TO_INTENT."
        )

    if INTENT_TO_INDEX != INTENT_TO_LABEL:

        raise ValueError(
            "INTENT_TO_INDEX must match "
            "INTENT_TO_LABEL."
        )

    if INDEX_TO_INTENT != LABEL_TO_INTENT:

        raise ValueError(
            "INDEX_TO_INTENT must match "
            "LABEL_TO_INTENT."
        )

    # --------------------------------------------------------
    # Special intent existence
    # --------------------------------------------------------

    required_intents = {
        "AMBIGUOUS_REQUEST",
        "CREATE_AUTOMATION",
        "GET_AUTOMATIONS",
        "GET_CLEANUP_PROGRESS",
        "GET_CLEANUP_RESULT",
        "GET_COUNTS",
        "GET_INVALID_NEIGHBOURS",
        "GET_INVALID_PERCENTAGE",
        "GET_JCS",
        "GET_NEIGHBOURS",
        "GET_PCI_INVALID",
        "GET_STATES",
        "GET_TAC_INVALID",
        "MISSING_INFORMATION",
        "OUT_OF_SCOPE",
        "PREVIEW_CLEANUP",
        "START_CLEANUP",
        "VALIDATE_NEIGHBOURS",
    }

    missing_required = (
        required_intents - set(INTENTS)
    )

    if missing_required:

        raise ValueError(
            "Required intents are missing: "
            f"{sorted(missing_required)}"
        )

    return True


# ============================================================
# VALIDATE ON IMPORT
# ============================================================

validate_intents()