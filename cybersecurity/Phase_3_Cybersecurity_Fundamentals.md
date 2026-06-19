# Phase 3 — Cybersecurity Fundamentals + Zero Trust
> Complete self-contained notes. No external resources needed.
> Estimated time: 3–4 weeks

---

## Table of Contents
1. [1. Security Principles](#1-security-principles)
2. [2. CIA Triad](#2-cia-triad)
3. [3. Authentication, Authorization & Accounting (AAA)](#3-authentication-authorization-accounting-aaa)
4. [4. Zero Trust Architecture](#4-zero-trust-architecture)
5. [5. Cryptography](#5-cryptography)
6. [6. Common Threats & Attack Types](#6-common-threats-attack-types)
7. [7. Security Controls](#7-security-controls)
8. [8. Risk Management Basics](#8-risk-management-basics)
9. [9. Network Security Fundamentals](#9-network-security-fundamentals)
10. [10. CompTIA Security+ Key Topics](#10-comptia-security-key-topics)
11. [11. Quick Reference Cheatsheet](#11-quick-reference-cheatsheet)

---

## 1. Security Principles

### Least Privilege
Every user, process, or system should have **only the minimum access** needed to do its job — nothing more.

- A web server process should NOT run as root
- A developer should NOT have access to production databases
- An intern should NOT have admin rights

**Why it matters:** If an account gets compromised, attacker only gets limited access — not everything.

---

### Need to Know
Even if a user HAS permission to access something, they should only access it **if they actually need it for their work.**

- Different from least privilege — this is about *information*, not just system access
- Example: HR can access salary data. IT admin technically could too, but shouldn't unless needed.

---

### Defense in Depth
**Never rely on a single security control.** Layer multiple defenses so if one fails, others catch it.

```
Internet → Firewall → IDS/IPS → WAF → App Auth → DB Encryption
```

- If firewall is bypassed → IDS/IPS catches it
- If IDS misses it → WAF blocks the payload
- If WAF fails → App requires auth
- If auth bypassed → DB is encrypted

**Analogy:** Castle with a moat, walls, guards, locked doors, and a vault — not just a locked door.

---

### Separation of Duties
No single person should have **complete control** over a critical process.

- Example: The person who approves payments should NOT be the same person who processes them
- Prevents fraud and insider threats
- In IT: Developer should NOT have direct production deployment access without approval

---

### Security through Obscurity (Bad Practice)
Relying on secrecy of design/implementation as the main security mechanism.

- Example: "Hackers won't find our admin panel at /supersecretadmin"
- This is NOT real security — it's a supplement at best
- Always assume attackers know your system design (Kerckhoffs's principle)

**Kerckhoffs's Principle:** A system should be secure even if everything about the system, except the key, is public knowledge.

---

### Fail Secure vs Fail Open

| Concept | Behaviour | Example |
|---------|-----------|---------|
| Fail Secure | On failure, system denies access | Bank vault locks if power fails |
| Fail Open | On failure, system allows access | Fire door opens if power fails (safety) |

Security systems should **fail secure**. Safety systems may need to fail open.

---

## 2. CIA Triad

The three core goals of information security. Every security decision maps to one or more of these.

```
        Confidentiality
             /\
            /  \
           /    \
          /______\
   Integrity    Availability
```

---

### Confidentiality
**Ensuring information is only accessible to those authorized to see it.**

Threats to confidentiality:
- Eavesdropping / sniffing
- Data breaches
- Unauthorized access
- Shoulder surfing
- Dumpster diving

Controls:
- Encryption (AES, TLS)
- Access controls (ACL, RBAC)
- Multi-factor authentication
- Data classification
- Need-to-know enforcement

---

### Integrity
**Ensuring data has not been altered or tampered with — by unauthorized parties or accidentally.**

Threats to integrity:
- Man-in-the-Middle attacks (modifying data in transit)
- Malware modifying files
- Insider data manipulation
- Accidental corruption

Controls:
- Hashing (SHA-256 to verify files haven't changed)
- Digital signatures (proves sender identity + integrity)
- Version control
- Checksums
- Write-once storage (WORM)

**Example:** You download a file. The website gives you a SHA-256 hash. You run `sha256sum file.iso` and compare. If it matches → integrity confirmed.

---

### Availability
**Ensuring systems and data are accessible to authorized users when needed.**

Threats to availability:
- DoS / DDoS attacks
- Hardware failures
- Natural disasters
- Ransomware (encrypts data, makes it unavailable)
- Human error (accidentally deleting data)

Controls:
- Redundancy (RAID, failover servers)
- Backups (3-2-1 rule)
- DDoS protection (Cloudflare, AWS Shield)
- UPS (Uninterruptible Power Supply)
- Load balancers
- Disaster Recovery Plans (DRP)

**3-2-1 Backup Rule:**
- 3 copies of data
- 2 different media types
- 1 offsite copy

---

### CIA in Practice — Examples

| Scenario | CIA Violation |
|----------|--------------|
| Attacker reads your encrypted emails | Confidentiality |
| Attacker modifies a bank transaction | Integrity |
| DDoS takes down a hospital website | Availability |
| Ransomware encrypts all files | Availability (+ Confidentiality) |
| Insider leaks customer database | Confidentiality |
| Admin accidentally deletes DB | Availability + Integrity |

---

### DAD Triad (Opposite of CIA)
Attackers aim for:
- **Disclosure** → breaks Confidentiality
- **Alteration** → breaks Integrity
- **Destruction/Denial** → breaks Availability

---

## 3. Authentication, Authorization & Accounting (AAA)

### Authentication — "Who are you?"
Verifying the identity of a user, device, or system.

**Authentication Factors:**

| Factor | Type | Examples |
|--------|------|---------|
| Something you know | Knowledge | Password, PIN, security questions |
| Something you have | Possession | OTP token, smart card, phone |
| Something you are | Inherence | Fingerprint, face, retina scan |
| Somewhere you are | Location | GPS location, IP geofencing |
| Something you do | Behaviour | Typing rhythm, mouse movement |

**MFA (Multi-Factor Authentication):** Using 2+ different factor *types*.
- Password + OTP = MFA ✅ (know + have)
- Password + security question = NOT MFA ❌ (both are "know")

---

### Authentication Protocols

**Kerberos**
- Used in Windows Active Directory environments
- Ticket-based authentication system
- Process:
  1. Client requests Ticket Granting Ticket (TGT) from KDC
  2. KDC verifies credentials, issues TGT
  3. Client uses TGT to request service tickets
  4. Service ticket grants access to specific resources
- Attack: Kerberoasting (request service tickets, crack offline)

**LDAP (Lightweight Directory Access Protocol)**
- Protocol for accessing directory services (like Active Directory)
- Port 389 (plain), 636 (LDAPS — encrypted)
- Used to look up users, groups, organizational info

**RADIUS**
- Remote Authentication Dial-In User Service
- Centralizes authentication for network access (VPN, WiFi)
- Client sends credentials → RADIUS server authenticates

**SAML (Security Assertion Markup Language)**
- XML-based SSO standard
- Used for enterprise SSO (login once, access many apps)
- Identity Provider (IdP) → Service Provider (SP) flow

**OAuth 2.0**
- Authorization framework (NOT authentication)
- Allows apps to access resources on behalf of user without sharing password
- Example: "Login with Google" — Google vouches for you

**OpenID Connect (OIDC)**
- Authentication layer built ON TOP of OAuth 2.0
- OAuth tells apps what you can access; OIDC tells apps who you are

---

### Authorization — "What can you do?"
Determining what an authenticated user is allowed to do.

**Access Control Models:**

**DAC — Discretionary Access Control**
- Resource owner decides who gets access
- Example: You own a file, you set its permissions
- Used in: Standard Linux/Windows file systems
- Weakness: Owner can accidentally grant too much access

**MAC — Mandatory Access Control**
- Access determined by labels/classifications set by policy, not owners
- Example: Top Secret files can only be accessed by Top Secret cleared users
- Used in: Military, government systems (SELinux)
- Strict — even file owners can't change access levels

**RBAC — Role-Based Access Control**
- Access based on job role, not individual identity
- Example: "Manager" role can approve expenses; "Employee" role cannot
- Most common in enterprise environments
- Easy to manage — change role, not individual permissions

**ABAC — Attribute-Based Access Control**
- Access based on attributes of user, resource, and environment
- Example: "Allow access IF user.department=HR AND resource.sensitivity=low AND time=business_hours"
- Most flexible, most complex
- Used in: Zero Trust, cloud IAM policies

**Rule-Based Access Control**
- Access based on rules (like firewall rules)
- Example: "Block all traffic from IP range X"
- Different from RBAC — rules apply to everyone, not roles

---

### Accounting — "What did you do?"
Tracking and logging what authenticated, authorized users actually did.

- Audit logs
- SIEM correlation
- Non-repudiation — user cannot deny their actions
- Used for forensics, compliance, billing

**Non-repudiation:** Proof that someone performed an action that they cannot deny.
- Digital signatures provide non-repudiation
- Log files + integrity controls provide non-repudiation

---

## 4. Zero Trust Architecture

### The Old Model (Perimeter Security)
```
Outside (Untrusted) | Firewall | Inside (Trusted)
```
- "If you're inside the network, you're trusted"
- VPN gives you access → you're trusted
- **Problem:** Once attacker gets inside (breach, insider threat, stolen VPN creds) → they have full access

### Why Perimeter Security Failed
- Remote work — employees work from everywhere
- Cloud — data is not inside a perimeter anymore
- Supply chain attacks — trusted vendors used as entry points
- Lateral movement — one breach = entire network compromised

---

### Zero Trust Core Principle
> **"Never trust, always verify."**
> Assume breach. Verify every request as if it originates from an untrusted network.

Every access request must be:
1. **Authenticated** — who is this?
2. **Authorized** — should they have access to THIS specific resource?
3. **Continuously validated** — are they still trusted mid-session?

---

### Zero Trust Pillars

**Identity**
- Strong MFA for every user
- Passwordless authentication where possible
- Identity is the new perimeter
- Tools: Azure AD, Okta, Ping Identity

**Device**
- Device health checked before access (is it patched? does it have antivirus?)
- MDM (Mobile Device Management) enrollment
- Certificate-based device identity
- Tools: Microsoft Intune, Jamf

**Network**
- Micro-segmentation — divide network into tiny zones
- No implicit trust based on network location
- Encrypt all traffic (even internal)
- Tools: VMware NSX, Illumio

**Application**
- Application-level access control (not network-level)
- ZTNA replaces VPN — access to specific app, not whole network
- Tools: Zscaler Private Access, Cloudflare Access, BeyondCorp

**Data**
- Classify data
- Encrypt data at rest and in transit
- DLP (Data Loss Prevention) policies
- Tools: Microsoft Purview, Forcepoint

---

### ZTNA vs Traditional VPN

| Feature | Traditional VPN | ZTNA |
|---------|----------------|------|
| Access granted to | Entire network | Specific application only |
| Trust model | Trust after auth | Continuous verification |
| Lateral movement | Easy for attacker | Prevented by design |
| User experience | Often slow, clunky | App-specific, fast |
| Visibility | Limited | Full session visibility |

---

### Zero Trust Implementation (NIST SP 800-207 Model)
1. Know your assets, users, data flows
2. Create micro-perimeters around sensitive resources
3. Inspect and log ALL traffic
4. Enforce least-privilege access
5. Continuously monitor and validate

---

## 5. Cryptography

### Why Cryptography?
- **Confidentiality** — encrypt so only intended recipient can read
- **Integrity** — detect if data was tampered (hashing)
- **Authentication** — prove identity (digital signatures)
- **Non-repudiation** — prove someone sent a message (digital signatures)

---

### Symmetric Encryption
**Same key** used to encrypt AND decrypt.

```
Plaintext → [Key + Algorithm] → Ciphertext → [Same Key + Algorithm] → Plaintext
```

**Algorithms:**

| Algorithm | Key Size | Status | Notes |
|-----------|----------|--------|-------|
| DES | 56-bit | Broken ❌ | Too short, cracked in 1999 |
| 3DES | 112/168-bit | Deprecated ⚠️ | Slow, being phased out |
| AES-128 | 128-bit | Secure ✅ | Standard for most use |
| AES-256 | 256-bit | Very Secure ✅ | Used for classified data |
| ChaCha20 | 256-bit | Secure ✅ | Used in TLS, mobile |

**AES Modes:**

| Mode | Notes |
|------|-------|
| ECB | Insecure — same plaintext = same ciphertext ❌ |
| CBC | Better — uses IV, but sequential ⚠️ |
| GCM | Best — authenticated encryption, parallel ✅ |
| CTR | Stream cipher mode, fast ✅ |

**Pros:** Fast, efficient for large data
**Cons:** Key distribution problem — how do you securely share the key?

---

### Asymmetric Encryption
**Two mathematically linked keys:**
- **Public key** — share with everyone, used to encrypt
- **Private key** — keep secret, used to decrypt

```
Sender encrypts with recipient's PUBLIC key
→ Only recipient's PRIVATE key can decrypt
```

**Algorithms:**

| Algorithm | Key Size | Use |
|-----------|----------|-----|
| RSA | 2048–4096 bit | Encryption, signatures |
| ECC (ECDSA) | 256–384 bit | Signatures, TLS (smaller keys, same strength) |
| Diffie-Hellman | 2048+ bit | Key exchange (not encryption itself) |
| DSA | 1024–3072 bit | Digital signatures only |

**Pros:** Solves key distribution problem
**Cons:** Slow — not used for bulk data encryption

**In practice:** Asymmetric used to exchange a symmetric key, then symmetric used for the actual data. This is how TLS works.

---

### Hashing
**One-way function** — converts data to fixed-length digest.
- Cannot be reversed (no key)
- Same input always = same output
- Different input = completely different output (avalanche effect)
- Used for: integrity verification, password storage

**Algorithms:**

| Algorithm | Output Size | Status |
|-----------|------------|--------|
| MD5 | 128-bit | Broken ❌ (collision attacks) |
| SHA-1 | 160-bit | Broken ❌ (collision attacks) |
| SHA-256 | 256-bit | Secure ✅ |
| SHA-512 | 512-bit | Secure ✅ |
| bcrypt | Variable | ✅ Best for passwords |
| Argon2 | Variable | ✅ Best for passwords (modern) |

**Why MD5/SHA-1 are broken:** Collision attacks — two different inputs can produce the same hash.

**Password Hashing:**
- Never store passwords in plaintext
- Never encrypt passwords (can be decrypted if key stolen)
- Always HASH with a salt
- **Salt** = random value added to password before hashing → prevents rainbow table attacks

```
stored_hash = bcrypt(password + random_salt)
```

---

### Digital Signatures
Prove **who sent** a message AND that it **wasn't modified**.

```
Sender:   hash(message) → encrypt hash with PRIVATE key → signature
Receiver: decrypt signature with PUBLIC key → compare with hash(message)
          If match → authentic + unmodified
```

- Provides: Authentication + Integrity + Non-repudiation
- Used in: Code signing, email (S/MIME), SSL certificates, git commits

---

### PKI — Public Key Infrastructure
System for managing digital certificates and public keys.

**Components:**

| Component | Role |
|-----------|------|
| CA (Certificate Authority) | Issues and signs certificates (DigiCert, Let's Encrypt) |
| RA (Registration Authority) | Verifies identity before CA issues cert |
| Certificate | Contains: public key, owner info, CA signature, expiry |
| CRL (Certificate Revocation List) | List of revoked certs |
| OCSP | Online cert status checking (real-time alternative to CRL) |

**Certificate Chain (Chain of Trust):**
```
Root CA (self-signed, highly trusted)
  └── Intermediate CA (signed by Root CA)
        └── End-entity cert (your website's cert)
```

Browsers trust Root CAs by default (built into OS/browser).

**X.509** — standard format for digital certificates.

---

### TLS/SSL Handshake

TLS (Transport Layer Security) is what makes HTTPS secure.

```
Client                          Server
  |                               |
  |── ClientHello ──────────────→ |  (TLS version, cipher suites, random)
  |← ServerHello ──────────────── |  (chosen cipher, server random, certificate)
  |                               |
  | [Client verifies certificate] |
  |                               |
  |── Key Exchange ─────────────→ |  (pre-master secret, encrypted with server pub key)
  |                               |
  | [Both derive session keys]    |
  |                               |
  |── Finished ─────────────────→ |  (encrypted with session key)
  |← Finished ──────────────────  |
  |                               |
  |════ Encrypted Application Data ════|
```

**TLS 1.3 (current standard):**
- Faster handshake (1-RTT, sometimes 0-RTT)
- Removed weak algorithms (RSA key exchange, MD5, SHA-1)
- Forward secrecy mandatory

**Cipher Suite Example:**
`TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384`
- `ECDHE` → Key exchange algorithm
- `RSA` → Authentication algorithm
- `AES_256_GCM` → Encryption algorithm
- `SHA384` → MAC algorithm

---

## 6. Common Threats & Attack Types

### Malware Types

| Type | How it works | Example |
|------|-------------|---------|
| Virus | Attaches to legitimate files, spreads when file runs | ILOVEYOU |
| Worm | Self-replicates across network without user action | WannaCry |
| Trojan | Disguised as legitimate software | RAT (Remote Access Trojan) |
| Rootkit | Hides itself deep in OS, hard to detect | Necurs |
| Spyware | Secretly monitors user activity | Keyloggers |
| Adware | Displays unwanted ads | Potentially unwanted programs |
| Ransomware | Encrypts files, demands payment | REvil, LockBit |
| Botnet | Army of infected machines controlled remotely | Mirai (IoT botnet) |
| Fileless Malware | Lives in memory, no file on disk | PowerShell-based attacks |
| Logic Bomb | Triggers on specific condition/time | Fired employee's revenge code |

---

### Phishing Variants

| Type | Target | Method |
|------|--------|--------|
| Phishing | Mass email | Generic lure (fake bank email) |
| Spear Phishing | Specific individual | Personalized, researched lure |
| Whaling | C-level executives | High-value target, sophisticated |
| Vishing | Via phone/voice | Pretending to be IT/bank/gov |
| Smishing | Via SMS | Fake delivery notifications |
| Pharming | DNS manipulation | Redirect legit URL to fake site |

**How to spot phishing:**
- Sender domain mismatch (paypa1.com vs paypal.com)
- Urgency ("Your account will be deleted in 24 hours!")
- Generic greeting ("Dear Customer")
- Suspicious links (hover to see real URL)
- Unexpected attachments

---

### Social Engineering Techniques

**Pretexting** — Creating a fabricated scenario to extract info
- "Hi, I'm from IT. We need your password to fix your account."

**Baiting** — Leaving infected USB drives in parking lots
- Curious employee plugs it in → malware installs

**Quid Pro Quo** — Offering something in exchange for info
- "I'll help you fix your computer if you give me your login"

**Tailgating / Piggybacking** — Following authorized person through secure door

**Impersonation** — Posing as a trusted entity (IT, executive, vendor)

**Influence Techniques (Cialdini's Principles):**
- Authority — "I'm from corporate IT"
- Urgency — "We need this NOW"
- Social proof — "Everyone else has already done this"
- Scarcity — "This is your last chance"
- Likability — Building rapport before the ask
- Reciprocity — Doing a favor, then asking for something

---

### Network Attacks

**Man-in-the-Middle (MitM)**
Attacker secretly intercepts and possibly alters communication between two parties.

```
Client ←→ [Attacker] ←→ Server
```

Types:
- ARP Spoofing — attacker poisons ARP cache to redirect traffic
- DNS Spoofing — fake DNS responses redirect to malicious IP
- SSL Stripping — downgrade HTTPS to HTTP
- Evil Twin — rogue WiFi AP with same SSID

Prevention: TLS, HSTS, certificate pinning, VPN

---

**DoS vs DDoS**

| Type | Source | Scale |
|------|--------|-------|
| DoS | Single attacker | Limited |
| DDoS | Botnet (thousands of IPs) | Massive |

**DDoS Types:**
- Volumetric — flood bandwidth (UDP flood, ICMP flood)
- Protocol — exhaust server resources (SYN flood — half-open connections)
- Application layer (L7) — target app logic (HTTP flood, Slowloris)

**SYN Flood explained:**
```
Normal: Client sends SYN → Server SYN-ACK → Client ACK (connection established)
Attack: Client sends thousands of SYNs, never sends ACK
        → Server keeps half-open connections until resources exhausted
```

---

**Replay Attack**
Attacker captures valid authentication data and replays it later.
- Prevention: timestamps, nonces (number used once), session tokens

**Pass-the-Hash**
Attacker steals hashed password from memory and uses it directly for auth (without cracking).
- Specific to Windows NTLM authentication
- Prevention: Credential Guard, MFA

---

### Ransomware — How it Works
1. **Delivery** — phishing email, RDP exploit, drive-by download
2. **Execution** — malware runs, may disable backups/shadow copies
3. **Encryption** — files encrypted with attacker's public key
4. **Ransom note** — instructions to pay (usually crypto)
5. **C2 communication** — malware calls back to attacker server

**Double extortion:** Encrypt AND steal data → threaten to publish if not paid.

**Prevention:**
- Offline backups (3-2-1 rule)
- Patch management
- Email filtering
- EDR solutions
- Network segmentation

---

### Insider Threats

**Types:**
- Malicious insider — intentionally steals/damages data (disgruntled employee)
- Negligent insider — accidentally causes breach (clicks phishing link)
- Compromised insider — account taken over by attacker

**Indicators:**
- Accessing data outside normal working hours
- Downloading large amounts of data
- Accessing systems unrelated to their role
- Recently disciplined or about to leave company

**Controls:**
- Least privilege
- DLP (Data Loss Prevention)
- UEBA (User and Entity Behavior Analytics)
- Separation of duties
- Exit procedures

---

## 7. Security Controls

### Control Categories

**By Function:**

| Category | Purpose | Examples |
|----------|---------|---------|
| Preventive | Stop attack before it happens | Firewall, encryption, MFA |
| Detective | Identify attacks in progress or after | IDS, SIEM, audit logs |
| Corrective | Fix damage after an attack | Backups, patch management, IR |
| Deterrent | Discourage attackers | Warning banners, CCTV signs |
| Compensating | Alternative when primary control not possible | Monitoring extra if MFA can't be implemented |
| Directive | Policies and procedures | Acceptable Use Policy |

**By Type:**

| Type | Examples |
|------|---------|
| Administrative / Managerial | Policies, training, background checks |
| Technical / Logical | Firewalls, encryption, MFA, IDS |
| Physical | Locks, CCTV, guards, biometrics |

---

### Firewall Types

| Type | How it works |
|------|-------------|
| Packet filtering | Checks IP/port, no state awareness |
| Stateful inspection | Tracks connection state |
| Application (L7) / WAF | Inspects application-layer content |
| NGFW (Next-Gen) | DPI, IPS, SSL inspection, app awareness |
| Proxy firewall | Intermediary, hides internal network |

---

### IDS vs IPS

| Feature | IDS | IPS |
|---------|-----|-----|
| Action | Detects and alerts | Detects and blocks |
| Placement | Out of band (copy of traffic) | Inline (traffic flows through it) |
| Risk | No false positive impact on traffic | False positive can block legit traffic |

**Detection Methods:**
- Signature-based — matches known attack patterns (fast, misses new attacks)
- Anomaly-based — detects deviation from baseline (catches new attacks, more false positives)
- Heuristic — rules-based behavioral analysis

---

### Endpoint Security

**Antivirus (AV):** Signature-based malware detection
**EDR (Endpoint Detection & Response):** Behavioral monitoring, threat hunting, response capabilities
**EPP (Endpoint Protection Platform):** AV + EDR combined

**DLP (Data Loss Prevention):**
- Prevents sensitive data leaving the organization
- Can block USB drives, email attachments, cloud uploads
- Types: Network DLP, Endpoint DLP, Cloud DLP

---

## 8. Risk Management Basics

### Key Terms

| Term | Definition |
|------|-----------|
| Asset | Anything of value (data, systems, people, reputation) |
| Threat | Potential cause of harm (hacker, natural disaster, employee error) |
| Vulnerability | Weakness that can be exploited |
| Risk | Likelihood × Impact of a threat exploiting a vulnerability |
| Exploit | Actual attack taking advantage of a vulnerability |
| Control / Safeguard | Measure to reduce risk |
| Residual Risk | Risk remaining after controls are applied |

**Risk Formula:**
```
Risk = Threat × Vulnerability × Impact
```

---

### Risk Treatment Options

| Option | Meaning | Example |
|--------|---------|---------|
| Accept | Live with the risk | Small risk, cost to fix is too high |
| Mitigate | Reduce likelihood or impact | Patch the vulnerability |
| Transfer | Shift risk to another party | Buy cyber insurance |
| Avoid | Eliminate the activity that causes risk | Don't collect data you don't need |

---

### Quantitative vs Qualitative Risk Assessment

**Qualitative:** Subjective ratings — High / Medium / Low
- Fast, good for initial assessment
- No dollar figures

**Quantitative:** Numbers and dollar values
- **AV (Asset Value)** — what is the asset worth?
- **EF (Exposure Factor)** — % of asset lost in an incident
- **SLE (Single Loss Expectancy)** = AV × EF
- **ARO (Annual Rate of Occurrence)** — how often per year?
- **ALE (Annual Loss Expectancy)** = SLE × ARO

**Example:**
- Server worth $100,000 (AV)
- Ransomware would destroy 60% of value (EF = 0.6)
- SLE = $100,000 × 0.6 = $60,000
- Ransomware hits this server type twice a year (ARO = 2)
- ALE = $60,000 × 2 = **$120,000/year**
- If security solution costs $30,000/year → worth it

---

### Business Continuity & Disaster Recovery

**BCP (Business Continuity Plan):** How to keep business running during a disaster
**DRP (Disaster Recovery Plan):** How to restore IT systems after a disaster

**Key Metrics:**

| Metric | Meaning |
|--------|---------|
| RTO (Recovery Time Objective) | Maximum acceptable downtime |
| RPO (Recovery Point Objective) | Maximum acceptable data loss (time) |
| MTTR (Mean Time To Recover) | Average time to restore service |
| MTBF (Mean Time Between Failures) | Average time between failures |

**Example:**
- RPO = 4 hours → backups must run every 4 hours
- RTO = 2 hours → system must be restored within 2 hours of failure

---

## 9. Network Security Fundamentals

### Common Ports — Security Relevant

| Port | Protocol | Notes |
|------|----------|-------|
| 21 | FTP | Unencrypted — use SFTP (22) instead |
| 22 | SSH | Encrypted remote access |
| 23 | Telnet | Unencrypted — never use ❌ |
| 25 | SMTP | Email — often abused for spam |
| 53 | DNS | UDP/TCP — DNS poisoning target |
| 80 | HTTP | Unencrypted web |
| 443 | HTTPS | Encrypted web |
| 445 | SMB | Windows file sharing — EternalBlue target |
| 3389 | RDP | Windows remote desktop — brute force target |
| 3306 | MySQL | Database — should never be public |
| 8080 | HTTP Alt | Common for dev servers |

---

### VPN Types

| Type | Use Case |
|------|---------|
| Site-to-Site | Connect two office networks permanently |
| Client-to-Site (Remote Access) | Employee connects from home |
| Split Tunneling | Only some traffic goes through VPN |
| Full Tunnel | ALL traffic goes through VPN |

**Protocols:**
- **OpenVPN** — open source, secure, TCP/UDP
- **WireGuard** — modern, fast, minimal codebase
- **IPSec** — used in site-to-site, complex but widely supported
- **L2TP/IPSec** — L2TP alone is not secure, IPSec adds encryption
- **PPTP** — outdated, broken ❌

---

### Network Segmentation
Dividing a network into segments to limit blast radius.

```
Internet
    │
  Firewall
    │
  DMZ (web servers, mail servers — public facing)
    │
  Firewall
    │
  Internal Network
    │
  ├── Workstations VLAN
  ├── Servers VLAN
  ├── IoT VLAN
  └── Management VLAN (most restricted)
```

**DMZ (Demilitarized Zone):**
- Sits between internet and internal network
- Hosts public-facing services (web, email, DNS)
- If DMZ server is compromised → attacker still can't reach internal network directly

---

### Wireless Security

| Protocol | Security Level | Notes |
|----------|---------------|-------|
| WEP | Broken ❌ | Never use |
| WPA | Weak ⚠️ | Avoid |
| WPA2-Personal | OK ✅ | Uses PSK (pre-shared key) |
| WPA2-Enterprise | Good ✅ | Uses 802.1X + RADIUS |
| WPA3 | Best ✅ | SAE replaces PSK, forward secrecy |

**802.1X:** Port-based network access control — requires authentication before network access granted.

---

## 10. CompTIA Security+ Key Topics

> Security+ (SY0-701) is the target cert for this phase. These are the exam domain weightings.

| Domain | Weight |
|--------|--------|
| General Security Concepts | 12% |
| Threats, Vulnerabilities, Mitigations | 22% |
| Security Architecture | 18% |
| Security Operations | 28% |
| Security Program Management & Oversight | 20% |

**Key things Security+ tests that often trip people up:**

1. **Difference between authentication and authorization** — auth proves identity, authz determines permissions
2. **Symmetric vs asymmetric** — symmetric is fast (bulk data), asymmetric solves key distribution
3. **Hashing is not encryption** — can't decrypt a hash
4. **IDS vs IPS** — IDS alerts, IPS blocks (inline)
5. **Risk = Likelihood × Impact**
6. **SLE = AV × EF, ALE = SLE × ARO**
7. **RPO vs RTO** — RPO is data loss tolerance, RTO is downtime tolerance
8. **Stateful vs stateless firewall** — stateful tracks connections
9. **Zero Trust = never trust, always verify**
10. **Types of malware** — know the differences

---

## 11. Quick Reference Cheatsheet

### CIA Triad
```
Confidentiality → Encryption, Access Control
Integrity       → Hashing, Digital Signatures
Availability    → Backups, Redundancy, DDoS Protection
```

### Encryption Quick Reference
```
Symmetric:   AES-256 (fast, same key both sides)
Asymmetric:  RSA-2048 / ECC (slow, pub/priv key pair)
Hashing:     SHA-256 (one-way, integrity)
Signatures:  Hash + encrypt with private key
TLS:         Asymmetric for key exchange → Symmetric for data
```

### Authentication Factors
```
Know  → Password, PIN
Have  → OTP, Smart card, Phone
Are   → Fingerprint, Face, Retina
Where → GPS, IP location
Do    → Typing pattern
```

### Access Control Models
```
DAC  → Owner decides (Linux file perms)
MAC  → Policy decides (military, SELinux)
RBAC → Role decides (enterprise IT)
ABAC → Attributes decide (Zero Trust, cloud IAM)
```

### Risk Formula
```
Risk = Likelihood × Impact
SLE  = Asset Value × Exposure Factor
ALE  = SLE × Annual Rate of Occurrence
```

### Control Types
```
Preventive  → Firewall, MFA, Encryption
Detective   → IDS, SIEM, Audit Logs
Corrective  → Backups, Patching, IR
Deterrent   → Warning banners, CCTV
```

### Common Ports (Must Know)
```
22  = SSH        80  = HTTP
23  = Telnet     443 = HTTPS
25  = SMTP       445 = SMB
53  = DNS        3389 = RDP
```

---

## Checklist — Phase 3 Complete When:

- [ ] Can explain CIA triad with real examples
- [ ] Know difference between authentication and authorization
- [ ] Understand all access control models (DAC/MAC/RBAC/ABAC)
- [ ] Can explain symmetric vs asymmetric encryption and when each is used
- [ ] Understand what hashing is and why it's not encryption
- [ ] Know how TLS handshake works at high level
- [ ] Can explain Zero Trust and how it differs from perimeter security
- [ ] Know the main malware types and how they differ
- [ ] Can calculate SLE and ALE
- [ ] Know difference between RTO and RPO
- [ ] Understand IDS vs IPS
- [ ] Know common ports by memory

---

*Next → Phase 4: Ethical Hacking & Penetration Testing*

#cybersecurity #phase3 #security-fundamentals #CIA-triad #cryptography #zero-trust #threats #risk-management #comptia-security-plus
