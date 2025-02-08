class TypeChecker:
    def __init__(self):
        self.scope = {}
        self.function_signatures = {}
        self.current_function = None
        self.loop_depth = 0

    def check(self, ast):
        for stmt in ast:
            self.check_statement(stmt)

    def check_statement(self, stmt):
        stmt_type = stmt[0]

        if stmt_type == "VAR_DECLARATION":
            self.check_variable_declaration(stmt)

        elif stmt_type == "ASSIGNMENT":
            self.check_variable_assignment(stmt)

        elif stmt_type == "INDEX_ASSIGNMENT":
            self.check_index_assignment(stmt)

        elif stmt_type == "RETURN":
            self.check_return_statement(stmt)

        elif stmt_type == "IF":
            self.check_if_statement(stmt)

        elif stmt_type == "WHILE":
            self.check_while_loop(stmt)

        elif stmt_type == "FUNCTION_DEF":
            self.check_function_definition(stmt)

        elif stmt_type == "FUNCTION_CALL":
            self.check_function_call(stmt)

        elif stmt_type == "EXPRESSION_STATEMENT":
            self.check_expression(stmt["expression"])

        elif stmt_type == "BREAK" or stmt_type == "CONTINUE":
            self.check_loop_control(stmt)

        else:
            raise TypeError(f"Unknown statement type: {stmt_type}")


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

    def check_index_assignment(self, stmt):
        var_name = stmt[1]
        if var_name not in self.scope:
            raise TypeError(f"Undefined variable: {var_name}")

        expected_type = self.scope[var_name][5:-1]
        value_type = self.check_expression(stmt[3])

        if expected_type != value_type:
            raise TypeError(f"Type mismatch in assignment: {var_name} expected {expected_type}, got {value_type}")

    def check_return_statement(self, stmt):
        if self.current_function is None:
            raise TypeError("Return statement outside of a function")

        return_type = self.check_expression(stmt[1])
        expected_type = self.current_function["return_type"]

        if return_type != expected_type:
            raise TypeError(f"Return type mismatch: Expected {expected_type}, got {return_type}")

    def check_if_statement(self, stmt):
        condition_type = self.check_expression(stmt[1])
        if condition_type != "bool":
            raise TypeError(f"If condition must be a boolean, got {condition_type}")

        for sub_stmt in stmt[2]:
            self.check_statement(sub_stmt)

        if stmt[3] is not None:
            for sub_stmt in stmt[3]:
                self.check_statement(sub_stmt)

    def check_while_loop(self, stmt):
        condition_type = self.check_expression(stmt[1])
        if condition_type != "bool":
            raise TypeError(f"While loop condition must be a boolean, got {condition_type}")

        self.loop_depth += 1
        for sub_stmt in stmt[2]:
            self.check_statement(sub_stmt)
        self.loop_depth -= 1

    def check_loop_control(self, stmt):
        if self.loop_depth == 0:
            raise TypeError(f"{stmt[0]} statement must be inside a loop")

    def check_function_definition(self, stmt):
        func_name = stmt[1]
        param_types = [param[0] for param in stmt[2]]
        return_type = stmt[4]

        self.function_signatures[func_name] = {
            "params": param_types,
            "return_type": return_type,
        }

        previous_scope = self.scope.copy()
        self.scope = {param[1]: param[0] for param in stmt[2]}
        self.current_function = {"name": func_name, "return_type": return_type}

        for sub_stmt in stmt[3]:
            self.check_statement(sub_stmt)

        # Restore previous scope
        self.scope = previous_scope
        self.current_function = None

    def check_function_call(self, stmt):
        func_name = stmt[1]
        if func_name == "print":
            return "void"

        if func_name not in self.function_signatures:
            raise TypeError(f"Undefined function: {func_name}")

        expected_params = self.function_signatures[func_name]["params"]
        given_args = stmt[2]

        if len(expected_params) != len(given_args):
            raise TypeError(f"Function {func_name} expects {len(expected_params)} arguments, got {len(given_args)}")

        for (expected_type, arg_expr) in zip(expected_params, given_args):
            arg_type = self.check_expression(arg_expr)
            if arg_type != expected_type:
                raise TypeError(f"Argument type mismatch for {func_name}: Expected {expected_type}, got {arg_type}")
        return self.function_signatures[func_name]["return_type"]

    def check_method_call(self, stmt):
        method_name = stmt[1]
        if method_name == "length":
            return "int"

        raise TypeError(f"Undefined method: {method_name}")

    def check_expression(self, expr):
        expr_type = expr[0]

        if expr_type == "NUMBER":
            return "int"  # Assume all numbers are integers

        elif expr_type == "STRING":
            return "str"

        elif expr_type == "BOOLEAN":
            return "bool"

        elif expr_type == "LIST_LITERAL":
            list_item_types = []
            for list_item in expr[1]:
                list_item_types.append(self.check_expression(list_item))
            if len(list_item_types) > 0 and [list_item_types[0]] * len(list_item_types) == list_item_types:
                return f"list<{list_item_types[0]}>"
            return "list<>"

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

        elif expr_type == "METHOD_CALL":
            return self.check_method_call(expr)

        else:
            raise TypeError(f"Unknown expression type: {expr_type}")

