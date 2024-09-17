import tree_sitter

import sharp_parser.type_resolver
from sharp_parser.functions.parameters import parse_parameters
from sharp_parser.sharp_types import CSharpType
from sharp_parser.vars.variables import CSharpVar


class CSharpDelegate:
    def __init__(self, modifiers, return_type: CSharpType, delegate_name: str, arguments: list[CSharpVar]):
        self.modifiers = modifiers
        self.return_type = return_type
        self.name = delegate_name
        self.arguments = arguments

    def __repr__(self):
        output = ""
        for modifier in self.modifiers:
            output += modifier + " "
        output += f"delegate {self.return_type} {self.name}("
        output += ', '.join(arg.as_param for arg in self.arguments)
        output += ');'

        return output


def parse_delegate(delegate_node: tree_sitter.Node, type_resolver: sharp_parser.type_resolver.TypeResolver):
    modifiers = []
    return_type = None
    delegate_name = None
    arguments: list[CSharpVar] = []
    for child in delegate_node.named_children:
        match child.type:
            case "modifier":
                modifiers.append(child.text.decode())
            case "identifier":
                if not return_type:
                    return_type = type_resolver.get_type_by_name(child.text.decode())
                else:
                    delegate_name = child.text.decode()
            case "parameter_list":
                parse_parameters(arguments, child, type_resolver)
    return CSharpDelegate(modifiers, return_type, delegate_name, arguments)
