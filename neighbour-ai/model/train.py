import json
import random

import numpy as np
import torch
import torch.nn as nn

from torch.utils.data import DataLoader

from tokenizer.tokenizer import SimpleTokenizer

from model.dataset import IntentDataset

from model.intent_mapping import (
    INTENTS,
    INTENT_TO_LABEL
)

from model.intent_model import IntentClassifier

import model.config as config


# ============================================================
# REPRODUCIBILITY
# ============================================================

def set_seed(seed):

    random.seed(seed)

    np.random.seed(seed)

    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    if hasattr(torch.backends, "cudnn"):

        torch.backends.cudnn.deterministic = True

        torch.backends.cudnn.benchmark = False


# ============================================================
# DEVICE
# ============================================================

def get_device():

    if torch.cuda.is_available():

        return torch.device("cuda")

    return torch.device("cpu")


# ============================================================
# CLASS WEIGHTS
# ============================================================

def calculate_class_weights(
    dataset,
    num_classes
):
    """
    Calculate conservative inverse-frequency class weights.

    The power parameter is controlled through config so the
    weighting strategy can be changed without changing code.
    """

    counts = np.zeros(
        num_classes,
        dtype=np.float64
    )

    for index in range(
        len(dataset)
    ):

        sample = dataset[index]

        label = int(
            sample["label"]
        )

        if 0 <= label < num_classes:

            counts[label] += 1

    if counts.sum() == 0:

        raise RuntimeError(
            "Training dataset contains no valid labels."
        )

    safe_counts = np.maximum(
        counts,
        1.0
    )

    total = safe_counts.sum()

    weights = total / (
        num_classes * safe_counts
    )

    weights = (
        weights
        / weights.mean()
    )

    power = getattr(
        config,
        "CLASS_WEIGHT_POWER",
        1.0
    )

    if power != 1.0:

        weights = np.power(
            weights,
            power
        )

        weights = (
            weights
            / weights.mean()
        )

    return (
        torch.tensor(
            weights,
            dtype=torch.float32
        ),
        counts
    )


# ============================================================
# EVALUATION
# ============================================================

def evaluate(
    model,
    data_loader,
    criterion,
    device
):

    model.eval()

    total_loss = 0.0

    correct = 0

    total = 0

    with torch.no_grad():

        for batch in data_loader:

            input_ids = batch[
                "input_ids"
            ].to(device)

            labels = batch[
                "label"
            ].to(device)

            outputs = model(
                input_ids
            )

            loss = criterion(
                outputs,
                labels
            )

            total_loss += (
                loss.item()
                * labels.size(0)
            )

            predictions = torch.argmax(
                outputs,
                dim=1
            )

            correct += (
                predictions == labels
            ).sum().item()

            total += labels.size(0)

    average_loss = (
        total_loss / total
        if total > 0
        else 0.0
    )

    accuracy = (
        correct / total
        if total > 0
        else 0.0
    )

    return (
        average_loss,
        accuracy
    )


# ============================================================
# SAVE TRAINING HISTORY
# ============================================================

def save_history(history):

    with open(
        config.HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4
        )


# ============================================================
# SAVE TRAINING CONFIGURATION
# ============================================================

def save_config(
    class_weights=None,
    class_counts=None
):

    training_config = {

        "train_file":
            str(config.TRAIN_FILE),

        "validation_file":
            str(config.VALIDATION_FILE),

        "test_file":
            str(config.TEST_FILE),

        "tokenizer_file":
            str(config.TOKENIZER_FILE),

        "max_length":
            config.MAX_LENGTH,

        "embedding_dim":
            config.EMBEDDING_DIM,

        "hidden_dim":
            config.HIDDEN_DIM,

        "num_hidden_layers":
            config.NUM_HIDDEN_LAYERS,

        "dropout":
            config.DROPOUT,

        "batch_size":
            config.BATCH_SIZE,

        "learning_rate":
            config.LEARNING_RATE,

        "epochs":
            config.EPOCHS,

        "random_seed":
            config.RANDOM_SEED,

        "num_intents":
            len(INTENTS),

        "intent_to_label":
            INTENT_TO_LABEL,

        "use_class_weights":
            getattr(
                config,
                "USE_CLASS_WEIGHTS",
                False
            ),

        "class_weight_power":
            getattr(
                config,
                "CLASS_WEIGHT_POWER",
                1.0
            ),

        "weight_decay":
            getattr(
                config,
                "WEIGHT_DECAY",
                0.0
            )
    }

    if class_weights is not None:

        training_config[
            "class_weights"
        ] = [
            float(weight)
            for weight in class_weights
        ]

    if class_counts is not None:

        training_config[
            "class_counts"
        ] = [
            int(count)
            for count in class_counts
        ]

    with open(
        config.CONFIG_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            training_config,
            file,
            indent=4
        )


