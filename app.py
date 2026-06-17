import streamlit as st
from pipeline_runner import run_pipeline

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
        "Run Complete Pipeline",
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
    Context Builder → Analysis → Remediation
    """
)

# =====================================
# RUN PIPELINE
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

        status = st.empty()

        progress_bar = st.progress(0)

        status.info(
            "Starting Pipeline..."
        )

        try:

            progress_bar.progress(10)

            results = run_pipeline(
                project_path,
                model_name,
                temperature,
                api_key
            )

            st.write("Pipeline Results:")
            st.json(results)

            if "error" in results:

                st.error(
                    results["error"]
                )

                st.code(
                    results["traceback"]
                )

            else:

                progress_bar.progress(100)

                status.success(
                    "Pipeline Completed Successfully"
                )

                # ========================
                # CONTEXT SUMMARY
                # ========================

                st.header(
                    "Context Summary"
                )

                context = results[
                    "context_summary"
                ]

                c1, c2, c3, c4 = st.columns(4)

                c1.metric(
                    "Dependency Files",
                    context[
                        "dependency_files"
                    ]
                )

                c2.metric(
                    "Functions",
                    context[
                        "functions"
                    ]
                )

                c3.metric(
                    "Contracts",
                    context[
                        "contracts"
                    ]
                )

                c4.metric(
                    "Call Graph",
                    context[
                        "call_graph"
                    ]
                )

                # ========================
                # ANALYSIS SUMMARY
                # ========================

                st.header(
                    "Analysis Summary"
                )

                analysis = results[
                    "analysis"
                ]

                a1, a2, a3, a4, a5 = st.columns(5)

                a1.metric(
                    "Files",
                    analysis[
                        "files_analyzed"
                    ]
                )

                a2.metric(
                    "Violations",
                    analysis[
                        "total_violations"
                    ]
                )

                a3.metric(
                    "High",
                    analysis["high"]
                )

                a4.metric(
                    "Medium",
                    analysis["medium"]
                )

                a5.metric(
                    "Low",
                    analysis["low"]
                )

                # ========================
                # REMEDIATION SUMMARY
                # ========================

                st.header(
                    "Remediation Summary"
                )

                remediation = results[
                    "remediation"
                ]

                r1, r2, r3 = st.columns(3)

                r1.metric(
                    "Reports Found",
                    remediation[
                        "reports_found"
                    ]
                )

                r2.metric(
                    "Files Remediated",
                    remediation[
                        "files_remediated"
                    ]
                )

                r3.metric(
                    "Files Skipped",
                    remediation[
                        "files_skipped"
                    ]
                )

        except Exception as e:

            st.error(
                str(e)
            )