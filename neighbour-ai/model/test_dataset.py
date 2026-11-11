from torch.utils.data import DataLoader

from tokenizer.tokenizer import SimpleTokenizer

from model.dataset import IntentDataset

from model.intent_mapping import (
    INTENT_TO_ID,
    ID_TO_INTENT
)


TOKENIZER_FILE = "model/tokenizer.json"
TRAIN_FILE = "dataset/train.json"


def main():

    # ----------------------------------------------------
    # Load tokenizer
    # ----------------------------------------------------

    tokenizer = SimpleTokenizer.load(
        TOKENIZER_FILE
    )

    print(
        "Tokenizer vocabulary:",
        len(tokenizer)
    )

    # ----------------------------------------------------
    # Create dataset
    # ----------------------------------------------------

    dataset = IntentDataset(
        dataset_path=TRAIN_FILE,
        tokenizer=tokenizer,
        intent_to_id=INTENT_TO_ID,
        max_length=32
    )

    print(
        "Dataset size:",
        len(dataset)
    )

    # ----------------------------------------------------
    # Read first example
    # ----------------------------------------------------

    example = dataset[0]

    print()
    print("First example:")
    print(
        "Text:",
        example["text"]
    )

    print(
        "Intent:",
        example["intent"]
    )

    print(
        "Label:",
        example["label"].item()
    )

    print(
        "Input IDs:",
        example["input_ids"]
    )

    print(
        "Input shape:",
        example["input_ids"].shape
    )

    # ----------------------------------------------------
    # Create DataLoader
    # ----------------------------------------------------

    loader = DataLoader(
        dataset,
        batch_size=8,
        shuffle=True
    )

    batch = next(
        iter(loader)
    )

    print()
    print("Batch:")
    print(
        "Input IDs shape:",
        batch["input_ids"].shape
    )

    print(
        "Labels shape:",
        batch["label"].shape
    )

    print()
    print(
        "Dataset + DataLoader test PASSED."
    )


if __name__ == "__main__":
    main()