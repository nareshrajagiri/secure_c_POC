import os


def build_file_context(
    current_file,
    project_context
):

    filename = os.path.basename(
        current_file
    )

    dependencies = project_context[
        "dependency_graph"
    ].get(
        filename,
        []
    )

    owned_functions = []

    for func, owner in project_context[
        "symbol_ownership"
    ]["functions"].items():

        if owner == filename:

            owned_functions.append(
                func
            )

    owned_peripherals = []

    for peripheral, info in project_context[
        "peripheral_ownership"
         ].items():

        if (
            info["owner"]
            ==
            filename
        ):

            owned_peripherals.append(
                peripheral
            )
            
    interface_contracts = {}

    for func in owned_functions:

        if func in project_context[
        "interface_contracts"
    ]:

             interface_contracts[func] = (
             project_context[
                "interface_contracts"
             ][func]
         )
        
     
    called_functions = {}

    for func in owned_functions:

        if func in project_context[
        "call_graph"
    ]:

             called_functions[func] = (
             project_context[
                "call_graph"
             ][func]
         )
         
    protected_regions = {

    "user_code_regions":
        project_context[
            "protected_regions"
        ]["user_code_regions"].get(
            filename,
            []
        ),

    "generated_functions":
        project_context[
            "protected_regions"
        ]["generated_functions"].get(
            filename,
            []
        )
}
     
    shared_variables = {}

    for variable, info in project_context[
        "shared_state_map"
        ].items():

        if (
            info["defined_in"]
            ==
            filename
        ):

            shared_variables[
                variable
                ] = info

    return {

    "dependencies":
        dependencies,

    "owned_functions":
        owned_functions,

    "owned_peripherals":
        owned_peripherals,

    "interface_contracts":
        interface_contracts,

    "called_functions":
        called_functions,

    "protected_regions":
        protected_regions,

    "shared_variables":
        shared_variables
}
