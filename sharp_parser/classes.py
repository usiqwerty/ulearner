from dataclasses import dataclass

from sharp_parser.variables import parse_field
from sharp_parser.methods import parse_method


def parse_record(class_in_file):
    print("рекорды нужно парстить")
    return parse_class(class_in_file)


def parse_class(class_in_file):
    class_modifiers = []
    class_name = None
    class_body = None
    class_fields = []
    class_methods = []
    class_generics = []
    for child in class_in_file.children:
        if child.type == "modifier":
            class_modifiers.append(child.child(0).type)
        if child.type == "identifier":
            class_name = child.text.decode()
        if child.type == "declaration_list":
            class_body = child
        if child.type == 'type_parameter_list':
            for value_type in child.named_children:
                class_generics.append(value_type.child(0).text.decode())
    for child in class_body.named_children:
        if child.type == "field_declaration":
            class_fields.append(parse_field(child))
        if child.type == "method_declaration":
            class_methods.append(parse_method(child))
    ans = CSharpClass(class_modifiers, class_name, class_fields + class_methods, class_generics)
    return ans


@dataclass
class CSharpClass:
    modifiers: list[str]
    name: str
    body: list  #: list[CSharpVar | CSharpMethod]
    generic_types: list  # CSharpClass

    @property
    def just_typename(self):
        typename = self.name
        if self.generic_types:
            typename+= f"<{', '.join(self.generic_types)}>"
        return typename
    def __repr__(self):
        signature = ""
        if self.modifiers:
            signature += ' '.join(self.modifiers) + ' '
        signature += f"class {self.name}"
        if self.generic_types:
            signature += f"<{', '.join(self.generic_types)}>"
        signature += " {\n"
        for thing in self.body:
            #thing: CSharpVar | CSharpMethod
            signature += " " * 4 + str(thing) + '\n'
        signature += "}"
        return signature


