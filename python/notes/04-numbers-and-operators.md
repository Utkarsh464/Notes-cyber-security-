# Numbers and Operators

python has ints, floats, and complex numbers. also `Decimal` for precise math and `Fraction` for rational.

## Integers

arbitrary precision — as big as memory allows:

```python
x = 42
y = 2 ** 1000          # no overflow in python
```

use underscores for readability with big numbers:

```python
million = 1_000_000
port_range = 1_024
```

different bases:

```python
hex_val = 0xFF          # 255
oct_val = 0o77          # 63
bin_val = 0b1010        # 10

# convert TO different bases
bin(255)       # "0b11111111"
oct(255)       # "0o377"
hex(255)       # "0xff"
hex(3735928559)  # "0xdeadbeef"
```

## Floats — Watch Out

floats are IEEE 754 double-precision (64-bit). they're not exact:

```python
print(0.1 + 0.2)        # 0.30000000000000004  — not 0.3!
print(0.1 + 0.2 == 0.3) # False
```

this isn't a python bug, it's how floats work everywhere. for accurate comparisons:

```python
import math
print(math.isclose(0.1 + 0.2, 0.3))  # True

# or use Decimal for exact math
from decimal import Decimal
Decimal("0.1") + Decimal("0.2") == Decimal("0.3")  # True
```

## Arithmetic Operators

```python
10 + 3    # 13
10 - 3    # 7
10 * 3    # 30
10 / 3    # 3.333...  — always returns float
10 // 3   # 3   — floor division
10 % 3    # 1   — modulus
10 ** 3   # 1000  — exponent

# negative floor division floors DOWN
-10 // 3  # -4
10 // -3  # -4
```

## Augmented Assignment

```python
x = 10
x += 3      # x = 13
x -= 3      # x = 10
x *= 2      # x = 20
x /= 4      # x = 5.0 (becomes float)
x //= 2     # x = 2.0
x **= 3     # x = 8.0
```

## Comparison Operators

```python
x = 5
x == 5    # True
x != 5    # False
x > 3     # True
x < 3     # False

# chaining
1 < x < 10       # True — same as 1 < x and x < 10
```

## Logical Operators

```python
True and False  # False
True or False   # True
not True        # False

# short-circuit: returns the first value that determines the result
result = None or "default"   # "default"
result = "first" or "second" # "first"

# handy for defaults
host = user_input or "localhost"
```

## Bitwise Operators — Useful for Low-Level Stuff

```python
a = 0b1100   # 12
b = 0b1010   # 10

a & b   # 0b1000 = 8   — AND
a | b   # 0b1110 = 14  — OR
a ^ b   # 0b0110 = 6   — XOR
~a      # -13  — NOT (two's complement)
a << 1  # 0b11000 = 24 — left shift (multiply by 2)
a >> 1  # 0b0110 = 6   — right shift (divide by 2)
```

practical stuff:

```python
# check permissions bits
perms = 0o755
is_executable = bool(perms & 0o111)

# extract IP octets from a 32-bit int
ip = 0xC0A80101  # 192.168.1.1
o1 = (ip >> 24) & 0xFF  # 192
o2 = (ip >> 16) & 0xFF  # 168
o3 = (ip >> 8) & 0xFF   # 1
o4 = ip & 0xFF          # 1

# XOR "encryption" (really just obfuscation)
data = b"secret"
key = 0xAB
enc = bytes(b ^ key for b in data)
dec = bytes(b ^ key for b in enc)
print(dec)  # b"secret"
```

## Type Conversion

```python
int("42")           # 42
int(3.99)           # 3  — truncates toward zero
int("0xFF", 16)     # 255
int("1010", 2)      # 10
float("3.14")       # 3.14
float("inf")        # infinity
float("nan")        # not a number
str(100)            # "100"
```

fun fact: `bool` is a subclass of `int`:

```python
print(True + True)   # 2
print(False * 5)     # 0
```

## Random Numbers

```python
import random

random.random()           # 0.0 <= float < 1.0
random.randint(1, 100)    # 1 <= int <= 100
random.choice(["a", "b", "c"])
random.shuffle(cards)     # shuffles in-place

# cryptographically secure (use this for real stuff)
import secrets
token = secrets.token_hex(16)        # 32-char hex string
secure_int = secrets.randbelow(1000)
```

## Gotchas

```python
# 1. always float division in python 3
5 / 2   # 2.5
5 // 2  # 2

# 2. float comparison
0.1 + 0.2 == 0.3   # False!

# 3. mixing types
"10" + 5          # TypeError

# 4. nan is weird — never equals itself
float("nan") == float("nan")  # False
import math
math.isnan(float("nan"))      # True — use this
```
