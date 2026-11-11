import torch
from torch.utils.data import DataLoader

from tokenizer import tokenizer
from tokenizer import tokenizer
from tokenizer.tokenizer import SimpleTokenizer

from model.dataset import IntentDataset

from model.intent_mapping import (
    INTENTS,
    INTENT_TO_ID,
    ID_TO_INTENT
)

from model.intent_model import IntentClassifier

import model.config as config


def main():

    print("=" * 60)
    print("PHASE 5B - COMPLETE PIPELINE TEST")
    print("=" * 60)

    # ========================================================
    # 1. LOAD TOKENIZER
    # ========================================================

    tokenizer = SimpleTokenizer.load(
        config.TOKENIZER_FILE
    )

    print()
    print("Tokenizer")
    print("-" * 60)

    print(
        "Vocabulary size:",
        len(tokenizer)
    )

    print(
        "Maximum vocabulary:",
        tokenizer.vocab_size
    )

    # ========================================================
    # 2. CREATE TRAIN DATASET
    # ========================================================

    train_dataset = IntentDataset(
        dataset_path=config.TRAIN_FILE,
        tokenizer=tokenizer,
        intent_to_id=INTENT_TO_ID,
        max_length=config.MAX_LENGTH
    )

    print()
    print("Training Dataset")
    print("-" * 60)

    print(
        "Examples:",
        len(train_dataset)
    )

    # ========================================================
    # 3. CREATE VALIDATION DATASET
    # ========================================================

    validation_dataset = IntentDataset(
        dataset_path=config.VALIDATION_FILE,
        tokenizer=tokenizer,
        intent_to_id=INTENT_TO_ID,
        max_length=config.MAX_LENGTH
    )

    print()
    print("Validation Dataset")
    print("-" * 60)

    print(
        "Examples:",
        len(validation_dataset)
    )

    # ========================================================
    # 4. CREATE TEST DATASET
    # ========================================================

    test_dataset = IntentDataset(
        dataset_path=config.TEST_FILE,
        tokenizer=tokenizer,
        intent_to_id=INTENT_TO_ID,
        max_length=config.MAX_LENGTH
    )

    print()
    print("Test Dataset")
    print("-" * 60)

    print(
        "Examples:",
        len(test_dataset)
    )

    # ========================================================
    # 5. CREATE DATALOADERS
    # ========================================================

    train_loader = DataLoader(
        train_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=True,
        num_workers=config.NUM_WORKERS
    )

    validation_loader = DataLoader(
        validation_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=False,
        num_workers=config.NUM_WORKERS
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=config.BATCH_SIZE,
        shuffle=False,
        num_workers=config.NUM_WORKERS
    )

    print()
    print("DataLoaders")
    print("-" * 60)

    print(
        "Training batches:",
        len(train_loader)
    )

    print(
        "Validation batches:",
        len(validation_loader)
    )

    print(
        "Test batches:",
        len(test_loader)
    )

    # ========================================================
    # 6. GET ONE TRAINING BATCH
    # ========================================================

    batch = next(
        iter(train_loader)
    )

    input_ids = batch["input_ids"]

    labels = batch["label"]

    print()
    print("Training Batch")
    print("-" * 60)

    print(
        "Input shape:",
        input_ids.shape
    )

    print(
        "Label shape:",
        labels.shape
    )

    # ========================================================
    # 7. CREATE MODEL
    # ========================================================

    model = IntentClassifier(
    vocab_size=len(tokenizer),
    num_intents=config.NUM_INTENTS,
    embedding_dim=config.EMBEDDING_DIM,
    hidden_dim=config.HIDDEN_DIM,
    hidden_layers=config.NUM_HIDDEN_LAYERS,
    dropout=config.DROPOUT,
 )

    print()
    print("Model")
    print("-" * 60)

    print(
        "Vocabulary:",
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

    # ========================================================
    # 8. FORWARD PASS
    # ========================================================

    model.eval()

    with torch.no_grad():

        output = model(
            input_ids
        )

    print()
    print("Forward Pass")
    print("-" * 60)

    print(
        "Input:",
        input_ids.shape
    )

    print(
        "Output:",
        output.shape
    )

    # ========================================================
    # 9. VERIFY OUTPUT
    # ========================================================

    expected_shape = (
        input_ids.shape[0],
        len(INTENTS)
    )

    assert output.shape == expected_shape

    assert labels.shape[0] == input_ids.shape[0]

    assert len(INTENT_TO_ID) == len(INTENTS)

    assert len(ID_TO_INTENT) == len(INTENTS)

    # ========================================================
    # 10. SHOW SAMPLE PREDICTION
    # ========================================================

    predicted_id = torch.argmax(
        output[0]
    ).item()

    predicted_intent = ID_TO_INTENT[
        predicted_id
    ]

    print()
    print("Sample")
    print("-" * 60)

    print(
        "Text:",
        batch["text"][0]
    )

    print(
        "Actual intent:",
        batch["intent"][0]
    )

    print(
        "Actual ID:",
        labels[0].item()
    )

    print(
        "Initial model prediction:",
        predicted_intent
    )

    # ========================================================
    # COMPLETE
    # ========================================================

    print()
    print("=" * 60)
    print("PHASE 5B PIPELINE TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()