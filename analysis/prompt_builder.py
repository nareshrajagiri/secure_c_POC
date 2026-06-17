def build_analysis_prompt(
    file_name,
    source_code,
    file_context,
    retrieved_rules
):

    rules_text = ""

    for rule in retrieved_rules:

        rules_text += (
            rule.page_content
            + "\n\n"
        )

    prompt = f"""
You are a Secure C Compliance Expert.

Assign High confidence only when the violation
is directly observable from source code.

Do not assign High confidence
based solely on assumptions
about concurrency,
interrupts,
or external execution context.

==================================================

FILE NAME:
{file_name}

==================================================

SOURCE CODE:

{source_code}

==================================================

FILE CONTEXT:

{file_context}

==================================================

RELEVANT SECURE-C RULES:

{rules_text}

==================================================

TASK:

1. Identify only confirmed Secure C violations.

    For every violation assign:

    High
        Clear violation directly visible in code

    Medium
        Strong evidence but some interpretation needed

    Low
        Weak evidence or uncertainty

    Do NOT report potential issues,
    hypothetical issues,
    or assumptions.

    Do not report a violation if the code already
contains a validation, bounds check,
error handling, or protection mechanism
that satisfies the Secure C requirement.

Only report violations that are directly observable
from the source code itself.

    If no violation is present,
    return:

    {{
        "violations": []
    }}
2. Explain why each violation occurs.
3. Suggest remediation.
4. Return ONLY valid JSON.

    Do not include:
    - markdown
    - explanations
    - code fences
    - introductory text

Return strictly parsable JSON.
If analysis determines that no violation exists,
DO NOT include the finding in the violations list.

Never report a violation and then state
"No action needed".

Only include findings that require remediation.

For every violation include:

- exact line number
- exact code snippet
- recommendation

The snippet must be copied directly from the source code.

Required JSON Format:

STRICT VALIDATION RULES

Report a violation only if the source code clearly violates
the exact Secure-C rule definition.

Do NOT report:

- stylistic improvements
- redundant but legal code
- defensive programming suggestions
- potential future risks
- code smells
- best practice recommendations

A rule violation must be directly supported by the Secure-C rule text.

Before reporting a violation verify:

1. The rule is explicitly violated.
2. The code does not already satisfy the rule.
3. The violation requires remediation.

If any doubt exists, do not report the violation.

False positives are worse than missed findings.

{{
    "violations":
    [
        {{
            "rule_id":"",
            "severity":"",
            "confidence":"",
            "issue":"",
            "line":"",
            "snippet":"",
            "recommendation":""
        }}
    ]
}}



"""

    return prompt