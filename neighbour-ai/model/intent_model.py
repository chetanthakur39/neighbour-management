import torch
import torch.nn as nn


class IntentClassifier(nn.Module):
    """
    Intent classifier using mean + max token pooling.

    Mean pooling captures the overall meaning of the command,
    while max pooling preserves strong intent/action/entity
    signals such as:

        cleanup
        delete
        remove
        automation
        schedule
        PCI
        TAC
        JC names
        state names

    The public constructor remains compatible with the existing
    training and evaluation pipeline.
    """

    def __init__(
        self,
        vocab_size,
        num_intents,
        embedding_dim=64,
        hidden_dim=128,
        hidden_layers=2,
        dropout=0.2
    ):
        super().__init__()

        self.embedding = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=embedding_dim,
            padding_idx=0
        )

        # Mean + max pooling doubles the input dimension.
        pooled_dim = embedding_dim * 2

        layers = []

        input_dim = pooled_dim

        for _ in range(hidden_layers):

            layers.append(
                nn.Linear(
                    input_dim,
                    hidden_dim
                )
            )

            layers.append(
                nn.LayerNorm(
                    hidden_dim
                )
            )

            layers.append(
                nn.ReLU()
            )

            layers.append(
                nn.Dropout(
                    dropout
                )
            )

            input_dim = hidden_dim

        self.hidden_layers = nn.Sequential(
            *layers
        )

        self.output = nn.Linear(
            hidden_dim,
            num_intents
        )

    def forward(self, input_ids):

        embeddings = self.embedding(
            input_ids
        )

        # ----------------------------------------------------
        # Padding mask
        # ----------------------------------------------------

        mask = (
            input_ids != 0
        )

        mask_3d = mask.unsqueeze(
            -1
        )

        # ----------------------------------------------------
        # Mean pooling
        # ----------------------------------------------------

        masked_embeddings = (
            embeddings * mask_3d
        )

        token_counts = (
            mask_3d.sum(dim=1)
            .clamp(min=1)
        )

        mean_pool = (
            masked_embeddings.sum(dim=1)
            / token_counts
        )

        # ----------------------------------------------------
        # Max pooling
        # ----------------------------------------------------

        masked_for_max = embeddings.masked_fill(
            ~mask_3d,
            float("-inf")
        )

        max_pool = masked_for_max.max(
            dim=1
        ).values

        # Safety fallback for an input containing only padding.
        max_pool = torch.where(
            torch.isfinite(max_pool),
            max_pool,
            torch.zeros_like(max_pool)
        )

        # ----------------------------------------------------
        # Combine pooling representations
        # ----------------------------------------------------

        pooled = torch.cat(
            [
                mean_pool,
                max_pool
            ],
            dim=1
        )

        # ----------------------------------------------------
        # Hidden layers
        # ----------------------------------------------------

        hidden = self.hidden_layers(
            pooled
        )

        # ----------------------------------------------------
        # Intent logits
        # ----------------------------------------------------

        logits = self.output(
            hidden
        )

        return logits