from tree_sitter_languages import get_language, get_parser

from sharp_parser.classes import parse_record, parse_class, CSharpClass
from sharp_parser.interfaces import parse_interface
from sharp_parser.sharp_types import TypeResolver

language = get_language('c_sharp')
parser = get_parser('c_sharp')


class NoClassInFile(Exception):
    pass


def parse_code_from_string(code: str, type_resolver: TypeResolver) -> tuple[CSharpClass, list[str]]:
    """
    Парсит класс из файла
    :param code: Код на C#
    :return: Распаршенный класс и список неизвестных имён классов
    """

    tree = parser.parse(code.encode())

    namespace = None
    for child in tree.root_node.children:
        if child.type == 'file_scoped_namespace_declaration':
            namespace = child
            break
        if child.type == 'namespace_declaration':
            raise Exception("Use file-scoped namespaces")
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
            ans = parse_record(child, type_resolver)
            break
        elif child.type == "interface_declaration":
            ans = parse_interface(child, type_resolver)
            break
    if not ans:
        raise NoClassInFile()

    return ans, type_resolver.unresolved
