from pathlib import Path
import json
import re
import shutil

from .rule_retriever import retrieve_rules
from .prompt_builder import build_analysis_prompt
from .llm_client import analyze_code


def get_source_files(project_path):

    src_path = Path(project_path) / "Core" / "Src"
    inc_path = Path(project_path) / "Core" / "Inc"

    source_files = []

    for file in src_path.glob("*.c"):
        source_files.append(str(file))

    for file in inc_path.glob("*.h"):
        source_files.append(str(file))

    return source_files



def read_source_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()
    
def get_analysis_files(context_path):

    with open(context_path, "r") as f:
        context = json.load(f)

    ownership = context["symbol_ownership"]["functions"]

    files = set()

    for _, file_name in ownership.items():
        files.add(file_name)

    return sorted(list(files))

def get_application_file_paths(
    project_path,
    context_path
):

    source_files = get_source_files(
        project_path
    )

    application_files = []

    allowed_files = {
        "command_handler.c",
        "main.c",
        "motor_controller.c",
        "position_sensing.c",
        "status_indicator.c",

        "command_handler.h",
        "main.h",
        "motor_controller.h",
        "position_sensing.h",
        "status_indicator.h"
    }

    for source_file in source_files:

        filename = Path(
            source_file
        ).name

        if filename in allowed_files:

            application_files.append(
                source_file
            )

    return application_files

def get_header_context(file_path):

    code = read_source_file(
        file_path
    )

    context = {
        "file_type": "header",
        "declared_functions": [],
        "includes": []
    }

    include_pattern = (
        r'#include\s+[<"]([^">]+)[">]'
    )

    function_pattern = (
        r'([A-Za-z_][A-Za-z0-9_\s\*]+)\s+'
        r'([A-Za-z_][A-Za-z0-9_]*)\s*'
        r'\([^;]*\)\s*;'
    )

    includes = re.findall(
        include_pattern,
        code
    )

    context["includes"] = includes

    functions = re.findall(
        function_pattern,
        code
    )

    for _, func_name in functions:

        context[
            "declared_functions"
        ].append(
            func_name
        )

    return context


def prepare_analysis_inputs(project_path, context_path):

    app_files = get_application_file_paths(
        project_path,
        context_path
    )


    analysis_inputs = []

    for file_path in app_files:

        analysis_inputs.append(
            {
                "file": Path(file_path).name,
                "path": str(file_path),
                "type": Path(file_path).suffix,
                "code": read_source_file(file_path)
            }
        )

    return analysis_inputs

def get_file_context(file_name, context_path):

    with open(context_path, "r", encoding="utf-8") as f:
        context = json.load(f)

    file_context = {
        "owned_functions": [],
        "called_functions": [],
        "peripherals": [],
        "shared_states": [],
        "protected_regions": []
    }

    # ----------------------------------
    # Owned Functions
    # ----------------------------------

    functions = context["symbol_ownership"]["functions"]

    for func_name, owner_file in functions.items():

        if owner_file == file_name:
            file_context["owned_functions"].append(func_name)

    # ----------------------------------
    # Called Functions
    # ----------------------------------

    call_graph = context["call_graph"]

    for owned_func in file_context["owned_functions"]:

        if owned_func in call_graph:

            file_context["called_functions"].extend(
                call_graph[owned_func]
            )

    # remove duplicates

    file_context["called_functions"] = list(
        set(file_context["called_functions"])
    )

    # ----------------------------------
    # Peripheral Ownership
    # ----------------------------------

    peripherals = context["peripheral_ownership"]

    for peripheral_name, peripheral_info in peripherals.items():

        if peripheral_info["owner"] == file_name:

            file_context["peripherals"].append(
                {
                    "name": peripheral_name,
                    "type": peripheral_info["type"]
                }
            )

    # ----------------------------------
    # Shared State Usage
    # ----------------------------------

    shared_state = context["shared_state_map"]

    for state_name, state_info in shared_state.items():

        if (
            state_info["defined_in"] == file_name
            or file_name in state_info["used_by"]
        ):

            file_context["shared_states"].append(
                state_name
            )

    # ----------------------------------
    # Protected Regions
    # ----------------------------------

    protected_regions = context["protected_regions"]

    user_regions = protected_regions.get(
        "user_code_regions",
        {}
    )

    if file_name in user_regions:

        file_context["protected_regions"] = (
            user_regions[file_name]
        )

    return file_context


