from dataclasses import dataclass

import tree_sitter

from sharp_parser.sharp_types import CSharpType, TypeResolver
from sharp_parser.variables import CSharpVar


@dataclass
class CSharpMethod:
    modifiers: list[str]
    return_type: CSharpType
    name: str
    arguments: list[CSharpVar]

    def __repr__(self):
        signature = ""
        if self.modifiers:
            signature += ' '.join(self.modifiers) + " "
        if self.return_type:
            signature += str(self.return_type) + " "
        signature += self.name  # + " "
        signature += "(" + ', '.join(x.as_param for x in self.arguments) + ")"
        return signature + ";"


def parse_method(method_node: tree_sitter.Node, type_resolver: TypeResolver) -> CSharpMethod:
    modifiers = []
    return_type: CSharpType = None
    arguments = []
    method_name = None
    for child in method_node.children:
        #method_node.child_by_field_name()
        if child.type == "modifier":
            modifiers.append(child.text.decode())
        elif child.type in ["predefined_type", "array_type", "generic_name"]:
            return_type = type_resolver.parse_type_node(child)

        elif child.type == "identifier":
            method_name = child.text.decode()
        elif child.type == "parameter_list":
            if len(child.named_children) == 0:
                continue
            parse_parameters(arguments, child, type_resolver)

    return CSharpMethod(modifiers, return_type, method_name, arguments)


def parse_parameters(arguments, params_node: tree_sitter.Node, type_resolver:TypeResolver):
    if params_node.named_child(0).type == "parameter":
        for param in params_node.named_children:
            if param.child(0).text.decode()=="this":
                continue
            param_type = type_resolver.parse_type_node(param.child(0))
            #param_type_str = param.child(0).text.decode()

            name = param.child(1).text.decode()

            arguments.append(CSharpVar([], param_type, name))
    else:
        param_type_str = params_node.named_child(0).text.decode()
        name = params_node.named_child(1).text.decode()

        arguments.append(CSharpVar([], type_resolver.get_type(param_type_str), name))
