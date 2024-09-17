import tree_sitter

from sharp_parser.type_resolver import TypeResolver
from sharp_parser.vars.variables import CSharpVar


def parse_multiple_parameters(parameters_children: list[tree_sitter.Node], type_resolver):
    params = []
    modifiers = []
    parameter_type = None
    parameter_name = None

    for param in parameters_children:
        match param.type:
            case '(':
                continue
            case ',' | '(' | ')':
                if parameter_type:
                    params.append((modifiers, parameter_type, parameter_name))
                parameter_type = None
                parameter_name = None
                modifiers = []
            case "params":
                modifiers.append("params")
            case "identifier":
                if not parameter_type:
                    parameter_type = type_resolver.get_type_by_name(param.text.decode())
                else:
                    parameter_name = param.text.decode()
            case "array_type":
                parameter_type = type_resolver.parse_type_node(param)
            case "parameter":
                if not param.children:
                    continue
                if param.child(0).text.decode() == "this":
                    modifiers.append("this")
                    continue
                if param.child(0).type == "attribute_list":
                    parameter_type = type_resolver.parse_type_node(param.child(1))
                    parameter_name = param.child(2).text.decode()
                    params.append((modifiers, parameter_type, parameter_name))
                else:
                    parameter_type = type_resolver.parse_type_node(param.child(0))
                    parameter_name = param.child(1).text.decode()
                    params.append((modifiers, parameter_type, parameter_name))

                parameter_type = None
                parameter_name = None
                modifiers = []
                continue
            case _:
                parameter_type = type_resolver.get_type_by_name(param.text.decode())

    return params


def parse_parameters(arguments, params_node: tree_sitter.Node, type_resolver: TypeResolver):
    if params_node.named_child(0).type == "parameter":
        for pmod, ptype, pname in parse_multiple_parameters(params_node.children, type_resolver):
            arguments.append(CSharpVar(pmod, ptype, pname))
    else:
        name = params_node.named_child(1).text.decode()
        var_type = type_resolver.parse_type_node(params_node.named_child(0))

        arguments.append(CSharpVar([], var_type, name))
