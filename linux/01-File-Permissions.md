# Linux File Permissions

> Personal notes by Utkarsh Solanki | Cybersecurity & AI Student  
> [LinkedIn](https://linkedin.com/in/utkarsh-solanki-337806252) · [GitHub](https://github.com/Utkarsh464)

---

## Table of Contents

- [Permission Basics](#permission-basics)
- [Reading Permissions](#reading-permissions)
- [chmod](#chmod)
- [chown & chgrp](#chown--chgrp)
- [Special Permissions — SUID, SGID, Sticky Bit](#special-permissions--suid-sgid-sticky-bit)
- [umask](#umask)
- [Security Perspective](#security-perspective)

---

## Permission Basics

Every file/directory in Linux has:
- An **owner** (user)
- A **group**
- **Others** (everyone else)

And three permission types:

| Symbol | Name | File | Directory |
|--------|------|------|-----------|
| `r` | Read | View contents | List files (`ls`) |
| `w` | Write | Modify file | Create/delete files inside |
| `x` | Execute | Run as program | Enter directory (`cd`) |

---

## Reading Permissions

```bash
ls -l
# -rwxr-xr-- 1 utkarsh dev 4096 Jun 10 file.sh
#  │││││││││
#  │││││││└└─ Others: r-- (read only)
#  ││││└└└─── Group:  r-x (read + execute)
#  │└└└─────── Owner:  rwx (read + write + execute)
#  └─────────── File type: - (file), d (dir), l (symlink)
```

### Octal Values

| Permission | Binary | Octal |
|------------|--------|-------|
| `---` | 000 | 0 |
| `--x` | 001 | 1 |
| `-w-` | 010 | 2 |
| `-wx` | 011 | 3 |
| `r--` | 100 | 4 |
| `r-x` | 101 | 5 |
| `rw-` | 110 | 6 |
| `rwx` | 111 | 7 |

> **Common combos:** `755` = rwxr-xr-x | `644` = rw-r--r-- | `600` = rw------- | `777` = rwxrwxrwx

---

## chmod

```bash
# Octal (numeric) mode
chmod 755 file.sh       # rwxr-xr-x
chmod 644 file.txt      # rw-r--r--
chmod 600 id_rsa        # rw------- (private key — must be this)
chmod 777 file          # rwxrwxrwx (dangerous)

# Symbolic mode
chmod u+x file.sh       # add execute for owner
chmod g-w file.txt      # remove write from group
chmod o-r file.txt      # remove read from others
chmod a+r file.txt      # add read for all (a = all)
chmod u+x,g-w file      # multiple changes

# Recursive
chmod -R 755 /var/www/  # apply to directory and all contents
```

---

## chown & chgrp

```bash
# Change owner
chown utkarsh file.txt

# Change owner and group
chown utkarsh:dev file.txt

# Change group only
chgrp dev file.txt

# Recursive
chown -R utkarsh:dev /var/www/

# View owner/group
ls -l file.txt
stat file.txt
```

---

## Special Permissions — SUID, SGID, Sticky Bit

### SUID (Set User ID) — Octal `4xxx`

```bash
chmod 4755 /usr/bin/passwd
# or
chmod u+s file
```

- When set on an **executable**: runs with the **owner's privileges**, not the caller's
- Classic example: `/usr/bin/passwd` — needs root to write `/etc/shadow`, but any user runs it
- **Security risk:** SUID on root-owned binaries = privilege escalation vector

```bash
# Find all SUID binaries (critical in pentesting)
find / -perm -4000 -type f 2>/dev/null
```

### SGID (Set Group ID) — Octal `2xxx`

```bash
chmod 2755 /shared/dir
# or
chmod g+s dir
```

- On a **file**: runs with group's privileges
- On a **directory**: new files inherit the directory's group (useful for shared dirs)

```bash
# Find SGID binaries
find / -perm -2000 -type f 2>/dev/null
```

### Sticky Bit — Octal `1xxx`

```bash
chmod 1777 /tmp
# or
chmod +t /tmp
```

- On a **directory**: only the file owner (or root) can delete their own files
- Classic use: `/tmp` — everyone can write, no one can delete others' files

```bash
# Check sticky bit
ls -ld /tmp
# drwxrwxrwt — the 't' at the end = sticky bit
```

### Reading Special Permissions

```bash
ls -l /usr/bin/passwd
# -rwsr-xr-x  → 's' in owner execute = SUID

ls -ld /shared
# drwxrwsr-x  → 's' in group execute = SGID

ls -ld /tmp
# drwxrwxrwt  → 't' in others execute = Sticky bit
```

---

## umask

`umask` defines **default permissions removed** from new files/directories.

```bash
umask          # view current umask (usually 022)
umask 027      # set new umask
```

| umask | New File (666-umask) | New Dir (777-umask) |
|-------|----------------------|---------------------|
| 022 | 644 (rw-r--r--) | 755 (rwxr-xr-x) |
| 027 | 640 (rw-r-----) | 750 (rwxr-x---) |
| 077 | 600 (rw-------) | 700 (rwx------) |

> Files never get execute by default — max is 666 before umask.

---

## Security Perspective

### Things to always check in pentesting / CTFs

```bash
# World-writable files (anyone can modify)
find / -perm -o+w -type f 2>/dev/null

# World-writable directories
find / -perm -o+w -type d 2>/dev/null

# SUID binaries (privilege escalation)
find / -perm -4000 -type f 2>/dev/null

# SGID binaries
find / -perm -2000 -type f 2>/dev/null

# Files owned by root but writable by others
find / -user root -perm -o+w 2>/dev/null

# No-owner files (orphaned)
find / -nouser -o -nogroup 2>/dev/null
```

### Hardening Rules

| Rule | Why |
|------|-----|
| SSH private keys must be `600` | If readable by others, SSH rejects them |
| Web files: `644` for files, `755` for dirs | Prevent execution of uploaded files |
| Never use `777` in production | Anyone can modify or execute |
| `/etc/passwd` should be `644` | Readable but not writable |
| `/etc/shadow` should be `640` or `000` | Only root reads password hashes |
| Scripts in cron: check write permissions | World-writable cron script = privesc |

---

*Last updated: June 2026*
