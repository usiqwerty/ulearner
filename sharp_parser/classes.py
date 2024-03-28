import tree_sitter

from sharp_parser.interfaces import CSharpInterface, parse_interface
from sharp_parser.sharp_types import TypeResolver


def parse_record(class_in_file, type_resolver: TypeResolver):
    # raise Exception("рекорды нужно парстить")
    return parse_class(class_in_file, type_resolver)


class CSharpClass(CSharpInterface):
    """Класс в языке C#"""

    @staticmethod
    def from_interface(iface: CSharpInterface):
        generated = CSharpClass(iface.modifiers, iface.name, iface.body, iface.generic_types)
        generated.syntax_name = "class"
        return generated


def parse_class(class_in_file: tree_sitter.Node, type_resolver: TypeResolver):
    """
    Порсит класс C#
    :param type_resolver: Резолвер шарповых типов
    :param class_in_file: treesitter нода класса
    :return: Объект класса
    """
    return CSharpClass.from_interface(parse_interface(class_in_file, type_resolver))
