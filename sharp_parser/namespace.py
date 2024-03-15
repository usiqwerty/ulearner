from sharp_parser.classes import CSharpClass
from sharp_parser.sharp_types import TypeResolver


class CSharpNamespace:
    """
    Пространство имён C#
    """
    defined_classes: list[CSharpClass] = []
    defined_interfaces: list[CSharpClass] = []
    type_resolver: TypeResolver

    def __init__(self):
        self.type_resolver = TypeResolver()
