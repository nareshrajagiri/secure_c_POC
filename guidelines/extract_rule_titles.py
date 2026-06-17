import fitz
import re
import json

pdf = fitz.open("cert_c.pdf")

all_text = ""

for page in pdf:
    all_text += page.get_text()

pattern = r'([A-Z]{3}\d{2}-C)\.\s+([^\n]+)'

matches = re.findall(pattern, all_text)

rules = []

seen = set()

for rule_id, description in matches:

    if rule_id not in seen:
        rules.append({
            "rule_id": rule_id,
            "description": description.strip()
        })

        seen.add(rule_id)

print(f"Found {len(rules)} rules")

with open("secure_c_rules.json", "w", encoding="utf-8") as f:
    json.dump(rules, f, indent=4)

print("JSON generated successfully")