"""
Central configuration for the Neighbour Management AI.

This file is the single configuration source for:

1. Dataset paths
2. Tokenizer
3. Model architecture
4. Model training
5. Model evaluation
6. Cleanup safety
7. Automation safety

IMPORTANT
---------
Existing public configuration names are preserved so that
train.py, evaluate.py, predict.py, dataset.py and the
rest of the project remain compatible.
"""

from pathlib import Path

from model.intent_mapping import get_num_intents


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ============================================================
# DIRECTORIES
# ============================================================

DATASET_DIR = PROJECT_ROOT / "dataset"

MODEL_DIR = PROJECT_ROOT / "model"


# ============================================================
# DATASET FILES
# ============================================================

TRAIN_FILE = DATASET_DIR / "train.json"

VALIDATION_FILE = DATASET_DIR / "validation.json"

TEST_FILE = DATASET_DIR / "test.json"


# Compatibility aliases

TRAIN_DATASET_PATH = TRAIN_FILE

VALIDATION_DATASET_PATH = VALIDATION_FILE

TEST_DATASET_PATH = TEST_FILE


# ============================================================
# TOKENIZER
# ============================================================

TOKENIZER_FILE = MODEL_DIR / "tokenizer.json"

TOKENIZER_PATH = TOKENIZER_FILE


# ============================================================
# MODEL FILES
# ============================================================

MODEL_FILE = MODEL_DIR / "intent_model.pth"

MODEL_PATH = MODEL_FILE


# ============================================================
# TRAINING OUTPUT FILES
# ============================================================

HISTORY_FILE = MODEL_DIR / "training_history.json"

CONFIG_FILE = MODEL_DIR / "training_config.json"


# Compatibility aliases

TRAINING_HISTORY_FILE = HISTORY_FILE

TRAINING_HISTORY_PATH = HISTORY_FILE

TRAINING_CONFIG_FILE = CONFIG_FILE

TRAINING_CONFIG_PATH = CONFIG_FILE


# ============================================================
# MODEL ARCHITECTURE
# ============================================================

# Maximum tokenizer vocabulary capacity.
#
# Actual vocabulary may be smaller.
# Example:
#
# Maximum vocabulary = 2000
# Current trained vocabulary = 235

VOCAB_SIZE = 2000


# Embedding dimension.

EMBEDDING_DIM = 64


# Hidden layer dimension.

HIDDEN_DIM = 128


# Number of hidden layers.

NUM_HIDDEN_LAYERS = 2


# Compatibility alias.

HIDDEN_LAYERS = NUM_HIDDEN_LAYERS


# Dropout probability.

DROPOUT = 0.2


# ============================================================
# INTENTS
# ============================================================

# intent_mapping.py is the single source of truth.

NUM_INTENTS = get_num_intents()


# Compatibility alias.

NUM_CLASSES = NUM_INTENTS


# ============================================================
# TOKENIZATION
# ============================================================

MAX_LENGTH = 32

MAX_SEQUENCE_LENGTH = MAX_LENGTH


# ============================================================
# TRAINING
# ============================================================

BATCH_SIZE = 16

LEARNING_RATE = 0.001

EPOCHS = 30


# ============================================================
# TRAINING REGULARIZATION
# ============================================================

# AdamW weight decay.

WEIGHT_DECAY = 0.0005


# Enable mild class weighting.
#
# This is useful because CREATE_AUTOMATION and
# MISSING_INFORMATION have different frequencies.

USE_CLASS_WEIGHTS = True


# 0.5 means inverse-square-root weighting:
#
# weight = 1 / sqrt(class_count)
#
# This is intentionally mild so that rare classes
# do not dominate training.

CLASS_WEIGHT_POWER = 0.5


# Gradient clipping.

GRADIENT_CLIP_NORM = 1.0


# ============================================================
# EARLY STOPPING
# ============================================================

# Number of validation epochs allowed without meaningful
# improvement before training stops.

EARLY_STOPPING_PATIENCE = 8


# Minimum validation improvement considered meaningful.

EARLY_STOPPING_MIN_DELTA = 0.0005


# ============================================================
# DATA LOADER
# ============================================================

# Windows + CPU safe.

NUM_WORKERS = 0


# ============================================================
# REPRODUCIBILITY
# ============================================================

RANDOM_SEED = 42


# ============================================================
# SAFETY CONFIGURATION
# ============================================================

# Default minimum number of neighbours that must remain.

DEFAULT_MINIMUM_NEIGHBOURS = 5


# Compatibility alias.

MINIMUM_NEIGHBOURS = DEFAULT_MINIMUM_NEIGHBOURS


# HARD SAFETY RULE:
#
# Never delete all neighbours for a selected
# State + JC.

