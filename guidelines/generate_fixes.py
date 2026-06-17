import json
import os
import time
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Load rules
with open("secure_c_rules_clean.json", "r", encoding="utf-8") as f:
    rules = json.load(f)

results = []

total_rules = len(rules)

print(f"Total Rules to Process: {total_rules}")
print("-" * 50)

for index, rule in enumerate(rules, start=1):

    rule_id = rule["rule_id"]
    description = rule["description"]

    print(f"[{index}/{total_rules}] Processing {rule_id}")

    prompt = f"""
You are an expert in CERT-C Secure Coding Standards.

For the given CERT-C rule:

Rule ID: {rule_id}

Description:
{description}

Tasks:
1. Improve or complete the rule description if it appears truncated.
2. Generate a short practical remediation fix.
3. Keep the fix concise and suitable for embedded C and STM32 projects.

Return ONLY raw JSON.

Do NOT use markdown.
Do NOT use ```json.
Do NOT use code fences.
Do NOT include explanations.

Format:

{{
    "rule_id": "{rule_id}",
    "category": "{rule_id[:3]}",
    "description": "<improved description>",
    "fix": "<short practical remediation>"
}}
"""

    try:

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        output = response.output_text.strip()

        # Remove markdown fences if present
        output = output.replace("```json", "")
        output = output.replace("```", "")
        output = output.strip()

        result = json.loads(output)

        required_keys = {
            "rule_id",
            "category",
            "description",
            "fix"
        }

        if not required_keys.issubset(result.keys()):
            raise ValueError(
                f"Missing required fields for {rule_id}"
            )

        results.append(result)

        print(f"SUCCESS: {rule_id}")

        # Prevent rate limit issues
        time.sleep(1)

    except Exception as e:

        print(f"FAILED: {rule_id}")
        print(f"ERROR : {e}")

        # Save partial progress
        with open(
            "secure_c_rules_partial.json",
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(results, f, indent=4)

        continue

# Save final output
with open(
    "secure_c_rules_final.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(results, f, indent=4)

print("\n" + "=" * 50)
print(f"Generated {len(results)} rules")
print("Output File: secure_c_rules_final.json")
print("=" * 50)