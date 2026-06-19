# Error Handling — Try, Except, and Writing Robust Security Tools

Your tool will hit unexpected inputs — handle them instead of crashing mid-scan.

## Try / Except

```python
try:
    num = int(input("enter a number: "))
    print(10 / num)
except ValueError:
    print("that's not a number")
except ZeroDivisionError:
    print("can't divide by zero")
```

## Catching All Errors

```python
try:
    # risky code
    result = some_function()
except Exception as e:
    print(f"something went wrong: {e}")
```

## Else and Finally

```python
try:
    file = open("data.txt")
    content = file.read()
except FileNotFoundError:
    print("file not found")
else:
    print("file read successfully")
finally:
    print("this always runs")
```

## Custom Exceptions

```python
def check_port(port):
    if port < 1 or port > 65535:
        raise ValueError(f"invalid port: {port}")
    print(f"port {port} is valid")

try:
    check_port(70000)
except ValueError as e:
    print(e)
```

## Common Built-in Exceptions

- `FileNotFoundError`
- `PermissionError`
- `ValueError`
- `TypeError`
- `IndexError`
- `KeyError`
- `ConnectionError`
