from evaluator import Evaluator
from lexer import Lexer
from token_parser import TokenParser
from type_checker import TypeChecker

text = """
list<str> x = ["test", "abc", "text"]
print(x)
x[2] = "new value"
print(x)
print(x.length())

int l = 0
print(l)
int i = 0
while i < 10
    i = i + 1
    if i == 3
        continue
    if i == 6
        break
    print(i)

int a = 1 + 2
if a == 3
    print("Hello there!")
else
    print("Value of a: {a}")

int add(int x, int y)
    return x + y

int multiply(int x, int y) 
    return x * y
    
print(multiply(add(2, 3), 2))
"""

lexer = Lexer(text)
tokens = lexer.tokenize()
for token in tokens:
    print(token)

parser = TokenParser(tokens)
ast = parser.parse()
print(ast)

type_checker = TypeChecker()
type_checker.check(ast)

evaluator = Evaluator()
evaluator.evaluate(ast)
