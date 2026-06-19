from compiler.compiler_node import run_compiler

report = run_compiler(
    "outputs/build_project/HVAC_Project_Vulnerable"
)

print()
print("Compiler Report")
print(report)