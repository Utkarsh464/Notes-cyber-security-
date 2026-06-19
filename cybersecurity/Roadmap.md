# Cybersecurity Roadmap 2026
> Updated for 2026 job market — AI Security, Zero Trust, Cloud moved earlier, GRC/Risk added.

---

## Overview

| Phase | Topic | Duration |
|-------|-------|----------|
| 1 | IT & Networking Fundamentals | 1–2 months |
| 2 | Linux & Scripting | 1–2 months |
| 3 | Cybersecurity Fundamentals + Zero Trust | 1 month |
| 4 | Ethical Hacking & Penetration Testing | 2–4 months |
| 5 | Web Application Security | 1–2 months |
| 5.5 | AI Security ⚡ NEW | 2–3 weeks |
| 6 | Cloud Security *(moved earlier)* | 1–2 months |
| 7 | Blue Team & Defensive Security | 1–2 months |
| 8 | GRC & Risk Management ⚡ NEW | 2–4 weeks |
| 9 | Advanced Specializations | 3–6 months |

---

## Phase 1 — IT & Networking Fundamentals
> Duration: 1–2 months | Foundation layer

### Operating Systems
- [ ] Windows basics — file system, registry, user accounts
- [ ] Linux CLI — navigation, file ops, man pages
- [ ] File systems (NTFS, ext4, FAT32)
- [ ] User & group management
- [ ] Process management (Task Manager / ps / top)
- [ ] Services & daemons (systemctl, sc)

### Networking Fundamentals
- [ ] OSI model — all 7 layers, what happens at each
- [ ] TCP/IP stack — handshake, packet structure
- [ ] IP addressing & subnetting (CIDR, /24, /16 etc.)
- [ ] DNS — A, MX, CNAME, PTR records
- [ ] DHCP — lease process, DORA
- [ ] HTTP / HTTPS — methods, status codes, headers
- [ ] Routing & switching — static routes, VLANs, trunking
- [ ] Firewalls & NAT — stateful vs stateless
- [ ] VPNs — site-to-site, client VPN, split tunneling

### Hardware Basics
- [ ] CPU, RAM, storage types (HDD vs SSD vs NVMe)
- [ ] Network interface cards, switches, routers
- [ ] Virtualization concepts (hypervisor Type 1 vs Type 2)

### Resources
- Cisco NetAcad — https://netacad.com
- TryHackMe Pre-Security Path — https://tryhackme.com
- Professor Messer CompTIA A+ / Net+

---

## Phase 2 — Linux & Scripting
> Duration: 1–2 months | Core skill set

### Linux Administration
- [ ] Directory structure (`/etc`, `/var`, `/proc`, `/home`)
- [ ] File permissions — chmod, chown, SUID/SGID/Sticky bit
- [ ] Package management — apt, yum/dnf, pacman
- [ ] Cron jobs — syntax, scheduling tasks
- [ ] SSH & remote access — key-based auth, config hardening
- [ ] Logs & syslog — `/var/log`, journalctl, log rotation
- [ ] Networking commands — netstat, ss, ip, ifconfig, nmap, curl

### Bash Scripting
- [ ] Variables, conditionals, loops
- [ ] Functions and arguments
- [ ] File I/O — read, write, append
- [ ] Regex — grep, awk, sed
- [ ] Pipelines and process substitution
- [ ] Automation scripts — recon pipelines, log parsers

### Python for Security
- [ ] Data types, control flow, functions
- [ ] File handling — open, read, write
- [ ] `socket` module — TCP/UDP clients
- [ ] `requests` library — HTTP automation
- [ ] `subprocess` and `os` modules
- [ ] Build a basic port scanner
- [ ] Script automation — API calls, parsing output

### Resources
- OverTheWire Bandit — https://overthewire.org
- Python Docs — https://docs.python.org
- Automate the Boring Stuff with Python (free online)

---

## Phase 3 — Cybersecurity Fundamentals + Zero Trust
> Duration: 1 month | Core concepts + 2026 model

### Security Principles
- [ ] CIA Triad — Confidentiality, Integrity, Availability
- [ ] Authentication vs Authorization vs Accounting (AAA)
- [ ] Least privilege and need-to-know
- [ ] Defense in depth
- [ ] Security policies, standards, procedures

