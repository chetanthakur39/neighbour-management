import json
from collections import Counter


FILE = "dataset/generated/generated_dataset.json"


with open(FILE, "r", encoding="utf-8") as file:
    dataset = json.load(file)


intent_counts = Counter(
    example["intent"]
    for example in dataset
)


print("\n===== DATASET SUMMARY =====")
print("Total examples:", len(dataset))

print("\nExamples per intent:")

for intent, count in sorted(intent_counts.items()):
    print(f"{intent}: {count}")


print("\nNumber of intents:", len(intent_counts))
