import json


FILE = "dataset/generated/generated_dataset.json"


VALID_STATE_JC = {
    "Andhra Pradesh": ["JC_Vijayawada"],
    "Assam": ["JC_Guwahati"],
    "Bihar": ["JC_Patna"],
    "Chandigarh": ["JC_Chandigarh"],
    "Delhi": ["JC_Central_Delhi"],
    "Goa": ["JC_Panaji"],
    "Gujarat": ["JC_Ahmedabad"],
    "Haryana": ["JC_Gurgaon"],
    "Himachal Pradesh": ["JC_Shimla"],
    "Jammu and Kashmir": ["JC_Srinagar"],
    "Jharkhand": ["JC_Ranchi"],
    "Karnataka": ["JC_Bangalore"],
    "Kerala": ["JC_Kochi"],
    "Madhya Pradesh": ["JC_Bhopal"],
    "Maharashtra": ["JC_Mumbai"],
    "Odisha": ["JC_Bhubaneswar"],
    "Punjab": ["JC_Chandigarh"],
    "Rajasthan": ["JC_Jaipur", "JC_Jaipur_North"],
    "Tamil Nadu": ["JC_Chennai"],
    "Telangana": ["JC_Hyderabad"],
    "Uttar Pradesh": ["JC_Lucknow"],
    "Uttarakhand": ["JC_Dehradun"],
    "West Bengal": ["JC_Kolkata"]
}


with open(FILE, "r", encoding="utf-8") as file:
    dataset = json.load(file)


errors = []


for index, example in enumerate(dataset):

    entities = example["entities"]

    state = entities.get("state")
    jc = entities.get("jc")

    if state and jc:

        valid_jcs = VALID_STATE_JC.get(state, [])

        if jc not in valid_jcs:

            errors.append({
                "index": index,
                "text": example["text"],
                "state": state,
                "jc": jc
            })


print("\n===== ENTITY VALIDATION =====")

if not errors:

    print("All State + JC combinations are valid.")
    print("Errors: 0")

else:

    print("Invalid combinations:", len(errors))

    for error in errors[:20]:
        print(error)