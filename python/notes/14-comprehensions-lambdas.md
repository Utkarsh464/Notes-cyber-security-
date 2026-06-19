# Comprehensions and Lambdas — Concise Iteration and Anonymous Functions

Write cleaner, faster code — transform lists, filter data, sort complex structures in one line.

## List Comprehension

```python
squares = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

even_squares = [x**2 for x in range(10) if x % 2 == 0]
# [0, 4, 16, 36, 64]
```

## Dictionary Comprehension

```python
squares_dict = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

ports = {22: "ssh", 80: "http", 443: "https"}
ports_upper = {k: v.upper() for k, v in ports.items()}
# {22: "SSH", 80: "HTTP", 443: "HTTPS"}
```

## Set Comprehension

```python
unique_lens = {len(word) for word in ["hi", "hello", "hey"]}
# {2, 3, 5}
```

## Lambda Functions

Anonymous one-line functions.

```python
square = lambda x: x ** 2
print(square(5))  # 25

# common use — sorting
data = [("alice", 30), ("bob", 25), ("charlie", 35)]
data.sort(key=lambda x: x[1])  # sort by age
print(data)
```

## Map, Filter, Reduce

```python
nums = [1, 2, 3, 4, 5]

doubled = list(map(lambda x: x * 2, nums))
# [2, 4, 6, 8, 10]

evens = list(filter(lambda x: x % 2 == 0, nums))
# [2, 4]
```
