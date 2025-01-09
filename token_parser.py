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

    def parse_expression(self):
        node = self.parse_term()
        while self.current_token() and self.current_token().type == "OPERATOR":
            op = self.eat("OPERATOR")
            right = self.parse_term()
            node = ("BIN_OP", op.value, node, right)
        return node

    def parse_term(self):
        token = self.current_token()
        if token.type == "NUMBER":
            self.eat("NUMBER")
            return ("NUMBER", token.value)
        elif token.type == "IDENTIFIER":
            self.eat("IDENTIFIER")
            return ("IDENTIFIER", token.value)
        elif token.type == "PARENTHESES" and token.value == "(":
            self.eat("PARENTHESES")
            node = self.parse_expression()
            self.eat("PARENTHESES")  # Expect ')'
            return node
        else:
            raise SyntaxError(f"Unexpected token {token}")
