# Strings

strings are sequences of characters in quotes. in python 3 they're unicode by default.

## Creating Strings

```python
single = 'hello'
double = "hello"
multi = """this is
a multi-line
string"""

# single and double quotes are the same, just be consistent
```

## Strings Are Immutable

you can't change a character in place:

```python
s = "hello"
s[0] = "H"           # TypeError

# gotta make a new string
s = "H" + s[1:]      # "Hello"
```

## Common String Methods

```python
text = "  python is cool  "

text.lower()                # "  python is cool  "
text.upper()                # "  PYTHON IS COOL  "
text.strip()                # "python is cool"
text.lstrip()               # "python is cool  "
text.rstrip()               # "  python is cool"
text.replace("cool", "powerful")
text.split()                # ["python", "is", "cool"]
text.split("i")             # ["  python ", "s cool  "]
"-".join(["a", "b", "c"])  # "a-b-c"
"python".startswith("p")    # True
"cool".endswith("cool")     # True
text.count("o")             # 2
text.find("is")             # 8 (returns -1 if not found)
"hello123".isalnum()        # True
"hello".isalpha()           # True
"123".isdigit()             # True
```

## Indexing and Slicing

0-based indexing, negative counts from the end.

```python
word = "python"
word[0]      # "p"
word[-1]     # "n"
word[0:3]    # "pyt"  — slice from 0 to 3 (exclusive)
word[:3]     # "pyt"  — start defaults to 0
word[3:]     # "hon"  — end defaults to length
word[::2]    # "pto"  — step of 2
word[::-1]   # "nohtyp"  — reverse the string
```

slicing never raises IndexError — out of bounds just gives you what's there or empty:

```python
"hi"[0:100]    # "hi"
"hi"[100:200]  # ""
```

## f-strings (Python 3.6+)

this is the modern way, use it 99% of the time:

```python
name = "alice"
role = "analyst"
print(f"{name} works as an {role}")
# alice works as an analyst

# expressions inside
port = 80
print(f"port {port} is {'open' if check_port(port) else 'closed'}")

# format specifiers
value = 3.14159
print(f"{value:.2f}")        # "3.14"
print(f"{255:08b}")          # "11111111" — binary
print(f"{255:08x}")          # "000000ff" — hex
```

## format() and %-formatting

older but you'll see them in existing code:

```python
# format()
"scanning {}:{}".format("10.0.0.1", 443)

# %-style (common in logging)
"scanning %s:%d" % ("10.0.0.1", 443)
```

## Escape Characters

```python
print("line1\nline2")       # newline
print("tab\there")          # tab
print("quote: \"hi\"")      # double quote
print("backslash: \\")      # literal backslash
```

## Raw Strings

prefix with `r` to ignore escapes. essential for regex and windows paths:

```python
# \n becomes newline without r!
path = "C:\Users\new\data"     # WRONG

path = r"C:\Users\new\data"    # correct
pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"  # ip regex
```

## Bytes and Encoding

strings are unicode. sockets and binary files use bytes. encode/decode to switch between them:

```python
# string -> bytes
"hello".encode("utf-8")    # b'hello'

# bytes -> string
b"hello".decode("utf-8")   # "hello"

# common in socket code
import socket
s = socket.socket()
s.connect(("example.com", 80))
s.send(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
response = s.recv(4096).decode("utf-8", errors="ignore")
```

## String Interning (Don't Rely On This)

CPython interns short string literals for performance, so sometimes `is` returns True for equal strings:

```python
a = "hello"
b = "hello"
print(a is b)   # True — interned

c = "hello world!"
d = "hello world!"
print(c is d)   # False — not interned

# always use == for strings
```

## Performance — Avoid += in Loops

strings are immutable so `+=` creates a new object every time:

```python
# BAD — O(n^2)
result = ""
for i in range(10000):
    result += str(i)

# GOOD — O(n), use join
parts = [str(i) for i in range(10000)]
result = "".join(parts)
```

## Membership with `in`

```python
print("admin" in "admin_user")         # True

# log analysis
log_line = '192.168.1.1 - - "GET /admin HTTP/1.1" 404'
if "404" in log_line:
    print("found a 404")
```

## Practical: Input Sanitization

```python
user_input = "admin' OR 1=1--"
dangerous = ["'", "\"", ";", "--", "/*", "*/"]
if any(c in user_input for c in dangerous):
    print("possible injection")
```