# ============================================================
# VALIDATE TRAINING CONFIGURATION
# ============================================================

def validate_configuration(
    tokenizer
):

    expected_intents = len(
        INTENTS
    )

    if expected_intents != 18:

        raise RuntimeError(
            "Unexpected number of intents. "
            f"Expected 18, got {expected_intents}."
        )

    if len(INTENT_TO_LABEL) != expected_intents:

        raise RuntimeError(
            "Intent mapping size does not match "
            "the number of intents."
        )

    labels = sorted(
        INTENT_TO_LABEL.values()
    )

    expected_labels = list(
        range(expected_intents)
    )

    if labels != expected_labels:

        raise RuntimeError(
            "Intent labels are not continuous."
        )

    if len(tokenizer) <= 0:

        raise RuntimeError(
            "Tokenizer vocabulary is empty."
        )

    if config.MAX_LENGTH <= 0:

        raise RuntimeError(
            "MAX_LENGTH must be greater than zero."
        )

    if config.BATCH_SIZE <= 0:

        raise RuntimeError(
            "BATCH_SIZE must be greater than zero."
        )

    if config.EMBEDDING_DIM <= 0:

        raise RuntimeError(
            "EMBEDDING_DIM must be greater than zero."
        )

    if config.HIDDEN_DIM <= 0:

        raise RuntimeError(
            "HIDDEN_DIM must be greater than zero."
        )

    if config.NUM_HIDDEN_LAYERS <= 0:

        raise RuntimeError(
            "NUM_HIDDEN_LAYERS must be greater than zero."
        )

    if config.EPOCHS <= 0:

        raise RuntimeError(
            "EPOCHS must be greater than zero."
        )


# ============================================================
# MAIN TRAINING
# ============================================================

