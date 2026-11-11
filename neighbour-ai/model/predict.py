import re
import difflib
import torch

from tokenizer.tokenizer import SimpleTokenizer
from model.intent_model import IntentClassifier
from model.intent_mapping import ID_TO_INTENT
from model.api_client import NeighbourManagementAPI

import model.config as config


# ============================================================
# MODEL / TOKENIZER
# ============================================================

def load_tokenizer():

    return SimpleTokenizer.load(
        config.TOKENIZER_FILE
    )


def load_model(
    device
):

    checkpoint = torch.load(
        config.MODEL_FILE,
        map_location=device
    )

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
            config.NUM_INTENTS
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

    model.to(
        device
    )

    model.eval()

    return model


# ============================================================
# INPUT PREPARATION
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

    input_ids = input_ids.to(
        device
    )

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

    if intent_id not in ID_TO_INTENT:

        raise ValueError(
            f"Model predicted invalid "
            f"intent ID: {intent_id}"
        )

    intent = ID_TO_INTENT[
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

def normalize_text(
    text
):

    if text is None:

        return ""

    text = str(
        text
    ).strip()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


# ============================================================
# EXTRACT NUMBER
# ============================================================

def extract_number(
    text
):

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
# EXTRACT MINIMUM NEIGHBOURS
# ============================================================
#
# IMPORTANT:
#
# We must NOT simply take the first number.
#
# Example:
#
# Create automation for Maharashtra JC_Mumbai
# at 12:35 with minimum retention of 2 neighbours
#
# Correct:
#
# execution_time = 12:35
# minimum_neighbours = 2
#
# Wrong:
#
# minimum_neighbours = 12
#
# ============================================================

def extract_minimum_neighbours(
    text
):

    patterns = [

        # minimum retention of 2
        r"\bminimum\s+retention\s+of\s+(\d+)\b",

        # minimum retention 2
        r"\bminimum\s+retention\s+(\d+)\b",

        # minimum neighbours of 2
        r"\bminimum\s+neighbours?\s+(?:of\s+)?(\d+)\b",

        # minimum neighbors of 2
        r"\bminimum\s+neighbors?\s+(?:of\s+)?(\d+)\b",

        # minimum 2 neighbours
        r"\bminimum\s+(\d+)\s+neighbours?\b",

        # minimum 2 neighbors
        r"\bminimum\s+(\d+)\s+neighbors?\b",

        # retain 2 neighbours
        r"\bretain\s+(\d+)\s+neighbours?\b",

        # retain 2 neighbors
        r"\bretain\s+(\d+)\s+neighbors?\b",

        # retain at least 2 neighbours
        r"\bretain\s+at\s+least\s+(\d+)\s+neighbours?\b",

        # retain at least 2 neighbors
        r"\bretain\s+at\s+least\s+(\d+)\s+neighbors?\b",

        # retention of 2 neighbours
        r"\bretention\s+of\s+(\d+)\s+neighbours?\b",

        # retention of 2 neighbors
        r"\bretention\s+of\s+(\d+)\s+neighbors?\b",

        # keep 2 neighbours
        r"\bkeep\s+(\d+)\s+neighbours?\b",

        # keep 2 neighbors
        r"\bkeep\s+(\d+)\s+neighbors?\b"
    ]


    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:

            return int(
                match.group(1)
            )


    return None


# ============================================================
# NORMALIZE FOR ENTITY MATCHING
# ============================================================

def normalize_entity_text(
    value
):

    if value is None:

        return ""

    value = str(value).lower()
    value = value.replace("_", " ")
    value = value.replace("-", " ")
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()

    return value


# ============================================================
# FIND BEST FUZZY MATCH
# ============================================================

def find_best_fuzzy_match(
    value,
    candidates,
    threshold
):

    if not value or not isinstance(candidates, list):
        return None

    normalized_value = normalize_entity_text(value)

    if not normalized_value:
        return None

    best_match = None
    best_score = 0.0

    for candidate in candidates:
        if candidate is None:
            continue

        candidate_text = str(candidate).strip()
        if not candidate_text:
            continue

        normalized_candidate = normalize_entity_text(candidate_text)

        if normalized_value == normalized_candidate:
            return candidate_text

        score = difflib.SequenceMatcher(
            None,
            normalized_value,
            normalized_candidate
        ).ratio()

        if score > best_score:
            best_score = score
            best_match = candidate_text

    if best_match is not None and best_score >= threshold:
        return best_match

    return None


# ============================================================
# ENTITY MATCH CONFIDENCE
# ============================================================

def calculate_entity_match_confidence(
    text,
    matched_entity
):

    if not text or not matched_entity:

        return None


    normalized_text = normalize_entity_text(
        text
    )


    normalized_entity = normalize_entity_text(
        matched_entity
    )


    if (
        not normalized_text
        or
        not normalized_entity
    ):

        return None


    pattern = (

        r"(?<![a-z0-9])"

        + re.escape(
            normalized_entity
        )

        + r"(?![a-z0-9])"
    )


    if re.search(

        pattern,

        normalized_text
    ):

        return 1.0


    words = normalized_text.split()


    entity_words = (
        normalized_entity.split()
    )


    if (

        not words

        or

        not entity_words
    ):

        return None


    max_window = min(

        len(words),

        len(entity_words) + 1
    )


    best_score = 0.0


    for size in range(

        1,

        max_window + 1
    ):

        for start in range(

            len(words) - size + 1
        ):

            phrase = " ".join(

                words[
                    start:
                    start + size
                ]
            )


            score = (

                difflib.SequenceMatcher(

                    None,

                    phrase,

                    normalized_entity

                ).ratio()
            )


            if score > best_score:

                best_score = score


    return best_score


# ============================================================
# EXTRACT ENTITY CONFIDENCE
# ============================================================

def extract_entity_confidence(
    text,
    entities
):

    return {

        "state":

            calculate_entity_match_confidence(

                text,

                entities.get(
                    "state"
                )
            ),


        "jc":

            calculate_entity_match_confidence(

                text,

                entities.get(
                    "jc"
                )
            )
    }


# ============================================================
# EXTRACT STATE
# ============================================================

def extract_state(
    text,
    api
):

    if not text:
        return None

    try:
        states = api.get_states()
    except Exception:
        return None

    if not isinstance(states, list):
        return None

    states = [
        str(state).strip()
        for state in states
        if state is not None and str(state).strip()
    ]

    if not states:
        return None

    normalized_text = normalize_entity_text(text)

    sorted_states = sorted(
        states,
        key=lambda value: len(normalize_entity_text(value)),
        reverse=True
    )

    for state in sorted_states:
        normalized_state = normalize_entity_text(state)

        if not normalized_state:
            continue

        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(normalized_state)
            + r"(?![a-z0-9])"
        )

        if re.search(pattern, normalized_text):
            return state

    words = normalized_text.split()

    if not words:
        return None

    max_state_words = max(
        len(normalize_entity_text(state).split())
        for state in states
    )

    best_match = None
    best_score = 0.0
    max_window = min(len(words), max_state_words + 1)

    for size in range(1, max_window + 1):
        for start in range(len(words) - size + 1):
            phrase = " ".join(words[start:start + size])

            for state in states:
                score = difflib.SequenceMatcher(
                    None,
                    phrase,
                    normalize_entity_text(state)
                ).ratio()

                if score > best_score:
                    best_score = score
                    best_match = state

    if best_match is not None and best_score >= 0.82:
        return best_match

    return None


