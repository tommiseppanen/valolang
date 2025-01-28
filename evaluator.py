class Evaluator:
    def __init__(self):
        self.functions = {}  # Function table: {name: (params, body)}

    def evaluate(self, ast):
        result = None
        context = {}
        for node in ast:
            result = self.eval_node(node, context)
        return result

    def eval_nodes(self, ast, context):
        result = None
        for node in ast:
            result = self.eval_node(node, context)
        return result

    def eval_node(self, node, context):
        node_type = node[0]

        if node_type == "NUMBER":
            return float(node[1]) if "." in node[1] else int(node[1])

        elif node_type == "IF":
            _, condition, true_block, false_block = node
            condition_result = self.eval_node(condition, context)

            if condition_result:
                return self.eval_node(true_block, context)
            elif false_block:
                return self.eval_node(false_block, context)
            return None

        elif node_type == "WHILE":
            _, condition, body = node

            while self.eval_node(condition, context):
                self.eval_nodes(body, context)

        elif node_type == 'IDENTIFIER':
            # Resolve variable name in the context
            name = node[1]
            if name in context:
                return context[name]
            else:
                raise NameError(f"Undefined variable '{name}'")

        elif node_type == "BIN_OP":
            _, operator, left_node, right_node = node
            left_value = self.eval_node(left_node, context)
            right_value = self.eval_node(right_node, context)

            if operator == "+":
                return left_value + right_value
            elif operator == "-":
                return left_value - right_value
            elif operator == "*":
                return left_value * right_value
            elif operator == "/":
                return left_value / right_value
            elif operator == ">":
                return left_value > right_value
            elif operator == "<":
                return left_value < right_value
            elif operator == "==":
                return left_value == right_value
            else:
                raise ValueError(f"Unknown operator: {operator}")

        elif node_type == 'FUNCTION_DEF':
            # Store function definition: ('FUNCTION_DEF', name, params, body)
            _, name, params, body = node
            self.functions[name] = (params, body)

        elif node_type == 'ASSIGNMENT':
            var_name = node[1]
            value = self.eval_node(node[2], context)
            context[var_name] = value
            return value

        elif node_type == 'STRING':
            return node[1]

        elif node_type == 'INTERPOLATED_STRING':
            parts = node[1]
            result = ''
            for part in parts:
                if isinstance(part, tuple):
                    # Evaluate embedded expression
                    result += str(self.eval_node(part, context))
                else:
                    # Append literal part
                    result += part
            return result

        elif node_type == 'FUNCTION_CALL':
            # Evaluate function call: ('FUNCTION_CALL', name, args)
            _, name, args = node

            # Handle built-in print function
            if name == 'print':
                evaluated_args = [self.eval_node(arg, context) for arg in args]
                print(*evaluated_args)
                return None

            # Lookup the function definition
            if name not in self.functions:
                raise NameError(f"Undefined function '{name}'")

            params, body = self.functions[name]

            # Check arity (number of arguments)
            if len(params) != len(args):
                raise TypeError(f"Function '{name}' expects {len(params)} arguments, got {len(args)}")

            # Evaluate arguments
            arg_values = [self.eval_node(arg, context) for arg in args]

            # Create a new context for the function execution
            function_context = {param: value for param, value in zip(params, arg_values)}

            # Evaluate the function body in its own context
            return self.eval_node(body, function_context)

        else:
            raise ValueError(f"Unknown node type: {node_type}")
