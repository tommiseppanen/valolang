import re
from language_token import LanguageToken


class Lexer:
    def __init__(self, source):
        token_rules = [
            (r"[ \t]+", None),
            (r"\/\/.*", None),  # single-line comments
            (r"\d+", "NUMBER"),
            (r"true|false", "BOOLEAN"),
            (r"if", "IF"),
            (r"else", "ELSE"),
            (r"while", "WHILE"),
            (r"break", "BREAK"),
            (r"continue", "CONTINUE"),
            (r"return", "RETURN"),
            (r"int", "TYPE_INT"),
            (r"bool", "TYPE_BOOL"),
            (r"str", "TYPE_STRING"),
            (r"void", "TYPE_VOID"),
            (r"list\s*<\s*[a-zA-Z_][a-zA-Z0-9_]*\s*>", "TYPE_LIST"),
            (r"[a-zA-Z_]\w*", "IDENTIFIER"),  # Variable/function names
            (r"[+\-*<>]|==|!=", "OPERATOR"),  # Arithmetic operators
            (r"\(", "LPAREN"),
            (r"\)", "RPAREN"),
            (r"\[", "LBRACKET"),
            (r"\]", "RBRACKET"),
            (r",", "COMMA"),
            (r"\.", "DOT"),
            (r"=", "ASSIGN"), # Variable assignment
            (r'"([^"\\]*(\\.[^"\\]*)*)"', "STRING"),  # Strings (including escaped quotes)
        ]
        self.rules = [
            (re.compile(pattern), token_type) for pattern, token_type in token_rules
        ]
        self.tokens = []
        self.line = 0
        self.column = 0
        self.text = source.splitlines()
        self.indent_stack = [0]
        self.comment_depth = 0

    def tokenize(self):
        while self.line < len(self.text):
            text_line = self.text[self.line]
            self.line += 1
            self.column = 0

            # Skip empty lines or lines with only whitespace
            if not text_line.strip():
                continue

            if self.comment_depth == 0:
                # Handle indentation
                self.tokens.extend(self.handle_indentation(text_line))

            # Tokenize the rest of the line with regex
            self.tokens.extend(self.tokenize_line(text_line))

        # Emit DEDENT tokens for remaining indentation
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(LanguageToken(type="DEDENT", value=None, line=self.line, column=self.column))
        return self.tokens

    def handle_indentation(self, text_line):
        tokens = []
        leading_spaces = len(text_line) - len(text_line.lstrip())
        self.column = leading_spaces
        current_indent = self.indent_stack[-1]

        if leading_spaces > current_indent:
            tokens.append(LanguageToken(type="INDENT", value=None, line=self.line, column=self.column))
            self.indent_stack.append(leading_spaces)
        elif leading_spaces < current_indent:
            while leading_spaces < self.indent_stack[-1]:
                self.indent_stack.pop()
                tokens.append(LanguageToken(type="DEDENT", value=None, line=self.line, column=self.column))

        return tokens

    def tokenize_line(self, text_line):
        """Tokenizes the rest of the line using regex."""
        tokens = []
        while self.column < len(text_line):

            # Start of a multi-line comment
            if text_line[self.column:self.column+2] == "/*":
                self.comment_depth += 1
                self.column += 2
                continue

            # End of a multi-line comment
            if text_line[self.column:self.column+2] == "*/" and self.comment_depth > 0:
                self.comment_depth -= 1
                self.column += 2
                continue

            # Skip characters if we are inside comment
            if self.comment_depth > 0:
                self.column += 1
                continue

            match = None
            for pattern, token_type in self.rules:
                match = pattern.match(text_line, self.column)
                if match:
                    value = match.group(0)

                    if token_type:
                        tokens.append(LanguageToken(token_type, value, self.line, self.column))

                    self.column += len(value)
                    break

            if not match:
                raise SyntaxError(
                    f"Illegal character at line: {self.line}, column: {self.column}"
                )
        return tokens