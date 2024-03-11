from ulearn.project.sharp_parser import parse_code_class
from file_manager.explorer import list_all_files, get_code_file


def resolve_all_dependencies(initial_source: str, project_name: str):
    initial_class, unresolved = parse_code_class(initial_source)
    project_files = list_all_files(project_name)

    dependencies=[]
    for file in project_files:
        aux_source = get_code_file(project_name, file, None)
        aux_class, unresolved = parse_code_class(aux_source)
        if aux_class.name in unresolved:
            unresolved.remove(aux_class.name)
            dependencies.append(aux_class)
    return dependencies