# ============================================================
# EXTRACT JC
# ============================================================

def extract_jc(
    text,
    state,
    api
):

    if not text:
        return None

    try:
        if state:
            jcs = api.get_jcs_by_state(state)
        else:
            jcs = api.get_all_jcs()
    except Exception:
        return None

    if not isinstance(jcs, list):
        return None

    jcs = [
        str(jc).strip()
        for jc in jcs
        if jc is not None and str(jc).strip()
    ]

    if not jcs:
        return None

    match = re.search(
        r"\bJC_[A-Za-z0-9_-]+\b",
        text,
        re.IGNORECASE
    )

    if match:
        extracted = match.group(0)

        for jc in jcs:
            if jc.lower() == extracted.lower():
                return jc

        fuzzy_match = find_best_fuzzy_match(
            extracted,
            jcs,
            threshold=0.78
        )

        if fuzzy_match:
            return fuzzy_match

    normalized_text = normalize_entity_text(text)
    words = normalized_text.split()

    if not words:
        return None

    max_jc_words = max(
        len(normalize_entity_text(jc).split())
        for jc in jcs
    )

    max_window = min(len(words), max_jc_words + 1)
    best_match = None
    best_score = 0.0

    for size in range(1, max_window + 1):
        for start in range(len(words) - size + 1):
            phrase = " ".join(words[start:start + size])

            for jc in jcs:
                score = difflib.SequenceMatcher(
                    None,
                    phrase,
                    normalize_entity_text(jc)
                ).ratio()

                if score > best_score:
                    best_score = score
                    best_match = jc

    if best_match is not None and best_score >= 0.78:
        return best_match

    return None