NEVER_DELETE_ALL_NEIGHBOURS = True


# ============================================================
# DIRECT CLEANUP
# ============================================================

DIRECT_CLEANUP_ENABLED = True


# ============================================================
# AUTOMATION
# ============================================================

AUTOMATION_DEFAULT_FREQUENCY = "DAILY"


AUTOMATION_DEFAULT_RULES = [
    "PCI",
    "TAC"
]


AUTOMATION_ALLOWED_FREQUENCIES = [
    "DAILY",
    "WEEKLY",
    "MONTHLY"
]


# ============================================================
# AUTOMATION SAFETY
# ============================================================

AUTOMATION_REQUIRES_SAFETY_CHECK = True


# ============================================================
# CLEANUP SAFETY FLOW
# ============================================================

CLEANUP_REQUIRES_SAFETY_CHECK = True


CLEANUP_REQUIRES_VALID_STATE_JC = True


CLEANUP_CHECK_INVALID_PERCENTAGE = True


# ============================================================
# CHECKPOINT COMPATIBILITY
# ============================================================

# Current terminology.

MODEL_INTENT_KEY = "num_intents"

MODEL_HIDDEN_LAYER_KEY = "hidden_layers"


# Legacy terminology.

LEGACY_MODEL_INTENT_KEY = "num_classes"

LEGACY_MODEL_HIDDEN_LAYER_KEY = "num_hidden_layers"


# ============================================================
# CONFIGURATION SUMMARY
# ============================================================

def get_config_summary():

    return {

        # ----------------------------------------------------
        # Project
        # ----------------------------------------------------

        "project_root":
            str(PROJECT_ROOT),

        "dataset_dir":
            str(DATASET_DIR),

        "model_dir":
            str(MODEL_DIR),

        # ----------------------------------------------------
        # Dataset
        # ----------------------------------------------------

        "train_file":
            str(TRAIN_FILE),

        "validation_file":
            str(VALIDATION_FILE),

        "test_file":
            str(TEST_FILE),

        # ----------------------------------------------------
        # Tokenizer
        # ----------------------------------------------------

        "tokenizer_file":
            str(TOKENIZER_FILE),

        # ----------------------------------------------------
        # Model
        # ----------------------------------------------------

        "model_file":
            str(MODEL_FILE),

        "vocab_size":
            VOCAB_SIZE,

        "num_intents":
            NUM_INTENTS,

        "embedding_dim":
            EMBEDDING_DIM,

        "hidden_dim":
            HIDDEN_DIM,

        "num_hidden_layers":
            NUM_HIDDEN_LAYERS,

        "dropout":
            DROPOUT,

        # ----------------------------------------------------
        # Tokenization
        # ----------------------------------------------------

        "max_length":
            MAX_LENGTH,

        # ----------------------------------------------------
        # Training
        # ----------------------------------------------------

        "batch_size":
            BATCH_SIZE,

        "learning_rate":
            LEARNING_RATE,

        "epochs":
            EPOCHS,

        "weight_decay":
            WEIGHT_DECAY,

        "use_class_weights":
            USE_CLASS_WEIGHTS,

        "class_weight_power":
            CLASS_WEIGHT_POWER,

        "gradient_clip_norm":
            GRADIENT_CLIP_NORM,

        "early_stopping_patience":
            EARLY_STOPPING_PATIENCE,

        "early_stopping_min_delta":
            EARLY_STOPPING_MIN_DELTA,

        # ----------------------------------------------------
        # DataLoader
        # ----------------------------------------------------

        "num_workers":
            NUM_WORKERS,

        # ----------------------------------------------------
        # Reproducibility
        # ----------------------------------------------------

        "random_seed":
            RANDOM_SEED,

        # ----------------------------------------------------
        # Safety
        # ----------------------------------------------------

        "default_minimum_neighbours":
            DEFAULT_MINIMUM_NEIGHBOURS,

        "minimum_neighbours":
            MINIMUM_NEIGHBOURS,

        "never_delete_all_neighbours":
            NEVER_DELETE_ALL_NEIGHBOURS,

        "direct_cleanup_enabled":
            DIRECT_CLEANUP_ENABLED,

        "cleanup_requires_safety_check":
            CLEANUP_REQUIRES_SAFETY_CHECK,

        "cleanup_requires_valid_state_jc":
            CLEANUP_REQUIRES_VALID_STATE_JC,

        "cleanup_check_invalid_percentage":
            CLEANUP_CHECK_INVALID_PERCENTAGE,

        # ----------------------------------------------------
        # Automation
        # ----------------------------------------------------

        "automation_default_frequency":
            AUTOMATION_DEFAULT_FREQUENCY,

        "automation_default_rules":
            AUTOMATION_DEFAULT_RULES,

        "automation_allowed_frequencies":
            AUTOMATION_ALLOWED_FREQUENCIES,

        "automation_requires_safety_check":
            AUTOMATION_REQUIRES_SAFETY_CHECK
    }


