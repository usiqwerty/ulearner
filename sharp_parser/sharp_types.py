from dataclasses import dataclass

import tree_sitter

@dataclass
class CSharpType:
    name: str
    generic_types: list

    @property
    def just_typename(self):
        return str(self)

    def __repr__(self):
        signature = f"{self.name}"
        if self.generic_types:
            signature += f"<{', '.join(self.generic_types)}>"
        return signature


def parse_generic_type(type_node: tree_sitter.Node) -> CSharpType:
    type_class: str = None
    value_types = []
    for child in type_node.named_children:
        if child.type == "identifier":
            type_class = child.text.decode()
        if child.type == 'type_argument_list':
            value_types = [x.text.decode() for x in child.named_children]
    return CSharpType(type_class, value_types) #CSharpClass([], type_class, [], value_types)


builtin_types="void int bool char double string float".split()


def create_dummy_type(name: str):
    return CSharpType(name, []) #CSharpClass([], name, [], [])


type_references: dict[str, CSharpType] = {builtin_type: create_dummy_type(builtin_type) for builtin_type in
                                           builtin_types}
unresolved: list[str] = []


class ArrayType(CSharpType):
    value_type: CSharpType
    def __init__(self, value_type: CSharpType):
        self.value_type=value_type
    @property
    def just_typename(self):
        return str(self)
    def __repr__(self):
        f"{self.value_type.just_typename}[]"
