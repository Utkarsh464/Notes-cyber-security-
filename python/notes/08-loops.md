# Loops — Iterating Through Data with for and while

Process lists of IPs, read log lines, brute-force directories — loops make it repeatable.

## For Loop

```python
for i in range(5):
    print(i)          # 0 1 2 3 4

for i in range(2, 6):
    print(i)          # 2 3 4 5

for i in range(0, 10, 2):
    print(i)          # 0 2 4 6 8
```

## Looping Over Collections

```python
for char in "hello":
    print(char)

for item in [1, 2, 3]:
    print(item)

for key, val in {"a": 1, "b": 2}.items():
    print(f"{key}: {val}")
```

## While Loop

```python
count = 0
while count < 5:
    print(count)
    count += 1
```

## Break and Continue

```python
for i in range(10):
    if i == 3:
        continue      # skip 3
    if i == 7:
        break         # stop at 7
    print(i)
```

## Else with Loops

```python
for i in range(5):
    print(i)
else:
    print("loop finished normally")

# else runs only if no break happened
```
