# Linux Users & Groups

> Personal notes by Utkarsh Solanki | Cybersecurity & AI Student  
> [LinkedIn](https://linkedin.com/in/utkarsh-solanki-337806252) · [GitHub](https://github.com/Utkarsh464)

---

## Table of Contents

- [Key Files](#key-files)
- [User Management](#user-management)
- [Group Management](#group-management)
- [sudo & su](#sudo--su)
- [Security Perspective](#security-perspective)

---

## Key Files

### /etc/passwd

Stores user account info. Readable by all users.

```
utkarsh:x:1000:1000:Utkarsh Solanki:/home/utkarsh:/bin/bash
│       │ │    │    │               │             └── Login shell
│       │ │    │    │               └── Home directory
│       │ │    │    └── Comment/Full name (GECOS)
│       │ │    └── Primary GID
│       │ └── UID
│       └── Password placeholder (x = in /etc/shadow)
└── Username
```

```bash
cat /etc/passwd
grep utkarsh /etc/passwd
```

### /etc/shadow

Stores **hashed passwords**. Only root can read.

```
utkarsh:$6$salt$hashedpassword:19000:0:99999:7:::
│       │                      │     │ │     └── Password warning days
│       │                      │     │ └── Max password age
│       │                      │     └── Min password age
│       │                      └── Last password change (days since epoch)
│       └── Hashed password ($6$ = SHA-512)
└── Username
```

Hash prefixes:
| Prefix | Algorithm |
|--------|-----------|
| `$1$` | MD5 (weak) |
| `$5$` | SHA-256 |
| `$6$` | SHA-512 (standard) |
| `$y$` | yescrypt (modern) |
| `*` or `!` | Account locked |

### /etc/group

```
dev:x:1001:utkarsh,bob
│   │ │    └── Members
│   │ └── GID
│   └── Password (rarely used)
└── Group name
```

```bash
cat /etc/group
groups utkarsh       # show groups a user belongs to
id utkarsh           # uid, gid, and all groups
```

---

## User Management

```bash
# Add user
useradd utkarsh                        # basic, no home dir
useradd -m utkarsh                     # with home directory
useradd -m -s /bin/bash utkarsh        # with bash shell
useradd -m -G sudo,dev utkarsh         # with supplementary groups

# Set/change password
passwd utkarsh

# Modify user
usermod -aG sudo utkarsh               # add to sudo group (don't miss -a)
usermod -s /bin/zsh utkarsh            # change shell
usermod -l newname utkarsh             # rename user
usermod -L utkarsh                     # lock account
usermod -U utkarsh                     # unlock account

# Delete user
userdel utkarsh                        # keep home dir
userdel -r utkarsh                     # remove home dir too

# Switch user
su utkarsh                             # switch to user
su - utkarsh                           # switch with environment
su -                                   # switch to root

# View user info
id                                     # current user
id utkarsh                             # specific user
whoami                                 # just the username
who                                    # logged-in users
w                                      # logged-in users + activity
last                                   # login history
lastlog                                # last login for all users
```

---

## Group Management

```bash
# Add group
groupadd dev

# Add user to group
usermod -aG dev utkarsh        # -a = append (important, not replace)
gpasswd -a utkarsh dev         # alternative

# Remove user from group
gpasswd -d utkarsh dev

# Delete group
groupdel dev

# View groups
groups                         # current user's groups
groups utkarsh                 # specific user
cat /etc/group | grep dev      # all members of a group
```

---

## sudo & su

### sudo

```bash
sudo command                   # run as root
sudo -u bob command            # run as another user
sudo -i                        # root shell (login shell)
sudo -s                        # root shell (current env)
sudo -l                        # list allowed sudo commands
sudo -l -U utkarsh             # list for specific user
sudo !!                        # re-run last command as sudo
```

### /etc/sudoers

```bash
visudo                         # always edit with visudo (validates syntax)

# Format:
# user  host=(runas)  commands

utkarsh ALL=(ALL:ALL) ALL      # full sudo
utkarsh ALL=(ALL) NOPASSWD: ALL  # no password (dangerous)
utkarsh ALL=(ALL) /bin/systemctl  # only specific command

# Group sudo
%sudo ALL=(ALL:ALL) ALL        # everyone in sudo group
```

### Dangerous sudoers entries to look for (privesc)

```bash
sudo -l
# If you see any of these, check GTFOBins:
# (ALL) NOPASSWD: /bin/bash
# (ALL) NOPASSWD: /usr/bin/python3
# (ALL) NOPASSWD: /usr/bin/vim
# (ALL) NOPASSWD: /usr/bin/find
```

---

## Security Perspective

```bash
# Find all users with UID 0 (root equivalent — should only be root)
awk -F: '($3 == 0)' /etc/passwd

# Find users with no password
awk -F: '($2 == "")' /etc/shadow

# Find users with login shell (actual human accounts)
grep -v '/nologin\|/false' /etc/passwd

# Check who has sudo access
cat /etc/sudoers
getent group sudo
getent group wheel

# Check for recently added users
ls -lt /home/
cat /etc/passwd | sort -t: -k3 -n   # sort by UID

# Check login history for suspicious activity
last
lastb                                 # failed login attempts
grep "Failed password" /var/log/auth.log

# Check running processes by user
ps aux | grep root
ps aux --sort=user
```

### Privilege Escalation Checklist

```bash
sudo -l                                          # misconfigured sudo
find / -perm -4000 2>/dev/null                   # SUID binaries
cat /etc/crontab                                 # writable cron scripts
find / -writable -type f 2>/dev/null             # writable files
env                                              # PATH hijacking opportunities
cat ~/.bash_history                              # credentials in history
find / -name "*.conf" 2>/dev/null | xargs grep -l "password"  # config leaks
```

---

*Last updated: June 2026*
