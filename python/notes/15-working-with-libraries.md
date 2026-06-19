# Working with Libraries — OS, Sockets, Requests, Subprocess, and More

Real security tools use `os`, `socket`, `requests`, `subprocess`, `re`, and `json` daily.

## Virtual Environments

Always use a virtual environment for projects.

```bash
python3 -m venv myenv
source myenv/bin/activate
pip install requests
```

## Requests — HTTP Library

```python
import requests

r = requests.get("https://api.github.com/users/Utkarsh464")
print(r.status_code)
print(r.json()["bio"])
```

## OS and Sys

```python
import os
import sys

os.getcwd()              # current directory
os.listdir(".")          # files in directory
os.environ["HOME"]       # environment variable
sys.argv                 # command-line arguments
sys.exit(1)              # exit with code
```

## Subprocess — Running Commands

```python
import subprocess

result = subprocess.run(["whoami"], capture_output=True, text=True)
print(result.stdout)

# or with shell=True (be careful)
subprocess.run("ping -c 1 8.8.8.8", shell=True)
```

## Socket — Network Connections

```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
result = s.connect_ex(("example.com", 80))
if result == 0:
    print("port is open")
s.close()
```

## Regex

```python
import re

pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
text = "server ip: 192.168.1.1"
match = re.search(pattern, text)
if match:
    print(match.group())  # 192.168.1.1
```

## JSON

```python
import json

data = {"name": "alice", "role": "admin"}
json_str = json.dumps(data)    # to string
parsed = json.loads(json_str)  # back to dict

# read/write JSON files
with open("config.json") as f:
    config = json.load(f)
```
