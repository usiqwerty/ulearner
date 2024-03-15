from sharp_parser.classes import CSharpClass
from sharp_parser.interfaces import CSharpInterface
from sharp_parser.sharp_types import TypeResolver


class CSharpNamespace:
    """
    Пространство имён C#
    """
    defined_classes: list[CSharpClass]
    defined_interfaces: list[CSharpInterface]
    type_resolver: TypeResolver

    def __init__(self):
        self.defined_classes = []
        self.defined_interfaces = []
        self.type_resolver = TypeResolver()