### Zero Trust Architecture ⚡
- [ ] "Never trust, always verify" model
- [ ] Identity-centric perimeter vs network perimeter
- [ ] Micro-segmentation
- [ ] Continuous verification (device posture, identity)
- [ ] ZTNA vs traditional VPN
- [ ] Key vendors — Zscaler, Cloudflare Access, BeyondCorp
- [ ] Zero Trust in cloud environments

### Cryptography Basics
- [ ] Symmetric encryption — AES (128/256), DES
- [ ] Asymmetric encryption — RSA, ECC, Diffie-Hellman
- [ ] Hashing — MD5, SHA-1, SHA-256 (and why MD5/SHA-1 are broken)
- [ ] PKI — CA, certificates, chain of trust
- [ ] TLS/SSL handshake — ClientHello, ServerHello, key exchange
- [ ] Digital signatures

### Common Threats
- [ ] Malware types — virus, worm, trojan, rootkit, spyware
- [ ] Phishing & spear phishing — techniques, detection
- [ ] Ransomware — delivery, encryption, C2
- [ ] Social engineering — pretexting, vishing, baiting
- [ ] Man-in-the-Middle attacks
- [ ] DoS / DDoS — volumetric, protocol, application layer
- [ ] Insider threats

### Certification Target
- CompTIA Security+ — https://www.comptia.org/certifications/security

---

## Phase 4 — Ethical Hacking & Penetration Testing
> Duration: 2–4 months | Offensive skills

### Reconnaissance
- [ ] Passive recon — OSINT, open sources
- [ ] Active recon — direct interaction with target
- [ ] Footprinting — org info, employees, tech stack
- [ ] Google dorks — filetype:, site:, intitle:, inurl:
- [ ] WHOIS, DNS enumeration (subfinder, amass, dnsx)
- [ ] Shodan, Censys — internet-facing asset discovery
- [ ] LinkedIn OSINT, Maltego

### Scanning & Enumeration
- [ ] Port scanning — `nmap -sV -sC -A -p-`
- [ ] Service & version detection
- [ ] OS fingerprinting
- [ ] SMB enumeration — enum4linux, smbclient
- [ ] FTP/SSH/SNMP enumeration
- [ ] Web directory fuzzing — ffuf, gobuster
- [ ] Vulnerability scanning — Nessus, OpenVAS, Nuclei

### Exploitation
- [ ] Metasploit framework — modules, payloads, sessions
- [ ] Exploit development basics — understanding CVEs
- [ ] Buffer overflow — stack-based (basic)
- [ ] Credential attacks — hydra, medusa
- [ ] Password cracking — Hashcat, John the Ripper
- [ ] Common exploits — EternalBlue, Log4Shell, ProxyLogon

### Post Exploitation
- [ ] Privilege escalation — Linux (SUID, cron, sudo) & Windows (token impersonation, services)
- [ ] Persistence mechanisms — cron, registry, startup, scheduled tasks
- [ ] Lateral movement — pass-the-hash, WMI, PSExec
- [ ] Pivoting — port forwarding, proxychains, Chisel
- [ ] Data exfiltration techniques
- [ ] Covering tracks — log clearing, timestomping

### Wireless Security
- [ ] WPA2 attacks — handshake capture, PMKID
- [ ] Evil twin / rogue AP attacks
- [ ] Deauthentication attacks
- [ ] Tools — aircrack-ng, airmon-ng, airodump-ng

### Key Tools
| Tool | Use |
|------|-----|
| Nmap | Port scanning, service detection |
| Wireshark | Packet capture & analysis |
| Metasploit | Exploitation framework |
| Burp Suite | Web proxy, web app testing |
| Hashcat | GPU-accelerated password cracking |
| John the Ripper | Password cracking |
| Netcat | Network utility, reverse shells |
| Gobuster / ffuf | Directory & DNS fuzzing |
| Subfinder | Subdomain enumeration |

### Practice Labs
- TryHackMe — https://tryhackme.com
- Hack The Box — https://hackthebox.com
- VulnHub — https://vulnhub.com

---

## Phase 5 — Web Application Security
> Duration: 1–2 months | OWASP focus

