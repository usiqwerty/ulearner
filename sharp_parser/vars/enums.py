import tree_sitter

import sharp_parser.sharp_types


class CSharpEnum:
    def __init__(self, modifiers: list[str], name: str, members: list[tuple[str, str]]):
        self.modifiers = modifiers
        self.name = name
        self.members = members

    def __repr__(self):
        output = ""
        for modifier in self.modifiers:
            output+=f"{modifier} "
        output+=f"enum {self.name}\n" + "{\n"
        for member_name, member_value in self.members:
            output+=f"    {member_name} = {member_value},\n"
        output+="}"
        return output

def parse_enum(enum_node: tree_sitter.Node, type_resolver: sharp_parser.sharp_types.TypeResolver) -> CSharpEnum:
    modifiers = []

    enum_name = None
    members = []

    for child in enum_node.named_children:
        match child.type:
            case "modifier":
                modifiers.append(child.text.decode())
            case "identifier":
                enum_name = child.text.decode()
            case "enum_member_declaration_list":
                for enum_member in child.named_children:
                    member_name = None
                    member_value = None
                    for enum_member_part in enum_member.named_children:

                        if enum_member_part.type == "identifier":
                            member_name = enum_member_part.text.decode()
                        else:
                            member_value = enum_member_part.text.decode()
                    members.append((member_name, member_value))

    return CSharpEnum(modifiers, enum_name, members)
