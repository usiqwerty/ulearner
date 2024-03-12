from dataclasses import dataclass

import tree_sitter

from sharp_parser.sharp_types import create_dummy_type, type_references, unresolved, CSharpType, ArrayType
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
            signature += str(self.return_type.just_typename) + " "
        signature += self.name+" "
        signature += " (" + ', '.join(x.as_param for x in self.arguments) +")"
        return signature+";"


def parse_method(method_node: tree_sitter.Node) -> CSharpMethod:
    modifiers = []
    return_type: CSharpType = None
    arguments = []
    method_name = None
    for child in method_node.children:
        if child.type == "modifier":
            modifiers.append(child.text.decode())
        if child.type == "predefined_type":
            return_type = type_references[child.text.decode()]
        if child.type == "array_type":
            vtype_str=child.named_child(0).text.decode()

            return_type = ArrayType(type_references[vtype_str])
        if child.type == "identifier":
            method_name = child.text.decode()
        if child.type == "parameter_list":
            if len(child.named_children)==0:
                continue
            if child.named_child(0).type =="parameter":
                for param in child.named_children:
                    type_str = param.child(0).text.decode()
                    name = param.child(1).text.decode()
                    if type_str not in type_references:
                        unresolved.append(type_str)
                        type_references[type_str] = create_dummy_type(type_str)

                    arguments.append(CSharpVar(modifiers, type_references[type_str], name))
            else:
                type_str = child.named_child(0).text.decode()
                name = child.named_child(1).text.decode()
                if type_str not in type_references:
                    unresolved.append(type_str)
                    type_references[type_str] = create_dummy_type(type_str)

                arguments.append(CSharpVar(modifiers, type_references[type_str], name))

    if method_name=="Parser":
        pass
    return CSharpMethod(modifiers, return_type, method_name, arguments)
