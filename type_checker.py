class TypeChecker:
    def __init__(self):
        self.scope = {}
        self.function_signatures = {}
        self.current_function = None

    def check(self, ast):
        for stmt in ast:
            self.check_statement(stmt)

    def check_statement(self, stmt):
        stmt_type = stmt[0]

        if stmt_type == "VAR_DECLARATION":
            self.check_variable_declaration(stmt)

        elif stmt_type == "ASSIGNMENT":
            self.check_variable_assignment(stmt)


    def check_variable_declaration(self, stmt):
        var_name = stmt[2]
        declared_type = stmt[1]
        value_type = self.check_expression(stmt[3])

        if declared_type != value_type:
            raise TypeError(f"Type mismatch in variable declaration: Expected {declared_type}, got {value_type}")

        self.scope[var_name] = declared_type

    def check_variable_assignment(self, stmt):
        var_name = stmt[1]
        if var_name not in self.scope:
            raise TypeError(f"Undefined variable: {var_name}")

        expected_type = self.scope[var_name]
        value_type = self.check_expression(stmt[2])

        if expected_type != value_type:
            raise TypeError(f"Type mismatch in assignment: {var_name} expected {expected_type}, got {value_type}")

    def check_function_definition(self, stmt):
        # TODO
        return

    def check_function_call(self, stmt):
        # TODO
        return "int"

    def check_expression(self, expr):
        expr_type = expr[0]

        if expr_type == "NUMBER":
            return "int"  # Assume all numbers are integers

        elif expr_type == "STRING":
            return "string"

        elif expr_type == "BOOLEAN":
            return "bool"

        elif expr_type == "IDENTIFIER":
            var_name = expr[1]
            if var_name not in self.scope:
                raise TypeError(f"Undefined variable: {var_name}")
            return self.scope[var_name]

        elif expr_type == "BIN_OP":
            left_type = self.check_expression(expr[2])
            right_type = self.check_expression(expr[3])
            operator = expr[1]

            if operator in {"+", "-", "*", "/"}:
                if left_type != "int" or right_type != "int":
                    raise TypeError(f"Operator '{operator}' expects two integers")
                return "int"

            elif operator in {"==", "!=", "<", ">", "<=", ">="}:
                if left_type != right_type:
                    raise TypeError(f"Comparison operator '{operator}' requires matching types")
                return "bool"

            elif operator in {"&&", "||"}:
                if left_type != "bool" or right_type != "bool":
                    raise TypeError(f"Logical operator '{operator}' expects boolean operands")
                return "bool"

            else:
                raise TypeError(f"Unknown binary operator: {operator}")

        elif expr_type == "FUNCTION_CALL":
            return self.check_function_call(expr)

        else:
            raise TypeError(f"Unknown expression type: {expr_type}")

