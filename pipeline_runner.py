from context_builder.context_builder import (
    build_context
)

from analysis.analysis_node import (
    run_analysis
)

from remediation.remediation_node import (
    run_remediation
)

import json
import traceback


def run_pipeline(
    project_path,
    model_name,
    temperature,
    api_key
):

    try:
       

        # -----------------------
        # Context Builder
        # -----------------------

        context = build_context(
            project_path
        )

        context_path = "context.json"

        with open(
            context_path,
            "w"
        ) as f:

            json.dump(
                context,
                f,
                indent=4
            )

        # -----------------------
        # Analysis
        # -----------------------

        analysis_summary = run_analysis(
            project_path,
            context_path,
            api_key,
            model_name,
            temperature
        )

        # -----------------------
        # Remediation
        # -----------------------

        remediation_summary = (
            run_remediation(
                api_key,
                model_name,
                temperature
            )
        )
        
        return {
            "context_summary": {
                "dependency_files":
                    len(
                        context["dependency_graph"]
                    ),

                "functions":
                    len(
                        context["symbol_ownership"]["functions"]
                    ),

                "contracts":
                    len(
                        context["interface_contracts"]
                    ),

                "call_graph":
                    len(
                        context["call_graph"]
                    )
            },

            "analysis":
                analysis_summary,

            "remediation":
                remediation_summary
        }

    except Exception as e:

        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }