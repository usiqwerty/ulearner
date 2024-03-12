from file_manager.explorer import list_all_files, get_code_file
from sharp_parser.sharp_parser import parse_code_from_string


def resolve_all_dependencies(initial_source: str, project_name: str):
    initial_class, unresolved = parse_code_from_string(initial_source)
    project_files = list_all_files(project_name)

    dependencies = []
    for file in project_files:
        aux_source = get_code_file(project_name, file, "")
        aux_class, _ = parse_code_from_string(aux_source)

        if not aux_class:
            continue

        if aux_class.name in unresolved:
            unresolved.remove(aux_class.name)
            dependencies.append(aux_class)
    print(dependencies)
    return dependencies
