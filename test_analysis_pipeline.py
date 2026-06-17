from analysis.analysis_node import run_analysis
from dotenv import load_dotenv
import os


summary = run_analysis(
    project_path="HVAC_Project_Vulnerable",
    context_path="context.json",
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-4.1",
    temperature=0
)

print(summary)