### OWASP Top 10 (2021)
- [ ] A01 — Broken Access Control (IDOR, path traversal)
- [ ] A02 — Cryptographic Failures (weak ciphers, plaintext data)
- [ ] A03 — Injection (SQLi, NoSQLi, LDAP injection, command injection)
- [ ] A04 — Insecure Design
- [ ] A05 — Security Misconfiguration (default creds, open S3, debug mode)
- [ ] A06 — Vulnerable & Outdated Components
- [ ] A07 — Identification & Authentication Failures
- [ ] A08 — Software & Data Integrity Failures (insecure deserialization)
- [ ] A09 — Security Logging & Monitoring Failures
- [ ] A10 — SSRF (Server-Side Request Forgery)

### Injection Attacks (deep dive)
- [ ] SQL injection — union-based, blind, error-based, time-based
- [ ] NoSQL injection — MongoDB operators (`$where`, `$gt`)
- [ ] LDAP injection
- [ ] Command injection — `;`, `|`, `&&`, backticks
- [ ] SSTI — Server-Side Template Injection (Jinja2, Twig)
- [ ] XXE — XML External Entity

### XSS
- [ ] Reflected XSS
- [ ] Stored XSS
- [ ] DOM-based XSS
- [ ] Filter bypass techniques
- [ ] CSP (Content Security Policy) — how to set & bypass

### Authentication Vulnerabilities
- [ ] Session hijacking — cookie theft, fixation
- [ ] CSRF — SameSite, CSRF tokens
- [ ] JWT attacks — none algorithm, HS256→RS256, weak secrets
- [ ] OAuth misconfigs — open redirect, token leakage
- [ ] Brute force & credential stuffing

### API Security
- [ ] REST API testing methodology
- [ ] GraphQL injection & introspection abuse
- [ ] Mass assignment / parameter pollution
- [ ] Rate limiting bypass
- [ ] API key exposure (GitHub dorks, headers)
- [ ] BOLA / BFLA (Broken Object Level / Function Level Authorization)

### Tools
| Tool | Use |
|------|-----|
| Burp Suite | Web proxy, scanner, intruder |
| OWASP ZAP | Open source web scanner |
| SQLmap | Automated SQLi |
| ffuf | Web fuzzing |
| Nikto | Web server scanner |

### Practice
- PortSwigger Web Security Academy — https://portswigger.net/web-security
- DVWA — https://dvwa.co.uk
- HackThisSite — https://hackthissite.org

---

## Phase 5.5 — AI Security ⚡ NEW for 2026
> Duration: 2–3 weeks | Critical gap in most roadmaps

### AI as an Attack Vector
- [ ] AI-generated phishing — detection techniques
- [ ] Deepfake voice/video in social engineering
- [ ] AI-automated vulnerability scanning & exploitation
- [ ] Adversarial ML — fooling classifiers with crafted inputs

### Attacking AI/LLM Systems
- [ ] Prompt injection — direct and indirect
- [ ] Jailbreaking techniques — how & why they work
- [ ] Data poisoning attacks on training data
- [ ] Model extraction / inversion attacks
- [ ] Insecure output handling in LLM apps

### Defending AI Systems
- [ ] Input validation & sanitization for LLM apps
- [ ] Output filtering and sandboxing
- [ ] Monitoring LLM usage for anomalies
- [ ] OWASP Top 10 for LLMs — https://owasp.org/www-project-top-10-for-large-language-model-applications/
- [ ] Guardrails and rate limiting on AI endpoints

### AI-Assisted Defense
- [ ] Using AI/ML for anomaly detection (UEBA)
- [ ] AI-powered SIEM correlation
- [ ] Automated threat hunting with LLMs
- [ ] LLM-assisted malware analysis

### Resources
- OWASP LLM Top 10 — https://owasp.org/www-project-top-10-for-large-language-model-applications
- MITRE ATLAS (AI threat matrix) — https://atlas.mitre.org
- Google's Secure AI Framework (SAIF)

---

## Phase 6 — Cloud Security *(moved earlier from Phase 7)*
> Duration: 1–2 months | Now a core skill, not optional

### Cloud Fundamentals
- [ ] IaaS / PaaS / SaaS differences
- [ ] Shared responsibility model (who secures what)
- [ ] Cloud-native services overview (compute, storage, network, IAM)
- [ ] Multi-cloud vs hybrid cloud

### Identity & Access Management (IAM)
- [ ] AWS IAM — users, roles, policies, permission boundaries
- [ ] Azure AD / Entra ID — RBAC, Conditional Access
- [ ] Privilege escalation in cloud (IAM misconfig chains)
- [ ] Service accounts & workload identity
- [ ] MFA enforcement, passwordless auth
- [ ] Secrets management — AWS Secrets Manager, HashiCorp Vault

