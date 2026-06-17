from remediation.remediation_node import run_remediation
import os

summary = run_remediation(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-4.1",
    temperature=0
)

print(summary)