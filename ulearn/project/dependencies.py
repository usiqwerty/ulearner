from file_manager.explorer import list_all_files, get_code_file
from sharp_parser.oop.classes import CSharpClass
from sharp_parser.oop.namespace import CSharpNamespace
from sharp_parser.sharp_parser import get_code_dependencies


def resolve_all_dependencies(initial_source: str, project_name: str) -> list[CSharpClass]:
    dependencies = []
    namespace = CSharpNamespace()

    # Первая итерация, чтобы найти все внешние зависимости
    get_code_dependencies(initial_source, namespace)

    # Вторая итерация, чтобы найти все классы в проекте.
    # Третья итерация, чтобы разрешить все зависимости
    # в остальных файлах проекта
    for i in range(2):
        for filename in list_all_files(project_name):
            aux_source = get_code_file(project_name, filename, "")
            dependencies += get_code_dependencies(aux_source, namespace)

    if namespace.type_resolver.unresolved:
        raise Exception(f"Unresolved dependencies: {namespace.type_resolver.unresolved}")
    return dependencies