# ============================================================
# EXTRACT FREQUENCY
# ============================================================

def extract_frequency(
    text
):

    lower = text.lower()


    if "daily" in lower:

        return "DAILY"


    if "weekly" in lower:

        return "WEEKLY"


    if "monthly" in lower:

        return "MONTHLY"


    return None


# ============================================================
# EXTRACT EXECUTION TIME
# ============================================================

def extract_execution_time(
    text
):

    # --------------------------------------------------------
    # 24-hour format
    # --------------------------------------------------------

    match = re.search(
        r"\b([01]?\d|2[0-3]):([0-5]\d)\b",
        text
    )


    if match:

        return (

            f"{int(match.group(1)):02d}:"
            f"{match.group(2)}"
        )


    # --------------------------------------------------------
    # 12-hour format
    # --------------------------------------------------------

    match = re.search(

        r"\b"
        r"(1[0-2]|0?[1-9])"
        r"(?:[:.]([0-5]\d))?"
        r"\s*"
        r"(AM|PM)"
        r"\b",

        text,

        re.IGNORECASE
    )


    if match:

        hour = int(
            match.group(1)
        )

        minute = (
            match.group(2)
            or
            "00"
        )

        period = (
            match.group(3)
            .upper()
        )


        if period == "AM":

            if hour == 12:

                hour = 0

        else:

            if hour != 12:

                hour += 12


        return (

            f"{hour:02d}:"
            f"{minute}"
        )


    # --------------------------------------------------------
    # Natural language times
    # --------------------------------------------------------

    natural_times = {

        "8 am": "08:00",
        "9 am": "09:00",
        "10 am": "10:00",
        "11 am": "11:00",

        "8 pm": "20:00",
        "9 pm": "21:00",
        "10 pm": "22:00",
        "11 pm": "23:00"
    }


    lower = text.lower()


    for phrase, value in (
        natural_times.items()
    ):

        if phrase in lower:

            return value


    return None


# ============================================================
# EXTRACT RULES
# ============================================================

def extract_rules(
    text
):

    lower = text.lower()


    has_pci = (
        "pci" in lower
    )

    has_tac = (
        "tac" in lower
    )


    if has_pci and has_tac:

        return [
            "PCI",
            "TAC"
        ]


    if has_pci:

        return [
            "PCI"
        ]


    if has_tac:

        return [
            "TAC"
        ]


    return None


# ============================================================
# EXTRACT TECHNOLOGY FLOW
# ============================================================

def extract_technology_flow(
    text
):

    lower = (
        text
        .lower()
        .replace(
            "-",
            "_"
        )
    )


    # --------------------------------------------------------
    # Explicit enum
    # --------------------------------------------------------

    if (
        "four_g_to_five_g"
        in lower
    ):

        return (
            "FOUR_G_TO_FIVE_G"
        )


    if (
        "five_g_to_four_g"
        in lower
    ):

        return (
            "FIVE_G_TO_FOUR_G"
        )


    # --------------------------------------------------------
    # 4G / 5G natural language
    # --------------------------------------------------------

    if (
        "4g to 5g"
        in lower
        or
        "4g to five g"
        in lower
        or
        "four g to 5g"
        in lower
        or
        "four g to five g"
        in lower
    ):

        return (
            "FOUR_G_TO_FIVE_G"
        )


    if (
        "5g to 4g"
        in lower
        or
        "5g to four g"
        in lower
        or
        "five g to 4g"
        in lower
        or
        "five g to four g"
        in lower
    ):

        return (
            "FIVE_G_TO_FOUR_G"
        )


    return None


# ============================================================
# FALLBACK LOW-CONFIDENCE ENTITY CANDIDATES
# ============================================================

def find_best_entity_candidate(value, candidates):
    if not value or not isinstance(candidates, list):
        return (None, None)
    normalized_value = normalize_entity_text(value)
    if not normalized_value:
        return (None, None)
    best_match = None
    best_score = 0.0
    for candidate in candidates:
        if candidate is None:
            continue
        candidate_text = str(candidate).strip()
        if not candidate_text:
            continue
        score = difflib.SequenceMatcher(None, normalized_value, normalize_entity_text(candidate_text)).ratio()
        if score > best_score:
            best_score = score
            best_match = candidate_text
    return (best_match, best_score)

