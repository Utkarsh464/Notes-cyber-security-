# Wireshark — Packet Capture Analysis Notes

> Personal notes by Utkarsh Solanki | Cybersecurity & AI Student  
> GitHub: [github.com/Utkarsh464](https://github.com/Utkarsh464) | LinkedIn: [linkedin.com/in/utkarsh-solanki-337806252](https://linkedin.com/in/utkarsh-solanki-337806252)

---

## Table of Contents

- [What is Wireshark?](#what-is-wireshark)
- [Wireshark Interface Layout](#wireshark-interface-layout)
- [Capture Filters](#capture-filters)
- [Display Filters](#display-filters)
- [Protocol Analysis](#protocol-analysis)
- [Finding Suspicious Traffic](#finding-suspicious-traffic)
- [Useful Shortcuts](#useful-shortcuts)
- [Common Analysis Scenarios](#common-analysis-scenarios)
- [CLI Alternative — tcpdump](#cli-alternative--tcpdump)

---

## What is Wireshark?

Wireshark is a **network protocol analyzer** (packet sniffer). It captures raw packets from a network interface and lets you inspect each one in detail.

Used for:
- Network troubleshooting
- Protocol learning
- Detecting malicious traffic
- CTF challenges
- Bug bounty / pentesting recon (passive)

---

## Wireshark Interface Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Menu Bar                                                   │
│  Toolbar                                                    │
├─────────────────────────────────────────────────────────────┤
│  Display Filter Bar  [ tcp.port == 80               ] ▶    │
├─────────────────────────────────────────────────────────────┤
│  Packet List Pane                                           │
│  No. | Time | Source | Destination | Protocol | Length |   │
│  1   | 0.00 | 192... | 8.8.8.8     | DNS      | 74     |  │
│  2   | 0.01 | 8.8.8  | 192...      | DNS      | 112    |  │
├─────────────────────────────────────────────────────────────┤
│  Packet Details Pane (expand layers)                        │
│  ▶ Frame 1                                                  │
│  ▶ Ethernet II                                              │
│  ▶ Internet Protocol (IP)                                   │
│  ▶ Transmission Control Protocol (TCP)                      │
│  ▶ Hypertext Transfer Protocol (HTTP)                       │
├─────────────────────────────────────────────────────────────┤
│  Packet Bytes Pane (hex + ASCII dump)                       │
│  0000  00 1a 2b 3c ...   ..+<...                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Capture Filters

Applied **before** capture starts. Reduces what gets saved. Uses BPF (Berkeley Packet Filter) syntax.

```bash
# Capture only HTTP traffic
port 80

# Capture DNS
port 53

# Capture traffic to/from specific IP
host 192.168.1.1

# Capture traffic from specific IP
src host 192.168.1.1

# Capture traffic to specific IP
dst host 8.8.8.8

# Capture TCP only
tcp

# Capture UDP only
udp

# Capture specific subnet
net 192.168.1.0/24

# Capture specific port range
portrange 1-1024

# Capture non-ARP, non-DNS (reduce noise)
not arp and not port 53

# Combine filters
host 192.168.1.5 and tcp and port 443
```

---

## Display Filters

Applied **after** capture. Most powerful feature of Wireshark. Can filter without losing packets.

### Basic Syntax

```
protocol.field == value
protocol.field contains "string"
protocol.field matches "regex"
```

### IP Filters

```
ip.addr == 192.168.1.1          # Any traffic to/from this IP
ip.src == 192.168.1.1           # Only from this IP
ip.dst == 8.8.8.8               # Only to this IP
ip.addr == 192.168.1.0/24       # Whole subnet
!(ip.addr == 192.168.1.1)       # Exclude an IP
```

### TCP/UDP Filters

```
tcp                              # All TCP
tcp.port == 80                   # TCP port 80
tcp.dstport == 443               # Destination port 443
tcp.srcport == 1234              # Source port 1234
tcp.flags.syn == 1               # SYN packets
tcp.flags.syn == 1 and tcp.flags.ack == 0    # Only SYN (new connections)
tcp.flags.rst == 1               # RST packets (connection resets)
tcp.flags.fin == 1               # FIN packets (graceful close)
tcp.analysis.retransmission      # Retransmissions (indicates packet loss)
```

### HTTP Filters

```
http                             # All HTTP
http.request                     # HTTP requests only
http.response                    # HTTP responses only
http.request.method == "POST"    # POST requests
http.request.method == "GET"     # GET requests
http.response.code == 200        # 200 OK
http.response.code == 404        # 404 Not Found
http.host == "example.com"       # Requests to specific host
http.request.uri contains "login"     # URLs containing "login"
http.cookie contains "session"        # Cookies with session
```

### DNS Filters

```
dns                              # All DNS
dns.qry.name == "google.com"     # Query for specific domain
dns.qry.type == 1                # A record queries (type 1)
dns.qry.type == 28               # AAAA record queries (IPv6)
dns.flags.response == 0          # DNS questions only
dns.flags.response == 1          # DNS answers only
```

### TLS/HTTPS Filters

```
tls                              # All TLS
tls.handshake                    # TLS handshake packets
tls.handshake.type == 1          # ClientHello
tls.handshake.type == 2          # ServerHello
tls.record.content_type == 23    # Application data (encrypted)
```

### ARP Filters

```
arp                              # All ARP
arp.opcode == 1                  # ARP Request
arp.opcode == 2                  # ARP Reply
arp.duplicate-address-detected   # Potential ARP spoofing
```

### ICMP Filters

```
icmp                             # All ICMP
icmp.type == 8                   # Echo Request (ping)
icmp.type == 0                   # Echo Reply
icmp.type == 3                   # Destination Unreachable
```

### Combining Filters

```
# HTTP or DNS
http or dns

# TCP on port 80 or 443
tcp.port == 80 or tcp.port == 443

# Requests from specific IP
ip.src == 192.168.1.5 and http.request

# Exclude noise
not arp and not icmp and not dns

# Find credentials in cleartext HTTP
http.request.method == "POST" and http contains "password"
```

---

## Protocol Analysis

### Analyzing a TCP Handshake

1. Filter: `tcp.flags.syn == 1`
2. Look for SYN → SYN-ACK → ACK sequence
3. Check Stream: Right-click → Follow → TCP Stream

### Analyzing HTTP Traffic

1. Filter: `http`
2. Check `http.request` for URLs, methods, headers
3. Right-click any HTTP packet → Follow → HTTP Stream to see full conversation
4. Look at cookies, auth headers, POST bodies for credentials

### Analyzing DNS

1. Filter: `dns`
2. Look at `dns.qry.name` — what domains are being resolved
3. Unusual domains, base64-encoded subdomains = potential DNS tunneling
4. Multiple NXDOMAIN responses = subdomain brute force or C2 beacon

### Following a Stream

Right-click a packet → **Follow** → **TCP Stream** / **UDP Stream** / **HTTP Stream**

Gives you the full conversation in readable form. Critical for:
- Seeing cleartext credentials in HTTP
- Reconstructing file transfers
- Reading IRC/chat traffic

---

## Finding Suspicious Traffic

### Port Scan Detection

```
# Many SYN packets to different ports from one source = port scan
tcp.flags.syn == 1 and tcp.flags.ack == 0

# High number of RST responses = closed port scan results
tcp.flags.rst == 1
```

Signs:
- One source IP → many destination ports
- Rapid SYN packets with no completion
- Lots of RST/ICMP unreachable responses

### ARP Spoofing

```
arp
```

Signs:
- Two devices claiming same IP (different MACs for same IP)
- Duplicate ARP replies
- Wireshark shows: `Duplicate IP address detected`

### DNS Tunneling

```
dns
```

Signs:
- Extremely long subdomain queries (data encoded in subdomain)
- High frequency of DNS queries to a single domain
- Unusual query types (TXT, NULL)
- Large DNS responses

### Cleartext Credentials

```
http.request.method == "POST"
ftp
telnet
```

Signs:
- POST to `/login`, `/auth`, `/signin` endpoints
- FTP USER/PASS commands visible
- Telnet sessions with readable keystrokes

### Beaconing (C2 Traffic)

Signs:
- Regular, periodic outbound connections (every N seconds)
- Same destination IP, same interval
- Low byte counts per connection

```
# Filter and sort by time to find periodic patterns
ip.dst == [suspicious_ip]
```

---

## Useful Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+F` | Find packet |
| `Ctrl+G` | Go to packet number |
| `Ctrl+E` | Stop capture |
| `Ctrl+K` | Start capture |
| `Ctrl+Shift+P` | Preferences |
| `Ctrl+Alt+Shift+T` | Follow TCP stream |
| `Ctrl+D` | Display filter expression |
| `Space` | Mark packet |
| `F8` | Next packet |
| `F7` | Previous packet |

---

## Common Analysis Scenarios

### Scenario 1: Investigate a suspicious connection

1. `Statistics → Conversations` — see all IP pairs
2. Sort by bytes — largest transfers = most suspicious
3. Click → Apply as Filter
4. Follow stream to inspect

### Scenario 2: Extract files from HTTP capture

1. Filter: `http`
2. `File → Export Objects → HTTP`
3. Lists all downloadable objects (images, scripts, executables)
4. Save and analyze

### Scenario 3: Find credentials

```
http.request.method == "POST"
```
Then follow stream — look for `username=`, `password=`, `email=` in POST body.

### Scenario 4: Detect port scan in PCAP

```
tcp.flags.syn == 1 and tcp.flags.ack == 0
```
Statistics → Conversations → sort by packets. One source with many destinations = scan.

### Scenario 5: Analyze malware traffic (CTF / lab)

1. `Statistics → Protocol Hierarchy` — see what protocols are present
2. `Statistics → DNS` — check for unusual domains
3. `Statistics → HTTP` — check hosts and URIs contacted
4. Follow suspicious streams

---

## CLI Alternative — tcpdump

When Wireshark GUI isn't available (remote SSH, Termux, server):

```bash
# Capture all traffic on eth0
tcpdump -i eth0

# Save to file
tcpdump -i eth0 -w capture.pcap

# Read a pcap file
tcpdump -r capture.pcap

# Capture DNS traffic
tcpdump -i eth0 port 53

# Capture HTTP
tcpdump -i eth0 port 80

# Capture from specific host
tcpdump -i eth0 host 192.168.1.1

# Verbose output with ASCII
tcpdump -i eth0 -A port 80

# Verbose output with hex
tcpdump -i eth0 -X port 80

# Capture top-level TCP SYNs (port scans)
tcpdump -i eth0 'tcp[tcpflags] & tcp-syn != 0'

# Limit packet count
tcpdump -i eth0 -c 100

# Combine filters
tcpdump -i eth0 'src 192.168.1.5 and port 443'
```

> **Tip:** Capture with `tcpdump -w file.pcap` on a remote machine, then transfer and open in Wireshark locally for GUI analysis.

---

## Wireshark for CTFs — Quick Checklist

- [ ] Check `Statistics → Protocol Hierarchy` first
- [ ] Check `Statistics → Conversations` for IP pairs
- [ ] Follow TCP/HTTP streams for readable data
- [ ] Export HTTP objects (`File → Export Objects`)
- [ ] Look for base64 strings in HTTP or DNS
- [ ] Check for FTP transfers (cleartext files)
- [ ] Filter for ICMP — data may be hidden in payload (ICMP tunneling)
- [ ] Check TLS — if decryption keys provided, add in `Preferences → TLS`

---

*Last updated: June 2026*
