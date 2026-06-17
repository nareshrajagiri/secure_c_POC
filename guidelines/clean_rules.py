import json

with open("secure_c_rules.json", "r", encoding="utf-8") as f:
    rules = json.load(f)

clean_rules = []

for rule in rules:

    rule_id = rule["rule_id"]

    prefix = rule_id[:3]

    valid_prefixes = {
        "PRE",
        "DCL",
        "EXP",
        "INT",
        "FLP",
        "ARR",
        "STR",
        "MEM",
        "FIO",
        "ENV",
        "SIG",
        "ERR",
        "CON",
        "MSC"
    }

    if prefix in valid_prefixes:

        number = rule_id[3:5]

        if int(number) >= 30:
            if rule_id == "FIO35-C":
                continue
            clean_rules.append(rule)

print(f"Original Rules : {len(rules)}")
print(f"Clean Rules    : {len(clean_rules)}")

with open(
    "secure_c_rules_clean.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(clean_rules, f, indent=4)