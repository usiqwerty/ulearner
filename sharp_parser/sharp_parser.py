from tree_sitter_languages import get_language, get_parser

from sharp_parser.classes import parse_record, parse_class, CSharpClass
from sharp_parser.sharp_types import TypeResolver

language = get_language('c_sharp')
parser = get_parser('c_sharp')


def parse_code_from_string(code: str) -> tuple[CSharpClass, list[str]]:
    """
    Парсит класс из файла
    :param code: Код на C#
    :return: Распаршенный класс и список неизвестных имён классов
    """
    type_resolver = TypeResolver()
    tree = parser.parse(code.encode())

    namespace = None
    for child in tree.root_node.children:
        if child.type == 'file_scoped_namespace_declaration':
            namespace = child
            break
    if not namespace:
        raise Exception("No namespace")

    if not namespace.children:
        raise Exception("Empty namespace")
    ans = None
    for child in namespace.children:
        if child.type == 'class_declaration':
            ans = parse_class(child, type_resolver)
            break
        elif child.type == "record_declaration":
            ans = parse_record(child)
            break
    if not ans:
        raise Exception("No class in file")

    return ans, type_resolver.unresolved
