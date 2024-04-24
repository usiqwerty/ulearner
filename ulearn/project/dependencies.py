from file_manager.explorer import list_all_files, get_code_file
from sharp_parser.oop.classes import CSharpClass
from sharp_parser.oop.namespace import CSharpNamespace
from sharp_parser.sharp_parser import parse_code_from_string


def resolve_all_dependencies(initial_source: str, project_name: str) -> list[CSharpClass]:
    dependencies = []
    namespace = CSharpNamespace()

    parse_code_from_string(initial_source, namespace)

    for i in range(2):
        for filename in list_all_files(project_name):
            aux_source = get_code_file(project_name, filename, "")
            dependencies += parse_code_from_string(aux_source, namespace)

    # if namespace.type_resolver.unresolved:
    #     raise Exception(f"Unresolved dependencies: {namespace.type_resolver.unresolved}")
    return dependencies