### Infrastructure Security
- [ ] VPC & security groups — inbound/outbound rules
- [ ] S3 bucket misconfigs — public ACLs, bucket policies
- [ ] Cloud logging — CloudTrail, Azure Monitor, GCP Cloud Audit Logs
- [ ] Container security — Docker hardening, image scanning
- [ ] Kubernetes security — RBAC, network policies, pod security
- [ ] Infrastructure as Code security (Terraform misconfigs)

### Cloud Attack Techniques
- [ ] SSRF to metadata endpoint (`169.254.169.254`)
- [ ] Enumeration with `aws cli`, `ScoutSuite`, `Pacu`
- [ ] Privilege escalation via role chaining
- [ ] Lambda & serverless attack vectors
- [ ] Publicly exposed storage (S3, Azure Blob, GCS)

### Supply Chain Security ⚡
- [ ] Third-party dependency risks (npm, PyPI poisoning)
- [ ] SolarWinds-style supply chain attacks
- [ ] Software Bill of Materials (SBOM)
- [ ] CI/CD pipeline security (secrets in GitHub Actions)
- [ ] Container image supply chain — signing (Cosign), SLSA framework

### Tools
| Tool | Use |
|------|-----|
| ScoutSuite | Multi-cloud security auditing |
| Pacu | AWS exploitation framework |
| Prowler | AWS/Azure/GCP security assessment |
| Trivy | Container image vulnerability scanning |
| Checkov | IaC static analysis |

### Certifications
- AWS Security Specialty
- Azure Security Engineer (AZ-500)
- Google Professional Cloud Security Engineer

---

## Phase 7 — Blue Team & Defensive Security
> Duration: 1–2 months | Detection & response

### Security Monitoring
- [ ] Log analysis — what to look for, log formats (JSON, CEF, Syslog)
- [ ] SIEM setup & use — Splunk, Elastic, Wazuh
- [ ] IDS/IPS — Snort, Suricata rules
- [ ] Network traffic analysis — Wireshark, Zeek
- [ ] Alert triage — false positive reduction, priority matrix

### Incident Response
- [ ] IR lifecycle — Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned (PICERL)
- [ ] Containment strategies — isolation, blocking, credential reset
- [ ] Evidence preservation — memory dumps, disk images
- [ ] Post-incident review & reporting
- [ ] Playbook creation for common scenarios

### Digital Forensics
- [ ] Disk imaging — dd, FTK Imager
- [ ] Memory forensics — Volatility (process list, network conns, injected code)
- [ ] Timeline analysis — log correlation
- [ ] Artifact recovery — deleted files, browser history, prefetch
- [ ] Chain of custody documentation

### Threat Hunting
- [ ] MITRE ATT&CK framework — tactics, techniques, procedures (TTPs)
- [ ] Hypothesis-driven hunting
- [ ] IOC vs TTP-based detection
- [ ] Threat intelligence feeds — MISP, VirusTotal, AlienVault OTX
- [ ] YARA rules — writing signatures for malware
- [ ] Sigma rules — SIEM-agnostic detection

### Tools
| Tool | Use |
|------|-----|
| Splunk | SIEM, log analysis |
| Wazuh | Open source SIEM/XDR |
| Elastic Security | SIEM + endpoint |
| Volatility | Memory forensics |
| Autopsy | Digital forensics |
| TheHive | Incident management |
| MISP | Threat intelligence sharing |

---

## Phase 8 — GRC & Risk Management ⚡ NEW for 2026
> Duration: 2–4 weeks | Required even at junior levels in India

### Governance, Risk & Compliance Basics
- [ ] What is GRC and why it matters
- [ ] Security governance frameworks
- [ ] Policies, standards, procedures, guidelines hierarchy
- [ ] Board-level vs technical security communication

### Risk Management
- [ ] Risk assessment methodology
- [ ] Risk = Likelihood × Impact
- [ ] Risk treatment — accept, mitigate, transfer, avoid
- [ ] Residual risk and risk appetite
- [ ] Vulnerability vs threat vs risk

