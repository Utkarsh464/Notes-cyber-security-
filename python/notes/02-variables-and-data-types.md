# Variables and Data Types

variables store data in memory. python is dynamically typed — you don't need to declare types and a var can change type whenever.

## Basic Types

```python
name = "john"       # string (str)
age = 25            # integer (int)
price = 19.99       # float (float)
is_admin = True     # boolean (bool)
nothing = None      # NoneType
```

quick ref:

| Type | Example | Mutable? |
|------|---------|----------|
| `int` | `42` | no |
| `float` | `3.14` | no |
| `bool` | `True` | no |
| `str` | `"hello"` | no |
| `bytes` | `b"hello"` | no |
| `list` | `[1, 2, 3]` | yes |
| `tuple` | `(1, 2, 3)` | no |
| `set` | `{1, 2, 3}` | yes |
| `dict` | `{"a": 1}` | yes |
| `NoneType` | `None` | — |

## Dynamic Typing

variables don't really have types — **values** do. a variable is just a label pointing to an object:

```python
x = 42
print(type(x))      # <class 'int'>

x = "now a string"
print(type(x))      # <class 'str'>
```

for type checking use `isinstance()`, not `type()`:

```python
def process_port(port):
    if not isinstance(port, int):
        raise TypeError("port must be an integer")
    if port < 1 or port > 65535:
        raise ValueError("port out of range")
```

## Naming Rules

- letters, numbers, underscores
- must start with letter or underscore
- case-sensitive (`Name` != `name`)
- can't use keywords (`if`, `for`, `class`, `def`, etc.)
- convention: `snake_case` for vars/functions, `UPPER_SNAKE` for constants

```python
# good
target_ip = "10.0.0.1"
SCAN_TIMEOUT = 2
_private = "hidden"

# bad
targetIp = "10.0.0.1"          # camelCase, just don't
2nd_target = "nope"            # starts with number
class = "test"                 # keyword
```

## Mutable vs Immutable — Important

immutable types can't be changed — any "change" creates a new object. mutable types can be modified in place.

```python
# immutable — strings
s = "hello"
s[0] = "H"                 # TypeError!

# mutable — lists
l = [1, 2, 3]
l[0] = 99                  # works
```

this matters because shared mutable objects cause side effects:

```python
def add_malicious_ip(ip_list):
    ip_list.append("10.0.0.1")    # modifies the original!

trusted = ["192.168.1.1"]
add_malicious_ip(trusted)
print(trusted)                    # ["192.168.1.1", "10.0.0.1"]
```

pass a copy or a tuple if you want to prevent this.

## `id()` and Identity

every object has a unique id (memory address in CPython):

```python
x = 256
y = 256
print(id(x) == id(y))   # True — small ints are cached

z = 257
w = 257
print(id(z) == id(w))   # False — larger ints get new objects
```

## `is` vs `==` — Common Bug

- `==` checks **value** — "same data?"
- `is` checks **identity** — "same object in memory?"

```python
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)   # True — same values
print(a is b)   # False — different objects

# use 'is' for None (always)
if result is None:
    print("no result")
```

## Type Conversion

python does some implicit conversions but not others:

```python
# implicit — int to float
result = 10 + 3.14       # 13.14

# error — str + int doesn't work
result = "port: " + 80   # TypeError

# explicit
result = "port: " + str(80)   # "port: 80"
```

handy conversion functions:

```python
int("42")           # 42
int("0xFF", 16)     # 255 — hex string
int("1010", 2)      # 10 — binary string
float("3.14")       # 3.14
str(100)            # "100"
bool(1)             # True
bool(0)             # False
bool("")            # False — empty stuff is falsy
bool("hello")       # True
```

## None

python's null, it's a singleton. always check with `is`:

```python
result = some_function()
if result is None:
    print("no result returned")
```

## Multiple Assignment

```python
x, y, z = 1, 2, 3
a = b = c = 0

# swapping — no temp var needed
a, b = b, a

# unpacking from functions
def get_scan_result():
    return "192.168.1.1", 80, "open"

ip, port, status = get_scan_result()
```
