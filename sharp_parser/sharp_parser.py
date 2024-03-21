from tree_sitter_languages import get_language, get_parser

from sharp_parser.classes import parse_record, parse_class, CSharpClass
from sharp_parser.interfaces import parse_interface
from sharp_parser.namespace import CSharpNamespace

language = get_language('c_sharp')
parser = get_parser('c_sharp')


def parse_code_from_string(code: str, namespace: CSharpNamespace) -> list[CSharpClass]:
    """
    Парсит файл и записывает в namespace
    :param code: Код на C#
    :param namespace: Пространство имён, в котором идёт парсинг
    :return: Зависимости кода
    """

    tree = parser.parse(code.encode())
    namespace_piece = None

    for child in tree.root_node.children:
        if child.type == 'file_scoped_namespace_declaration':
            namespace_piece = child
            break
        if child.type == 'namespace_declaration':
            namespace_piece = child.named_children[-1]

    if not namespace_piece:
        raise Exception("No namespace")
    if not namespace_piece.children:
        raise Exception("Empty namespace")

    dependencies = []
    for child in namespace_piece.children:
        match child.type:
            case 'class_declaration':
                ans = parse_class(child, namespace.type_resolver)
                if ans.name in namespace.type_resolver.unresolved:
                    dependencies.append(ans)
                    namespace.defined_classes.append(ans)
                    namespace.type_resolver.mark_type_as_resolved(ans.name)
            case "record_declaration":
                ans = parse_record(child, namespace.type_resolver)
                if ans.name in namespace.type_resolver.unresolved:
                    dependencies.append(ans)
                    namespace.defined_classes.append(ans)
                    namespace.type_resolver.mark_type_as_resolved(ans.name)
            case "interface_declaration":
                ans = parse_interface(child, namespace.type_resolver)
                if ans.name in namespace.type_resolver.unresolved:
                    dependencies.append(ans)
                    namespace.defined_interfaces.append(ans)
                    namespace.type_resolver.mark_type_as_resolved(ans.name)

    return dependencies
