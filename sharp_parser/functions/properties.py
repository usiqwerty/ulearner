from tree_sitter import Node

import sharp_parser.sharp_types
from sharp_parser.type_resolver import TypeResolver


class CSharpPropery:
    def __init__(self, modifiers, prop_type, name, get: str, set: str):
        self.modifiers = modifiers
        self.prop_type = prop_type
        self.name = name
        self.get = get
        self.set = set

    def __repr__(self):
        return f"{' '.join(self.modifiers)} {self.prop_type} {self.name} {{ {self.get}; {self.set} }}"


def parse_property(property_node: Node, type_resolver: TypeResolver):
    modifiers = []
    prop_type = None
    prop_name = None
    get = "get"
    set = ""
    for child in property_node.named_children:
        match child.type:
            case "modifier":
                modifiers.append(child.text.decode())
            case "array_type":
                prop_type = type_resolver.parse_type_node(child)
            case "predefined_type":
                prop_type = type_resolver.get_type_by_name(child.text.decode())
            case "identifier":
                if not prop_type:
                    prop_type = type_resolver.get_type_by_name(child.text.decode())
                else:
                    prop_name = child.text.decode()
            case "generic_name":
                prop_type = type_resolver.parse_type_node(child)
            case "qualified_name":
                prop_type = type_resolver.parse_type_node(child)
            case "nullable_type":
                prop_type = type_resolver.parse_type_node(child)
            case "arrow_expression_clause":
                set = ""
                get = "get"
            case "accessor_list":
                for accs in child.named_children:
                    get_type = True
                    accessor = ""
                    for part in accs.children:
                        if part.type in ["get", "set"]:
                            get_type = part.type == "get"
                            accessor += part.type
                            break
                        if part.type == "modifier":
                            accessor += part.text.decode() + " "
                    if get_type:
                        get = accessor
                    else:
                        set = accessor
    return CSharpPropery(modifiers, prop_type, prop_name, get, set)