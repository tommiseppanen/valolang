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
        elif self.current_token().type == 'IDENTIFIER':
            return self.function_call()
        else:
            raise SyntaxError(f"Unexpected token {self.current_token()}")

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
