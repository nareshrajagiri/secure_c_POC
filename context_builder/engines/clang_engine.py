from clang import cindex


cindex.Config.set_library_file(
    r"C:\Program Files\LLVM\bin\libclang.dll"
)


class ClangEngine:

    def __init__(self):

        self.index = cindex.Index.create()


    def parse_file(
        self,
        file_path,
        include_paths,
        defines
    ):

        args = []

        for path in include_paths:

            args.append(
                "-I" + path
            )
        args.append(
    r"-IC:\Program Files\LLVM\lib\clang\14.0.6\include")


        for define in defines:

            args.append(
                "-D" + define
            )

        args.extend([
    "-D__GNUC__",
    "-D__ARM_ARCH_7EM__",
    "-D__CORTEX_M=4",
    "-DSTM32F407xx",
    "-DUSE_HAL_DRIVER"
])

        tu = self.index.parse(
    file_path,
    args=args
)

        errors = []

        for diagnostic in tu.diagnostics:

            if diagnostic.severity >= 3:

                errors.append(
                    str(diagnostic)
                )

        if errors:

            '''print(
                f"[CLANG WARNING] {file_path}"
            )'''

            for error in errors:

                print(error)

        '''print(
            f"[CLANG PARSED] {file_path}"
        )'''

        return tu
