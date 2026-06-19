# Conditionals — Controlling Program Flow with if/elif/else

Every decision your tool makes — allow or block, scan or skip, alert or ignore — starts here.

## Basic Syntax

```python
age = 18

if age >= 18:
    print("you are an adult")
else:
    print("you are a minor")
```

## Multiple Conditions

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
```

## Nested Conditionals

```python
if user == "admin":
    if password == "secret":
        print("access granted")
    else:
        print("wrong password")
else:
    print("unknown user")
```

## Truthy and Falsy Values

```python
# Falsy values:
# False, None, 0, 0.0, "", [], {}, ()

if []:
    print("this won't run")

name = ""
if not name:
    print("name is empty")
```

## Ternary Operator

```python
status = "active" if logged_in else "inactive"
```
