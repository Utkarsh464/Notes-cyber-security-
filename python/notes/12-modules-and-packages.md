# Modules and Packages — Importing, Organizing, and Using Libraries

Split your tools into modules, reuse code, and tap into Python's massive ecosystem.

## Importing Modules

```python
import math
print(math.sqrt(16))  # 4.0

from math import sqrt, pi
print(sqrt(25))       # 5.0
print(pi)             # 3.14...

from math import *
# imports everything (not recommended)
```

## Creating a Module

Save this as `tools.py`:

```python
def scan_port(ip, port):
    print(f"scanning {ip}:{port}")

def get_banner(socket):
    return socket.recv(1024)
```

Use it in another file:

```python
import tools

tools.scan_port("10.0.0.1", 22)
```

## Useful Standard Library Modules

- `os` — operating system interface
- `sys` — system-specific parameters
- `socket` — network connections
- `re` — regular expressions
- `json` — JSON parsing
- `subprocess` — run system commands
- `datetime` — date and time
- `argparse` — command-line arguments

## Installing Third-Party Packages

```bash
pip install requests
pip install scapy
pip install paramiko
```

```python
import requests
response = requests.get("https://example.com")
print(response.status_code)
```
