from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

response = client.responses.create(
    model="gpt-4.1-mini",
    input="""
Rule ID: STR31-C

Description:
Guarantee that storage for strings has sufficient space for character

Generate:
1. Correct full description
2. One concise remediation fix

Return JSON only.
"""
)

print(response.output_text)