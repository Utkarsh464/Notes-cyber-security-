# Lists

lists are ordered, mutable collections. they're probably the most used data structure in python. can hold any type, mixed types, and they grow/shrink dynamically.

## Creating Lists

```python
fruits = ["apple", "banana", "cherry"]
mixed = [1, "hello", 3.14, True, None]
empty = []
nested = [[1, 2], [3, 4], [5, 6]]

# list() constructor
chars = list("hello")       # ["h", "e", "l", "l", "o"]
nums = list(range(5))       # [0, 1, 2, 3, 4]

# repeat elements
zeros = [0] * 10            # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
pattern = [1, 2] * 3        # [1, 2, 1, 2, 1, 2]
```

## Accessing Items

```python
fruits = ["apple", "banana", "cherry", "date"]

fruits[0]       # "apple"
fruits[-1]      # "date"  (negative = from end)
fruits[-2]      # "cherry"

# slicing — returns a NEW list
fruits[0:2]     # ["apple", "banana"]
fruits[:2]      # same thing, 0 is optional
fruits[2:]      # ["cherry", "date"]
fruits[::-1]    # ["date", "cherry", "banana", "apple"] — reverse
```

slicing never errors on out-of-bounds:

```python
fruits[0:100]   # ["apple", "banana", "cherry", "date"]
fruits[100:200] # []
```

## Common Methods

```python
fruits = ["apple", "banana", "cherry"]

# adding
fruits.append("orange")         # to end
fruits.insert(1, "grape")       # at index
fruits.extend(["kiwi", "mango"])  # add multiple

# removing
fruits.remove("banana")         # by value (raises ValueError if missing)
popped = fruits.pop()           # remove & return last
popped = fruits.pop(0)          # remove & return at index

# searching
fruits.index("cherry")          # index of first match (raises ValueError)
fruits.count("apple")           # count occurrences

# sorting / reversing
fruits.sort()                   # in-place, ascending
fruits.sort(reverse=True)
fruits.reverse()

# misc
len(fruits)
"apple" in fruits               # membership check

# copy
copy1 = fruits.copy()           # shallow copy
copy2 = fruits[:]               # same thing
```

be safe with `remove()` and `index()` — they raise errors if not found:

```python
if "z" in items:
    items.remove("z")

# or catch it
try:
    items.remove("z")
except ValueError:
    pass
```

## Looping Over Lists

```python
for fruit in fruits:
    print(fruit)

# with index
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")

# multiple lists at once
ips = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]
ports = [22, 80, 443]
for ip, port in zip(ips, ports):
    print(f"scanning {ip}:{port}")
```

## List Comprehensions — Super Useful

syntax: `[expression for item in iterable if condition]`

```python
squares = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

evens = [x for x in range(20) if x % 2 == 0]

# nested loops
pairs = [(x, y) for x in [1, 2] for y in [3, 4]]
# [(1, 3), (1, 4), (2, 3), (2, 4)]

# practical — filter scan results
results = [(22, "open"), (80, "open"), (443, "closed")]
open_ports = [port for port, status in results if status == "open"]
# [22, 80]

# filter IPs
ips = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]
private = [ip for ip in ips if ip.startswith(("10.", "172.", "192.168."))]
```

they're faster than manual `for`-`append` loops.

## Nested Lists

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

matrix[0][1]   # 2

# flatten
flat = [item for row in matrix for item in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

## Copying — Shallow vs Deep

lists hold **references**, not the actual objects. this trips people up:

```python
# shallow copy — inner objects are shared
original = [[1, 2], [3, 4]]
shallow = original.copy()
shallow[0][0] = 99
print(original)     # [[99, 2], [3, 4]]  — changed!

# deep copy — fully independent
import copy
deep = copy.deepcopy(original)
deep[0][0] = 88
print(original)     # [[99, 2], [3, 4]]  — unchanged
```

for flat lists (strings, ints) shallow copy is fine since those are immutable.

## How Lists Actually Work

CPython lists are dynamic arrays (not linked lists). they overallocate space so `append()` is usually O(1) but occasionally O(n) when it needs to resize:

```python
import sys
l = []
print(sys.getsizeof(l))    # 56 bytes
l.append(1)
print(sys.getsizeof(l))    # 88 bytes (128 after resize overhead)
```

if you know the final size, preallocating is faster:

```python
# BAD — many resizes
results = []
for i in range(100000):
    results.append(i)

# GOOD — preallocate
results = [None] * 100000
for i in range(100000):
    results[i] = i

# BEST — list comp (if it fits)
results = [i for i in range(100000)]
```

## When to Use Something Else

| Need | Use |
|------|-----|
| fast index access | list |
| fast appends/popped from end | list |
| fast inserts/removals from front | `deque` |
| unique elements | `set` |
| key-value pairs | `dict` |
| immutable sequence | `tuple` |
| FIFO queue | `deque` |

```python
from collections import deque

q = deque(["a", "b", "c"])
q.append("d")          # add to right
first = q.popleft()    # "a" — O(1) from left
```

## Sorting

```python
# in-place
nums = [3, 1, 4, 1, 5]
nums.sort()

# with custom key
data = [("alice", 30), ("bob", 25), ("charlie", 35)]
data.sort(key=lambda x: x[1])  # sort by age

# sorted() returns new list, original unchanged
sorted_copy = sorted(original)

# sort is stable — equal elements keep original order
```

## Common Pitfalls

```python
# 1. Don't modify a list while iterating it
items = [1, 2, 3, 4, 5]
for item in items:          # BUG!
    if item % 2 == 0:
        items.remove(item)

# fix: iterate over a copy
for item in items.copy():
    if item % 2 == 0:
        items.remove(item)

# or use a list comp
items[:] = [x for x in items if x % 2 != 0]

# 2. Shared references with * operator
row = [0] * 3
matrix = [row] * 3          # same row object 3 times!
matrix[0][0] = 1
print(matrix)               # [[1, 0, 0], [1, 0, 0], [1, 0, 0]]

# fix:
matrix = [[0] * 3 for _ in range(3)]

# 3. Mutable default arguments
def add_item(item, items=[]):   # BAD — same list every call
    items.append(item)
    return items

print(add_item(1))  # [1]
print(add_item(2))  # [1, 2]  — same list!

# fix:
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```
