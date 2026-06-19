# OS Security — Locking Down the Machine

> Personal notes by Utkarsh Solanki | Cybersecurity & AI Student  
> GitHub: [github.com/Utkarsh464](https://github.com/Utkarsh464) | LinkedIn: [linkedin.com/in/utkarsh-solanki-337806252](https://linkedin.com/in/utkarsh-solanki-337806252)

---

## The Mindset

Operating systems are complex. Complexity breeds bugs. Bugs breed exploits. The goal of OS security is to **reduce the attack surface** — turn off what you don't need, update what you do, and layer defenses so no single failure is catastrophic.

**Defense in depth** on a single machine:
```
Application layer → User permissions → OS hardening → Kernel security → Hardware security
```

---

## User Accounts & Privilege Separation

The most fundamental security concept in any OS: **don't run as admin/root**.

### Windows — UAC

UAC (User Account Control) is the popup that says "Do you want to allow this app to make changes?" It runs admin tasks with a split token — the user gets a standard token by default and only escalates when needed.

```powershell
# Check UAC status
Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "EnableLUA"
# 1 = enabled, 0 = disabled (don't disable)

# Check if you're admin
net user %username%
```

**What attackers do:** Bypass UAC with techniques like:
- **CMSTP** — code execution via Microsoft Connection Manager Profile Installer
- **Fodhelper** — exploits Windows features to elevate without prompt
- **DLL hijacking** — plant a malicious DLL in a path the admin tool loads

### Linux — sudo and su

```bash
# Never log in as root. Use sudo for specific commands.
sudo apt update           # run ONE command as root
sudo -i                   # root shell (be careful)
sudo -l                   # what commands can this user sudo?
```

**Common misconfigurations attackers look for:**
```bash
# If a user can sudo ANY of these without password → game over
sudo /usr/bin/vim
sudo /usr/bin/find
sudo /usr/bin/python3
sudo /bin/bash

# Check GTFOBins for exploitation methods
# https://gtfobins.github.io
```

### macOS — SIP and Gatekeeper

- **SIP (System Integrity Protection)** — prevents even root from modifying system files
- **Gatekeeper** — only allows signed/notarized apps to run
- **FileVault** — full disk encryption

---

## The Principle of Least Privilege

Every user, process, and service should have **only the permissions it actually needs**.

- A database server doesn't need to write to the web directory
- A developer doesn't need production access
- A web server shouldn't run as root

**Attackers always escalate.** They get in as a low-privilege user, then hunt for misconfigurations that let them become root/admin.

---

## Authentication & Logon

### Password Storage

| OS | Hash Storage | Algorithm |
|----|-------------|-----------|
| Linux | `/etc/shadow` | SHA-512 (default), yescrypt (modern) |
| Windows | SAM file (System32/config/SAM) | NTLM hash |
| macOS | `/var/db/dslocal/` | PBKDF2-derived |

```bash
# Linux — hashes are in /etc/shadow (root only)
sudo cat /etc/shadow
# $6$salt$hash — the $6$ means SHA-512

# Windows — dump SAM hashes (need SYSTEM privileges)
# meterpreter> hashdump
# or: impacket-secretsdump
```

### Lockout Policies

Always enable account lockout after X failed attempts. Prevents brute force.

```bash
# Linux — /etc/pam.d/common-auth
# Windows: secpol.msc → Account Lockout Policy
```

---

## Patch Management

Unpatched software is the #1 reason systems get breached.

| Vulnerability | Year | What it did |
|--------------|------|-------------|
| EternalBlue (MS17-010) | 2017 | SMB RCE — took down the NHS with WannaCry |
| Log4Shell (CVE-2021-44228) | 2021 | RCE in Java logging library |
| PrintNightmare (CVE-2021-34527) | 2021 | Windows Print Spooler RCE |
| Dirty Pipe (CVE-2022-0847) | 2022 | Linux kernel privesc |

**The fix is boring but works:** Update. Regularly. Test updates before deploying to production.

```bash
# Linux
sudo apt update && sudo apt upgrade   # Debian/Ubuntu
sudo yum update                        # RHEL/CentOS

# Windows
# Settings → Windows Update or:
wuauclt /detectnow /updatenow
```

---

## Secure Boot & Trusted Boot

### UEFI Secure Boot

Ensures that only trusted, signed bootloaders and kernel can start the system. Prevents **bootkits** — malware that loads before the OS and is invisible to normal security tools.

```bash
# Check Secure Boot status on Linux
mokutil --sb-state
# SecureBoot: enabled

# Check on Windows
msinfo32 → Secure Boot State
```

### Measured Boot (Windows)

Windows records measurements (hashes) of every boot component in the TPM chip. If anything has changed (malware modified the bootloader), the system can detect it.

---

## Hardening Checklists

### Windows Hardening

```powershell
# 1. Keep Windows updated
# 2. Enable Windows Defender + Real-time protection
# 3. Enable BitLocker (disk encryption)
# 4. Disable SMBv1 (ancient, vulnerable)
Disable-WindowsOptionalFeature -Online -FeatureName smb1protocol
# 5. Enable firewall, block inbound by default
# 6. Turn off unnecessary services (Print Spooler if not needed)
# 7. Enable PowerShell logging and constrained language mode
# 8. Use LAPS for local admin passwords
# 9. Restrict RDP to specific IPs
# 10. Enable Credential Guard (prevents pass-the-hash)
```

### Linux Hardening

```bash
# 1. Keep packages updated
sudo apt update && sudo apt upgrade

# 2. Disable root login over SSH
# In /etc/ssh/sshd_config:
PermitRootLogin no

# 3. Use SSH key auth, disable password auth
PasswordAuthentication no

# 4. Set restrictive umask
umask 027

# 5. Enable and configure firewall
sudo ufw enable
sudo ufw default deny incoming
sudo ufw allow ssh

# 6. Secure shared memory
# In /etc/fstab:
tmpfs /run/shm tmpfs defaults,noexec,nosuid 0 0

# 7. Check for unusual cron jobs
ls -la /etc/cron*

# 8. Audit SUID binaries
find / -perm -4000 -type f 2>/dev/null

# 9. Enable automatic security updates
sudo dpkg-reconfigure --priority=low unattended-upgrades

# 10. Harden kernel parameters (sysctl)
# /etc/sysctl.d/99-hardening.conf
net.ipv4.conf.all.rp_filter = 1        # Reverse path filtering
net.ipv4.tcp_syncookies = 1            # SYN flood protection
net.ipv4.conf.all.log_martians = 1     # Log spoofed IPs
kernel.dmesg_restrict = 1              # Restrict kernel log access
```

---

## Logging & Auditing

### Windows Event Logs

| Log | What it contains |
|-----|-----------------|
| Security (Event ID 4624) | Successful logons |
| Security (Event ID 4625) | Failed logons |
| Security (Event ID 4688) | Process creation |
| System | Service starts/stops, driver loads |

```powershell
# Query last 10 failed logins
Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625} -MaxEvents 10

# Enable command-line logging (captures what commands were run)
# Via GPO: Administrative Templates → System → Audit Process Creation
```

### Linux Logs

```bash
/var/log/auth.log          # Authentication attempts
/var/log/syslog            # General system messages
/var/log/kern.log          # Kernel messages
journalctl -xe             # Systemd journal

# Monitor auth failures in real-time
tail -f /var/log/auth.log | grep "Failed password"

# See all sudo commands executed
grep "sudo" /var/log/auth.log

# Check for brute force attempts
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn
```

---

## Common OS Vulnerabilities (What Attackers Exploit)

### Linux

| Vulnerability | What it does |
|--------------|-------------|
| Dirty Cow (CVE-2016-5195) | Race condition in kernel → root |
| Dirty Pipe (CVE-2022-0847) | Overwrite any file (including /etc/passwd) |
| PwnKit (CVE-2021-4034) | Buffer overflow in pkexec → root |
| Sudo Baron Samedit (CVE-2021-3156) | Heap overflow in sudo → root |

### Windows

| Vulnerability | What it does |
|--------------|-------------|
| EternalBlue (MS17-010) | SMB RCE |
| PrintNightmare | Print Spooler RCE |
| ZeroLogon (CVE-2020-1472) | Domain controller compromise |
| PetitPotam | Force domain controller to authenticate to attacker |

**Real talk:** Most breaches don't use zero-days. They use **unpatched known vulnerabilities** that are years old. Patch management is the single highest-impact security investment you can make.

---

## The 80/20 of OS Security

If you do nothing else:

1. **Update everything** — OS, browser, apps
2. **Don't run as admin** — use a standard user account
3. **Use strong, unique passwords** (+ a password manager)
4. **Enable disk encryption** — BitLocker, LUKS, FileVault
5. **Enable the firewall** — block inbound by default
6. **Review logs** — know what normal looks like so you spot abnormal
7. **Back up** — 3-2-1 rule for anything you can't afford to lose

---

*Last updated: June 2026*
