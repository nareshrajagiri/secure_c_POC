
def format_rules(rules):

    if not rules:
        return "None"

    return "\n".join(f"- {rule}" for rule in rules)

def format_peripherals(peripherals):

    if not peripherals:
        return "None"

    result = []

    for p in peripherals:

        if isinstance(p, dict):
            result.append(
                f"- {p.get('type', 'UNKNOWN')} : {p.get('name', 'UNKNOWN')}"
            )
        else:
            result.append(f"- {p}")

    return "\n".join(result)

def format_violations(violations):

    if not violations:
        return "No violations found."

    result = []

    for idx, violation in enumerate(violations, start=1):

        result.append(
            f"""
Violation {idx}

Rule ID: {violation.get('rule_id', 'N/A')}
Severity: {violation.get('severity', 'N/A')}
Line: {violation.get('line', 'N/A')}

Issue:
{violation.get('issue', 'N/A')}

Snippet:
{violation.get('snippet', 'N/A')}

Recommendation:
{violation.get('recommendation', 'N/A')}

---------------------------------
"""
        )

    return "\n".join(result)

def format_context(context):

    if not context:
        return "No context available."

    return f"""
FILE CONTEXT

Owned Functions:
{chr(10).join('- ' + f for f in context.get('owned_functions', []))}

Called Functions:
{chr(10).join('- ' + f for f in context.get('called_functions', []))}

Shared States:
{chr(10).join('- ' + s for s in context.get('shared_states', []))}

Peripherals:
{format_peripherals(context.get('peripherals', []))}
"""



def build_remediation_prompt(
    source_code,
    violations,
    context,
    retrieved_rules,
    file_name
):

    formatted_violations = format_violations(violations)

    formatted_context = format_context(context)

    prompt = f"""
You are an Embedded Software Security Expert.

TASK:
Fix only the listed Secure C violations.

OBJECTIVE:

Remediate all listed Secure C violations while preserving
the existing STM32 application behavior.

IMPORTANT REMEDIATION CONSTRAINTS

- Modify only code required to fix listed violations.
- Preserve all STM32 HAL APIs.
- Preserve all USER CODE regions.
- Preserve all function signatures.
- Preserve all global variables.
- Preserve all macros and defines.
- Preserve include statements.
- Preserve all #include statements.
- Preserve all HAL peripheral handles.
- Preserve STM32 CubeMX generated code.
- Preserve existing comments whenever possible.
- Do not introduce placeholder code.
- Do not remove functionality.
- Do not rename functions.
- Do not rename variables.
- Do not change interfaces.
- Ensure resulting code remains compilable.
- Return ONLY the complete corrected source file.
- Do not use markdown.

OUTPUT REQUIREMENTS
- Return ONLY raw C source code.
- Do not include explanations.
- Do not include markdown.
- Do not include code fences.
- Do not include comments describing your changes.
- The first line of your response must be valid C code.


FILE:
{file_name}

SECURE C RULES:
{format_rules(retrieved_rules)}

VIOLATIONS:
{formatted_violations}

CONTEXT:
{formatted_context}

SOURCE CODE START

{source_code}

SOURCE CODE END
"""

    return prompt