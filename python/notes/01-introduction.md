# Introduction to Python

python is a high-level interpreted language. super popular in cyber for automation, scripting, tool dev, exploit prototyping.

## Why Python?

- easy to read/write, clean syntax
- huge standard lib — networking, file io, regex, os stuff built in
- great for quick prototypes — can write a port scanner in like 20 lines
- used in nmap, sqlmap, burp extensions, tons of custom exploits
- huge ecosystem: requests, scapy, paramiko, impacket

## Python Implementations

the main one is **CPython** (written in C, compiles to bytecode then interprets). others:

- **PyPy** — JIT compiled, faster for long running stuff
- **Cython** — lets you write C-like extensions
- **MicroPython** — for embedded devices

for most stuff including CTFs just use CPython.

## First Program

```python
print("Hello, world!")
```

python runs line by line. `print()` outputs to console.

## The `__name__ == "__main__"` Thing

when you run a file directly, `__name__` is `"__main__"`. when you import it, `__name__` is the module name. use this to make files that work both ways:

```python
# scanner.py
def scan(ip):
    print(f"scanning {ip}")

if __name__ == "__main__":
    scan("192.168.1.1")
```

now `python3 scanner.py` runs the scan, but `import scanner` doesn't auto-run anything.

## Shebang Line (Linux)

add this at the top of a .py file to make it executable directly:

```python
#!/usr/bin/env python3
```

then `chmod +x script.py` and run `./script.py`

## Ways to Run Python

1. **interactive** — type `python3` in terminal, good for testing quick stuff
2. **script mode** — `python3 file.py`
3. **as module** — `python3 -m http.server 8080`
4. **one-liner** — `python3 -c "print('yo')"` — super useful for quick automation

the `-c` flag is handy:

```bash
python3 -c "import socket; print(socket.gethostbyname('example.com'))"
```

## Comments

```python
# this is a comment
print("hello")  # inline comment too

"""
multi-line strings can act as comments
but they're actually string literals
that just get ignored
"""
```

## Docstrings

these document functions/classes and are accessible at runtime via `help()`:

```python
def scan_port(ip, port):
    """scan a single port on target ip.

    args:
        ip: target ip as string
        port: port number as int

    returns:
        true if open, false otherwise
    """
    return True
```

## Virtual Environments

always use venvs to avoid dependency hell:

```bash
python3 -m venv myenv
source myenv/bin/activate
pip install requests scapy
deactivate
```

i keep different envs for different toolchains (web testing, network tools, exploit dev).

## Random Tips

- **indentation matters** — python uses 4 spaces (usually) for blocks. DON'T mix tabs and spaces.
- **python 2 is dead** — EOL was 2020, everything here is python 3.8+
- **`print` is a function** — needs parentheses in python 3