### Compliance Frameworks
- [ ] ISO 27001 — ISMS structure, Annex A controls
- [ ] NIST CSF — Identify, Protect, Detect, Respond, Recover
- [ ] SOC 2 — Type I vs Type II
- [ ] GDPR basics — data protection, breach notification
- [ ] India-specific — IT Act 2000, DPDP Act 2023
- [ ] PCI-DSS basics (if targeting fintech)

### Audit & Assessment
- [ ] Internal vs external audits
- [ ] Security assessment reports
- [ ] Evidence collection for audits
- [ ] Control testing

### Resources
- NIST CSF — https://www.nist.gov/cyberframework
- ISO 27001 overview — https://www.iso.org/isoiec-27001-information-security.html
- ISACA resources — https://www.isaca.org

---

## Phase 9 — Advanced Specializations
> Duration: 3–6 months | Pick your path

### Path A — Red Team
- [ ] Active Directory attacks — enumeration, BloodHound, SharpHound
- [ ] Kerberoasting, AS-REP roasting
- [ ] Pass-the-Hash, Pass-the-Ticket, DCSync
- [ ] C2 frameworks — Cobalt Strike, Sliver, Havoc
- [ ] Adversary emulation — MITRE ATT&CK red team ops
- [ ] Custom payload development — AV evasion basics
- [ ] Malware analysis — static (strings, PE headers) & dynamic (sandboxes)
- [ ] Physical security — badge cloning, lock picking (optional)

**Certification:** OSCP — https://www.offensive-security.com/pwk-oscp/

### Path B — Blue Team / SOC
- [ ] SOC analyst workflows — L1/L2/L3 triage
- [ ] Threat intelligence production
- [ ] DFIR deep dives — full incident investigations
- [ ] Detection engineering — writing detection rules at scale
- [ ] YARA + Sigma + Suricata rule writing
- [ ] Deception technology — honeypots, honeyfiles

**Certifications:** GCIH, BTL1 (Blue Team Labs), CySA+

### Path C — Application Security
- [ ] Secure code review — reading source for vulns
- [ ] SAST tools — Semgrep, SonarQube, Bandit
- [ ] DAST tools — OWASP ZAP, Burp Suite automated scanning
- [ ] Secure SDLC — threat modeling, security requirements
- [ ] Bug bounty — HackerOne, Bugcrowd methodology
- [ ] Mobile app security — OWASP MASVS, ADB, Frida

**Certification:** GWEB, eWPTX

### Path D — Cloud Security (Advanced)
- [ ] Kubernetes security — CIS benchmark, pod security policies
- [ ] DevSecOps — security in CI/CD pipelines
- [ ] Cloud threat detection — GuardDuty, Microsoft Defender for Cloud
- [ ] Cloud incident response — IR in AWS/Azure
- [ ] CSPM & CWPP tools

**Certification:** AWS Security Specialty, CCSP

---

## Certification Roadmap

```
Beginner              Intermediate          Advanced
─────────             ────────────          ────────
CompTIA A+    ──→     Security+     ──→     OSCP
Network+      ──→     eJPT          ──→     CRTP (AD)
Linux+        ──→     CySA+         ──→     CCSP (Cloud)
                      AWS SAA       ──→     AWS Security
                      AZ-900        ──→     AZ-500
```

---

## Job Targets After Completion

| Role | Phases Needed | Key Skills |
|------|--------------|------------|
| SOC Analyst | 1–3, 7 | SIEM, log analysis, IR |
| Junior Pentester | 1–5 | Web app testing, recon, Burp Suite |
| Security Analyst | 1–3, 7, 8 | Monitoring, GRC, reporting |
| Cloud Security Engineer | 1–3, 6 | AWS/Azure IAM, misconfig auditing |
| Bug Bounty Hunter | 4–5, 5.5 | Web vulns, OWASP, API testing |

---

## Daily Study Plan (2 hrs/day)

| Time | Activity |
|------|----------|
| 30 min | Theory — read notes, watch a lesson |
| 30 min | Linux / Python / scripting practice |
| 45 min | Hands-on lab (TryHackMe / HTB / PortSwigger) |
| 15 min | Security news — Krebs, DarkReading, BleepingComputer |

> **Rule:** Labs > Theory. Employers test what you can do, not what you know.

---

## Tags
#cybersecurity #roadmap #2026 #ethical-hacking #web-security #cloud-security #ai-security #zero-trust #blue-team #red-team #oscp #tryhackme #hackthebox
