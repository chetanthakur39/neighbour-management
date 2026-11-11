import json
from pathlib import Path

from tokenizer.tokenizer import SimpleTokenizer


TRAIN_FILE = Path(
    "dataset/train.json"
)

TOKENIZER_FILE = Path(
    "model/tokenizer.json"
)


def load_training_texts():

    with open(
        TRAIN_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        dataset = json.load(file)

    texts = [
        example["text"]
        for example in dataset
    ]

    return texts


def main():

    print(
        "Loading training dataset..."
    )

    texts = load_training_texts()

    print(
        "Training examples:",
        len(texts)
    )

    # ----------------------------------------------------
    # Create tokenizer
    # ----------------------------------------------------

    tokenizer = SimpleTokenizer(
        vocab_size=2000
    )

    # ----------------------------------------------------
    # Train vocabulary ONLY on train data
    # ----------------------------------------------------

    tokenizer.train(
        texts
    )

    # ----------------------------------------------------
    # Save tokenizer
    # ----------------------------------------------------

    tokenizer.save(
        TOKENIZER_FILE
    )

    print()
    print(
        "Tokenizer trained successfully."
    )

    print(
        "Vocabulary size:",
        len(tokenizer)
    )

    print(
        "Maximum vocabulary:",
        tokenizer.vocab_size
    )

    print(
        "Saved to:",
        TOKENIZER_FILE
    )


if __name__ == "__main__":
    main()