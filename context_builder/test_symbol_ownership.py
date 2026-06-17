from context_builder.symbol_ownership_clang import (
    build_symbol_ownership_clang
)

include_paths = [

    "workspace/remediated_project/Core/Inc",

    "workspace/remediated_project/Drivers/CMSIS/Device/ST/STM32F4xx/Include",

    "workspace/remediated_project/Drivers/CMSIS/Include",

    "workspace/remediated_project/Drivers/STM32F4xx_HAL_Driver/Inc"
]

defines = [

    "STM32F407xx",

    "USE_HAL_DRIVER",

    "DEBUG"
]

ownership = build_symbol_ownership_clang(
    "workspace/remediated_project",
    include_paths,
    defines
)

from pprint import pprint

pprint(ownership)
