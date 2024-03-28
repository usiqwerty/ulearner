from dataclasses import dataclass


from sharp_parser.methods import parse_method, CSharpMethod
from sharp_parser.properties import parse_property
from sharp_parser.sharp_types import CSharpType
from sharp_parser.variables import parse_field, CSharpVar


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
            # thing: CSharpVar | CSharpMethod
            signature += " " * 4 + str(thing) + '\n'
        signature += "}"
        return signature


def parse_interface(interface_in_file, type_resolver):
    """
    :param interface_in_file: Нода интерфейса
    :param type_resolver: Резолвер типов
    :return:
    """
    interface_modifiers = []
    interface_name = None
    interface_body = None
    interface_fields = []
    interface_methods = []
    interface_generics = []

    for child in interface_in_file.children:
        match child.type:
            case "modifier":
                interface_modifiers.append(child.child(0).type)
            case "identifier":
                interface_name = child.text.decode()
            case "declaration_list":
                interface_body = child
            case 'type_parameter_list':
                for value_type in child.named_children:
                    generic_vtype = type_resolver.get_type_by_name(value_type.child(0).text.decode())
                    interface_generics.append(generic_vtype)
            case "base_list":
                for base in child.named_children:
                    type_resolver.parse_type_node(base)
    for child in interface_body.named_children:
        match child.type:
            case "field_declaration":
                interface_fields.append(parse_field(child, type_resolver))
            case "method_declaration":
                interface_methods.append(parse_method(child, type_resolver))
            case "property_declaration":
                x= parse_property(child, type_resolver)
                interface_fields.append(x)
            case "operator_declaration":
                pass
    ans = CSharpInterface(interface_modifiers, interface_name, interface_fields + interface_methods, interface_generics)
    return ans
