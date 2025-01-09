from evaluator import Evaluator
from lexer import Lexer, rules
from token_parser import TokenParser


lexer = Lexer(rules)

text = "1 + 2"
tokens = lexer.tokenize(text)
for token in tokens:
    print(token)

parser = TokenParser(tokens)
ast = parser.parse_expression()
print(ast)

evaluator = Evaluator(ast)
print(f"Result: {evaluator.evaluate()}")
