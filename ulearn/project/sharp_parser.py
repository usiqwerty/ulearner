import tree_sitter
from tree_sitter_languages import get_language, get_parser

from ulearn.project.sharp_types import CSharpClass, CSharpVar, CSharpMethod


builtin_types="void int bool char double string float".split()
def create_dummy_type(name: str):
    return CSharpClass([], name, [], [])

type_references: dict[str, CSharpClass] = {builtin_type: create_dummy_type(builtin_type) for builtin_type in builtin_types}
unresolved: list[str] = []


def parse_code_class(code: str) -> tuple[CSharpClass, list[str]]:
    """
    Парсит класс из файла
    :param code: Код на C#
    :return: Распаршенный класс и список неизвестных имён классов
    """
    tree = parser.parse(code.encode())
    # node = tree.root_node
    namespace = tree_sitter.Node()
    for child in tree.root_node.children:
        if child.type == 'file_scoped_namespace_declaration':
            namespace = child
            break
    if not namespace.children: raise Exception("Empty namespace")
    class_in_file = None
    for child in namespace.children:
        if child.type == 'class_declaration':
            class_in_file = child
            break
    class_modifiers = []
    class_name = None
    class_body = None
    class_fields = []
    class_methods = []
    class_generics = []
    for child in class_in_file.children:
        if child.type == "modifier":
            class_modifiers.append(child.child(0).type)
        if child.type == "identifier":
            class_name = child.text.decode()
        if child.type == "declaration_list":
            class_body = child
        if child.type == 'type_parameter_list':
            for value_type in child.named_children:
                class_generics.append(value_type.child(0).text.decode())

    for child in class_body.named_children:
        if child.type == "field_declaration":
            class_fields.append(parse_field(child))
        if child.type == "method_declaration":
            class_methods.append(parse_method(child))
    ans = CSharpClass(class_modifiers, class_name, class_fields + class_methods, class_generics)
    return ans, unresolved


def parse_generic_type(type_node: tree_sitter.Node) -> CSharpClass:
    type_class = None
    value_types = []
    for child in type_node.named_children:
        if child.type == "identifier":
            type_class = child.text.decode()
        if child.type == 'type_argument_list':
            value_types = [x.text.decode() for x in child.named_children]
    return CSharpClass([], type_class, [], value_types)


def parse_field(field_node: tree_sitter.Node) -> CSharpVar:
    modifiers = []
    var_type = None
    var_name = None
    for child in field_node.named_children:
        if child.type == "modifier":
            modifiers.append(child.child(0).type)
        if child.type == "variable_declaration":

            for var_part in child.children:
                if var_part.type == "generic_name":
                    var_type = parse_generic_type(var_part)
                if var_part.type == "variable_declarator":
                    var_name = var_part.child(0).text.decode()
            pass
    return CSharpVar(modifiers, var_type, var_name)


def parse_method(method_node: tree_sitter.Node) -> CSharpMethod:
    modifiers = []
    return_type = None
    arguments = []
    method_name = None
    for child in method_node.children:
        if child.type == "modifier":
            modifiers.append(child.text.decode())
        if child.type == "predefined_type":
            return_type = child.text.decode()
        if child.type == "identifier":
            method_name = child.text.decode()
        if child.type == "parameter_list":
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

    return CSharpMethod(modifiers, type_references[return_type], method_name, arguments)


language = get_language('c_sharp')
parser = get_parser('c_sharp')
