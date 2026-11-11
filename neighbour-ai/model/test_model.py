import torch

from model.intent_model import IntentClassifier
from model.intent_mapping import get_num_intents


def main():

    print("=" * 60)
    print("PHASE 5A - MODEL ARCHITECTURE TEST")
    print("=" * 60)

    # --------------------------------------------------------
    # Configuration
    # --------------------------------------------------------

    vocab_size = 1000
    num_intents = get_num_intents()

    embedding_dim = 64
    hidden_dim = 128
    hidden_layers = 2
    dropout = 0.2

    batch_size = 4
    sequence_length = 10

    # --------------------------------------------------------
    # Validate intent configuration
    # --------------------------------------------------------

    if num_intents <= 0:
        raise RuntimeError(
            f"Invalid number of intents: {num_intents}"
        )

    print()
    print("Intent classes:")
    print(num_intents)

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

    print()
    print("Model created successfully.")
    print()

    print(model)

    # --------------------------------------------------------
    # Create dummy input
    # --------------------------------------------------------

    input_ids = torch.randint(
        low=0,
        high=vocab_size,
        size=(
            batch_size,
            sequence_length
        )
    )

    print()
    print("Input shape:")
    print(input_ids.shape)

    # --------------------------------------------------------
    # Forward pass
    # --------------------------------------------------------

    model.eval()

    with torch.no_grad():

        output = model(
            input_ids
        )

    print()
    print("Output shape:")
    print(output.shape)

    # --------------------------------------------------------
    # Validate output
    # --------------------------------------------------------

    expected_shape = (
        batch_size,
        num_intents
    )

    if output.shape != expected_shape:

        raise RuntimeError(
            f"Unexpected output shape. "
            f"Expected {expected_shape}, "
            f"got {output.shape}"
        )

    print()
    print("Forward pass successful.")

    print()
    print(
        "Phase 5A model test PASSED."
    )


if __name__ == "__main__":

    main()