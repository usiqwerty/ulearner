from tree_sitter import Tree, Node
from tree_sitter_languages import get_language, get_parser

from sharp_parser.functions.delegates import parse_delegate
from sharp_parser.oop.classes import parse_class, CSharpClass
from sharp_parser.oop.interfaces import parse_interface
from sharp_parser.oop.namespace import CSharpNamespace
from sharp_parser.oop.records import parse_record
from sharp_parser.vars.enums import parse_enum, CSharpEnum

language = get_language('c_sharp')
parser = get_parser('c_sharp')


def get_code_dependencies(code: str, namespace: CSharpNamespace) -> list[CSharpClass | CSharpEnum]:
    """
    Парсит файл и записывает в namespace
    :param code: Код на C#
    :param namespace: Пространство имён, в котором идёт парсинг
    :return: Зависимости кода
    """

    tree = parser.parse(code.encode())
    namespace_piece = get_namespace_piece_in_tree(tree)

    if namespace_piece is None:
        return []
        # raise Exception("No namespace")
    if not namespace_piece.children:
        raise Exception("Empty namespace")

    dependencies = get_definitions_for_unresolved(namespace, namespace_piece)
    return dependencies


def get_definitions_for_unresolved(namespace: CSharpNamespace, namespace_piece: Node):
    dependencies = []
    for child in namespace_piece.children:
        match child.type:
            case 'class_declaration':
                ans = parse_class(child, namespace.type_resolver)
                namespace.defined_classes.append(ans)
            case "record_declaration":
                ans = parse_record(child, namespace.type_resolver)
                namespace.defined_classes.append(ans)
            case "interface_declaration":
                ans = parse_interface(child, namespace.type_resolver)
                namespace.defined_interfaces.append(ans)
            case "delegate_declaration":
                ans = parse_delegate(child, namespace.type_resolver)
            case "enum_declaration":
                ans = parse_enum(child, namespace.type_resolver)
            case _:
                continue

        if ans.name in namespace.type_resolver.unresolved:
            dependencies.append(ans)
            namespace.type_resolver.mark_type_as_resolved(ans.name)
    return dependencies


def get_namespace_piece_in_tree(tree: Tree) -> Node | None:
    namespace_piece = None
    for child in tree.root_node.children:
        if child.type == 'file_scoped_namespace_declaration':
            namespace_piece = child
            break
        if child.type == 'namespace_declaration':
            namespace_piece = child.named_children[-1]
    return namespace_piece
