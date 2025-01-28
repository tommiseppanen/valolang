from evaluator import Evaluator
from lexer import Lexer
from token_parser import TokenParser




text = """
i = 0
while i < 5
    print(i)
    i = i + 1

print("Hello world")
a = 1 + 2
if a == 3
    print("Hello there!")
else
    print("Value of a: {a}")
    
def add(x, y)
    x + y

def multiply(x, y) 
    x * y
    
multiply(add(2, 3), 2)
"""
lexer = Lexer(text)
tokens = lexer.tokenize()
for token in tokens:
    print(token)

parser = TokenParser(tokens)
ast = parser.parse()
print(ast)

evaluator = Evaluator()
print(f"Result: {evaluator.evaluate(ast)}")