def run_analysis(
    project_path,
    context_path,
    api_key,
    model_name,
    temperature
):
    
    # ----------------------------------
    # Clean Previous Outputs
    # ----------------------------------

    Path("outputs").mkdir(
        exist_ok=True
    )

    output_dirs = [
        "outputs/file_reports"
    ]
    for directory in output_dirs:
            Path(directory).mkdir(
                parents=True,
                exist_ok=True
            )

    # ----------------------------------
    # Prepare Analysis Inputs
    # ----------------------------------

  

    analysis_inputs = prepare_analysis_inputs(
        project_path,
        context_path
    )

    for f in analysis_inputs:
        print(f["file"])
    
    all_file_reports = []

    # ----------------------------------
    # Analyze Every File
    # ----------------------------------

    for current_file in analysis_inputs:

        print(
            f"\nAnalyzing: "
            f"{current_file['file']}"
        )

        # ------------------------------
        # Context
        # ------------------------------

        if current_file["type"] == ".c":

            file_context = get_file_context(
                current_file["file"],
                context_path
            )

        else:
            file_context = get_header_context(
                current_file["path"]
            )

        
        # ------------------------------
        # Rule Retrieval
        # ------------------------------

        retrieved_rules = retrieve_rules(
            current_file["code"]
        )

        rules_output = []

        for doc in retrieved_rules:

            rules_output.append(
                {
                    "metadata":
                    doc.metadata,

                    "content":
                    doc.page_content
                }
            )


        # ------------------------------
        # Prompt Creation
        # ------------------------------

        prompt = build_analysis_prompt(
            current_file["file"],
            current_file["code"],
            file_context,
            retrieved_rules
        )


        # ------------------------------
        # OpenAI Analysis
        # ------------------------------
        
        analysis_result = analyze_code(
            prompt,
            api_key,
            model_name,
            temperature
        )

        # ------------------------------
        # Convert JSON String
        # ------------------------------

        try:

            parsed_result = json.loads(
                analysis_result
            )

        except Exception:

            parsed_result = {
                "violations": [],
                "error":
                "Invalid JSON returned by LLM"
            }

        # ------------------------------
        # Store File Result
        # ------------------------------

        retrieved_rule_ids = [
            doc.metadata["rule_id"]
            for doc in retrieved_rules
        ]

        file_report = {
            "file":
                current_file["file"],

            "path":
                current_file["path"],

            "retrieved_rules":
                retrieved_rule_ids,

            "context":
                file_context,

            "violations":
                parsed_result.get(
                    "violations",
                    []
                )
        }
        report_name = (
            current_file["file"]
                .replace(".c", "")
                .replace(".h", "_h")
        )

        with open(
            f"outputs/file_reports/{report_name}_analysis.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                file_report,
                f,
                indent=4
            )
        all_file_reports.append(
            file_report
        )

        

    # ----------------------------------
    # Save Final Project Report
    # ----------------------------------
    summary = {
        "files_analyzed": 0,
        "total_violations": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }

    summary["files_analyzed"] = len(
        all_file_reports
    )

    for file_data in all_file_reports:

        violations = file_data["violations"]

        summary["total_violations"] += len(
            violations
        )

        for violation in violations:

            severity = violation.get(
                "severity",
                ""
            ).lower()

            if severity == "high":
                summary["high"] += 1

            elif severity == "medium":
                summary["medium"] += 1

            elif severity == "low":
                summary["low"] += 1

    with open(
        "outputs/analysis_summary.json",
        "w",
        encoding="utf-8"
        ) as f:

            json.dump(
                summary,
                f,
                indent=4
            )

    print(
    "\nProject Analysis Completed Successfully\n"
)

    print("\nGenerated Files:")

    print("outputs/analysis_summary.json")
    print("outputs/file_reports/")

    return summary
    


if __name__ == "__main__":
    print(
        "Run from pipeline_runner.py"
    )