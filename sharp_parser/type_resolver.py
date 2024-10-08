from tree_sitter import Node

from sharp_parser.sharp_types import CSharpType, create_dummy_type, builtin_types, CSharpTuple


class TypeResolver:
    unresolved: list[str]
    type_references: dict[str, CSharpType]

    def __init__(self):
        self.unresolved = []
        self.type_references = {builtin_type: create_dummy_type(builtin_type)
                                for builtin_type in builtin_types}

    def get_type_by_name(self, typename: str) -> CSharpType:
        if typename not in self.type_references:
            self.unresolved.append(typename)
            self.type_references[typename] = create_dummy_type(typename)

        return self.type_references[typename]

    def mark_type_as_resolved(self, typename: str):
        if typename in self.unresolved:
            self.unresolved.remove(typename)
        if typename not in self.type_references:
            self.type_references[typename] = create_dummy_type(typename)

    def parse_type_node(self, type_node: Node) -> CSharpType:
        if type_node.named_children and type_node.named_child(0).type == "tuple_element":
            from sharp_parser.vars.variables import parse_field
            return CSharpTuple([parse_field(child, self) for child in type_node.named_children])
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
            case "nullable_type":
                ty = self.get_type_by_name(type_node.named_child(0).text.decode())
                ty.nullable = True
                return ty
            case "qualified_name":
                return self.get_type_by_name(type_node.text.decode())
        raise Exception(f'Unknown var type: {type_node.type}')

    def parse_generic_type_node(self, type_node: Node) -> CSharpType:
        type_class = ""
        value_types = []

        for child in type_node.named_children:
            if child.type == "identifier":
                type_class = child.text.decode()
            if child.type == 'type_argument_list':
                value_types = [self.parse_type_node(x) for x in child.named_children]
        self.get_type_by_name(type_class)

        return CSharpType(type_class, value_types)