def main():

    # --------------------------------------------------------
    # Seed
    # --------------------------------------------------------

    set_seed(
        config.RANDOM_SEED
    )

    # --------------------------------------------------------
    # Device
    # --------------------------------------------------------

    device = get_device()

    print("=" * 60)
    print("PHASE 5C - MODEL TRAINING")
    print("=" * 60)

    print()
    print(
        "Device:",
        device
    )

    # --------------------------------------------------------
    # Load tokenizer
    # --------------------------------------------------------

    print()
    print(
        "Loading tokenizer..."
    )

    tokenizer = SimpleTokenizer.load(
        config.TOKENIZER_FILE
    )

    print(
        "Vocabulary size:",
        len(tokenizer)
    )

    # --------------------------------------------------------
    # Validate configuration
    # --------------------------------------------------------

    validate_configuration(
        tokenizer
    )

    # --------------------------------------------------------
    # Load datasets
    # --------------------------------------------------------

    print()
    print(
        "Loading datasets..."
    )

    train_dataset = IntentDataset(
        dataset_path=config.TRAIN_FILE,
        tokenizer=tokenizer,
        intent_to_id=INTENT_TO_LABEL,
        max_length=config.MAX_LENGTH
    )

    validation_dataset = IntentDataset(
        dataset_path=config.VALIDATION_FILE,
        tokenizer=tokenizer,
        intent_to_id=INTENT_TO_LABEL,
        max_length=config.MAX_LENGTH
    )

    print(
        "Training examples:",
        len(train_dataset)
    )

    print(
        "Validation examples:",
        len(validation_dataset)
    )

    if len(train_dataset) == 0:

        raise RuntimeError(
            "Training dataset is empty."
        )

    if len(validation_dataset) == 0:

        raise RuntimeError(
            "Validation dataset is empty."
        )

    # --------------------------------------------------------
    # Reproducible DataLoader generator
    # --------------------------------------------------------

    generator = torch.Generator()

    generator.manual_seed(
        config.RANDOM_SEED
    )

    # --------------------------------------------------------
    # DataLoaders
    # --------------------------------------------------------

    train_loader = DataLoader(
        train_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=True,
        num_workers=config.NUM_WORKERS,
        generator=generator
    )

    validation_loader = DataLoader(
        validation_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=False,
        num_workers=config.NUM_WORKERS
    )

    # --------------------------------------------------------
    # Create model
    # --------------------------------------------------------

    model = IntentClassifier(
        vocab_size=len(tokenizer),
        num_intents=len(INTENTS),
        embedding_dim=config.EMBEDDING_DIM,
        hidden_dim=config.HIDDEN_DIM,
        hidden_layers=config.NUM_HIDDEN_LAYERS,
        dropout=config.DROPOUT
    )

    model = model.to(
        device
    )

    print()
    print(
        "Model configuration"
    )

    print("-" * 60)

    print(
        "Vocabulary size:",
        len(tokenizer)
    )

    print(
        "Intent classes:",
        len(INTENTS)
    )

    print(
        "Embedding dimension:",
        config.EMBEDDING_DIM
    )

    print(
        "Hidden dimension:",
        config.HIDDEN_DIM
    )

    print(
        "Hidden layers:",
        config.NUM_HIDDEN_LAYERS
    )

    print(
        "Dropout:",
        config.DROPOUT
    )

    print(
        "Batch size:",
        config.BATCH_SIZE
    )

    print(
        "Learning rate:",
        config.LEARNING_RATE
    )

    print(
        "Epochs:",
        config.EPOCHS
    )

    # --------------------------------------------------------
    # Class weights
    # --------------------------------------------------------

    use_class_weights = getattr(
        config,
        "USE_CLASS_WEIGHTS",
        False
    )

    class_weights = None

    class_counts = None

    if use_class_weights:

        (
            class_weights,
            class_counts
        ) = calculate_class_weights(
            train_dataset,
            len(INTENTS)
        )

        class_weights = class_weights.to(
            device
        )

        print()
        print(
            "Class weights:",
            True
        )

        print(
            "Class weight power:",
            getattr(
                config,
                "CLASS_WEIGHT_POWER",
                1.0
            )
        )

        print()
        print(
            "Class distribution"
        )

        print("-" * 60)

        for index, intent in enumerate(
            INTENTS
        ):

            print(
                f"{intent:<30} "
                f"{int(class_counts[index]):>4} "
                f"weight="
                f"{class_weights[index].item():.4f}"
            )

    else:

        print()
        print(
            "Class weights:",
            False
        )

    # --------------------------------------------------------
    # Loss
    # --------------------------------------------------------

    criterion = nn.CrossEntropyLoss(
        weight=class_weights
    )

    # --------------------------------------------------------
    # Optimizer
    # --------------------------------------------------------

    weight_decay = getattr(
        config,
        "WEIGHT_DECAY",
        0.0
    )

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=config.LEARNING_RATE,
        weight_decay=weight_decay
    )

    print(
        "Weight decay:",
        weight_decay
    )

    # --------------------------------------------------------
    # Save configuration
    # --------------------------------------------------------

    save_config(
        class_weights=(
            class_weights.detach()
            .cpu()
            .tolist()
            if class_weights is not None
            else None
        ),
        class_counts=class_counts
    )

    # --------------------------------------------------------
    # History
    # --------------------------------------------------------

    history = {

        "train_loss": [],

        "train_accuracy": [],

        "validation_loss": [],

        "validation_accuracy": []
    }

    # --------------------------------------------------------
    # Best model
    # --------------------------------------------------------

    best_validation_accuracy = -1.0

    best_validation_loss = float(
        "inf"
    )

    best_epoch = 0

    # ========================================================
    # TRAINING LOOP
    # ========================================================

    print()
    print("=" * 60)
    print(
        "STARTING TRAINING"
    )
    print("=" * 60)

    for epoch in range(
        config.EPOCHS
    ):

        model.train()

        running_loss = 0.0

        correct = 0

        total = 0

        # ----------------------------------------------------
        # Training batches
        # ----------------------------------------------------

        for batch in train_loader:

            input_ids = batch[
                "input_ids"
            ].to(device)

            labels = batch[
                "label"
            ].to(device)

            # ------------------------------------------------
            # Clear gradients
            # ------------------------------------------------

            optimizer.zero_grad(
                set_to_none=True
            )

            # ------------------------------------------------
            # Forward
            # ------------------------------------------------

            outputs = model(
                input_ids
            )

            # ------------------------------------------------
            # Loss
            # ------------------------------------------------

            loss = criterion(
                outputs,
                labels
            )

            # ------------------------------------------------
            # Backpropagation
            # ------------------------------------------------

            loss.backward()

            # ------------------------------------------------
            # Gradient clipping
            # ------------------------------------------------

            torch.nn.utils.clip_grad_norm_(
                model.parameters(),
                max_norm=1.0
            )

            # ------------------------------------------------
            # Optimizer
            # ------------------------------------------------

            optimizer.step()

            # ------------------------------------------------
            # Metrics
            # ------------------------------------------------

            running_loss += (
                loss.item()
                * labels.size(0)
            )

            predictions = torch.argmax(
                outputs,
                dim=1
            )

            correct += (
                predictions == labels
            ).sum().item()

            total += labels.size(0)

        # ----------------------------------------------------
        # Training metrics
        # ----------------------------------------------------

        train_loss = (
            running_loss / total
            if total > 0
            else 0.0
        )

        train_accuracy = (
            correct / total
            if total > 0
            else 0.0
        )

        # ----------------------------------------------------
        # Validation
        # ----------------------------------------------------

        (
            validation_loss,
            validation_accuracy
        ) = evaluate(
            model,
            validation_loader,
            criterion,
            device
        )

        # ----------------------------------------------------
        # History
        # ----------------------------------------------------

        history[
            "train_loss"
        ].append(
            train_loss
        )

        history[
            "train_accuracy"
        ].append(
            train_accuracy
        )

        history[
            "validation_loss"
        ].append(
            validation_loss
        )

        history[
            "validation_accuracy"
        ].append(
            validation_accuracy
        )

        # ----------------------------------------------------
        # Print
        # ----------------------------------------------------

        print(
            f"Epoch {epoch + 1:02d}/"
            f"{config.EPOCHS:02d} | "
            f"Train Loss: {train_loss:.4f} | "
            f"Train Acc: "
            f"{train_accuracy * 100:.2f}% | "
            f"Val Loss: "
            f"{validation_loss:.4f} | "
            f"Val Acc: "
            f"{validation_accuracy * 100:.2f}%"
        )

        # ----------------------------------------------------
        # Best model selection
        #
        # Primary metric:
        # validation accuracy
        #
        # Tie-breaker:
        # validation loss
        # ----------------------------------------------------

        is_better = (

            validation_accuracy
            > best_validation_accuracy

            or (

                validation_accuracy
                == best_validation_accuracy

                and validation_loss
                < best_validation_loss
            )
        )

        if is_better:

            best_validation_accuracy = (
                validation_accuracy
            )

            best_validation_loss = (
                validation_loss
            )

            best_epoch = (
                epoch + 1
            )

            checkpoint = {

                "model_state_dict":
                    model.state_dict(),

                "vocab_size":
                    len(tokenizer),

                "num_classes":
                    len(INTENTS),

                "num_intents":
                    len(INTENTS),

                "embedding_dim":
                    config.EMBEDDING_DIM,

                "hidden_dim":
                    config.HIDDEN_DIM,

                "num_hidden_layers":
                    config.NUM_HIDDEN_LAYERS,

                "hidden_layers":
                    config.NUM_HIDDEN_LAYERS,

                "dropout":
                    config.DROPOUT,

                "max_length":
                    config.MAX_LENGTH,

                "intent_to_id":
                    INTENT_TO_LABEL,

                "intent_to_label":
                    INTENT_TO_LABEL,

                "class_weights":
                    (
                        class_weights.detach()
                        .cpu()
                        .tolist()
                        if class_weights is not None
                        else None
                    ),

                "weight_decay":
                    weight_decay,

                "best_validation_accuracy":
                    best_validation_accuracy,

                "best_validation_loss":
                    best_validation_loss,

                "best_epoch":
                    best_epoch
            }

            torch.save(
                checkpoint,
                config.MODEL_FILE
            )

    # --------------------------------------------------------
    # Save history
    # --------------------------------------------------------

    save_history(
        history
    )

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print()
    print("=" * 60)
    print(
        "TRAINING COMPLETED"
    )
    print("=" * 60)

    print(
        "Best validation accuracy:",
        f"{best_validation_accuracy * 100:.2f}%"
    )

    print(
        "Best validation loss:",
        f"{best_validation_loss:.4f}"
    )

    print(
        "Best epoch:",
        best_epoch
    )

    print()
    print(
        "Best model saved to:",
        config.MODEL_FILE
    )

    print(
        "Training history saved to:",
        config.HISTORY_FILE
    )

    print(
        "Training configuration saved to:",
        config.CONFIG_FILE
    )


if __name__ == "__main__":

    main()