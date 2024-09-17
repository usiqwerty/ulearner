from dataclasses import dataclass

import tree_sitter

from sharp_parser.functions.parameters import parse_parameters
from sharp_parser.sharp_types import CSharpType
from sharp_parser.type_resolver import TypeResolver
from sharp_parser.vars.variables import CSharpVar


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
        signature += self.name
        signature += "(" + ', '.join(x.as_param for x in self.arguments) + ")"
        return signature + ";"


def parse_method(method_node: tree_sitter.Node, type_resolver: TypeResolver) -> CSharpMethod:
    modifiers = []
    return_type: CSharpType = type_resolver.get_type_by_name('void')
    arguments = []
    method_name = None
    for child in method_node.children:
        match child.type:
            case "modifier":
                modifiers.append(child.text.decode())
            case "predefined_type" | "array_type" | "generic_name":
                return_type = type_resolver.parse_type_node(child)

            case "identifier":
                method_name = child.text.decode()
            case "parameter_list":
                if len(child.named_children) == 0:
                    continue
                parse_parameters(arguments, child, type_resolver)

    return CSharpMethod(modifiers, return_type, method_name, arguments)


def parse_operator(method_node: tree_sitter.Node, type_resolver: TypeResolver) -> CSharpMethod:
    modifiers = []
    return_type: CSharpType = None
    arguments = []
    method_name = None

    for child in method_node.children:
        match child.type:
            case "modifier":
                modifiers.append(child.text.decode())
            case "predefined_type" | "array_type" | "generic_name":

                return_type = type_resolver.parse_type_node(child)
            case "+" | "-" | "*" | "/" | "==" | "^" | "%" | ">>" | "<<":
                method_name = "operator "+child.text.decode()
            case "identifier":
                if not return_type:
                    return_type = type_resolver.get_type_by_name(child.text.decode())
                else:
                    method_name = child.text.decode()

            case "parameter_list":
                if len(child.named_children) == 0:
                    continue
                parse_parameters(arguments, child, type_resolver)

    return CSharpMethod(modifiers, return_type, method_name, arguments)

