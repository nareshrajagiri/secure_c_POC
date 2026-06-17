from pipeline_runner import run_pipeline

results = run_pipeline(
    project_path=r"C:\Users\nares\OneDrive\Desktop\Secure_C_POC\HVAC_Project",
    model_name="gpt-4.1-mini",
    temperature=0,
    api_key="YOUR_KEY"
)

print(results)