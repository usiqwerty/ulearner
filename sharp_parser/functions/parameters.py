import tree_sitter

from sharp_parser.sharp_types import TypeResolver
from sharp_parser.vars.variables import CSharpVar


def parse_multiple_parameters(parameters_children: list[tree_sitter.Node], type_resolver):
    params = []
    modifiers = []
    ptype = None
    pname = None

    for param in parameters_children:
        match param.type:
            case '(':
                continue
            case ',' | '(' | ')':
                if ptype:
                    params.append((modifiers, ptype, pname))
                ptype = None
                pname = None
                modifiers = []
            case "params":
                modifiers.append("params")
            case "identifier":
                if not ptype:
                    ptype = type_resolver.get_type_by_name(param.text.decode())
                else:
                    pname = param.text.decode()
            case "array_type":
                ptype = type_resolver.parse_type_node(param)
            case "parameter":
                if not param.children:
                    continue
                if param.child(0).text.decode() == "this":
                    modifiers.append("this")
                    continue
                if param.child(0).type=="attribute_list":
                    ptype = type_resolver.parse_type_node(param.child(1))
                    pname = param.child(2).text.decode()
                    params.append((modifiers, ptype, pname))
                else:
                    ptype = type_resolver.parse_type_node(param.child(0))
                    pname = param.child(1).text.decode()
                    params.append((modifiers, ptype, pname))

                ptype = None
                pname = None
                modifiers = []
                continue
            case _:
                ptype = type_resolver.get_type_by_name(param.text.decode())

    return params


def parse_parameters(arguments, params_node: tree_sitter.Node, type_resolver: TypeResolver):
    if params_node.named_child(0).type == "parameter":
        for pmod, ptype, pname in parse_multiple_parameters(params_node.children, type_resolver):
            arguments.append(CSharpVar(pmod, ptype, pname))
    else:
        name = params_node.named_child(1).text.decode()
        var_type = type_resolver.parse_type_node(params_node.named_child(0))

        arguments.append(CSharpVar([], var_type, name))
