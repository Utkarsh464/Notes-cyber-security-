# Networking Cheatsheet — TCP/IP, DNS, HTTP, Subnetting

> Personal notes by Utkarsh Solanki | Cybersecurity & AI Student  
> GitHub: [github.com/Utkarsh464](https://github.com/Utkarsh464) | LinkedIn: [linkedin.com/in/utkarsh-solanki-337806252](https://linkedin.com/in/utkarsh-solanki-337806252)

---

## Table of Contents

- [OSI Model Quick Reference](#osi-model-quick-reference)
- [TCP/IP](#tcpip)
- [DNS](#dns)
- [HTTP / HTTPS](#http--https)
- [Subnetting](#subnetting)
- [Common Ports](#common-ports)

---

## OSI Model Quick Reference

| Layer | Number | Protocol Examples | What it does |
|-------|--------|-------------------|--------------|
| Application | 7 | HTTP, DNS, FTP, SMTP | User-facing services |
| Presentation | 6 | SSL/TLS, JPEG, ASCII | Encoding, encryption |
| Session | 5 | NetBIOS, RPC | Session management |
| Transport | 4 | TCP, UDP | End-to-end delivery |
| Network | 3 | IP, ICMP, ARP | Routing |
| Data Link | 2 | Ethernet, MAC | Node-to-node |
| Physical | 1 | Cables, Hubs | Raw bits |

> **Memory trick:** All People Seem To Need Data Processing (top to bottom)

---

## TCP/IP

### TCP vs UDP

| Feature | TCP | UDP |
|---------|-----|-----|
| Connection | Connection-oriented | Connectionless |
| Reliability | Guaranteed delivery | Best-effort |
| Speed | Slower | Faster |
| Order | Ordered packets | No ordering |
| Use case | HTTP, SSH, FTP | DNS, VoIP, streaming |

### TCP 3-Way Handshake

```
Client ──── SYN ────────────────► Server
Client ◄─── SYN-ACK ────────────  Server
Client ──── ACK ────────────────► Server
       [Connection Established]
```

- **SYN** — Client says "I want to connect, my seq = X"
- **SYN-ACK** — Server says "OK, my seq = Y, ack = X+1"
- **ACK** — Client confirms "ack = Y+1, we're connected"

### TCP 4-Way Termination

```
Client ──── FIN ────► Server
Client ◄─── ACK ────  Server
Client ◄─── FIN ────  Server
Client ──── ACK ────► Server
```

### TCP Flags (Know these for Wireshark/Recon)

| Flag | Meaning |
|------|---------|
| SYN | Synchronize — initiate connection |
| ACK | Acknowledge — confirm receipt |
| FIN | Finish — close connection |
| RST | Reset — abruptly terminate |
| PSH | Push — send data immediately |
| URG | Urgent — prioritize data |

### TCP Header Fields

| Field | Size | Purpose |
|-------|------|---------|
| Source Port | 16 bits | Sender port |
| Destination Port | 16 bits | Receiver port |
| Sequence Number | 32 bits | Byte ordering |
| Acknowledgment | 32 bits | Next expected byte |
| Flags | 9 bits | Control bits (SYN, ACK, etc.) |
| Window Size | 16 bits | Flow control |
| Checksum | 16 bits | Error detection |

### IP Header Fields (IPv4)

| Field | Purpose |
|-------|---------|
| Version | IPv4 or IPv6 |
| TTL (Time to Live) | Hop limit — decremented at each router |
| Protocol | Encapsulated protocol (6=TCP, 17=UDP, 1=ICMP) |
| Source IP | Sender's IP address |
| Destination IP | Receiver's IP address |

### ICMP (Used in ping, traceroute)

| Type | Meaning |
|------|---------|
| 0 | Echo Reply (ping response) |
| 3 | Destination Unreachable |
| 8 | Echo Request (ping) |
| 11 | Time Exceeded (TTL = 0, used in traceroute) |

```bash
# Useful commands
ping 8.8.8.8             # ICMP echo request
traceroute 8.8.8.8       # Trace hops to destination
```

---

## DNS

### What is DNS?

DNS (Domain Name System) = Internet's phonebook.  
Translates human-readable domain names → IP addresses.

```
Browser types: google.com
      ↓
DNS Resolver queries → Root Server → TLD Server (.com) → Authoritative Server
      ↓
Returns: 142.250.195.46
      ↓
Browser connects to IP
```

### DNS Record Types

| Record | Purpose | Example |
|--------|---------|---------|
| A | Domain → IPv4 | `google.com → 142.250.195.46` |
| AAAA | Domain → IPv6 | `google.com → 2607:f8b0::...` |
| CNAME | Alias to another domain | `www → google.com` |
| MX | Mail server | `mail.google.com` |
| TXT | Text info (SPF, DKIM, verification) | `v=spf1 include:...` |
| NS | Authoritative nameserver | `ns1.google.com` |
| PTR | Reverse lookup — IP → domain | `142.250.195.46 → google.com` |
| SOA | Start of Authority — zone info | Primary NS, serial |

### DNS Lookup Flow

1. Browser checks **local cache**
2. Checks **OS cache** (`/etc/hosts`)
3. Queries **Recursive Resolver** (usually ISP or 8.8.8.8)
4. Resolver queries **Root Name Servers** (.)
5. Root refers to **TLD server** (.com, .in, etc.)
6. TLD refers to **Authoritative server** (e.g., ns1.google.com)
7. Authoritative returns the **A record**
8. Resolver **caches** and returns to client

### DNS Commands

```bash
# Basic lookup
nslookup google.com
dig google.com

# Specific record types
dig google.com MX
dig google.com TXT
dig google.com NS

# Reverse DNS lookup
dig -x 8.8.8.8

# Use specific DNS server
dig @8.8.8.8 google.com

# Trace full resolution path
dig +trace google.com

# Check zone transfer (potential vuln)
dig axfr @ns1.target.com target.com
```

### Security Notes

| Attack | What happens |
|--------|-------------|
| DNS Spoofing / Cache Poisoning | Attacker injects fake DNS responses → redirect to malicious IP |
| DNS Zone Transfer (AXFR) | Misconfigured server leaks all DNS records — useful in recon |
| DNS Amplification (DDoS) | Small query → large response, reflected to victim |
| Subdomain Enumeration | Enumerate subdomains to find hidden attack surface |

```bash
# Subdomain enum tools
subfinder -d target.com
amass enum -d target.com
```

---

## HTTP / HTTPS

### HTTP Request Structure

```
GET /index.html HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0
Accept: text/html
Cookie: session=abc123
```

### HTTP Response Structure

```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1024
Set-Cookie: session=abc123; HttpOnly; Secure

<html>...</html>
```

### HTTP Methods

| Method | Purpose | Idempotent |
|--------|---------|-----------|
| GET | Retrieve data | Yes |
| POST | Submit data | No |
| PUT | Replace resource | Yes |
| PATCH | Partial update | No |
| DELETE | Remove resource | Yes |
| HEAD | Like GET but no body | Yes |
| OPTIONS | Check allowed methods | Yes |

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 301 | Moved Permanently |
| 302 | Found (Redirect) |
| 400 | Bad Request |
| 401 | Unauthorized (not logged in) |
| 403 | Forbidden (logged in, no permission) |
| 404 | Not Found |
| 405 | Method Not Allowed |
| 500 | Internal Server Error |
| 502 | Bad Gateway |
| 503 | Service Unavailable |

### HTTPS

- HTTP + TLS (Transport Layer Security)
- Default port: **443** (HTTP = **80**)
- TLS handshake occurs before HTTP data flows
- Certificate verifies server identity (CA-signed)

### TLS Handshake (simplified)

```
Client ──── ClientHello (supported ciphers) ────► Server
Client ◄─── ServerHello + Certificate ──────────  Server
Client      [Verify cert against CA]
Client ──── Key exchange ────────────────────────► Server
       [Encrypted session begins]
```

### Security-Relevant HTTP Headers

| Header | Purpose |
|--------|---------|
| `Strict-Transport-Security` | Force HTTPS (HSTS) |
| `Content-Security-Policy` | Restrict resource origins (prevents XSS) |
| `X-Frame-Options` | Prevent clickjacking |
| `X-Content-Type-Options: nosniff` | Prevent MIME sniffing |
| `Set-Cookie: HttpOnly; Secure` | Protect cookies |

### HTTP Versions

| Version | Key Change |
|---------|-----------|
| HTTP/1.0 | One request per connection |
| HTTP/1.1 | Persistent connections, pipelining |
| HTTP/2 | Multiplexing, binary, header compression |
| HTTP/3 | QUIC protocol (UDP-based), faster |

---

## Subnetting

### Why Subnetting?

- Divide a large network into smaller sub-networks
- Reduces broadcast traffic
- Improves security and management

### IPv4 Address Structure

```
192.168.1.100 / 24
│             │  └── Subnet Mask = 24 bits
│             └───── Host part
└─────────────────── Network part
```

An IPv4 address = **32 bits** = 4 octets (8 bits each)

### CIDR to Subnet Mask

| CIDR | Subnet Mask | Hosts |
|------|-------------|-------|
| /8 | 255.0.0.0 | 16,777,214 |
| /16 | 255.255.0.0 | 65,534 |
| /24 | 255.255.255.0 | 254 |
| /25 | 255.255.255.128 | 126 |
| /26 | 255.255.255.192 | 62 |
| /27 | 255.255.255.224 | 30 |
| /28 | 255.255.255.240 | 14 |
| /29 | 255.255.255.248 | 6 |
| /30 | 255.255.255.252 | 2 |
| /32 | 255.255.255.255 | 1 (host route) |

> **Formula:** Usable hosts = 2^(32 - prefix) - 2

### Subnetting Example

**Network:** `192.168.1.0/24`

| Component | Value |
|-----------|-------|
| Network Address | 192.168.1.0 |
| Subnet Mask | 255.255.255.0 |
| First Usable | 192.168.1.1 |
| Last Usable | 192.168.1.254 |
| Broadcast | 192.168.1.255 |
| Total Hosts | 254 |

### Private IP Ranges (RFC 1918)

| Range | CIDR | Use |
|-------|------|-----|
| 10.0.0.0 – 10.255.255.255 | /8 | Large enterprise |
| 172.16.0.0 – 172.31.255.255 | /12 | Medium networks |
| 192.168.0.0 – 192.168.255.255 | /16 | Home/small office |

### Special Addresses

| Address | Purpose |
|---------|---------|
| 127.0.0.1 | Loopback (localhost) |
| 0.0.0.0 | Default route / unspecified |
| 255.255.255.255 | Limited broadcast |
| 169.254.x.x | APIPA (no DHCP found) |

### Quick Subnetting Trick

For a `/26`:
- Hosts per subnet = 2^(32-26) - 2 = 64 - 2 = **62**
- Subnets from /24 = 2^(26-24) = **4 subnets**
- Subnet ranges: `.0`, `.64`, `.128`, `.192`

```bash
# Subnetting tools
ipcalc 192.168.1.0/26
python3 -c "import ipaddress; print(list(ipaddress.ip_network('192.168.1.0/26').hosts()))"
```

---

## Common Ports

| Port | Protocol | Service |
|------|----------|---------|
| 21 | TCP | FTP |
| 22 | TCP | SSH |
| 23 | TCP | Telnet (insecure) |
| 25 | TCP | SMTP |
| 53 | TCP/UDP | DNS |
| 67/68 | UDP | DHCP |
| 80 | TCP | HTTP |
| 110 | TCP | POP3 |
| 143 | TCP | IMAP |
| 443 | TCP | HTTPS |
| 445 | TCP | SMB |
| 3306 | TCP | MySQL |
| 3389 | TCP | RDP |
| 8080 | TCP | HTTP Alt |
| 8443 | TCP | HTTPS Alt |

```bash
# Port scanning
nmap -sV -p 22,80,443 192.168.1.1
nmap -p- --open 192.168.1.0/24
```

---

*Last updated: June 2026*
