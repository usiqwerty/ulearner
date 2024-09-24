from dataclasses import dataclass

builtin_types = [
    'void', 'object', 'int', 'short', 'bool', 'char', 'double', 'string',
    'float', 'byte', 'Random', 'Func', 'Action', 'Dictionary', 'List',
    'IEnumerable', 'IDictionary', 'DateTime', 'Exception', 'T', 'IEnumerator',
    'IReadOnlyList', 'HashSet', 'Queue', 'Point', 'DirectoryInfo', 'Path',
    'Application', 'Canvas', 'Task', 'Avalonia.Point', 'PointerEventArgs',
    'PointerWheelEventArgs', 'DrawingContext', 'Size', 'Bitmap', 'Window',
    'DispatcherTimer', 'KeyEventArgs', 'Matrix', 'Vector', 'PointerPressedEventArgs',
    'PointerReleasedEventArgs', "ITransform", 'TimeSpan', 'Button', 'Key',
    'Image', 'Data', 'Stack', 'Tuple', 'StringWriter', 'IList', 'Regex',
    'DocumentTokens', 'Attribute', 'ConsoleColor', 'Guid'
]


@dataclass
class CSharpType:
    name: str
    generic_types: list
    is_array: bool = False
    nullable = False

    @property
    def just_typename(self):
        return str(self) + "?" if self.nullable else ''

    def __repr__(self):
        signature = f"{self.name}"
        if self.generic_types:
            signature += f"<{', '.join(str(x) for x in self.generic_types)}>"
        if self.is_array:
            signature += "[]"
        return signature


class CSharpTuple(CSharpType):
    def __init__(self, elements: list):
        self.elements = elements

    def __repr__(self):
        return "(" + ', '.join(str(x) for x in self.elements) + ")"


def create_dummy_type(name: str):
    return CSharpType(name, [])


