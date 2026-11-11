"""
Dataset utilities for the Neighbour Management AI.

This module converts the JSON intent datasets into PyTorch
datasets while keeping the tokenizer, intent mapping and
training pipeline consistent.

Expected dataset format:

[
    {
        "text": "Show invalid neighbours in Uttar Pradesh",
        "intent": "GET_INVALID_NEIGHBOURS",
        ...
    }
]

Only "text" and "intent" are required by the model.
Additional fields such as entities and missing information
are preserved in the original JSON but are not required for
classification training.
"""

import json
from pathlib import Path
from typing import Dict, List, Any

import torch
from torch.utils.data import Dataset

from tokenizer.tokenizer import SimpleTokenizer


class IntentDataset(Dataset):
    """
    PyTorch Dataset for intent classification.

    The public constructor intentionally remains compatible
    with the existing train.py:

        IntentDataset(
            dataset_path=...,
            tokenizer=...,
            intent_to_id=...,
            max_length=...
        )
    """

    def __init__(
        self,
        dataset_path,
        tokenizer,
        intent_to_id,
        max_length=32
    ):
        self.dataset_path = Path(dataset_path)
        self.tokenizer = tokenizer
        self.intent_to_id = dict(intent_to_id)
        self.max_length = int(max_length)

        self._validate_constructor_arguments()

        self.data = self._load_dataset()

        self._validate_dataset()

    # ========================================================
    # INITIALIZATION VALIDATION
    # ========================================================

    def _validate_constructor_arguments(self):
        """Validate constructor inputs."""

        if not self.dataset_path.exists():

            raise FileNotFoundError(
                f"Dataset file does not exist: "
                f"{self.dataset_path}"
            )

        if not self.dataset_path.is_file():

            raise ValueError(
                f"Dataset path is not a file: "
                f"{self.dataset_path}"
            )

        if self.tokenizer is None:

            raise ValueError(
                "Tokenizer cannot be None."
            )

        if not hasattr(
            self.tokenizer,
            "encode"
        ):

            raise TypeError(
                "Tokenizer must provide an encode() method."
            )

        if not hasattr(
            self.tokenizer,
            "token_to_id"
        ):

            raise TypeError(
                "Tokenizer must provide token_to_id."
            )

        if not isinstance(
            self.intent_to_id,
            dict
        ):

            raise TypeError(
                "intent_to_id must be a dictionary."
            )

        if not self.intent_to_id:

            raise ValueError(
                "intent_to_id cannot be empty."
            )

        if self.max_length <= 0:

            raise ValueError(
                "max_length must be greater than 0."
            )

        # ----------------------------------------------------
        # Validate tokenizer special token
        # ----------------------------------------------------

        if (
            SimpleTokenizer.PAD_TOKEN
            not in self.tokenizer.token_to_id
        ):

            raise ValueError(
                "Tokenizer does not contain the required "
                f"PAD token: {SimpleTokenizer.PAD_TOKEN}"
            )

        pad_id = self.tokenizer.token_to_id[
            SimpleTokenizer.PAD_TOKEN
        ]

        if not isinstance(pad_id, int):

            raise ValueError(
                "Tokenizer PAD token ID must be an integer."
            )

        if pad_id < 0:

            raise ValueError(
                "Tokenizer PAD token ID cannot be negative."
            )

    # ========================================================
    # DATA LOADING
    # ========================================================

    def _load_dataset(self) -> List[Dict[str, Any]]:
        """Load and parse the JSON dataset."""

        try:

            with open(
                self.dataset_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

        except json.JSONDecodeError as error:

            raise ValueError(
                f"Invalid JSON in dataset "
                f"{self.dataset_path}: {error}"
            ) from error

        except OSError as error:

            raise OSError(
                f"Unable to read dataset "
                f"{self.dataset_path}: {error}"
            ) from error

        if not isinstance(data, list):

            raise ValueError(
                f"Dataset must be a JSON list: "
                f"{self.dataset_path}"
            )

        if not data:

            raise ValueError(
                f"Dataset is empty: "
                f"{self.dataset_path}"
            )

        return data

    # ========================================================
    # DATASET VALIDATION
    # ========================================================

    def _validate_dataset(self):
        """Validate every dataset example."""

        errors = []

        for index, example in enumerate(self.data):

            # ------------------------------------------------
            # Example type
            # ------------------------------------------------

            if not isinstance(example, dict):

                errors.append(
                    f"Example {index} must be an object."
                )

                continue

            # ------------------------------------------------
            # Required text field
            # ------------------------------------------------

            if "text" not in example:

                errors.append(
                    f"Example {index} is missing 'text'."
                )

                continue

            text = example["text"]

            if not isinstance(text, str):

                errors.append(
                    f"Example {index} 'text' must be a string."
                )

            elif not text.strip():

                errors.append(
                    f"Example {index} 'text' cannot be empty."
                )

            # ------------------------------------------------
            # Required intent field
            # ------------------------------------------------

            if "intent" not in example:

                errors.append(
                    f"Example {index} is missing 'intent'."
                )

                continue

            intent = example["intent"]

            if not isinstance(intent, str):

                errors.append(
                    f"Example {index} 'intent' must be a string."
                )

                continue

            if intent not in self.intent_to_id:

                errors.append(
                    f"Example {index} has unknown intent "
                    f"'{intent}'."
                )

                continue

            # ------------------------------------------------
            # Validate numeric label
            # ------------------------------------------------

            label = self.intent_to_id[intent]

            if not isinstance(label, int):

                errors.append(
                    f"Example {index} intent '{intent}' "
                    f"has a non-integer label."
                )

            elif label < 0:

                errors.append(
                    f"Example {index} intent '{intent}' "
                    f"has a negative label."
                )

        if errors:

            preview = "\n".join(
                errors[:20]
            )

            if len(errors) > 20:

                preview += (
                    f"\n... and "
                    f"{len(errors) - 20} more errors."
                )

            raise ValueError(
                "Dataset validation failed:\n"
                f"{preview}"
            )

    # ========================================================
    # TOKEN ENCODING
    # ========================================================

    def _encode_text(self, text: str) -> List[int]:
        """
        Convert text into exactly max_length token IDs.

        Pipeline:

            text
              ↓
            tokenizer
              ↓
            special tokens
              ↓
            truncation
              ↓
            padding
        """

        if not isinstance(text, str):

            raise TypeError(
                "Text must be a string."
            )

        text = text.strip()

        if not text:

            raise ValueError(
                "Text cannot be empty."
            )

        # ----------------------------------------------------
        # Tokenize
        # ----------------------------------------------------

        token_ids = self.tokenizer.encode(
            text,
            add_special_tokens=True
        )

        if not isinstance(
            token_ids,
            list
        ):

            token_ids = list(token_ids)

        # ----------------------------------------------------
        # Validate token IDs
        # ----------------------------------------------------

        for token_id in token_ids:

            if not isinstance(
                token_id,
                int
            ):

                raise ValueError(
                    "Tokenizer returned a non-integer "
                    "token ID."
                )

            if token_id < 0:

                raise ValueError(
                    "Tokenizer returned a negative "
                    "token ID."
                )

        # ----------------------------------------------------
        # Truncate
        # ----------------------------------------------------

        token_ids = token_ids[
            :self.max_length
        ]

        # ----------------------------------------------------
        # Padding
        # ----------------------------------------------------

        pad_id = self.tokenizer.token_to_id[
            SimpleTokenizer.PAD_TOKEN
        ]

        while len(token_ids) < self.max_length:

            token_ids.append(
                pad_id
            )

        # ----------------------------------------------------
        # Final shape guarantee
        # ----------------------------------------------------

        if len(token_ids) != self.max_length:

            raise RuntimeError(
                "Internal dataset error: encoded sequence "
                "does not match max_length."
            )

        return token_ids

    # ========================================================
    # PYTORCH DATASET API
    # ========================================================

    def __len__(self):
        """Return number of examples."""

        return len(self.data)

    def __getitem__(self, index):
        """Return one training example."""

        if index < 0:

            index += len(self.data)

        if index < 0 or index >= len(self.data):

            raise IndexError(
                f"Dataset index out of range: {index}"
            )

        example = self.data[index]

        text = example["text"]

        intent = example["intent"]

        # ----------------------------------------------------
        # Encode text
        # ----------------------------------------------------

        input_ids = self._encode_text(
            text
        )

        # ----------------------------------------------------
        # Convert intent → class ID
        # ----------------------------------------------------

        label = self.intent_to_id[
            intent
        ]

        return {
            "input_ids": torch.tensor(
                input_ids,
                dtype=torch.long
            ),

            "label": torch.tensor(
                label,
                dtype=torch.long
            ),

            # Preserve these because the evaluation and
            # debugging pipeline may use them.

            "text": text,

            "intent": intent
        }

    # ========================================================
    # DATASET INFORMATION
    # ========================================================

    def get_intent_counts(self) -> Dict[str, int]:
        """
        Return the number of examples for every intent.
        """

        counts = {
            intent: 0
            for intent in self.intent_to_id
        }

        for example in self.data:

            intent = example["intent"]

            counts[intent] += 1

        return counts

    def get_label_counts(self) -> Dict[int, int]:
        """
        Return example counts by numeric label.
        """

        counts = {
            label: 0
            for label in self.intent_to_id.values()
        }

        for example in self.data:

            intent = example["intent"]

            label = self.intent_to_id[
                intent
            ]

            counts[label] += 1

        return counts

    def get_class_weights(
        self,
        power: float = 0.5
    ) -> torch.Tensor:
        """
        Calculate mild inverse-frequency class weights.

        Formula:

            weight = (total / class_count) ** power

        The weights are normalized so that the mean weight
        is approximately 1.

        Args:
            power:
                0 gives equal weights.
                0.5 gives mild inverse-frequency weighting.
                1 gives full inverse-frequency weighting.

        Returns:
            Float tensor indexed by numeric intent ID.
        """

        if not 0 <= power <= 1:

            raise ValueError(
                "power must be between 0 and 1."
            )

        label_counts = self.get_label_counts()

        number_of_classes = len(
            label_counts
        )

        total_examples = len(
            self.data
        )

        weights = torch.ones(
            number_of_classes,
            dtype=torch.float32
        )

        for label in range(
            number_of_classes
        ):

            count = label_counts.get(
                label,
                0
            )

            if count <= 0:

                weights[label] = 1.0

            else:

                weights[label] = (
                    total_examples / count
                ) ** power

        # ----------------------------------------------------
        # Normalize mean weight to 1
        # ----------------------------------------------------

        mean_weight = weights.mean()

        if mean_weight > 0:

            weights = (
                weights / mean_weight
            )

        return weights

    # ========================================================
    # DEBUG INFORMATION
    # ========================================================

    def summary(self) -> Dict[str, Any]:
        """
        Return a compact dataset summary.
        """

        return {
            "dataset_path":
                str(self.dataset_path),

            "examples":
                len(self.data),

            "intents":
                len(self.intent_to_id),

            "max_length":
                self.max_length,

            "vocabulary_size":
                len(self.tokenizer),

            "intent_counts":
                self.get_intent_counts()
        }