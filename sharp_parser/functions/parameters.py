import tree_sitter

from sharp_parser.sharp_types import TypeResolver
from sharp_parser.vars.variables import CSharpVar


def parse_parameters(arguments, params_node: tree_sitter.Node, type_resolver: TypeResolver):
    is_params = False
    if params_node.named_child(0).type == "parameter":
        for param in params_node.children:
            if param.type in [',', '(', ')']: continue

            match param.type:
                case "params":
                    is_params = True
                    continue
                case "parameter":
                    if not param.children or param.child(0).text.decode() == "this":
                        continue
                    param_type = type_resolver.parse_type_node(param.child(0))
                    name = param.child(1).text.decode()
                    arguments.append(CSharpVar([], param_type, name))
                    param_type = None
                    name = None
                    continue
                case "identifier":
                    if not param_type:
                        param_type = type_resolver.get_type_by_name(param.text.decode())
                    else:
                        name = param.text.decode()
                case "array_type":
                    param_type = type_resolver.parse_type_node(param)
                case _:
                    param_type = type_resolver.get_type_by_name(param.text.decode())
            if not name:
                pass
            if param_type.name == "Args":
                pass
            if not name:
                continue
            arguments.append(CSharpVar(["params"] if is_params else [], param_type, name))
            is_params = False
    else:
        name = params_node.named_child(1).text.decode()
        var_type = type_resolver.parse_type_node(params_node.named_child(0))

        arguments.append(CSharpVar(["params"] if is_params else [], var_type, name))
