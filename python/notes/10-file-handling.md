# File Handling — Reading, Writing, and Parsing Files

Parse auth logs, write scan results, read configs — file I/O is everywhere in security.

## Opening a File

```python
file = open("data.txt", "r")
content = file.read()
file.close()
```

Modes: `r` (read), `w` (write — overwrites), `a` (append), `r+` (read+write)

## Using With Statement (Recommended)

```python
with open("data.txt", "r") as file:
    content = file.read()
# file is auto-closed here
```

## Reading Methods

```python
with open("data.txt") as f:
    whole = f.read()           # entire file as string
    line = f.readline()        # one line
    lines = f.readlines()      # list of lines

# or loop directly
with open("data.txt") as f:
    for line in f:
        print(line.strip())
```

## Writing Files

```python
with open("output.txt", "w") as f:
    f.write("hello\n")
    f.write("world\n")

# append mode
with open("log.txt", "a") as f:
    f.write("new entry\n")
```

## Working with Paths

```python
import os

os.path.exists("data.txt")
os.path.join("folder", "file.txt")
os.remove("old.txt")
```

## Example: Reading Logs

```python
with open("access.log") as f:
    for line in f:
        if "404" in line:
            print(line.strip())
```
