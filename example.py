from evaluator import Evaluator
from lexer import Lexer
from token_parser import TokenParser
from type_checker import TypeChecker

text = """
str a = "First part of the text in a long line. This will continue " + 
"in next line. Rest of the text in here"
print(a)

void testVoidReturn(int i)
    if i == 1
        return
    print(i)
    
testVoidReturn(1)
//regular comment

/*
Multiline comment
*/

/* 
Nested multiline comments are supported:
  /*
  Nested comment in here
  */
  // Another nested comment
*/

print("€#sdf"/*Also inline comments work*/)

print("You can use /* and */ for nested comments")
print("You can use // for regular comments")
list<str> x = ["test", "abc", "text"]
print(x)
x[2] = "new value"
print(x)
print(x.length())

int l
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

int test(list<str> s)
    return s.length()
list<str> createList()
    return ["1", "2", "3", "4"]
void myPrintInt(int i)
    print(i)
    return
myPrintInt(test(createList()))

bool myBool = true
if myBool == true
    print("true block")
else
    print("false block")

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
