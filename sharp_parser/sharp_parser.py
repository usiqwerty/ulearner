from tree_sitter_languages import get_language, get_parser

from sharp_parser.classes import parse_record, parse_class, CSharpClass
from sharp_parser.sharp_types import type_references, unresolved

language = get_language('c_sharp')
parser = get_parser('c_sharp')

type_references[None] = None


def parse_code_from_string(code: str) -> tuple[CSharpClass, list[str]]:
    """
    Парсит класс из файла
    :param code: Код на C#
    :return: Распаршенный класс и список неизвестных имён классов
    """
    tree = parser.parse(code.encode())
    # node = tree.root_node
    namespace = None #tree_sitter.Node()
    for child in tree.root_node.children:
        if child.type == 'file_scoped_namespace_declaration':
            namespace = child
            break
    #print(namespace.id)
    if not namespace:
        return None, None
        raise Exception("No namespace")
    if not namespace.children: raise Exception("Empty namespace")
    class_in_file = None
    ans=None
    for child in namespace.children:
        if child.type =='class_declaration':
            ans = parse_class(child)
            break
        elif child.type == "record_declaration":
            ans = parse_record(child)
            break
    if not ans:
        raise Exception("No class in file")
    return ans, unresolved


