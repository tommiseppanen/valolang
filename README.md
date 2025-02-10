# valolang
Experimental programming language. I have been developing this to understand how interpreters and compilers work behind the scenes. P.S. ChatGPT has been used to help with the implementation.

## Examples:
Hello World
```
print("Hello World")
```

Assignment
```
int a = 1 + 2
print("Value of a: {a}")
```

Functions
```
int add(int x, int y)
    return x + y
int multiply(int x, int y)
    return x * y
print(multiply(add(2, 3), 2))
```

If statement
```
int a = 1 + 2
if a == 3
    print("Hello there!")
else
    print("Value of a: {a}")
```

While statement
```
int i = 0
while i < 10
    i = i + 1
    if i == 3
        continue
    if i == 6
        break
    print(i)
```

Lists
```
list<str> x = ["test", "abc", "text"]
x[2] = "new value"
print(x)
print(x.length())
```

Comments
```
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
```
