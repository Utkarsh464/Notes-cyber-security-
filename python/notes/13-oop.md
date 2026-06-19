# Object-Oriented Programming — Classes, Inheritance, and Encapsulation

Model real-world objects — scanners, exploits, listeners — as reusable classes.

## Defining a Class

```python
class Scanner:
    def __init__(self, target, port):
        self.target = target
        self.port = port

    def scan(self):
        print(f"scanning {self.target}:{self.port}")
```

## Using a Class

```python
s = Scanner("10.0.0.1", 80)
s.scan()
```

## The `__init__` Method

This is the constructor — runs when you create an object.

```python
class User:
    def __init__(self, name, role="user"):
        self.name = name
        self.role = role
        self.logged_in = False
```

## Inheritance

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return f"{self.name} says woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says meow!"
```

## Getters and Setters

```python
class Profile:
    def __init__(self):
        self._email = ""

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" in value:
            self._email = value
        else:
            print("invalid email")
```
