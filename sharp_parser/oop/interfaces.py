from dataclasses import dataclass

from tree_sitter import Node

from sharp_parser.functions.methods import parse_method, CSharpMethod, parse_operator
from sharp_parser.functions.properties import parse_property
from sharp_parser.sharp_types import CSharpType
from sharp_parser.type_resolver import TypeResolver
from sharp_parser.vars.variables import parse_field, CSharpVar


@dataclass
class CSharpInterface:
    """Интерфейс в языке C#"""
    modifiers: list[str]
    name: str
    body: list[CSharpVar | CSharpMethod]
    generic_types: list[CSharpType]
    syntax_name = "interface"

    def __repr__(self):
        signature = ""
        if self.modifiers:
            signature += ' '.join(self.modifiers) + ' '
        signature += f"{self.syntax_name} {self.name}"

        if self.generic_types:
            signature += f"<{', '.join(str(x) for x in self.generic_types)}>"
        signature += " {\n"
        for thing in self.body:
            signature += " " * 4 + str(thing) + '\n'
        signature += "}"
        return signature


def parse_interface(interface_in_file: Node, type_resolver):
    """
    :param interface_in_file: Нода интерфейса
    :param type_resolver: Резолвер типов
    :return:
    """

    interface = CSharpInterface([], "None", [], [])

    interface_body_node = parse_signature(interface, interface_in_file, type_resolver)
    parse_body(interface, interface_body_node, type_resolver)

    return interface


def parse_signature(interface: CSharpInterface, interface_in_file, type_resolver) -> Node | None:
    interface_body: Node | None = None
    for child in interface_in_file.children:
        match child.type:
            case "modifier":
                interface.modifiers.append(child.child(0).type)
            case "identifier":
                interface.name = child.text.decode()
            case "declaration_list":
                interface_body = child
            case 'type_parameter_list':
                for value_type in child.named_children:
                    generic_vtype = type_resolver.get_type_by_name(value_type.child(0).text.decode())
                    interface.generic_types.append(generic_vtype)
            case "base_list":
                for base in child.named_children:
                    type_resolver.parse_type_node(base)
    return interface_body


def parse_body(interface: CSharpInterface, interface_body: Node, type_resolver: TypeResolver):
    interface_fields = []
    interface_methods = []
    for child in interface_body.named_children:
        match child.type:
            case "field_declaration":
                interface_fields.append(parse_field(child, type_resolver))
            case "method_declaration":
                interface_methods.append(parse_method(child, type_resolver))
            case "property_declaration":
                x = parse_property(child, type_resolver)
                interface_fields.append(x)
            case "operator_declaration":
                interface_methods.append(parse_operator(child, type_resolver))
    interface.body = interface_fields + interface_methods
