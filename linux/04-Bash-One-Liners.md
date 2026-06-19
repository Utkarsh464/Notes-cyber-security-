# Bash One-Liners — Security & Sysadmin

> Personal notes by Utkarsh Solanki | Cybersecurity & AI Student  
> [LinkedIn](https://linkedin.com/in/utkarsh-solanki-337806252) · [GitHub](https://github.com/Utkarsh464)

---

## Recon & Enumeration

```bash
# Ping sweep — find live hosts in a subnet
for i in $(seq 1 254); do ping -c1 -W1 192.168.1.$i &>/dev/null && echo "192.168.1.$i is UP"; done

# DNS lookup for a list of domains
for d in $(cat domains.txt); do dig +short $d; done

# Grab banners from open ports
for port in 21 22 25 80 443; do echo "" | nc -w1 192.168.1.1 $port 2>/dev/null && echo "Port $port open"; done

# Subdomain brute force (basic)
for sub in $(cat wordlist.txt); do host $sub.target.com 2>/dev/null | grep "has address"; done

# HTTP status check for a list of URLs
while read url; do code=$(curl -s -o /dev/null -w "%{http_code}" "$url"); echo "$code $url"; done < urls.txt

# Check HTTP headers
curl -sI https://target.com | grep -i "server\|x-powered-by\|content-security"

# Whois + DNS in one shot
domain="example.com"; echo "=== WHOIS ===" && whois $domain; echo "=== DNS ===" && dig +short $domain; echo "=== MX ===" && dig +short MX $domain
```

---

## File & System Enumeration

```bash
# Find all config files
find /etc -name "*.conf" 2>/dev/null

# Search for passwords in files
grep -rn "password\|passwd\|secret\|api_key" /var/www/ 2>/dev/null

# Find large files (>100MB)
find / -size +100M -type f 2>/dev/null

# Find files modified in last hour
find / -mmin -60 -type f 2>/dev/null

# List all SUID binaries
find / -perm -4000 -type f -exec ls -la {} \; 2>/dev/null

# Find world-writable files
find / -perm -o+w -not -path "/proc/*" -type f 2>/dev/null

# Show all cron jobs (all users)
for user in $(cut -f1 -d: /etc/passwd); do crontab -u $user -l 2>/dev/null | grep -v "^#"; done

# Find files owned by a specific user
find / -user www-data -type f 2>/dev/null
```

---

## User & Permission Analysis

```bash
# List all users with login shells
grep -v '/nologin\|/false' /etc/passwd | cut -d: -f1

# Find users with UID 0 (root-level)
awk -F: '($3==0){print $1}' /etc/passwd

# List all sudoers
grep -v "^#" /etc/sudoers | grep -v "^$"

# Check group memberships for all users
while IFS=: read user x uid gid gecos home shell; do echo "$user: $(groups $user 2>/dev/null)"; done < /etc/passwd

# Failed SSH login attempts
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn | head -10

# Successful logins
grep "Accepted password\|Accepted publickey" /var/log/auth.log
```

---

## Network One-Liners

```bash
# Show all listening services with PID
ss -tulpn | grep LISTEN

# Find what process is using a port
lsof -i :80

# Active connections count by IP
ss -an | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn | head -10

# Quick port scan with bash (no nmap)
for port in $(seq 1 1024); do (echo >/dev/tcp/192.168.1.1/$port) 2>/dev/null && echo "Port $port open"; done

# Download and execute (dangerous — know what you're running)
curl -s https://example.com/script.sh | bash

# Get public IP
curl -s ifconfig.me

# Monitor live connections
watch -n1 'ss -an | grep ESTABLISHED | wc -l'
```

---

## Log Analysis

```bash
# Count requests per IP in Apache access log
awk '{print $1}' /var/log/apache2/access.log | sort | uniq -c | sort -rn | head -20

# Find 404 errors
grep " 404 " /var/log/apache2/access.log | awk '{print $7}' | sort | uniq -c | sort -rn

# Find POST requests (possible attacks)
grep "POST" /var/log/apache2/access.log | awk '{print $1, $7}' | sort | uniq -c | sort -rn

# Extract unique IPs from log
awk '{print $1}' /var/log/nginx/access.log | sort -u

# Find auth failures in last 100 lines
tail -100 /var/log/auth.log | grep "Failed"

# Live log monitoring
tail -f /var/log/auth.log | grep --line-buffered "Failed\|Invalid"
```

---

## Text Processing

```bash
# Extract IPs from a file
grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' file.txt

# Extract emails from a file
grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' file.txt

# Extract URLs from a file
grep -oE 'https?://[^ ]+' file.txt

# Base64 encode/decode
echo "hello" | base64
echo "aGVsbG8=" | base64 -d

# URL encode a string
python3 -c "import urllib.parse; print(urllib.parse.quote('hello world'))"

# Count occurrences of each line
sort file.txt | uniq -c | sort -rn

# Remove blank lines
grep -v "^$" file.txt

# Print specific lines (e.g., 10-20)
sed -n '10,20p' file.txt
```

---

## Useful Aliases to Add to ~/.bashrc

```bash
alias ll='ls -la'
alias gs='git status'
alias ports='ss -tulpn'
alias myip='curl -s ifconfig.me'
alias suid='find / -perm -4000 -type f 2>/dev/null'
alias www='find / -perm -o+w -type f 2>/dev/null'
alias hh='history | grep'
alias path='echo $PATH | tr ":" "\n"'
```

```bash
# Apply changes
source ~/.bashrc
```

---

*Last updated: June 2026*
