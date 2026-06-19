# Tuples, Sets, and Dictionaries — Immutable, Unique, and Key-Value Collections

Tuples for fixed data, sets for deduplication, dicts for lookups — essential for security tooling.

## Tuples

Tuples are ordered and immutable. Useful for data that shouldn't change.

```python
coords = (10, 20)
single = (5,)      # comma needed

x, y = coords      # unpacking
print(x)           # 10
```

## Sets

Sets are unordered collections of unique items.

```python
unique_ports = {22, 80, 443, 22}
# {80, 443, 22}  — duplicates removed

unique_ports.add(8080)
unique_ports.remove(80)

{1, 2, 3} | {3, 4, 5}  # union: {1, 2, 3, 4, 5}
{1, 2, 3} & {3, 4, 5}  # intersection: {3}
{1, 2, 3} - {3, 4, 5}  # difference: {1, 2}
```

## Dictionaries

Dictionaries store key-value pairs.

```python
user = {
    "name": "alice",
    "role": "admin",
    "age": 30
}

user["name"]               # "alice"
user.get("email", "N/A")   # "N/A" (safe access)
user["email"] = "alice@hack.com"

user.keys()    # dict_keys(["name", "role", "age"])
user.values()  # dict_values(["alice", "admin", 30])
user.items()   # key-value pairs

for key, val in user.items():
    print(f"{key}: {val}")
```
