import streamlit as st
import json

from pathlib import Path

from context_builder.context_builder import (
    build_context
)

from analysis.analysis_node import (
    run_analysis
)

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Secure C Compliance Analyzer",
    layout="wide"
)

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.header("LLM Settings")

    api_key = st.text_input(
        "OpenAI API Key",
        type="password"
    )
    api_key = api_key.strip()

    model_name = st.selectbox(
        "Model",
        [
            "gpt-4.1-mini",
            "gpt-4.1",
            "gpt-4o"
        ]
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.1
    )

    st.divider()

    st.header("STM32 Project")

    project_path = st.text_input(
        "Project Location"
    )

    run_button = st.button(
        "Run Analysis",
        use_container_width=True
    )

# =====================================
# MAIN PAGE
# =====================================

st.title(
    "Secure C Compliance Analyzer"
)

st.markdown(
    """
    Context Builder → Analysis
    """
)

workflow_status = st.empty()

# =====================================
# RUN
# =====================================

if run_button:

    if not api_key:

        st.error(
            "Please enter OpenAI API Key"
        )

    elif not project_path:

        st.error(
            "Please enter STM32 Project Path"
        )

    else:

        status_messages = []

        def update_status(message):

            status_messages.append(message)

            workflow_status.text(
                "\n".join(status_messages)
            )

        try:

            # =====================================
            # CONTEXT BUILDER
            # =====================================

            update_status(
                "Starting Context Builder..."
            )

            context = build_context(
                project_path,
                status_callback=update_status
            )

            with open(
                "context.json",
                "w"
            ) as f:

                json.dump(
                    context,
                    f,
                    indent=4
                )

            st.success(
                "Context Generated Successfully"
            )

            # =====================================
            # CONTEXT SUMMARY
            # =====================================

            st.header(
                "Context Summary"
            )

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "Dependency Files",
                len(
                    context["dependency_graph"]
                )
            )

            c2.metric(
                "Functions",
                len(
                    context["symbol_ownership"]["functions"]
                )
            )

            c3.metric(
                "Contracts",
                len(
                    context["interface_contracts"]
                )
            )

            c4.metric(
                "Call Graph",
                len(
                    context["call_graph"]
                )
            )

            # =====================================
            # ANALYSIS
            # =====================================

            update_status(
                "Starting Analysis..."
            )

            analysis_summary = run_analysis(
                project_path,
                "context.json",
                api_key,
                model_name,
                temperature,
                status_callback=update_status
            )

            st.success(
                "Analysis Completed Successfully"
            )

            # =====================================
            # ANALYSIS SUMMARY
            # =====================================

            st.header(
                "Analysis Summary"
            )

            a1, a2, a3, a4, a5 = st.columns(5)

            a1.metric(
                "Files",
                analysis_summary[
                    "files_analyzed"
                ]
            )

            a2.metric(
                "Violations",
                analysis_summary[
                    "total_violations"
                ]
            )

            a3.metric(
                "High",
                analysis_summary[
                    "high"
                ]
            )

            a4.metric(
                "Medium",
                analysis_summary[
                    "medium"
                ]
            )

            a5.metric(
                "Low",
                analysis_summary[
                    "low"
                ]
            )

            # =====================================
            # VIOLATION DETAILS
            # =====================================

            st.header(
                "Violation Details"
            )

            report_folder = Path(
                "outputs/file_reports"
            )

            report_files = sorted(
                report_folder.glob("*.json")
            )

            violations_found = False

            for report_file in report_files:

                with open(
                    report_file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    report = json.load(f)

                violations = report.get(
                    "violations",
                    []
                )

                if not violations:
                    continue

                violations_found = True

                with st.expander(
                    f"{report['file']} ({len(violations)} violations)"
                ):

                    for i, violation in enumerate(
                        violations,
                        start=1
                    ):

                        st.markdown(
                            f"### Violation {i}"
                        )

                        st.write(
                            f"**Rule ID:** "
                            f"{violation.get('rule_id','')}"
                        )

                        st.write(
                            f"**Severity:** "
                            f"{violation.get('severity','')}"
                        )

                        st.write(
                            f"**Line:** "
                            f"{violation.get('line','')}"
                        )

                        st.write(
                            f"**Issue:** "
                            f"{violation.get('issue','')}"
                        )

                        st.write(
                            f"**Recommendation:** "
                            f"{violation.get('recommendation','')}"
                        )

                        st.divider()

            if not violations_found:

                st.success(
                    "No violations found."
                )

            # REMEDIATION

            run_remediation_button = st.button(
                "Run Remediation"
            )
            
            

        except Exception as e:

            st.error(
                str(e)
            )

            