def extract_state_fallback_candidate(text, api):
    if not text:
        return (None, None)

    try:
        states = api.get_states()
    except Exception:
        return (None, None)

    if not isinstance(states, list):
        return (None, None)

    # Locate the JC first. The State is normally the text immediately
    # before it, whether or not the user wrote the word "in".
    jc_match = re.search(
        r"\bJC_[A-Za-z0-9_-]+\b",
        text,
        re.IGNORECASE
    )

    if not jc_match:
        return (None, None)

    prefix = text[:jc_match.start()].strip()

    # Remove command words without changing the normal fuzzy matcher.
    prefix = re.sub(
        r"^(?:show|get|list|validate|validation|check|preview|start|create)\b",
        "",
        prefix,
        flags=re.IGNORECASE
    ).strip()

    prefix = re.sub(
        r"^(?:(?:invalid|valid|pci|tac|neighbours?|neighbors?)\s+)+",
        "",
        prefix,
        flags=re.IGNORECASE
    ).strip()

    prefix = re.sub(
        r"^(?:in\s+)?",
        "",
        prefix,
        flags=re.IGNORECASE
    ).strip()

    prefix = re.sub(
        r"\s+and\s*$",
        "",
        prefix,
        flags=re.IGNORECASE
    ).strip()

    if not prefix:
        return (None, None)

    # Try suffix windows so commands such as:
    # "Validate neighbours in raji JC_jai"
    # and
    # "Validate neighbours raji JC_jai"
    # can both produce a low-confidence State candidate.
    words = normalize_entity_text(prefix).split()

    best_candidate = None
    best_score = 0.0

    max_window = min(len(words), 4)

    for size in range(1, max_window + 1):
        value = " ".join(words[-size:])

        candidate, score = find_best_entity_candidate(
            value,
            states
        )

        if score is not None and score > best_score:
            best_candidate = candidate
            best_score = score

    if best_candidate is not None and best_score >= 0.55:
        return (
            best_candidate,
            min(best_score, 0.74)
        )

    return (None, None)

def extract_jc_fallback_candidate(text, state, api):
    if not text:
        return (None, None)
    try:
        jcs = api.get_jcs_by_state(state) if state else api.get_all_jcs()
    except Exception:
        return (None, None)
    if not isinstance(jcs, list):
        return (None, None)
    match = re.search(r"\b(JC_[A-Za-z0-9_-]+)\b", text, re.IGNORECASE)
    if not match:
        return (None, None)
    candidate, score = find_best_entity_candidate(match.group(1), jcs)
    if candidate is not None and score >= 0.55:
        return (candidate, min(score, 0.74))
    return (None, None)


# ============================================================
# EXTRACT ENTITIES
# ============================================================

def extract_entities(
    text,
    intent,
    api
):

    state = extract_state(
        text,
        api
    )


    state_confidence_override = None


    if state is None:

        (
            fallback_state,
            fallback_state_confidence
        ) = extract_state_fallback_candidate(

            text,

            api
        )


        if fallback_state is not None:

            state = fallback_state

            state_confidence_override = (
                fallback_state_confidence
            )


    jc = extract_jc(
        text,
        state,
        api
    )


    jc_confidence_override = None


    if jc is None:

        (
            fallback_jc,
            fallback_jc_confidence
        ) = extract_jc_fallback_candidate(

            text,

            state,

            api
        )


        if fallback_jc is not None:

            jc = fallback_jc

            jc_confidence_override = (
                fallback_jc_confidence
            )


    entities = {

        "state":
            state,

        "jc":
            jc,

        "_entity_confidence_override": {

            "state":
                state_confidence_override,

            "jc":
                jc_confidence_override
        },

        "minimum_neighbours":
            None,

        "execution_time":
            None,

        "frequency":
            None,

        "rules":
            None,

        "technology_flow":
            None
    }


    # ========================================================
    # CLEANUP
    # ========================================================

    if intent in (
        "START_CLEANUP",
        "PREVIEW_CLEANUP"
    ):

        entities[
            "minimum_neighbours"
        ] = extract_minimum_neighbours(
            text
        )


    # ========================================================
    # AUTOMATION
    # ========================================================

    if intent == "CREATE_AUTOMATION":

        entities[
            "frequency"
        ] = extract_frequency(
            text
        )


        entities[
            "execution_time"
        ] = extract_execution_time(
            text
        )


        entities[
            "minimum_neighbours"
        ] = extract_minimum_neighbours(
            text
        )


        entities[
            "rules"
        ] = extract_rules(
            text
        )


        entities[
            "technology_flow"
        ] = extract_technology_flow(
            text
        )


    return entities


# ============================================================
# LIVE ENTITY VALIDATION
# ============================================================

def validate_entities(
    entities,
    intent,
    api
):

    state = entities[
        "state"
    ]

    jc = entities[
        "jc"
    ]


    validation = {

        "state_exists":
            None,

        "jc_exists":
            None,

        "state_jc_exists":
            None
    }


    if state is not None:

        validation[
            "state_exists"
        ] = api.state_exists(
            state
        )


    if (
        state is not None
        and
        jc is not None
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


    return validation


# ============================================================
# MISSING INFORMATION
# ============================================================

def get_missing_information(
    intent,
    entities
):

    missing = []


    # --------------------------------------------------------
    # Operations requiring State + JC
    # --------------------------------------------------------

    if intent in (

        "START_CLEANUP",

        "PREVIEW_CLEANUP",

        "CREATE_AUTOMATION",

        "VALIDATE_NEIGHBOURS"
    ):

        if entities[
            "state"
        ] is None:

            missing.append(
                "state"
            )


        if entities[
            "jc"
        ] is None:

            missing.append(
                "jc"
            )


    # --------------------------------------------------------
    # Read operations
    # --------------------------------------------------------

    elif intent in (

        "GET_NEIGHBOURS",

        "GET_INVALID_NEIGHBOURS",

        "GET_PCI_INVALID",

        "GET_TAC_INVALID",

        "GET_COUNTS",

        "GET_INVALID_PERCENTAGE"
    ):

        if (

            entities[
                "state"
            ] is None

            and

            entities[
                "jc"
            ] is None
        ):

            missing.append(
                "state_or_jc"
            )


    return missing


# ============================================================
# ENTITY ERRORS
# ============================================================

def get_entity_errors(
    entities,
    entity_validation
):

    errors = []


    state = entities[
        "state"
    ]

    jc = entities[
        "jc"
    ]


    if (

        state is not None

        and

        entity_validation[
            "state_exists"
        ] is False
    ):

        errors.append(

            f"State '{state}' "
            f"does not exist in "
            f"the database."
        )


    if (

        state is not None

        and

        jc is not None

        and

        entity_validation[
            "state_jc_exists"
        ] is False
    ):

        errors.append(

            f"JC '{jc}' does not belong "
            f"to State '{state}'."
        )


    return errors


# ============================================================
# OUT OF SCOPE
# ============================================================

OUT_OF_SCOPE_PATTERNS = (

    "book a flight",
    "book a train",
    "train ticket",
    "book a hotel",
    "find a restaurant",
    "order food",
    "order a laptop",
    "buy a laptop",
    "weather",
    "play music",
    "play a song",
    "send an email",
    "send an email to",
    "send a message",
    "social media",
    "instagram",
    "set an alarm",
    "write an essay",
    "translate this",
    "show me a movie",
    "find a movie",
    "give me directions",
    "order something online",
    "buy something for me"
)


def _contains_any(
    text,
    phrases
):

    lower = text.lower()


    return any(

        phrase in lower

        for phrase in phrases
    )


# ============================================================
# INTENT GUARD
# ============================================================

def apply_intent_guard(
    text,
    model_intent,
    entities
):

    # --------------------------------------------------------
    # IMPORTANT FIX
    #
    # Do NOT directly use:
    #
    # config.INTENT_GUARD_ENABLED
    #
    # because older config.py versions may not contain it.
    #
    # getattr(..., True) keeps the guard enabled by default.
    # --------------------------------------------------------

    intent_guard_enabled = getattr(

        config,

        "INTENT_GUARD_ENABLED",

        True
    )


    if not intent_guard_enabled:

        return (
            model_intent,
            "MODEL"
        )


    lower = text.lower()


    # ========================================================
    # OUT OF SCOPE
    # ========================================================

    if _contains_any(
        text,
        OUT_OF_SCOPE_PATTERNS
    ):

        return (
            "OUT_OF_SCOPE",
            "GUARD"
        )


    # ========================================================
    # GET STATES
    # ========================================================

    if (

        "state list" in lower

        or

        "all states" in lower

        or

        "every state" in lower

        or

        "available states" in lower

        or

        "configured states" in lower

        or

        "get states" in lower

        or

        "get the name of the states"
        in lower

        or

        "what states" in lower

        or

        "which states" in lower
    ):

        return (
            "GET_STATES",
            "GUARD"
        )


    # ========================================================
    # GET JCS
    # ========================================================

    if (

        "get jc" in lower

        or

        "get jcs" in lower

        or

        "show jc" in lower

        or

        "show jcs" in lower

        or

        "list jc" in lower

        or

        "list jcs" in lower

        or

        "all jc" in lower

        or

        "all jcs" in lower

        or

        "which jcs" in lower

        or

        "what jcs" in lower
    ):

        return (
            "GET_JCS",
            "GUARD"
        )


    # ========================================================
    # NEIGHBOUR COUNT
    #
    # MUST BE BEFORE GENERIC GET_NEIGHBOURS.
    # ========================================================

    if any(

        phrase in lower

        for phrase in (

            "how many neighbours",

            "how many neighbour",

            "how many neighbors",

            "how many neighbor",

            "number of neighbours",

            "number of neighbour",

            "number of neighbors",

            "number of neighbor",

            "count neighbours",

            "count neighbour",

            "count neighbors",

            "count neighbor",

            "total neighbours",

            "total neighbour",

            "total neighbors",

            "total neighbor",

            "neighbour count",

            "neighbor count",

            "neighbour statistics",

            "neighbor statistics",

            "neighbour totals",

            "neighbor totals"
        )
    ):

        return (
            "GET_COUNTS",
            "GUARD"
        )


    # ========================================================
    # VALIDATE NEIGHBOURS
    #
    # Explicit validation requests are routed directly instead
    # of relying on the neural model. This prevents "validate"
    # from being confused with TAC/PCI invalid intents.
    # ========================================================

    if any(

        phrase in lower

        for phrase in (

            "validate neighbours",

            "validate neighbour",

            "validate neighbors",

            "validate neighbor",

            "run validation",

            "run validate",

            "get validate neighbours",

            "get validate neighbour",

            "get validate neighbors",

            "get validate neighbor",

            "show validate neighbours",

            "show validate neighbour",

            "show validate neighbors",

            "show validate neighbor",

            "check neighbours",

            "check neighbour",

            "check neighbors",

            "check neighbor"
        )
    ):

        return (
            "VALIDATE_NEIGHBOURS",
            "GUARD"
        )


    # ========================================================
    # TAC INVALID NEIGHBOURS
    #
    # TAC-specific requests must be checked before the generic
    # invalid-neighbours rule.
    # ========================================================

    if (

        "tac" in lower

        and

        any(

            word in lower

            for word in (

                "invalid",

                "mismatch",

                "failed",

                "failure",

                "problem"
            )
        )
    ):

        return (
            "GET_TAC_INVALID",
            "GUARD"
        )


    # ========================================================
    # PCI INVALID NEIGHBOURS
    #
    # PCI-specific requests must be checked before the generic
    # invalid-neighbours rule.
    # ========================================================

    if (

        "pci" in lower

        and

        any(

            word in lower

            for word in (

                "invalid",

                "mismatch",

                "failed",

                "failure",

                "problem"
            )
        )
    ):

        return (
            "GET_PCI_INVALID",
            "GUARD"
        )


    # ========================================================
    # INVALID NEIGHBOURS
    #
    # This is a read-only operation. It must never be routed
    # to cleanup and minimum neighbours must not be required.
    #
    # This includes commands without show/get/list, for example:
    # "invalid neighbours in Maharashtra JC_Mumbai".
    # ========================================================

    if any(

        phrase in lower

        for phrase in (

            "invalid neighbours",

            "invalid neighbour",

            "invalid neighbors",

            "invalid neighbor",

            "list invalid",

            "get invalid",

            "show invalid",

            "find invalid neighbours",

            "find invalid neighbour",

            "find invalid neighbors",

            "find invalid neighbor",

            "which neighbours are invalid",

            "which neighbour is invalid",

            "which neighbors are invalid",

            "which neighbor is invalid"
        )
    ):

        return (
            "GET_INVALID_NEIGHBOURS",
            "GUARD"
        )


    # ========================================================
    # GET NEIGHBOURS
    # ========================================================

    if any(

        phrase in lower

        for phrase in (

            "show neighbours",

            "show neighbour",

            "show neighbors",

            "show neighbor",

            "list neighbours",

            "list neighbour",

            "list neighbors",

            "list neighbor",

            "get neighbours",

            "get neighbour",

            "get neighbors",

            "get neighbor",

            "give me the neighbours",

            "give me the neighbour",

            "give me the neighbors",

            "give me the neighbor"
        )
    ):

        return (
            "GET_NEIGHBOURS",
            "GUARD"
        )


    # ========================================================
    # AUTOMATION LIST
    #
    # IMPORTANT:
    #
    # This must be checked BEFORE generic automation creation.
    # ========================================================

    if (

        "automation list" in lower

        or

        "list my automations" in lower

        or

        "list all automations" in lower

        or

        "configured automations" in lower

        or

        "automation jobs" in lower

        or

        "scheduled automations" in lower

        or

        "show my automations" in lower

        or

        "get automations" in lower
    ):

        return (
            "GET_AUTOMATIONS",
            "GUARD"
        )


    # ========================================================
    # CREATE AUTOMATION
    # ========================================================

    automation_signal = any(

        phrase in lower

        for phrase in (

            "create an automation",

            "create automation",

            "set up an automation",

            "setup an automation",

            "set up automation",

            "schedule",

            "scheduled job",

            "scheduled cleanup",

            "automated cleanup",

            "automated neighbour validation",

            "automated neighbor validation",

            "configure an automation",

            "create a cleanup automation",

            "create a scheduled job"
        )
    )


    if automation_signal:

        if (

            entities.get(
                "state"
            )

            and

            entities.get(
                "jc"
            )
        ):

            return (
                "CREATE_AUTOMATION",
                "GUARD"
            )


        return (
            "MISSING_INFORMATION",
            "GUARD"
        )


    # ========================================================
    # DIRECT CLEANUP
    # ========================================================

    cleanup_signal = any(

        phrase in lower

        for phrase in (

            "start cleanup",

            "run cleanup",

            "run the cleanup",

            "perform cleanup",

            "execute cleanup",

            "delete invalid neighbours",

            "delete invalid neighbour",

            "delete invalid neighbors",

            "delete invalid neighbor",

            "remove invalid neighbours",

            "remove invalid neighbour",

            "remove invalid neighbors",

            "remove invalid neighbor",

            "clean invalid neighbours",

            "clean invalid neighbour",

            "clean invalid neighbors",

            "clean invalid neighbor",

            "clean the invalid neighbours",

            "clean the invalid neighbors",

            "clean bad neighbours",

            "clean bad neighbors",

            "delete invalid neighbour records",

            "remove invalid neighbour records"
        )
    )


    if cleanup_signal:

        if (

            entities.get(
                "state"
            )

            and

            entities.get(
                "jc"
            )
        ):

            return (
                "START_CLEANUP",
                "GUARD"
            )


        return (
            "MISSING_INFORMATION",
            "GUARD"
        )


    # ========================================================
    # CLEANUP RESULT
    # ========================================================

    if (

        "cleanup result" in lower

        or

        "cleanup summary" in lower

        or

        "deletion result" in lower

        or

        "what was deleted" in lower

        or

        "what did the cleanup remove"
        in lower

        or

        "how many neighbours were deleted"
        in lower

        or

        "how many records were removed"
        in lower
    ):

        return (
            "GET_CLEANUP_RESULT",
            "GUARD"
        )


    # ========================================================
    # CLEANUP PROGRESS
    # ========================================================

    if (

        "cleanup progress" in lower

        or

        "cleanup status" in lower

        or

        "how far has cleanup progressed"
        in lower

        or

        "how much cleanup is complete"
        in lower
    ):

        return (
            "GET_CLEANUP_PROGRESS",
            "GUARD"
        )


    # ========================================================
    # MODEL FALLBACK
    # ========================================================

    return (
        model_intent,
        "MODEL"
    )


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


    # --------------------------------------------------------
    # Empty command
    # --------------------------------------------------------

    if not text:

        return {

            "text":
                "",

            "intent":
                "AMBIGUOUS_REQUEST",

            "model_intent":
                "AMBIGUOUS_REQUEST",

            "intent_source":
                "GUARD",

            "confidence":
                1.0,

            "entities": {

                "state":
                    None,

                "jc":
                    None,

                "minimum_neighbours":
                    None,

                "execution_time":
                    None,

                "frequency":
                    None,

                "rules":
                    None,

                "technology_flow":
                    None
            },

            "missing":
                [],

            "entity_validation": {

                "state_exists":
                    None,

                "jc_exists":
                    None,

                "state_jc_exists":
                    None
            },

            "entity_errors":
                []
        }


    # --------------------------------------------------------
    # Initial entities
    #
    # The guard needs State + JC to decide whether an
    # operational command is complete.
    # --------------------------------------------------------

    initial_entities = extract_entities(

        text,

        "CREATE_AUTOMATION",

        api
    )


    # --------------------------------------------------------
    # Neural model prediction
    # --------------------------------------------------------

    (
        model_intent,
        confidence,
        probabilities
    ) = predict_intent(

        text,

        model,

        tokenizer,

        device
    )


    # --------------------------------------------------------
    # Hybrid intent guard
    # --------------------------------------------------------

    (
        final_intent,
        intent_source
    ) = apply_intent_guard(

        text,

        model_intent,

        initial_entities
    )


    # --------------------------------------------------------
    # Re-extract entities using final intent
    # --------------------------------------------------------

    entities = extract_entities(

        text,

        final_intent,

        api
    )


    # --------------------------------------------------------
    # Entity match confidence
    # --------------------------------------------------------

    entity_confidence = extract_entity_confidence(

        text,

        entities
    )


    # --------------------------------------------------------
    # Apply fallback confidence overrides.
    # Fallback candidates remain low-confidence and therefore
    # use the existing clarification flow instead of being
    # auto-executed as strong fuzzy matches.
    # --------------------------------------------------------

    confidence_overrides = entities.get(

        "_entity_confidence_override",

        {}
    )


    if isinstance(
        confidence_overrides,
        dict
    ):

        for entity_name in (

            "state",

            "jc"
        ):

            override = confidence_overrides.get(
                entity_name
            )


            if override is not None:

                entity_confidence[
                    entity_name
                ] = override


    entities.pop(

        "_entity_confidence_override",

        None
    )


    # --------------------------------------------------------
    # Live database validation
    # --------------------------------------------------------

    entity_validation = validate_entities(

        entities,

        final_intent,

        api
    )


    # --------------------------------------------------------
    # Missing information
    # --------------------------------------------------------

    missing = get_missing_information(

        final_intent,

        entities
    )


    # --------------------------------------------------------
    # Entity errors
    # --------------------------------------------------------

    entity_errors = get_entity_errors(

        entities,

        entity_validation
    )


    return {

        "text":
            text,

        "intent":
            final_intent,

        "model_intent":
            model_intent,

        "intent_source":
            intent_source,

        "confidence":
            confidence,

        "entities":
            entities,

        "entity_confidence":
            entity_confidence,

        "missing":
            missing,

        "entity_validation":
            entity_validation,

        "entity_errors":
            entity_errors
    }


# ============================================================
# DISPLAY COMMAND ANALYSIS
# ============================================================

def display_result(
    result
):

    print()

    print(
        "=" * 60
    )

    print(
        "COMMAND ANALYSIS"
    )

    print(
        "=" * 60
    )

    print()

    print(
        "Command:",
        result["text"]
    )

    print(
        "Intent:",
        result["intent"]
    )

    print(
        "Model intent:",
        result["model_intent"]
    )

    print(
        "Intent source:",
        result["intent_source"]
    )

    print(
        "Confidence:",
        f"{result['confidence'] * 100:.2f}%"
    )


    print()

    print(
        "Entities"
    )

    print(
        "-" * 60
    )


    for key, value in result[
        "entities"
    ].items():

        print(
            f"{key}: {value}"
        )


    print()

    print(
        "Entity Match Confidence"
    )

    print(
        "-" * 60
    )


    for key, value in result.get(

        "entity_confidence",

        {}

    ).items():

        if value is None:

            print(
                f"{key}: None"
            )

        else:

            print(
                f"{key}: {value * 100:.2f}%"
            )


    print()

    print(
        "Missing information"
    )

    print(
        "-" * 60
    )


    if result[
        "missing"
    ]:

        print(
            ", ".join(
                result[
                    "missing"
                ]
            )
        )

    else:

        print(
            "None"
        )


    print()

    print(
        "Live Database Validation"
    )

    print(
        "-" * 60
    )


    for key, value in result[
        "entity_validation"
    ].items():

        print(
            f"{key}: {value}"
        )


    print()

    print(
        "Entity Validation Errors"
    )

    print(
        "-" * 60
    )


    if result[
        "entity_errors"
    ]:

        for error in result[
            "entity_errors"
        ]:

            print(
                "ERROR:",
                error
            )

    else:

        print(
            "None"
        )


    print()

    print(
        "Execution Status"
    )

    print(
        "-" * 60
    )


    if result[
        "entity_errors"
    ]:

        print(
            "BLOCKED - invalid database entity."
        )

    elif result[
        "missing"
    ]:

        print(
            "BLOCKED - missing information."
        )

    elif result[
        "intent"
    ] == "OUT_OF_SCOPE":

        print(
            "BLOCKED - out of scope."
        )

    else:

        print(
            "READY - command is structurally complete."
        )


    print(
        "=" * 60
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print(
        "=" * 60
    )

    print(
        "NEIGHBOUR MANAGEMENT AI"
    )

    print(
        "PHASE 6B - LIVE DATABASE INTEGRATION"
    )

    print(
        "=" * 60
    )


    # --------------------------------------------------------
    # DEVICE
    # --------------------------------------------------------

    device = (

        torch.device(
            "cuda"
        )

        if torch.cuda.is_available()

        else

        torch.device(
            "cpu"
        )
    )


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
    # API
    # --------------------------------------------------------

    api = NeighbourManagementAPI()


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

    print(
        "=" * 60
    )


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