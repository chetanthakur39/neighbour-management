import json

import torch
import torch.nn as nn

from torch.utils.data import DataLoader

from tokenizer.tokenizer import SimpleTokenizer

from model.dataset import IntentDataset

from model.intent_mapping import (
    INTENTS,
    INTENT_TO_LABEL,
    LABEL_TO_INTENT,
)

from model.intent_model import IntentClassifier

import model.config as config


# ============================================================
# INTENT HELPERS
# ============================================================

def get_intent_name(label):
    """
    Convert numeric intent ID to intent name.

    Uses the project's single source of truth:
        LABEL_TO_INTENT
    """

    return LABEL_TO_INTENT.get(
        int(label),
        "UNKNOWN"
    )


# ============================================================
# LOAD MODEL
# ============================================================

def load_model(
    tokenizer,
    device
):
    """
    Load the trained IntentClassifier.

    The model architecture must exactly match the architecture
    used during training.
    """

    checkpoint = torch.load(
        config.MODEL_FILE,
        map_location=device
    )

    # --------------------------------------------------------
    # Checkpoint configuration
    # --------------------------------------------------------

    vocab_size = checkpoint.get(
        "vocab_size",
        len(tokenizer)
    )

    num_intents = checkpoint.get(
        "num_intents",
        checkpoint.get(
            "num_classes",
            len(INTENTS)
        )
    )

    hidden_layers = checkpoint.get(
        "hidden_layers",
        checkpoint.get(
            "num_hidden_layers",
            config.NUM_HIDDEN_LAYERS
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

    dropout = checkpoint.get(
        "dropout",
        config.DROPOUT
    )

    # --------------------------------------------------------
    # Validate configuration
    # --------------------------------------------------------

    if num_intents != len(INTENTS):

        raise ValueError(
            "Checkpoint intent count does not match "
            "current intent mapping. "
            f"Checkpoint={num_intents}, "
            f"Current={len(INTENTS)}"
        )

    if vocab_size != len(tokenizer):

        raise ValueError(
            "Checkpoint vocabulary size does not match "
            "current tokenizer. "
            f"Checkpoint={vocab_size}, "
            f"Tokenizer={len(tokenizer)}"
        )

    if vocab_size <= 0:

        raise ValueError(
            "Invalid checkpoint vocabulary size."
        )

    if num_intents <= 0:

        raise ValueError(
            "Invalid checkpoint intent count."
        )

    # --------------------------------------------------------
    # Create model
    # --------------------------------------------------------

    model = IntentClassifier(
        vocab_size=vocab_size,
        num_intents=num_intents,
        embedding_dim=embedding_dim,
        hidden_dim=hidden_dim,
        hidden_layers=hidden_layers,
        dropout=dropout
    )

    # --------------------------------------------------------
    # Load weights
    # --------------------------------------------------------

    if "model_state_dict" not in checkpoint:

        raise KeyError(
            "Checkpoint does not contain "
            "'model_state_dict'."
        )

    model.load_state_dict(
        checkpoint["model_state_dict"],
        strict=True
    )

    model.to(device)

    model.eval()

    return model


# ============================================================
# EVALUATE MODEL
# ============================================================

def evaluate_model(
    model,
    data_loader,
    criterion,
    device
):
    """
    Evaluate the model on a dataset.
    """

    model.eval()

    total_loss = 0.0
    correct = 0
    total = 0

    results = []

    with torch.no_grad():

        for batch in data_loader:

            input_ids = batch[
                "input_ids"
            ].to(device)

            labels = batch[
                "label"
            ].to(device)

            # ------------------------------------------------
            # Forward pass
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
            # Probabilities
            # ------------------------------------------------

            probabilities = torch.softmax(
                outputs,
                dim=1
            )

            confidence, predictions = torch.max(
                probabilities,
                dim=1
            )

            # ------------------------------------------------
            # Statistics
            # ------------------------------------------------

            batch_size = labels.size(0)

            total_loss += (
                loss.item()
                * batch_size
            )

            correct += (
                predictions == labels
            ).sum().item()

            total += batch_size

            # ------------------------------------------------
            # Individual predictions
            # ------------------------------------------------

            for i in range(batch_size):

                actual_id = int(
                    labels[i].item()
                )

                predicted_id = int(
                    predictions[i].item()
                )

                actual_intent = get_intent_name(
                    actual_id
                )

                predicted_intent = get_intent_name(
                    predicted_id
                )

                results.append(
                    {
                        "text": batch["text"][i],

                        "actual":
                            actual_intent,

                        "predicted":
                            predicted_intent,

                        "actual_id":
                            actual_id,

                        "predicted_id":
                            predicted_id,

                        "confidence":
                            float(
                                confidence[i].item()
                            ),

                        "correct":
                            actual_id == predicted_id
                    }
                )

    # --------------------------------------------------------
    # Final metrics
    # --------------------------------------------------------

    if total == 0:

        average_loss = 0.0
        accuracy = 0.0

    else:

        average_loss = (
            total_loss / total
        )

        accuracy = (
            correct / total
        )

    return (
        average_loss,
        accuracy,
        correct,
        total,
        results
    )


# ============================================================
# CONFUSION SUMMARY
# ============================================================

def print_confusion_summary(
    results
):

    confusion = {}

    for result in results:

        actual = result["actual"]
        predicted = result["predicted"]

        if actual == predicted:
            continue

        key = (
            actual,
            predicted
        )

        confusion[key] = (
            confusion.get(
                key,
                0
            ) + 1
        )

    print()
    print("=" * 60)
    print("CONFUSION SUMMARY")
    print("=" * 60)

    if not confusion:

        print()
        print(
            "No incorrect predictions."
        )

        return

    sorted_confusion = sorted(
        confusion.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for (
        actual,
        predicted
    ), count in sorted_confusion:

        print(
            f"{actual} -> {predicted}: {count}"
        )


# ============================================================
# PER-INTENT ACCURACY
# ============================================================

def print_intent_accuracy(
    results
):

    statistics = {}

    for intent in INTENTS:

        statistics[intent] = {
            "correct": 0,
            "total": 0
        }

    for result in results:

        actual = result["actual"]

        if actual not in statistics:
            continue

        statistics[
            actual
        ]["total"] += 1

        if result["correct"]:

            statistics[
                actual
            ]["correct"] += 1

    print()
    print("=" * 60)
    print("PER-INTENT TEST ACCURACY")
    print("=" * 60)

    for intent in INTENTS:

        correct = statistics[
            intent
        ]["correct"]

        total = statistics[
            intent
        ]["total"]

        accuracy = (
            (correct / total) * 100
            if total > 0
            else 0.0
        )

        print(
            f"{intent:30s} "
            f"{correct:2d}/{total:2d} "
            f"({accuracy:6.2f}%)"
        )


# ============================================================
# INCORRECT PREDICTIONS
# ============================================================

def print_incorrect_predictions(
    results
):

    incorrect = [
        result
        for result in results
        if not result["correct"]
    ]

    print()
    print("=" * 60)
    print("INCORRECT TEST PREDICTIONS")
    print("=" * 60)

    if not incorrect:

        print()
        print(
            "No incorrect predictions."
        )

        return

    for index, result in enumerate(
        incorrect,
        start=1
    ):

        print()
        print(
            f"{index}. {result['text']}"
        )

        print(
            "   Actual:    ",
            result["actual"]
        )

        print(
            "   Predicted: ",
            result["predicted"]
        )

        print(
            "   Confidence:",
            f"{result['confidence'] * 100:.2f}%"
        )


# ============================================================
# LOW CONFIDENCE PREDICTIONS
# ============================================================

def print_low_confidence(
    results,
    threshold=0.70
):

    low_confidence = [
        result
        for result in results
        if result["confidence"] < threshold
    ]

    print()
    print("=" * 60)
    print(
        f"LOW CONFIDENCE PREDICTIONS "
        f"(< {threshold * 100:.0f}%)"
    )
    print("=" * 60)

    if not low_confidence:

        print()
        print(
            "No low-confidence predictions."
        )

        return

    for index, result in enumerate(
        low_confidence,
        start=1
    ):

        status = (
            "CORRECT"
            if result["correct"]
            else "WRONG"
        )

        print()
        print(
            f"{index}. "
            f"[{status}] "
            f"{result['text']}"
        )

        print(
            "   Actual:    ",
            result["actual"]
        )

        print(
            "   Predicted: ",
            result["predicted"]
        )

        print(
            "   Confidence:",
            f"{result['confidence'] * 100:.2f}%"
        )


# ============================================================
# MODEL INFORMATION
# ============================================================

def print_model_information(
    tokenizer
):

    checkpoint = torch.load(
        config.MODEL_FILE,
        map_location="cpu"
    )

    checkpoint_num_intents = checkpoint.get(
        "num_intents",
        checkpoint.get(
            "num_classes",
            len(INTENTS)
        )
    )

    checkpoint_hidden_layers = checkpoint.get(
        "hidden_layers",
        checkpoint.get(
            "num_hidden_layers",
            config.NUM_HIDDEN_LAYERS
        )
    )

    print()
    print("=" * 60)
    print("MODEL INFORMATION")
    print("=" * 60)

    print()
    print(
        "Vocabulary:",
        len(tokenizer)
    )

    print(
        "Intent classes:",
        checkpoint_num_intents
    )

    print(
        "Expected intent classes:",
        len(INTENTS)
    )

    print(
        "Embedding dimension:",
        checkpoint.get(
            "embedding_dim",
            config.EMBEDDING_DIM
        )
    )

    print(
        "Hidden dimension:",
        checkpoint.get(
            "hidden_dim",
            config.HIDDEN_DIM
        )
    )

    print(
        "Hidden layers:",
        checkpoint_hidden_layers
    )

    print(
        "Dropout:",
        checkpoint.get(
            "dropout",
            config.DROPOUT
        )
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("PHASE 5D - TEST EVALUATION")
    print("=" * 60)

    # --------------------------------------------------------
    # Device
    # --------------------------------------------------------

    device = (
        torch.device("cuda")
        if torch.cuda.is_available()
        else torch.device("cpu")
    )

    print()
    print(
        "Device:",
        device
    )

    # --------------------------------------------------------
    # Load tokenizer
    # --------------------------------------------------------

    tokenizer = SimpleTokenizer.load(
        config.TOKENIZER_FILE
    )

    print(
        "Vocabulary size:",
        len(tokenizer)
    )

    # --------------------------------------------------------
    # Load test dataset
    # --------------------------------------------------------

    test_dataset = IntentDataset(
        dataset_path=config.TEST_FILE,
        tokenizer=tokenizer,
        intent_to_id=INTENT_TO_LABEL,
        max_length=config.MAX_LENGTH
    )

    print(
        "Test examples:",
        len(test_dataset)
    )

    # --------------------------------------------------------
    # DataLoader
    # --------------------------------------------------------

    test_loader = DataLoader(
        test_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=False,
        num_workers=config.NUM_WORKERS
    )

    # --------------------------------------------------------
    # Load trained model
    # --------------------------------------------------------

    model = load_model(
        tokenizer,
        device
    )

    print()
    print(
        "Trained model loaded successfully."
    )

    # --------------------------------------------------------
    # Model information
    # --------------------------------------------------------

    print_model_information(
        tokenizer
    )

    # --------------------------------------------------------
    # Loss
    # --------------------------------------------------------

    criterion = nn.CrossEntropyLoss()

    # --------------------------------------------------------
    # Evaluate
    # --------------------------------------------------------

    (
        test_loss,
        test_accuracy,
        correct,
        total,
        results
    ) = evaluate_model(
        model,
        test_loader,
        criterion,
        device
    )

    # --------------------------------------------------------
    # Overall results
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("TEST RESULTS")
    print("=" * 60)

    print()
    print(
        "Test Loss:",
        f"{test_loss:.4f}"
    )

    print(
        "Correct:",
        correct
    )

    print(
        "Incorrect:",
        total - correct
    )

    print(
        "Total:",
        total
    )

    print(
        "Test Accuracy:",
        f"{test_accuracy * 100:.2f}%"
    )

    # --------------------------------------------------------
    # Detailed analysis
    # --------------------------------------------------------

    print_intent_accuracy(
        results
    )

    print_confusion_summary(
        results
    )

    print_incorrect_predictions(
        results
    )

    print_low_confidence(
        results
    )

    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    output_file = (
        config.MODEL_DIR
        / "test_results.json"
    )

    output_data = {

        "phase":
            "5D",

        "model_file":
            str(config.MODEL_FILE),

        "tokenizer_file":
            str(config.TOKENIZER_FILE),

        "vocabulary_size":
            len(tokenizer),

        "num_intents":
            len(INTENTS),

        "test_loss":
            test_loss,

        "test_accuracy":
            test_accuracy,

        "correct":
            correct,

        "incorrect":
            total - correct,

        "total":
            total,

        "results":
            results
    }

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print()
    print(
        "Detailed results saved to:",
        output_file
    )

    print()
    print("=" * 60)
    print(
        "PHASE 5D EVALUATION COMPLETED"
    )
    print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()