from clang import cindex

cindex.Config.set_library_file(
    r"C:\Program Files\LLVM\bin\libclang.dll"
)

index = cindex.Index.create()

print("Clang initialized successfully")