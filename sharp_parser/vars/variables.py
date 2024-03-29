from dataclasses import dataclass

import tree_sitter

from sharp_parser.sharp_types import CSharpType, TypeResolver


@dataclass
class CSharpVar:
    modifiers: list[str]
    var_type: CSharpType
    name: str

    @property
    def as_param(self):
        return f"{self.var_type} {self.name}"

    def __repr__(self):
        return f"{' '.join(self.modifiers)} {self.var_type} {self.name};"


def parse_field(field_node: tree_sitter.Node, type_resolver: TypeResolver) -> CSharpVar:
    """
    Парсит поле класса
    :param type_resolver: Резолвер шарповых типов
    :param field_node: нода treesitter
    :return: Объект поля класса
    """
    modifiers = []
    var_type = None
    var_name = None
    for child in field_node.named_children:
        if child.type == "modifier":
            modifiers.append(child.child(0).type)
        if child.type == "variable_declaration":

            for var_part in child.children:
                if var_part.type == "identifier":
                    var_type = type_resolver.get_type_by_name(var_part.text.decode())
                if var_part.type == "generic_name":
                    var_type = type_resolver.parse_generic_type_node(var_part)
                if var_part.type == "variable_declarator":
                    var_name = var_part.child(0).text.decode()
            pass
    return CSharpVar(modifiers, var_type, var_name)
