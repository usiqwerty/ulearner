from dataclasses import dataclass

import tree_sitter

builtin_types = "void object int bool char double string float byte Random Func Action Dictionary List".split()


@dataclass
class CSharpType:
    name: str
    generic_types: list
    is_array: bool = False

    @property
    def just_typename(self):
        return str(self)

    def __repr__(self):
        signature = f"{self.name}"
        if self.generic_types:
            signature += f"<{', '.join(str(x) for x in self.generic_types)}>"
        if self.is_array:
            signature += "[]"
        return signature


def create_dummy_type(name: str):
    return CSharpType(name, [])


class TypeResolver:
    unresolved: list[str]
    type_references: dict[str, CSharpType]

    def __init__(self):
        self.unresolved = []
        self.type_references = {builtin_type: create_dummy_type(builtin_type) for builtin_type in
                                builtin_types}

    def get_type_by_name(self, typename: str):
        if typename not in self.type_references:
            print(f"Unresolved type: {typename}")
            self.unresolved.append(typename)
            self.type_references[typename] = create_dummy_type(typename)

        return self.type_references[typename]

    def mark_type_as_resolved(self, typename: str):
        self.unresolved.remove(typename)
        if typename not in self.type_references:
            self.type_references[typename] = create_dummy_type(typename)

    def parse_type_node(self, type_node: tree_sitter.Node) -> CSharpType:
        match type_node.type:
            case "predefined_type":
                return self.get_type_by_name(type_node.text.decode())
            case "generic_name":
                return self.parse_generic_type_node(type_node)
            case "array_type":
                value_type = self.parse_type_node(type_node.named_child(0))
                return CSharpType(value_type.name, value_type.generic_types, True)
            case "identifier":
                return self.get_type_by_name(type_node.text.decode())
        raise Exception('Unknown var type')

    def parse_generic_type_node(self, type_node: tree_sitter.Node) -> CSharpType:
        type_class = ""
        value_types = []

        for child in type_node.named_children:
            if child.type == "identifier":
                type_class = child.text.decode()
            if child.type == 'type_argument_list':
                value_types = [self.parse_type_node(x) for x in child.named_children]
        self.get_type_by_name(type_class)

        return CSharpType(type_class, value_types)
