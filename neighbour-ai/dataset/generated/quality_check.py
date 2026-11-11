import json
from collections import Counter


FILES = {
    "TRAIN": "dataset/train.json",
    "VALIDATION": "dataset/validation.json",
    "TEST": "dataset/test.json"
}


def load_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def check_dataset(name, data):

    print(f"\n===== {name} =====")
    print("Total:", len(data))

    intents = Counter(
        item["intent"]
        for item in data
    )

    print("\nIntent distribution:")

    for intent, count in sorted(intents.items()):
        print(f"{intent}: {count}")


def check_empty_text(data):

    errors = []

    for i, item in enumerate(data):

        text = item.get("text", "").strip()

        if not text:
            errors.append(i)

    return errors


def check_missing_fields(data):

    errors = []

    for i, item in enumerate(data):

        if "text" not in item:
            errors.append(
                (i, "missing text")
            )

        if "intent" not in item:
            errors.append(
                (i, "missing intent")
            )

        if "entities" not in item:
            errors.append(
                (i, "missing entities")
            )

    return errors


def main():

    datasets = {}

    for name, path in FILES.items():

        datasets[name] = load_file(path)

        check_dataset(
            name,
            datasets[name]
        )

    print("\n===== STRUCTURE CHECK =====")

    total_errors = 0

    for name, data in datasets.items():

        empty = check_empty_text(data)
        missing = check_missing_fields(data)

        if empty:
            print(
                f"{name}: Empty text entries = {len(empty)}"
            )
            total_errors += len(empty)

        if missing:
            print(
                f"{name}: Missing fields = {len(missing)}"
            )
            total_errors += len(missing)

    if total_errors == 0:
        print("Structure check: PASSED")
    else:
        print(
            "Structure check: FAILED",
            total_errors
        )


if __name__ == "__main__":
    main()