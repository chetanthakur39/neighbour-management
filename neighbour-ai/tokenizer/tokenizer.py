import json
import re
from collections import Counter
from pathlib import Path


class SimpleTokenizer:
    """
    Lightweight tokenizer used by the Neighbour Management AI.

    This class is intentionally kept compatible with the existing
    project API and tokenizer.json format.

    Special token IDs are always:

        <PAD> = 0
        <UNK> = 1
        <BOS> = 2
        <EOS> = 3

    The tokenizer stores:

        token_to_id
        id_to_token

    and supports:

        train()
        encode()
        decode()
        save()
        load()

    The vocabulary is intentionally limited by vocab_size.
    """

    # ========================================================
    # SPECIAL TOKENS
    # ========================================================

    PAD_TOKEN = "<PAD>"
    UNK_TOKEN = "<UNK>"
    BOS_TOKEN = "<BOS>"
    EOS_TOKEN = "<EOS>"

    SPECIAL_TOKENS = (
        PAD_TOKEN,
        UNK_TOKEN,
        BOS_TOKEN,
        EOS_TOKEN,
    )

    # ========================================================
    # TOKENIZATION PATTERN
    # ========================================================

    # Keep the same tokenization behavior used by the existing
    # project so that the existing tokenizer.json remains
    # compatible with the trained model.
    TOKEN_PATTERN = re.compile(
        r"[a-zA-Z]+(?:_[a-zA-Z0-9]+)*|\d+(?:\.\d+)?|[^\w\s]"
    )

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self, vocab_size=2000):

        if not isinstance(vocab_size, int):
            raise TypeError(
                "vocab_size must be an integer."
            )

        if vocab_size < len(self.SPECIAL_TOKENS):
            raise ValueError(
                f"vocab_size must be at least "
                f"{len(self.SPECIAL_TOKENS)}."
            )

        self.vocab_size = vocab_size

        self.token_to_id = {}
        self.id_to_token = {}

        self._initialize_special_tokens()

    # ========================================================
    # SPECIAL TOKENS
    # ========================================================

    def _initialize_special_tokens(self):
        """
        Initialize special tokens in a fixed order.

        This MUST remain stable because the model uses
        <PAD> = 0 as the padding index.
        """

        for token in self.SPECIAL_TOKENS:
            self._add_token(token)

    # ========================================================
    # ADD TOKEN
    # ========================================================

    def _add_token(self, token):
        """
        Add a token if it does not already exist.

        Returns:
            int: token ID
        """

        if token in self.token_to_id:
            return self.token_to_id[token]

        if len(self.token_to_id) >= self.vocab_size:
            return self.token_to_id.get(
                self.UNK_TOKEN,
                1,
            )

        token_id = len(self.token_to_id)

        self.token_to_id[token] = token_id
        self.id_to_token[token_id] = token

        return token_id

    # ========================================================
    # SPLIT TEXT
    # ========================================================

    def _split_text(self, text):
        """
        Convert text into normalized tokens.

        The existing project uses lowercase tokenization,
        therefore this behavior is preserved.
        """

        if text is None:
            return []

        if not isinstance(text, str):
            text = str(text)

        text = text.lower().strip()

        if not text:
            return []

        return self.TOKEN_PATTERN.findall(text)

    # ========================================================
    # TRAIN TOKENIZER
    # ========================================================

    def train(self, texts):
        """
        Build vocabulary from a collection of texts.

        Vocabulary selection is deterministic:
        - higher frequency tokens first;
        - alphabetical order for equal-frequency tokens.

        Existing special tokens are never replaced.
        """

        if texts is None:
            return

        counter = Counter()

        for text in texts:

            if text is None:
                continue

            tokens = self._split_text(text)

            if tokens:
                counter.update(tokens)

        available_slots = (
            self.vocab_size
            - len(self.token_to_id)
        )

        if available_slots <= 0:
            return

        # Deterministic ordering.
        #
        # Counter.most_common() depends on insertion order
        # for ties. Explicit sorting makes tokenizer training
        # reproducible even when dataset ordering changes.
        sorted_tokens = sorted(
            counter.items(),
            key=lambda item: (
                -item[1],
                item[0],
            ),
        )

        for token, _ in sorted_tokens:

            if token in self.token_to_id:
                continue

            if len(self.token_to_id) >= self.vocab_size:
                break

            self._add_token(token)

    # ========================================================
    # ENCODE
    # ========================================================

    def encode(
        self,
        text,
        add_special_tokens=True,
    ):
        """
        Convert text into token IDs.

        Unknown tokens are mapped to <UNK>.

        When add_special_tokens=True:

            <BOS> + tokens + <EOS>

        is returned.
        """

        tokens = self._split_text(text)

        ids = []

        if add_special_tokens:
            ids.append(
                self.token_to_id[
                    self.BOS_TOKEN
                ]
            )

        unk_id = self.token_to_id[
            self.UNK_TOKEN
        ]

        for token in tokens:

            token_id = self.token_to_id.get(
                token,
                unk_id,
            )

            ids.append(token_id)

        if add_special_tokens:
            ids.append(
                self.token_to_id[
                    self.EOS_TOKEN
                ]
            )

        return ids

    # ========================================================
    # DECODE
    # ========================================================

    def decode(self, ids):
        """
        Convert token IDs back to text.

        Special tokens are omitted from the decoded text.
        Unknown IDs become <UNK>.
        """

        if ids is None:
            return ""

        tokens = []

        special_tokens = set(
            self.SPECIAL_TOKENS
        )

        for token_id in ids:

            try:
                token_id = int(token_id)
            except (TypeError, ValueError):
                token = self.UNK_TOKEN
            else:
                token = self.id_to_token.get(
                    token_id,
                    self.UNK_TOKEN,
                )

            if token not in special_tokens:
                tokens.append(token)

        return " ".join(tokens)

    # ========================================================
    # SAVE
    # ========================================================

    def save(self, filepath):
        """
        Save tokenizer in the existing tokenizer.json format.

        Existing project compatibility is preserved:

        {
            "vocab_size": ...,
            "token_to_id": {...}
        }
        """

        filepath = Path(filepath)

        filepath.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = {
            "vocab_size": self.vocab_size,
            "token_to_id": self.token_to_id,
        }

        with open(
            filepath,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

    # ========================================================
    # LOAD
    # ========================================================

    @classmethod
    def load(cls, filepath):
        """
        Load tokenizer from tokenizer.json.

        The method accepts the existing project tokenizer
        format and validates the vocabulary structure before
        returning the tokenizer.
        """

        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(
                f"Tokenizer file not found: {filepath}"
            )

        with open(
            filepath,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError(
                "Invalid tokenizer file format."
            )

        if "vocab_size" not in data:
            raise ValueError(
                "Tokenizer file is missing 'vocab_size'."
            )

        if "token_to_id" not in data:
            raise ValueError(
                "Tokenizer file is missing 'token_to_id'."
            )

        vocab_size = data["vocab_size"]
        token_to_id_data = data["token_to_id"]

        if not isinstance(vocab_size, int):
            raise ValueError(
                "Tokenizer vocab_size must be an integer."
            )

        if not isinstance(token_to_id_data, dict):
            raise ValueError(
                "Tokenizer token_to_id must be a dictionary."
            )

        tokenizer = cls(vocab_size)

        # Restore token -> ID mapping exactly.
        tokenizer.token_to_id = {
            str(token): int(token_id)
            for token, token_id
            in token_to_id_data.items()
        }

        # Rebuild ID -> token mapping.
        tokenizer.id_to_token = {
            int(token_id): token
            for token, token_id
            in tokenizer.token_to_id.items()
        }

        tokenizer._validate_loaded_vocabulary()

        return tokenizer

    # ========================================================
    # VALIDATE LOADED VOCABULARY
    # ========================================================

    def _validate_loaded_vocabulary(self):
        """
        Validate the loaded tokenizer without modifying it.
        """

        if len(self.token_to_id) > self.vocab_size:
            raise ValueError(
                "Tokenizer vocabulary exceeds configured "
                "vocab_size."
            )

        if len(self.token_to_id) != len(
            self.id_to_token
        ):
            raise ValueError(
                "Tokenizer token mappings are inconsistent."
            )

        # Ensure special token IDs remain stable.
        expected_ids = {
            self.PAD_TOKEN: 0,
            self.UNK_TOKEN: 1,
            self.BOS_TOKEN: 2,
            self.EOS_TOKEN: 3,
        }

        for token, expected_id in expected_ids.items():

            actual_id = self.token_to_id.get(token)

            if actual_id != expected_id:
                raise ValueError(
                    f"Invalid special token mapping: "
                    f"{token}={actual_id}; "
                    f"expected {expected_id}."
                )

        # Ensure every token ID points back to the same token.
        for token, token_id in self.token_to_id.items():

            if self.id_to_token.get(token_id) != token:
                raise ValueError(
                    "Tokenizer token mappings are inconsistent "
                    f"for token '{token}'."
                )

    # ========================================================
    # VOCABULARY SIZE
    # ========================================================

    def __len__(self):
        """Return the actual number of vocabulary entries."""

        return len(self.token_to_id)

    # ========================================================
    # REPRESENTATION
    # ========================================================

    def __repr__(self):

        return (
            f"SimpleTokenizer("
            f"vocab_size={self.vocab_size}, "
            f"actual_vocab={len(self)}, "
            f"special_tokens={len(self.SPECIAL_TOKENS)}"
            f")"
        )