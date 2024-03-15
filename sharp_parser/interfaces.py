from dataclasses import dataclass


from sharp_parser.methods import parse_method, CSharpMethod
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


def parse_interface(class_in_file, type_resolver):
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
    ans = CSharpInterface(class_modifiers, class_name, class_fields + class_methods, class_generics)
    return ans
