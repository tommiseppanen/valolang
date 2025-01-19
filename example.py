from evaluator import Evaluator
from lexer import Lexer, rules
from token_parser import TokenParser


lexer = Lexer(rules)

text = """
print("Hello world {1+2}")
def add(x, y) { x + y }
def multiply(x, y) { x * y }
multiply(add(2, 3), 2)
"""

tokens = lexer.tokenize(text)
for token in tokens:
    print(token)

parser = TokenParser(tokens)
ast = parser.parse()
print(ast)

evaluator = Evaluator()
print(f"Result: {evaluator.evaluate(ast)}")