# ============================================================
# CONFIGURATION VALIDATION
# ============================================================

def validate_config():

    errors = []

    # --------------------------------------------------------
    # Paths
    # --------------------------------------------------------

    required_directories = [
        DATASET_DIR,
        MODEL_DIR
    ]

    for directory in required_directories:

        if not directory.exists():

            try:
                directory.mkdir(
                    parents=True,
                    exist_ok=True
                )

            except Exception as error:

                errors.append(
                    f"Could not create directory "
                    f"{directory}: {error}"
                )

    # --------------------------------------------------------
    # Model
    # --------------------------------------------------------

    if VOCAB_SIZE <= 0:

        errors.append(
            "VOCAB_SIZE must be greater than 0."
        )

    if NUM_INTENTS <= 0:

        errors.append(
            "NUM_INTENTS must be greater than 0."
        )

    if EMBEDDING_DIM <= 0:

        errors.append(
            "EMBEDDING_DIM must be greater than 0."
        )

    if HIDDEN_DIM <= 0:

        errors.append(
            "HIDDEN_DIM must be greater than 0."
        )

    if NUM_HIDDEN_LAYERS <= 0:

        errors.append(
            "NUM_HIDDEN_LAYERS must be greater than 0."
        )

    if not 0 <= DROPOUT < 1:

        errors.append(
            "DROPOUT must be >= 0 and < 1."
        )

    # --------------------------------------------------------
    # Tokenization
    # --------------------------------------------------------

    if MAX_LENGTH <= 0:

        errors.append(
            "MAX_LENGTH must be greater than 0."
        )

    # --------------------------------------------------------
    # Training
    # --------------------------------------------------------

    if BATCH_SIZE <= 0:

        errors.append(
            "BATCH_SIZE must be greater than 0."
        )

    if LEARNING_RATE <= 0:

        errors.append(
            "LEARNING_RATE must be greater than 0."
        )

    if EPOCHS <= 0:

        errors.append(
            "EPOCHS must be greater than 0."
        )

    if WEIGHT_DECAY < 0:

        errors.append(
            "WEIGHT_DECAY cannot be negative."
        )

    if not 0 <= CLASS_WEIGHT_POWER <= 1:

        errors.append(
            "CLASS_WEIGHT_POWER must be "
            "between 0 and 1."
        )

    if GRADIENT_CLIP_NORM <= 0:

        errors.append(
            "GRADIENT_CLIP_NORM must be "
            "greater than 0."
        )

    if EARLY_STOPPING_PATIENCE < 1:

        errors.append(
            "EARLY_STOPPING_PATIENCE must be "
            "at least 1."
        )

    if EARLY_STOPPING_MIN_DELTA < 0:

        errors.append(
            "EARLY_STOPPING_MIN_DELTA cannot "
            "be negative."
        )

    # --------------------------------------------------------
    # DataLoader
    # --------------------------------------------------------

    if NUM_WORKERS < 0:

        errors.append(
            "NUM_WORKERS cannot be negative."
        )

    # --------------------------------------------------------
    # Safety
    # --------------------------------------------------------

    if DEFAULT_MINIMUM_NEIGHBOURS < 1:

        errors.append(
            "DEFAULT_MINIMUM_NEIGHBOURS "
            "must be at least 1."
        )

    if not NEVER_DELETE_ALL_NEIGHBOURS:

        errors.append(
            "NEVER_DELETE_ALL_NEIGHBOURS "
            "must remain True."
        )

    # --------------------------------------------------------
    # Automation
    # --------------------------------------------------------

    if (
        AUTOMATION_DEFAULT_FREQUENCY
        not in AUTOMATION_ALLOWED_FREQUENCIES
    ):

        errors.append(
            "AUTOMATION_DEFAULT_FREQUENCY "
            "is not supported."
        )

    if not AUTOMATION_DEFAULT_RULES:

        errors.append(
            "AUTOMATION_DEFAULT_RULES "
            "cannot be empty."
        )

    if (
        not isinstance(
            AUTOMATION_DEFAULT_RULES,
            list
        )
    ):

        errors.append(
            "AUTOMATION_DEFAULT_RULES "
            "must be a list."
        )

    # --------------------------------------------------------
    # Final validation
    # --------------------------------------------------------

    if errors:

        raise ValueError(
            "\n".join(errors)
        )

    return True


# ============================================================
# VALIDATE ON IMPORT
# ============================================================

validate_config()