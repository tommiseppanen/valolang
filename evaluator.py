class Evaluator:
    def __init__(self, ast):
        self.ast = ast

    def evaluate(self):
        return self.eval_node(self.ast)

    def eval_node(self, node):
        node_type = node[0]

        if node_type == "NUMBER":
            return float(node[1]) if "." in node[1] else int(node[1])

        elif node_type == "BIN_OP":
            _, operator, left_node, right_node = node
            left_value = self.eval_node(left_node)
            right_value = self.eval_node(right_node)

            if operator == "+":
                return left_value + right_value
            elif operator == "-":
                return left_value - right_value
            elif operator == "*":
                return left_value * right_value
            elif operator == "/":
                return left_value / right_value
            else:
                raise ValueError(f"Unknown operator: {operator}")

        else:
            raise ValueError(f"Unknown node type: {node_type}")
