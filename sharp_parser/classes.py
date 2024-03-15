from dataclasses import dataclass

import tree_sitter

from sharp_parser.interfaces import CSharpInterface
from sharp_parser.methods import parse_method, CSharpMethod
from sharp_parser.sharp_types import CSharpType, TypeResolver
from sharp_parser.variables import parse_field, CSharpVar


def parse_record(class_in_file, type_resolver: TypeResolver):
    raise Exception("рекорды нужно парстить")

    return parse_class(class_in_file, type_resolver)


class CSharpClass (CSharpInterface):
    """Класс в языке C#"""
    syntax_name = "class"


def parse_class(class_in_file: tree_sitter.Node, type_resolver: TypeResolver):
    """
    Порсит класс C#
    :param type_resolver: Резолвер шарповых типов
    :param class_in_file: treesitter нода класса
    :return: Объект класса
    """
    class_modifiers = []
    class_name = None
    class_body = None
    class_fields = []
    class_methods = []
    class_generics = []

    for child in class_in_file.children:
        match child.type:
            case "modifier":
                class_modifiers.append(child.child(0).type)
            case "identifier":
                class_name = child.text.decode()
            case "declaration_list":
                class_body = child
            case 'type_parameter_list':
                for value_type in child.named_children:
                    generic_vtype = type_resolver.get_type(value_type.child(0).text.decode())
                    class_generics.append(generic_vtype)
            case "base_list":
                for base in child.named_children:
                    type_resolver.parse_type_node(base)
    for child in class_body.named_children:
        if child.type == "field_declaration":
            class_fields.append(parse_field(child, type_resolver))
        if child.type == "method_declaration":
            class_methods.append(parse_method(child, type_resolver))
    ans = CSharpClass(class_modifiers, class_name, class_fields + class_methods, class_generics)
    return ans
