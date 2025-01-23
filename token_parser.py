from lexer import Lexer, rules


class TokenParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, token_type):
        token = self.current_token()
        if token and token.type == token_type:
            self.pos += 1
            return token
        else:
            raise SyntaxError(f"Expected {token_type}, got {token}")

    def parse(self):
        statements = []
        while self.current_token() is not None:
            statements.append(self.statement())
        return statements

    def assignment(self):
        identifier = self.eat("IDENTIFIER").value
        self.eat("ASSIGN")
        value = self.expression()
        return "ASSIGNMENT", identifier, value

    def function_definition(self):
        self.eat("DEF")
        name = self.eat("IDENTIFIER").value
        self.eat("LPAREN")
        parameters = self.parameter_list()
        self.eat("RPAREN")
        self.eat("LBRACE")
        body = self.expression()
        self.eat("RBRACE")
        return "FUNCTION_DEF", name, parameters, body

    def parameter_list(self):
        parameters = []
        if self.current_token().type == "IDENTIFIER":
            parameters.append(self.eat("IDENTIFIER").value)
            while self.current_token() and self.current_token().type == "COMMA":
                self.eat("COMMA")
                parameters.append(self.eat("IDENTIFIER").value)
        return parameters

    def statement(self):
        if self.current_token().type == 'DEF':
            return self.function_definition()
        elif self.current_token().type == 'IDENTIFIER' and self.peek_next().type == 'ASSIGN':
            return self.assignment()
        elif self.current_token().type == 'IDENTIFIER':
            return self.function_call()
        else:
            raise SyntaxError(f"Unexpected token {self.current_token()}")

    def peek_next(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return None

    def expression(self):
        node = self.term()
        while self.current_token() and self.current_token().type == 'OPERATOR':
            op = self.eat('OPERATOR').value
            right = self.term()
            node = ('BIN_OP', op, node, right)
        return node

    def function_call(self):
        name = self.eat("IDENTIFIER").value
        self.eat("LPAREN")
        args = self.argument_list()
        self.eat("RPAREN")
        return "FUNCTION_CALL", name, args

    def term(self):
        token = self.current_token()
        if token.type == 'NUMBER':
            return 'NUMBER', self.eat('NUMBER').value
        elif token.type == 'IDENTIFIER':
            # Look ahead to check if it's a function call
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == 'LPAREN':
                return self.function_call()
            else:
                return 'IDENTIFIER', self.eat('IDENTIFIER').value
        elif token.type == 'STRING':
            # Check if the string contains placeholders `{}` for interpolation
            string_value = self.eat('STRING').value[1:-1]  # Remove quotes
            if '{' in string_value and '}' in string_value:
                return self.parse_interpolated_string(string_value)
            else:
                return 'STRING', string_value
        elif token.type == 'LPAREN':
            # Handle parentheses for grouping
            self.eat('LPAREN')
            expr = self.expression()
            self.eat('RPAREN')
            return expr

    def argument_list(self):
        args = []
        if self.current_token().type != "RPAREN":  # Non-empty argument list
            args.append(self.expression())
            while self.current_token() and self.current_token().type == "COMMA":
                self.eat("COMMA")
                args.append(self.expression())
        return args

    def parse_interpolated_string(self, string):
        parts = []
        current = ''
        i = 0

        while i < len(string):
            if string[i] == '{':
                # Flush the current literal part
                if current:
                    parts.append(current)
                    current = ''

                # Parse the embedded expression inside {}
                i += 1
                expr_start = i
                while i < len(string) and string[i] != '}':
                    i += 1
                if i >= len(string):
                    raise SyntaxError("Unclosed interpolation brace in string")

                embedded_expr = string[expr_start:i]
                parts.append(self.expression_from_string(embedded_expr))
            else:
                current += string[i]
            i += 1

        # Flush the final literal part
        if current:
            parts.append(current)

        return 'INTERPOLATED_STRING', parts

    def expression_from_string(self, expression_code):
        lexer = Lexer(rules)
        tokens = lexer.tokenize(expression_code)

        parser = TokenParser(tokens)
        ast = parser.expression()  # Use `expression()` to get a single expression

        return ast
