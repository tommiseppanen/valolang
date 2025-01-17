import re
from language_token import LanguageToken


class Lexer:
    def __init__(self, rules):
        self.rules = [
            (re.compile(pattern), token_type) for pattern, token_type in rules
        ]

    def tokenize(self, text):
        tokens = []
        line = 1
        column = 1
        idx = 0

        while idx < len(text):
            match = None
            for pattern, token_type in self.rules:
                match = pattern.match(text, idx)
                if match:
                    value = match.group(0)

                    if token_type:
                        tokens.append(LanguageToken(token_type, value, line, column))

                    idx += len(value)
                    column += len(value)

                    if token_type is None and "\n" in value:
                        line += value.count("\n")
                        column = 1

                    break

            if not match:
                raise SyntaxError(
                    f"Illegal character at line: {line}, column: {column}"
                )

        return tokens


rules = [
    (r"[ \t\n]+", None),
    (r"\d+", "NUMBER"),  # Number
    (r"def", "DEF"),  # Function definition keyword
    (r"[a-zA-Z_]\w*", "IDENTIFIER"),  # Identifiers
    (r"[+\-*/]", "OPERATOR"),  # Arithmetic operators
    (r"\(", "LPAREN"),  # Left parenthesis
    (r"\)", "RPAREN"),  # Right parenthesis
    (r",", "COMMA"),  # Comma
    (r"\{", "LBRACE"),  # Left curly brace
    (r"\}", "RBRACE"),  # Right curly brace
    (r"=", "ASSIGN"),  # Assignment
    (r"[;]", "SEMICOLON"),  # Semicolon
]
