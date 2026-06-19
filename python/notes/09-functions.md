# Functions — Writing Reusable and Modular Code

Build once, use everywhere — scan, parse, connect, log. Functions are the backbone of every security tool.

## Defining a Function

```python
def greet(name):
    print(f"hello, {name}")

greet("alice")
```

## Return Values

```python
def add(a, b):
    return a + b

result = add(3, 5)   # 8
```

## Default Arguments

```python
def scan(host, port=80):
    print(f"scanning {host}:{port}")

scan("192.168.1.1")          # port 80
scan("192.168.1.1", 443)     # port 443
```

## Keyword Arguments

```python
def connect(host, port, protocol):
    print(f"{protocol}://{host}:{port}")

connect(host="10.0.0.1", port=22, protocol="ssh")
```

## Variable Number of Arguments

```python
def total(*args):
    return sum(args)

def print_info(**kwargs):
    for k, v in kwargs.items():
        print(f"{k}: {v}")

total(1, 2, 3, 4)        # 10
print_info(name="alice", age=25)
```

## Scope

```python
x = 10  # global

def my_func():
    x = 5  # local — different variable
    print(x)  # 5

my_func()
print(x)  # 10
```
