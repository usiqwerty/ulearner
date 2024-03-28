from sharp_parser.oop.classes import CSharpClass, parse_class
from sharp_parser.functions.methods import parse_parameters
from sharp_parser.sharp_types import TypeResolver
from sharp_parser.vars.variables import CSharpVar


class CSharpRecord(CSharpClass):
    parameters: list[CSharpVar]

    @staticmethod
    def from_class(as_class: CSharpClass):
        generated = CSharpRecord(as_class.modifiers, as_class.name, as_class.body, as_class.generic_types)
        generated.parameters = []
        generated.syntax_name = "record"
        return generated

    def __repr__(self):
        signature = ""
        if self.modifiers:
            signature += ' '.join(self.modifiers) + ' '

        if self.generic_types:
            signature += f"<{', '.join(str(x) for x in self.generic_types)}>"
        signature += f"{self.syntax_name} {self.name} ("
        if self.parameters:
            signature += ', '.join(param.as_param for param in self.parameters)
        signature += ")"

        signature += " {\n"
        for thing in self.body:
            signature += " " * 4 + str(thing) + '\n'
        signature += "}"
        return signature


def parse_record(class_in_file, type_resolver: TypeResolver) -> CSharpRecord:
    # raise Exception("рекорды нужно парстить")
    params = []

    as_class = parse_class(class_in_file, type_resolver)
    as_record = CSharpRecord.from_class(as_class)

    for child in class_in_file.named_children:
        if child.type == "parameter_list":
            parse_parameters(params, child, type_resolver)
            break
    as_record.parameters = params

    return as_record
