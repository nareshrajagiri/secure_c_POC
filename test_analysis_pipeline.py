from analysis.analysis_node import run_analysis

summary = run_analysis(
    project_path="HVAC_Project",
    context_path="context.json",
    api_key="",
    model_name="gpt-4.1",
    temperature=0
)

print(summary)