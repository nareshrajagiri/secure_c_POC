from compiler.log_parser import parse_build_log

result = parse_build_log(
    "compiler/outputs/build.log"
)

print(result)