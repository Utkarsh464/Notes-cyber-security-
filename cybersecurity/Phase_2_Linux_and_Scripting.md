# Phase 2 — Linux & Scripting
> Complete self-contained notes. No external resources needed.
> Estimated time: 1–2 months

---

## Table of Contents
1. [1. Linux Directory Structure](#1-linux-directory-structure)
2. [2. Essential Linux Commands](#2-essential-linux-commands)
3. [3. File Permissions](#3-file-permissions)
4. [4. Users & Groups](#4-users--groups)
5. [5. Process Management](#5-process-management)
6. [6. Package Management](#6-package-management)
7. [7. Networking Commands](#7-networking-commands)
8. [8. SSH & Remote Access](#8-ssh--remote-access)
9. [9. Services & Systemd](#9-services--systemd)
10. [10. Cron Jobs](#10-cron-jobs)
11. [11. Log Analysis](#11-log-analysis)
12. [12. Bash Scripting](#12-bash-scripting)
13. [13. Python for Security](#13-python-for-security)
14. [14. Quick Reference Cheatsheet](#14-quick-reference-cheatsheet)

---

## 1. Linux Directory Structure

Everything in Linux is a file. There is one root `/` and everything branches from it.

```
/
├── bin       → Essential user binaries (ls, cp, mv, cat)
├── sbin      → System binaries (only root, ifconfig, iptables)
├── etc       → Configuration files (passwd, hosts, ssh/sshd_config)
├── home      → User home directories (/home/akio)
├── root      → Root user's home directory
├── var       → Variable data (logs, databases, mail)
│   └── log   → System logs
├── tmp       → Temporary files (cleared on reboot)
├── usr       → User programs and libraries
│   ├── bin   → Non-essential user binaries
│   └── local → Manually installed software
├── proc      → Virtual filesystem — running kernel/process info
├── sys       → Virtual filesystem — hardware/kernel info
├── dev       → Device files (disks, terminals)
├── lib       → Shared libraries
├── mnt       → Mount point for temporary mounts
├── media     → Auto-mounted removable media (USB)
├── opt       → Optional/third-party software
└── boot      → Boot loader, kernel
```

**Key files to know (security context):**

| File | Purpose |
|------|---------|
| `/etc/passwd` | User accounts (no passwords) |
| `/etc/shadow` | Hashed passwords (root only) |
| `/etc/group` | Group definitions |
| `/etc/hosts` | Static hostname → IP mappings |
| `/etc/hostname` | Machine hostname |
| `/etc/resolv.conf` | DNS server config |
| `/etc/sudoers` | Who can run sudo and what |
| `/etc/ssh/sshd_config` | SSH server config |
| `/etc/crontab` | System cron jobs |
| `/var/log/auth.log` | Authentication events |
| `/var/log/syslog` | General system log |
| `/proc/version` | Kernel version |
| `/proc/net/tcp` | Network connections |

---

## 2. Essential Linux Commands

### Navigation
```bash
pwd                    # print working directory
ls                     # list files
ls -la                 # long format + hidden files
ls -lh                 # human readable sizes
cd /path/to/dir        # change directory
cd ..                  # go up one level
cd ~                   # go to home directory
cd -                   # go to previous directory
```

### File Operations
```bash
touch file.txt         # create empty file
mkdir dirname          # create directory
mkdir -p a/b/c         # create nested directories
cp file.txt copy.txt   # copy file
cp -r dir/ newdir/     # copy directory recursively
mv file.txt new.txt    # move/rename file
rm file.txt            # delete file
rm -rf dirname/        # delete directory (CAREFUL — no undo)
ln -s /path/to/file symlink   # create symbolic link
```

### Reading Files
```bash
cat file.txt           # print entire file
less file.txt          # paginated view (q to quit)
more file.txt          # older paginator
head file.txt          # first 10 lines
head -n 20 file.txt    # first 20 lines
tail file.txt          # last 10 lines
tail -n 20 file.txt    # last 20 lines
tail -f file.txt       # follow live (great for logs)
wc -l file.txt         # count lines
wc -w file.txt         # count words
```

### Searching
```bash
# find — search for files
find / -name "passwd"               # find by name
find / -name "*.txt"                # find by extension
find / -type f -name "config*"      # files only
find / -type d -name "log*"         # directories only
find / -size +10M                   # larger than 10MB
find / -mtime -7                    # modified in last 7 days
find / -perm -4000                  # SUID files (security!)
find / -user root -writable 2>/dev/null   # root-owned writable files

# locate — faster but uses database
locate passwd
updatedb                            # update locate database

# which / whereis — find binaries
which python3
whereis nmap
```

### Text Processing
```bash
# grep — search inside files
grep "error" file.txt               # find lines with "error"
grep -i "error" file.txt            # case insensitive
grep -r "password" /etc/            # recursive search
grep -n "error" file.txt            # show line numbers
grep -v "error" file.txt            # invert — exclude matching lines
grep -c "error" file.txt            # count matching lines
grep -E "error|warning" file.txt    # regex — OR
grep -A 3 "error" file.txt          # show 3 lines AFTER match
grep -B 3 "error" file.txt          # show 3 lines BEFORE match

# cut — extract columns
cut -d':' -f1 /etc/passwd           # extract field 1, delimiter ':'
cut -d',' -f2,3 file.csv            # extract fields 2 and 3

# awk — column-based processing
awk '{print $1}' file.txt           # print first column
awk '{print $1,$3}' file.txt        # print col 1 and 3
awk -F':' '{print $1}' /etc/passwd  # use ':' as delimiter
awk '$3 > 1000' /etc/passwd         # print lines where col 3 > 1000
awk '{print NR, $0}' file.txt       # print line numbers

# sed — stream editor
sed 's/old/new/g' file.txt          # replace all occurrences
sed 's/old/new/' file.txt           # replace first on each line
sed -i 's/old/new/g' file.txt       # edit file in-place
sed '/pattern/d' file.txt           # delete lines matching pattern
sed -n '5,10p' file.txt             # print lines 5 to 10
sed 'G' file.txt                    # add blank line after each line

# sort & uniq
sort file.txt                       # alphabetical sort
sort -n file.txt                    # numerical sort
sort -r file.txt                    # reverse sort
sort -u file.txt                    # sort and remove duplicates
uniq file.txt                       # remove adjacent duplicates
uniq -c file.txt                    # count occurrences
sort file.txt | uniq -c | sort -rn  # frequency count (very useful)

# tr — translate/delete characters
echo "HELLO" | tr 'A-Z' 'a-z'      # lowercase
cat file.txt | tr -d '\r'           # remove carriage returns
cat file.txt | tr -s ' '            # squeeze multiple spaces

# Combining with pipes
cat /etc/passwd | cut -d':' -f1 | sort           # list all usernames sorted
grep "Failed" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn
```

### Input / Output Redirection
```bash
command > file.txt         # redirect stdout to file (overwrite)
command >> file.txt        # redirect stdout to file (append)
command 2> error.txt       # redirect stderr to file
command 2>&1               # redirect stderr to stdout
command > out.txt 2>&1     # both stdout and stderr to file
command < input.txt        # use file as stdin
command1 | command2        # pipe stdout of cmd1 to stdin of cmd2

# /dev/null — discard output
command 2>/dev/null        # suppress errors
command > /dev/null 2>&1   # suppress all output
```

### Disk Usage
```bash
df -h                      # disk free — filesystem usage
du -sh /var/log/           # disk usage of directory
du -sh *                   # size of each item in current dir
du -sh * | sort -h         # sort by size
lsblk                      # list block devices
fdisk -l                   # partition info (root)
mount                      # show mounted filesystems
```

### Archiving & Compression
```bash
# tar
tar -cvf archive.tar dir/          # create tar
tar -xvf archive.tar               # extract tar
tar -czvf archive.tar.gz dir/      # create compressed tar.gz
tar -xzvf archive.tar.gz           # extract tar.gz
tar -cjvf archive.tar.bz2 dir/     # create tar.bz2
tar -xjvf archive.tar.bz2          # extract tar.bz2
tar -tf archive.tar                # list contents without extracting

# zip/unzip
zip archive.zip file1 file2
zip -r archive.zip dir/
unzip archive.zip
unzip archive.zip -d /target/dir/

# gzip
gzip file.txt              # compress (replaces file with file.txt.gz)
gunzip file.txt.gz         # decompress
zcat file.txt.gz           # read without decompressing
```

---

## 3. File Permissions

### Understanding Permission Bits

```
-rwxr-xr--  1  root  admin  4096  Jan 1 12:00  file.txt
│├──┤├──┤├──┤
│ │   │   └── Other permissions
│ │   └────── Group permissions
│ └────────── Owner permissions
└──────────── File type (- file, d directory, l symlink)

r = read    (4)
w = write   (2)
x = execute (1)
- = no permission (0)
```

**Reading permissions:**
```
rwx = 7 (4+2+1)
rw- = 6 (4+2+0)
r-x = 5 (4+0+1)
r-- = 4 (4+0+0)
-wx = 3 (0+2+1)
-w- = 2 (0+2+0)
--x = 1 (0+0+1)
--- = 0 (0+0+0)
```

**Common permission patterns:**
```
755 = rwxr-xr-x  → Owner: full, Group: read+exec, Other: read+exec (typical for dirs/scripts)
644 = rw-r--r--  → Owner: read+write, Group: read, Other: read (typical for files)
600 = rw-------  → Owner: read+write only (SSH private keys)
777 = rwxrwxrwx  → Everyone full access (DANGEROUS)
000 = ---------  → No permissions
```

### chmod — Change Permissions
```bash
# Numeric (octal) mode
chmod 755 file.txt         # rwxr-xr-x
chmod 644 file.txt         # rw-r--r--
chmod 600 ~/.ssh/id_rsa    # SSH key — must be 600
chmod 700 ~/.ssh/          # SSH dir
chmod -R 755 dir/          # recursive

# Symbolic mode
chmod u+x file.txt         # add execute for owner
chmod g-w file.txt         # remove write for group
chmod o+r file.txt         # add read for others
chmod a+x file.txt         # add execute for all (a = all)
chmod u=rwx,g=rx,o=r file  # set exact permissions
```

### chown — Change Ownership
```bash
chown user file.txt              # change owner
chown user:group file.txt        # change owner and group
chown :group file.txt            # change group only
chown -R user:group dir/         # recursive
```

### Special Permissions

**SUID (Set User ID) — 4000:**
When executed, file runs as the file OWNER (not the user running it).
```bash
chmod u+s file             # set SUID
chmod 4755 file            # numeric (4 prefix)
ls -la file                # shows: -rwsr-xr-x (s in owner execute position)

# Security risk: SUID root binary can be exploited for privilege escalation
find / -perm -4000 2>/dev/null    # find all SUID files
```

**SGID (Set Group ID) — 2000:**
File runs as the file's GROUP. On directories: new files inherit directory's group.
```bash
chmod g+s dir/             # set SGID on directory
chmod 2755 file            # numeric
ls -la                     # shows: drwxr-sr-x
```

**Sticky Bit — 1000:**
On directories: users can only delete their OWN files (used on /tmp).
```bash
chmod +t /tmp              # set sticky bit
chmod 1777 /tmp            # numeric
ls -la /tmp                # shows: drwxrwxrwt (t at end)
```

### umask
Default permissions for new files. New file permissions = max permissions - umask.
```bash
umask                      # show current umask (usually 022)
umask 022                  # set umask
# File default: 666 - 022 = 644
# Dir default:  777 - 022 = 755
```

---

## 4. Users & Groups

### User Management
```bash
# View users
cat /etc/passwd            # all users
# Format: username:x:UID:GID:comment:home:shell
# Example: akio:x:1000:1000:Akio:/home/akio:/bin/bash

id                         # current user UID, GID, groups
id username                # specific user
whoami                     # current username
who                        # logged in users
w                          # logged in users + activity
last                       # login history
lastlog                    # last login for all users

# Create user
useradd username           # basic creation
useradd -m -s /bin/bash -G sudo username   # with home, shell, group
passwd username            # set password
adduser username           # interactive (Debian/Ubuntu)

# Modify user
usermod -aG groupname username   # add to group (-a = append)
usermod -s /bin/bash username    # change shell
usermod -d /new/home username    # change home dir
usermod -L username              # lock account
usermod -U username              # unlock account

# Delete user
userdel username           # delete user
userdel -r username        # delete user + home directory
```

### /etc/passwd Format
```
root:x:0:0:root:/root:/bin/bash
 │   │ │ │  │      │      └── Login shell
 │   │ │ │  │      └───────── Home directory
 │   │ │ │  └──────────────── Comment/GECOS
 │   │ │ └─────────────────── Primary GID
 │   │ └───────────────────── UID
 │   └───────────────────────  Password ('x' = in /etc/shadow)
 └───────────────────────────  Username
```

**Special UIDs:**
- `0` = root
- `1–999` = system accounts
- `1000+` = regular users

### /etc/shadow Format
```
root:$6$salt$hashedpassword:18000:0:99999:7:::
  │       │                   │
  │       │                   └── Days since Jan 1 1970 password last changed
  │       └───────────────────── Hashed password ($6$ = SHA-512)
  └───────────────────────────── Username
```

### Group Management
```bash
cat /etc/group             # all groups
# Format: groupname:x:GID:members

groups                     # groups current user belongs to
groups username            # groups of specific user

groupadd groupname         # create group
groupmod -n newname oldname   # rename group
groupdel groupname         # delete group
gpasswd -a username group  # add user to group
gpasswd -d username group  # remove user from group
```

### sudo
```bash
sudo command               # run as root
sudo -u user command       # run as specific user
sudo -i                    # interactive root shell
sudo -l                    # list what current user can sudo
sudo su -                  # switch to root (full environment)
su - username              # switch to user

# /etc/sudoers — configure sudo access
# NEVER edit directly — use:
visudo

# Examples in /etc/sudoers:
# akio ALL=(ALL) ALL             → akio can run anything as anyone
# akio ALL=(ALL) NOPASSWD: ALL   → without password
# akio ALL=(root) /usr/bin/apt   → only apt as root
```

---

## 5. Process Management

### Viewing Processes
```bash
ps                         # processes in current shell
ps aux                     # ALL processes (a=all users, u=user format, x=no terminal)
ps aux | grep nginx        # find specific process
ps -ef                     # full format
pstree                     # tree view of processes

top                        # interactive process viewer (q to quit)
htop                       # better top (may need install)

# top keyboard shortcuts:
# k → kill process
# r → renice (change priority)
# q → quit
# M → sort by memory
# P → sort by CPU
# 1 → show per-core CPU

# Process info from /proc
ls /proc/                  # one dir per PID
cat /proc/1/status         # info about PID 1
cat /proc/1/cmdline        # command that started it
cat /proc/1/environ        # environment variables
```

### Process States
```
R = Running
S = Sleeping (interruptible)
D = Sleeping (uninterruptible — waiting for I/O)
Z = Zombie (finished but parent hasn't cleaned up)
T = Stopped
```

### Controlling Processes
```bash
# Run in background
command &                  # run in background
jobs                       # list background jobs
fg %1                      # bring job 1 to foreground
bg %1                      # send job 1 to background
Ctrl+Z                     # pause current process (send to background stopped)
Ctrl+C                     # kill current process

# Kill processes
kill PID                   # send SIGTERM (graceful stop)
kill -9 PID                # send SIGKILL (force kill)
kill -15 PID               # SIGTERM (same as default)
kill -1 PID                # SIGHUP (reload config)
killall nginx              # kill all processes named nginx
pkill -f "python3 server"  # kill by pattern

# Signals
# SIGTERM (15) = Please stop gracefully
# SIGKILL (9)  = Stop NOW, no cleanup
# SIGHUP  (1)  = Reload configuration
# SIGSTOP (19) = Pause process
# SIGCONT (18) = Resume paused process
```

### Process Priority (Nice)
```bash
# Nice value: -20 (highest priority) to 19 (lowest priority)
nice -n 10 command         # start with nice value 10
renice 10 -p PID           # change priority of running process
renice -5 -p PID           # increase priority (needs root)
```

### nohup & screen/tmux
```bash
# nohup — keep running after logout
nohup command &
nohup python3 server.py > output.log 2>&1 &

# screen — terminal multiplexer
screen                     # start session
screen -S name             # named session
Ctrl+A, D                  # detach
screen -ls                 # list sessions
screen -r name             # reattach

# tmux — better alternative
tmux                       # start
tmux new -s name           # named session
Ctrl+B, D                  # detach
tmux ls                    # list
tmux attach -t name        # reattach
```

---

## 6. Package Management

### Debian/Ubuntu — APT
```bash
# Update & upgrade
apt update                 # refresh package lists
apt upgrade                # upgrade installed packages
apt full-upgrade           # upgrade + remove obsolete

# Install / remove
apt install package        # install
apt install pkg1 pkg2      # install multiple
apt remove package         # remove (keep config)
apt purge package          # remove + config files
apt autoremove             # remove unused dependencies

# Search
apt search keyword         # search packages
apt show package           # package details
dpkg -l | grep package     # check if installed
dpkg -l                    # list all installed

# dpkg (low-level)
dpkg -i package.deb        # install .deb file
dpkg -r package            # remove
dpkg -l                    # list installed
dpkg --get-selections      # all installed packages

# Cache
apt clean                  # clear downloaded packages
apt autoclean              # clear old downloaded packages
```

### RHEL/CentOS — YUM/DNF
```bash
# DNF (modern, Fedora/RHEL 8+)
dnf update
dnf install package
dnf remove package
dnf search keyword
dnf info package
dnf list installed

# YUM (older RHEL/CentOS 7)
yum update
yum install package
yum remove package
yum search keyword

# RPM (low-level)
rpm -ivh package.rpm       # install
rpm -e package             # remove
rpm -qa                    # list all installed
rpm -qi package            # package info
```

### Compiling from Source
```bash
wget https://source.tar.gz
tar -xzvf source.tar.gz
cd source/
./configure
make
sudo make install
```

---

## 7. Networking Commands

### Network Interfaces
```bash
ip a                       # show all interfaces and IPs
ip addr show eth0          # specific interface
ip link show               # link layer info
ip link set eth0 up        # bring interface up
ip link set eth0 down      # bring interface down
ifconfig                   # older command (may need net-tools)
ifconfig eth0              # specific interface

# Set IP manually
ip addr add 192.168.1.100/24 dev eth0
ip addr del 192.168.1.100/24 dev eth0
```

### Routing
```bash
ip route                   # routing table
ip route show              # same
route -n                   # older command
ip route add default via 192.168.1.1    # add default gateway
ip route add 10.0.0.0/8 via 192.168.1.1  # add route
ip route del 10.0.0.0/8                  # delete route
```

### DNS
```bash
nslookup google.com        # DNS lookup (interactive)
nslookup google.com 8.8.8.8  # use specific DNS server
dig google.com             # detailed DNS lookup
dig google.com MX          # MX records
dig @8.8.8.8 google.com    # use specific DNS server
host google.com            # simple lookup
cat /etc/resolv.conf       # DNS server config
```

### Connectivity Testing
```bash
ping google.com            # ICMP ping
ping -c 4 google.com       # ping 4 times
ping -i 0.2 google.com     # ping every 0.2 seconds
traceroute google.com      # trace network path
tracepath google.com       # similar, no root needed
mtr google.com             # continuous traceroute (interactive)

curl https://google.com    # HTTP request
curl -I https://google.com # headers only
curl -L https://google.com # follow redirects
curl -o file.html https://google.com   # save to file
wget https://google.com/file.zip       # download file
```

### Connection Monitoring
```bash
netstat -antup             # all connections + PIDs
netstat -tlnp              # listening TCP ports
netstat -s                 # statistics

ss -antup                  # modern replacement for netstat
ss -tlnp                   # listening ports (fast)
ss -s                      # summary

# Reading ss/netstat output:
# LISTEN     = waiting for connections
# ESTABLISHED = active connection
# TIME_WAIT  = connection closing
# CLOSE_WAIT = remote side closed, waiting local

lsof -i :80                # what's using port 80
lsof -i TCP                # all TCP connections
fuser 80/tcp               # PID using port 80
```

### Packet Analysis
```bash
# tcpdump — CLI packet capture
tcpdump -i eth0            # capture on interface
tcpdump -i eth0 port 80    # filter by port
tcpdump -i eth0 host 192.168.1.100   # filter by host
tcpdump -i eth0 -w capture.pcap      # save to file
tcpdump -r capture.pcap    # read saved file
tcpdump -i eth0 'tcp port 80 and host 192.168.1.100'

# Wireshark — GUI packet analyzer
# Open .pcap files or capture live
# Useful filters:
# http                     → HTTP traffic
# tcp.port == 443          → HTTPS
# ip.addr == 192.168.1.1   → specific IP
# http.request.method == "POST"
```

### Netcat — The Swiss Army Knife
```bash
# Listen for connections
nc -lvnp 4444              # listen on port 4444

# Connect to host
nc 192.168.1.100 80        # connect to port 80

# Transfer files
# Receiver:
nc -lvnp 4444 > received_file
# Sender:
nc 192.168.1.100 4444 < file_to_send

# Banner grabbing
nc 192.168.1.100 22        # grab SSH banner
nc 192.168.1.100 80        # then type: HEAD / HTTP/1.0

# Port scanning
nc -zvn 192.168.1.100 20-80  # scan ports 20-80

# Chat
# Host A: nc -lvnp 4444
# Host B: nc hostA_IP 4444
```

### Firewall (iptables / ufw)
```bash
# UFW (simple frontend — Ubuntu)
ufw status
ufw enable
ufw disable
ufw allow 22               # allow SSH
ufw allow 80/tcp           # allow HTTP
ufw deny 23                # block telnet
ufw allow from 192.168.1.0/24  # allow subnet
ufw delete allow 80        # remove rule

# iptables (powerful, complex)
iptables -L                # list rules
iptables -L -n -v          # verbose with packet counts
iptables -A INPUT -p tcp --dport 22 -j ACCEPT    # allow SSH
iptables -A INPUT -p tcp --dport 80 -j ACCEPT    # allow HTTP
iptables -A INPUT -j DROP  # drop everything else
iptables -D INPUT -j DROP  # delete rule
iptables-save > rules.txt  # save rules
iptables-restore < rules.txt  # restore rules
```

---

## 8. SSH & Remote Access

### SSH Basics
```bash
ssh user@host              # connect
ssh user@192.168.1.100     # connect by IP
ssh -p 2222 user@host      # custom port
ssh -i ~/.ssh/id_rsa user@host  # specify key

# First connection — verify host fingerprint
# The authenticity of host '...' can't be established.
# RSA key fingerprint is SHA256:...
# Are you sure you want to continue connecting? yes
```

### SSH Key Authentication (More Secure Than Passwords)
```bash
# Generate key pair
ssh-keygen -t ed25519 -C "your@email.com"    # modern, recommended
ssh-keygen -t rsa -b 4096                     # RSA 4096-bit

# Keys created:
# ~/.ssh/id_ed25519      → PRIVATE key (never share)
# ~/.ssh/id_ed25519.pub  → PUBLIC key (safe to share)

# Copy public key to server
ssh-copy-id user@host
# or manually:
cat ~/.ssh/id_ed25519.pub | ssh user@host "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# Permissions must be correct
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
chmod 600 ~/.ssh/authorized_keys
```

### SSH Config File
`~/.ssh/config` — save connection settings:
```
Host myserver
    HostName 192.168.1.100
    User akio
    Port 2222
    IdentityFile ~/.ssh/id_ed25519

Host jumphost
    HostName jump.target.com
    User admin
    ForwardAgent yes
```
Now connect with just: `ssh myserver`

### Hardening SSH Server (/etc/ssh/sshd_config)
```bash
# Edit config
nano /etc/ssh/sshd_config

# Key settings:
Port 2222                          # change default port
PermitRootLogin no                 # disable root login
PasswordAuthentication no          # keys only
PubkeyAuthentication yes           # enable key auth
MaxAuthTries 3                     # limit attempts
AllowUsers akio                    # whitelist users
X11Forwarding no                   # disable if not needed
ClientAliveInterval 300            # timeout idle sessions
ClientAliveCountMax 2

# Restart after changes
systemctl restart sshd
```

### SSH Tunneling
```bash
# Local port forward — access remote service locally
ssh -L 8080:192.168.1.10:80 user@jumphost
# Now: curl http://localhost:8080 → reaches 192.168.1.10:80

# Remote port forward — expose local service to remote
ssh -R 9090:localhost:3000 user@jumphost
# Now: accessing jumphost:9090 → reaches your localhost:3000

# Dynamic SOCKS proxy
ssh -D 9050 user@jumphost
# Use with proxychains: proxychains curl http://internal.site

# Keep alive
ssh -N -f -L 8080:192.168.1.10:80 user@jumphost
# -N = no command, -f = background
```

### SCP & SFTP (Secure File Transfer)
```bash
# SCP — secure copy
scp file.txt user@host:/remote/path/         # upload
scp user@host:/remote/file.txt /local/path/  # download
scp -r dir/ user@host:/remote/path/          # directory
scp -P 2222 file.txt user@host:/path/        # custom port

# SFTP — interactive
sftp user@host
sftp> ls
sftp> get remote_file
sftp> put local_file
sftp> mkdir newdir
sftp> exit
```

---

## 9. Services & Systemd

### systemctl — Service Management
```bash
# Service control
systemctl start nginx          # start service
systemctl stop nginx           # stop service
systemctl restart nginx        # stop then start
systemctl reload nginx         # reload config (no downtime)
systemctl status nginx         # check status
systemctl enable nginx         # start on boot
systemctl disable nginx        # don't start on boot
systemctl is-active nginx      # check if running
systemctl is-enabled nginx     # check if enabled

# System-wide
systemctl list-units           # all active units
systemctl list-units --type=service   # services only
systemctl list-unit-files      # all unit files + enabled status
systemctl daemon-reload        # reload systemd config
systemctl reboot               # reboot
systemctl poweroff             # shutdown
```

### Systemd Unit File
```ini
# /etc/systemd/system/myapp.service

[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
User=appuser
WorkingDirectory=/opt/myapp
ExecStart=/usr/bin/python3 /opt/myapp/app.py
Restart=always
RestartSec=3
Environment=PORT=8080

[Install]
WantedBy=multi-user.target
```

```bash
# After creating unit file:
systemctl daemon-reload
systemctl enable myapp
systemctl start myapp
systemctl status myapp
```

### journalctl — View Logs
```bash
journalctl                     # all logs (oldest first)
journalctl -r                  # reverse (newest first)
journalctl -f                  # follow live logs
journalctl -n 50               # last 50 lines
journalctl -u nginx            # logs for specific service
journalctl -u nginx -f         # follow nginx logs
journalctl -u nginx --since "1 hour ago"
journalctl -u nginx --since "2024-01-01" --until "2024-01-02"
journalctl -p err              # only errors
journalctl -p warning          # warnings and above
journalctl -b                  # logs since last boot
journalctl -b -1               # logs from previous boot
journalctl --disk-usage        # how much space logs use
journalctl --vacuum-time=7d    # delete logs older than 7 days

# Priority levels:
# 0=emerg, 1=alert, 2=crit, 3=err, 4=warning, 5=notice, 6=info, 7=debug
```

---

## 10. Cron Jobs

### Cron Syntax
```
* * * * * command
│ │ │ │ └── Day of week (0-7, 0 and 7 = Sunday)
│ │ │ └──── Month (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)

* = every
*/5 = every 5
1-5 = range (1 through 5)
1,3,5 = list
```

**Examples:**
```bash
# Every minute
* * * * * /script.sh

# Every day at 2:30 AM
30 2 * * * /backup.sh

# Every Monday at 9 AM
0 9 * * 1 /weekly_report.sh

# Every 15 minutes
*/15 * * * * /check.sh

# Every hour
0 * * * * /hourly.sh

# Every day at midnight
0 0 * * * /daily.sh

# First day of month at 6 AM
0 6 1 * * /monthly.sh

# Every weekday (Mon-Fri) at 8 AM
0 8 * * 1-5 /workday.sh
```

### Managing Cron Jobs
```bash
crontab -e                 # edit current user's cron jobs
crontab -l                 # list current user's cron jobs
crontab -r                 # remove all cron jobs (careful!)
crontab -u username -e     # edit another user's cron (root)

# System-wide cron files
cat /etc/crontab           # system crontab (has username field)
ls /etc/cron.d/            # drop-in cron files
ls /etc/cron.daily/        # scripts run daily
ls /etc/cron.weekly/       # scripts run weekly
ls /etc/cron.monthly/      # scripts run monthly
ls /etc/cron.hourly/       # scripts run hourly
```

### Cron Security Note
```bash
# Attackers look for:
# 1. Scripts in cron that you can overwrite (privesc)
# 2. Cron running as root
# 3. Wildcard injection in cron commands

# Check cron for security research:
cat /etc/crontab
cat /var/spool/cron/crontabs/*   # all users' cron
find / -name "*.cron" 2>/dev/null
```

---

## 11. Log Analysis

### Key Log Files
```bash
/var/log/auth.log          # SSH logins, sudo, su, PAM (Debian/Ubuntu)
/var/log/secure            # same but RHEL/CentOS
/var/log/syslog            # general system messages (Debian/Ubuntu)
/var/log/messages          # same but RHEL/CentOS
/var/log/kern.log          # kernel messages
/var/log/dpkg.log          # package installs/removals
/var/log/apt/history.log   # APT package history
/var/log/cron.log          # cron job execution
/var/log/mail.log          # mail server logs
/var/log/nginx/access.log  # web server access
/var/log/nginx/error.log   # web server errors
/var/log/apache2/access.log
/var/log/mysql/error.log   # database errors
/var/log/fail2ban.log      # IPs blocked by fail2ban
```

### Reading Logs
```bash
# Real-time monitoring
tail -f /var/log/auth.log
tail -f /var/log/syslog
journalctl -f

# Search in logs
grep "Failed password" /var/log/auth.log
grep "Accepted password" /var/log/auth.log
grep "sudo" /var/log/auth.log
grep "CRON" /var/log/syslog

# Read compressed logs
zcat /var/log/auth.log.2.gz
zcat /var/log/auth.log.2.gz | grep "Failed"
zgrep "Failed" /var/log/auth.log.2.gz    # grep compressed files

# Count occurrences
grep -c "Failed password" /var/log/auth.log
```

### Security-Focused Log Analysis
```bash
# Find brute force attempts — failed SSH logins
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn | head

# Find successful logins
grep "Accepted password\|Accepted publickey" /var/log/auth.log

# Find users who used sudo
grep "sudo" /var/log/auth.log | grep "COMMAND"

# Find new user creation
grep "useradd\|adduser\|new user" /var/log/auth.log

# Find su attempts
grep "su\[" /var/log/auth.log

# Web server — find 404s (possible scanning)
grep " 404 " /var/log/nginx/access.log | awk '{print $1}' | sort | uniq -c | sort -rn

# Web server — find POST requests (form submissions, potential attacks)
grep "POST" /var/log/nginx/access.log

# Top IPs hitting web server
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head 20

# Cron execution log
grep "CRON" /var/log/syslog | tail -50

# Kernel errors
grep -i "error\|warning\|critical" /var/log/kern.log
```

### Log Formats

**Auth.log format:**
```
Jan  1 12:00:01 hostname sshd[1234]: Failed password for root from 192.168.1.50 port 12345 ssh2
│date+time│  │host │ │service│    │message
```

**Nginx access.log format:**
```
192.168.1.1 - - [01/Jan/2024:12:00:01 +0000] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
│src IP│       │timestamp│              │method + path + protocol│ │status│ │size│
```

### Log Rotation
```bash
cat /etc/logrotate.conf    # main config
ls /etc/logrotate.d/       # per-service configs

# Logrotate config example:
/var/log/nginx/*.log {
    daily                  # rotate daily
    missingok              # ok if file missing
    rotate 14              # keep 14 days
    compress               # compress old logs
    delaycompress          # compress previous log on next run
    notifempty             # don't rotate empty log
    create 0640 www-data adm
    postrotate
        nginx -s reopen
    endscript
}

# Manually run logrotate
logrotate -f /etc/logrotate.conf
```

---

## 12. Bash Scripting

### Script Basics
```bash
#!/bin/bash
# This is a comment
# First line must be shebang: #!/bin/bash

echo "Hello World"

# Make executable and run
chmod +x script.sh
./script.sh
bash script.sh
```

### Variables
```bash
#!/bin/bash

# Assign (no spaces around =)
name="Akio"
age=20
pi=3.14

# Use ($ prefix)
echo "Name: $name"
echo "Age: ${age}"     # braces for clarity

# Command substitution
current_date=$(date)
files=$(ls -la)
ip=$(hostname -I)

echo "Date: $current_date"
echo "IP: $ip"

# Special variables
echo $0        # script name
echo $1        # first argument
echo $2        # second argument
echo $@        # all arguments
echo $#        # number of arguments
echo $$        # current PID
echo $?        # exit code of last command (0 = success)
echo $!        # PID of last background process

# Readonly variable
readonly PI=3.14159

# Unset variable
unset name
```

### User Input
```bash
#!/bin/bash

read -p "Enter your name: " username
echo "Hello, $username!"

read -sp "Enter password: " password    # -s = silent (no echo)
echo ""
echo "Password entered."

read -t 5 -p "Enter within 5 seconds: " timed_input   # timeout
```

### Arithmetic
```bash
#!/bin/bash

a=10
b=3

# Arithmetic expansion
echo $((a + b))      # 13
echo $((a - b))      # 7
echo $((a * b))      # 30
echo $((a / b))      # 3 (integer division)
echo $((a % b))      # 1 (modulo)
echo $((a ** b))     # 1000 (power)

# let command
let result=a+b
echo $result

# expr (older)
result=$(expr $a + $b)

# bc — floating point
echo "scale=2; 10/3" | bc   # 3.33
echo "scale=4; $pi*2" | bc
```

### String Operations
```bash
#!/bin/bash

str="Hello World"

echo ${#str}                # length: 11
echo ${str:0:5}             # substring: Hello (start:length)
echo ${str:6}               # substring from pos 6: World
echo ${str,,}               # lowercase: hello world
echo ${str^^}               # uppercase: HELLO WORLD
echo ${str/World/Akio}      # replace first: Hello Akio
echo ${str//l/L}            # replace all: HeLLo WorLd

# Remove prefix/suffix
file="backup_2024_01_01.tar.gz"
echo ${file%.tar.gz}        # remove suffix: backup_2024_01_01
echo ${file#backup_}        # remove prefix: 2024_01_01.tar.gz

# String comparison
if [[ "$str" == "Hello World" ]]; then
    echo "Strings match"
fi

# Check if empty
if [[ -z "$var" ]]; then
    echo "Variable is empty"
fi

if [[ -n "$str" ]]; then
    echo "Variable is not empty"
fi
```

### Conditionals
```bash
#!/bin/bash

# if / elif / else
if [ condition ]; then
    # commands
elif [ condition ]; then
    # commands
else
    # commands
fi

# File tests
if [ -f /etc/passwd ]; then echo "File exists"; fi
if [ -d /tmp ]; then echo "Directory exists"; fi
if [ -r file.txt ]; then echo "File is readable"; fi
if [ -w file.txt ]; then echo "File is writable"; fi
if [ -x file.sh ]; then echo "File is executable"; fi
if [ -s file.txt ]; then echo "File is not empty"; fi
if [ ! -f file.txt ]; then echo "File does NOT exist"; fi

# Numeric comparisons ([ ] or (( )))
if [ $a -eq $b ]; then echo "Equal"; fi           # equal
if [ $a -ne $b ]; then echo "Not equal"; fi        # not equal
if [ $a -gt $b ]; then echo "Greater"; fi          # greater than
if [ $a -lt $b ]; then echo "Less"; fi             # less than
if [ $a -ge $b ]; then echo "GTE"; fi              # greater or equal
if [ $a -le $b ]; then echo "LTE"; fi              # less or equal

# Cleaner numeric with (( ))
if (( a > b )); then echo "a is greater"; fi
if (( a == 10 )); then echo "a is 10"; fi

# String comparisons
if [ "$str1" == "$str2" ]; then echo "Equal"; fi
if [ "$str1" != "$str2" ]; then echo "Not equal"; fi
if [ "$str1" \< "$str2" ]; then echo "str1 < str2"; fi

# Logical operators
if [ $a -gt 5 ] && [ $b -lt 10 ]; then    # AND
if [ $a -gt 5 ] || [ $b -lt 10 ]; then    # OR
if [[ $a -gt 5 && $b -lt 10 ]]; then      # AND (double bracket)
if [[ $a -gt 5 || $b -lt 10 ]]; then      # OR (double bracket)
```

### Loops
```bash
#!/bin/bash

# for loop — list
for item in apple banana cherry; do
    echo "Fruit: $item"
done

# for loop — range
for i in {1..10}; do
    echo "Number: $i"
done

# for loop — range with step
for i in {0..20..5}; do
    echo $i    # 0 5 10 15 20
done

# C-style for loop
for (( i=0; i<10; i++ )); do
    echo $i
done

# for loop — files
for file in /var/log/*.log; do
    echo "Processing: $file"
    wc -l "$file"
done

# while loop
counter=1
while [ $counter -le 5 ]; do
    echo "Count: $counter"
    ((counter++))
done

# while read — read file line by line
while IFS= read -r line; do
    echo "Line: $line"
done < /etc/passwd

# until loop (opposite of while)
until [ $counter -gt 5 ]; do
    echo $counter
    ((counter++))
done

# Loop control
for i in {1..10}; do
    if [ $i -eq 5 ]; then
        continue    # skip 5
    fi
    if [ $i -eq 8 ]; then
        break       # stop at 8
    fi
    echo $i
done
```

### Functions
```bash
#!/bin/bash

# Define function
greet() {
    local name=$1           # local variable (scoped to function)
    echo "Hello, $name!"
}

# Call function
greet "Akio"
greet "World"

# Function with return value
add() {
    local a=$1
    local b=$2
    echo $((a + b))        # use echo to "return" values
}

result=$(add 5 3)
echo "Result: $result"

# Function with exit code
check_root() {
    if [ "$(id -u)" -eq 0 ]; then
        return 0            # success
    else
        return 1            # failure
    fi
}

if check_root; then
    echo "Running as root"
else
    echo "Not root"
fi
```

### Arrays
```bash
#!/bin/bash

# Create array
fruits=("apple" "banana" "cherry")
ports=(22 80 443 8080)

# Access elements
echo ${fruits[0]}          # apple
echo ${fruits[1]}          # banana
echo ${fruits[-1]}         # last element: cherry

# All elements
echo ${fruits[@]}
echo ${fruits[*]}

# Length
echo ${#fruits[@]}         # 3

# Add element
fruits+=("grape")

# Loop array
for fruit in "${fruits[@]}"; do
    echo $fruit
done

# Loop with index
for i in "${!fruits[@]}"; do
    echo "$i: ${fruits[$i]}"
done

# Associative array (dictionary)
declare -A person
person["name"]="Akio"
person["age"]=20
person["city"]="Kasganj"

echo ${person["name"]}
for key in "${!person[@]}"; do
    echo "$key: ${person[$key]}"
done
```

### Error Handling
```bash
#!/bin/bash

# Exit on error
set -e                     # exit script if any command fails
set -u                     # error on undefined variables
set -o pipefail            # exit if any pipe command fails
set -euo pipefail          # all three (recommended)

# Check exit code
if command; then
    echo "Success"
else
    echo "Failed"
fi

# Or:
command || { echo "Command failed"; exit 1; }
command && echo "Success"

# Trap — cleanup on exit
cleanup() {
    echo "Cleaning up..."
    rm -f /tmp/tempfile
}
trap cleanup EXIT          # run cleanup() on script exit
trap cleanup INT           # also on Ctrl+C

# Error with line number
error() {
    echo "Error on line $1"
    exit 1
}
trap 'error $LINENO' ERR
```

### Practical Security Scripts

**Port Scanner:**
```bash
#!/bin/bash
# Simple port scanner

target=$1
start_port=${2:-1}
end_port=${3:-1000}

echo "Scanning $target ports $start_port-$end_port"

for port in $(seq $start_port $end_port); do
    (echo >/dev/tcp/$target/$port) 2>/dev/null && \
        echo "Port $port: OPEN"
done
```

**Failed Login Monitor:**
```bash
#!/bin/bash
# Monitor failed SSH logins

LOGFILE="/var/log/auth.log"
THRESHOLD=5

echo "=== Failed SSH Login Attempts ==="
grep "Failed password" $LOGFILE | \
    awk '{print $11}' | \
    sort | \
    uniq -c | \
    sort -rn | \
    while read count ip; do
        if [ $count -ge $THRESHOLD ]; then
            echo "ALERT: $ip failed $count times"
        fi
    done
```

**Backup Script:**
```bash
#!/bin/bash
# Simple backup script

SOURCE="/home/akio"
DEST="/backup"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_$DATE.tar.gz"

echo "Starting backup..."

tar -czvf "$DEST/$BACKUP_FILE" "$SOURCE" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "Backup successful: $BACKUP_FILE"
    # Keep only last 7 backups
    ls -t $DEST/backup_*.tar.gz | tail -n +8 | xargs rm -f
else
    echo "Backup FAILED!"
    exit 1
fi
```

**System Info Script:**
```bash
#!/bin/bash
# System information

echo "========== SYSTEM INFO =========="
echo "Hostname:   $(hostname)"
echo "OS:         $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
echo "Kernel:     $(uname -r)"
echo "Uptime:     $(uptime -p)"
echo ""
echo "========== RESOURCES =========="
echo "CPU Usage:  $(top -bn1 | grep Cpu | awk '{print $2}')%"
echo "Memory:     $(free -h | grep Mem | awk '{print $3"/"$2}')"
echo "Disk:       $(df -h / | tail -1 | awk '{print $3"/"$2" ("$5" used)"}')"
echo ""
echo "========== NETWORK =========="
echo "IP:         $(hostname -I)"
echo "Connections: $(ss -ant | grep ESTABLISHED | wc -l) established"
echo ""
echo "========== LOGGED IN =========="
who
```

---

## 13. Python for Security

### Python Basics
```python
# Data types
name = "Akio"           # string
age = 20                # int
pi = 3.14               # float
active = True           # bool
data = None             # NoneType

# Collections
list1 = [1, 2, 3, "four"]          # mutable, ordered
tuple1 = (1, 2, 3)                  # immutable
dict1 = {"key": "value", "a": 1}   # key-value pairs
set1 = {1, 2, 3, 4}                # unique values, unordered

# String formatting
print(f"Hello {name}, you are {age}")   # f-string (preferred)
print("Hello {}, you are {}".format(name, age))

# Input
user_input = input("Enter value: ")
```

### Control Flow
```python
# if/elif/else
if age >= 18:
    print("Adult")
elif age >= 13:
    print("Teen")
else:
    print("Child")

# Loops
for i in range(10):
    print(i)

for item in ["a", "b", "c"]:
    print(item)

# Enumerate
for index, value in enumerate(["a", "b", "c"]):
    print(f"{index}: {value}")

# While
count = 0
while count < 5:
    print(count)
    count += 1

# List comprehension
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
```

### Functions
```python
def greet(name, greeting="Hello"):    # default parameter
    return f"{greeting}, {name}!"

print(greet("Akio"))                 # Hello, Akio!
print(greet("Akio", "Hi"))           # Hi, Akio!

# *args and **kwargs
def log(*args, **kwargs):
    print(args)
    print(kwargs)

log("error", "critical", level="high", source="auth")
```

### File Handling
```python
# Read file
with open("file.txt", "r") as f:
    content = f.read()          # entire file as string
    
with open("file.txt", "r") as f:
    lines = f.readlines()       # list of lines

with open("file.txt", "r") as f:
    for line in f:              # iterate line by line
        print(line.strip())

# Write file
with open("output.txt", "w") as f:
    f.write("Hello World\n")

# Append
with open("log.txt", "a") as f:
    f.write("New log entry\n")

# with statement auto-closes file (use always)
```

### os and subprocess Modules
```python
import os
import subprocess

# OS operations
print(os.getcwd())              # current directory
os.chdir("/tmp")                # change directory
os.listdir(".")                 # list directory
os.makedirs("dir/sub", exist_ok=True)   # create dirs
os.remove("file.txt")          # delete file
os.rename("old.txt", "new.txt")
os.path.exists("/etc/passwd")  # check if exists
os.path.isfile("/etc/passwd")  # is a file?
os.path.isdir("/etc")          # is a directory?
os.path.basename("/etc/passwd")  # passwd
os.path.dirname("/etc/passwd")   # /etc
os.path.join("/etc", "passwd")   # /etc/passwd

# Environment variables
os.environ.get("HOME")          # get env var
os.environ["NEW_VAR"] = "value" # set env var

# Run system commands
# Method 1: subprocess.run (recommended)
result = subprocess.run(["ls", "-la"], capture_output=True, text=True)
print(result.stdout)
print(result.returncode)   # 0 = success

# Method 2: subprocess.run with shell=True (careful — injection risk)
result = subprocess.run("ls -la /tmp", shell=True, capture_output=True, text=True)

# Method 3: os.system (simple, no output capture)
os.system("echo hello")

# Get output directly
output = subprocess.check_output(["whoami"]).decode().strip()
print(output)
```

### socket Module — Networking
```python
import socket

# Basic TCP client
def tcp_connect(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((host, port))
        banner = s.recv(1024).decode().strip()
        s.close()
        return banner
    except:
        return None

# Port scanner
def scan_ports(host, ports):
    open_ports = []
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((host, port))   # 0 = open
            if result == 0:
                open_ports.append(port)
            s.close()
        except:
            pass
    return open_ports

if __name__ == "__main__":
    host = "192.168.1.1"
    ports = range(1, 1025)
    open_ports = scan_ports(host, ports)
    print(f"Open ports on {host}: {open_ports}")

# DNS resolution
ip = socket.gethostbyname("google.com")
hostname = socket.gethostbyaddr("8.8.8.8")
```

### requests Module — HTTP
```python
import requests

# GET request
response = requests.get("https://httpbin.org/get")
print(response.status_code)    # 200
print(response.headers)        # dict of headers
print(response.text)           # response body as text
print(response.json())         # parse JSON response

# GET with params
params = {"page": 1, "limit": 10}
r = requests.get("https://api.example.com/users", params=params)

# POST request
data = {"username": "admin", "password": "password123"}
r = requests.post("https://target.com/login", data=data)

# POST JSON
r = requests.post("https://api.example.com/data", json={"key": "value"})

# Custom headers
headers = {
    "User-Agent": "Mozilla/5.0",
    "Authorization": "Bearer TOKEN",
    "Cookie": "session=abc123"
}
r = requests.get("https://target.com", headers=headers)

# Session (maintains cookies)
session = requests.Session()
session.post("https://target.com/login", data={"user": "admin", "pass": "admin"})
r = session.get("https://target.com/dashboard")  # authenticated

# Error handling
try:
    r = requests.get("https://target.com", timeout=5)
    r.raise_for_status()    # raises exception for 4xx/5xx
except requests.exceptions.ConnectionError:
    print("Connection failed")
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")

# Disable SSL verification (for testing)
r = requests.get("https://target.com", verify=False)
```

### Practical Python Security Scripts

**Web Directory Brute Forcer:**
```python
import requests
from concurrent.futures import ThreadPoolExecutor

def check_path(url, path):
    full_url = f"{url}/{path}"
    try:
        r = requests.get(full_url, timeout=3, allow_redirects=False)
        if r.status_code not in [404, 403]:
            print(f"[{r.status_code}] {full_url}")
    except:
        pass

def brute_force(url, wordlist):
    with open(wordlist, "r") as f:
        paths = [line.strip() for line in f]
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        for path in paths:
            executor.submit(check_path, url, path)

if __name__ == "__main__":
    brute_force("http://target.com", "common.txt")
```

**Log Parser:**
```python
import re
from collections import Counter

def parse_auth_log(logfile):
    failed_ips = []
    success_ips = []
    
    with open(logfile, "r") as f:
        for line in f:
            # Find failed logins
            failed = re.search(r"Failed password.*from (\d+\.\d+\.\d+\.\d+)", line)
            if failed:
                failed_ips.append(failed.group(1))
            
            # Find successful logins
            success = re.search(r"Accepted.*from (\d+\.\d+\.\d+\.\d+)", line)
            if success:
                success_ips.append(success.group(1))
    
    print("Top Failed Login IPs:")
    for ip, count in Counter(failed_ips).most_common(10):
        print(f"  {count:4d}  {ip}")
    
    print("\nSuccessful Logins From:")
    for ip, count in Counter(success_ips).most_common(10):
        print(f"  {count:4d}  {ip}")

parse_auth_log("/var/log/auth.log")
```

**Subnet Scanner:**
```python
import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor

def ping_host(ip):
    """Check if host is up by trying to connect to port 80 or 22"""
    for port in [22, 80, 443]:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            if s.connect_ex((str(ip), port)) == 0:
                s.close()
                return str(ip)
        except:
            pass
    return None

def scan_subnet(cidr):
    network = ipaddress.ip_network(cidr, strict=False)
    live_hosts = []
    
    print(f"Scanning {cidr}...")
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(ping_host, network.hosts())
        live_hosts = [r for r in results if r]
    
    print(f"\nLive hosts ({len(live_hosts)}):")
    for host in sorted(live_hosts, key=lambda x: ipaddress.ip_address(x)):
        print(f"  {host}")

scan_subnet("192.168.1.0/24")
```

---

## 14. Quick Reference Cheatsheet

### Essential Commands
```bash
# Navigation
pwd | ls -la | cd /path | cd .. | cd ~

# Files
touch | mkdir -p | cp -r | mv | rm -rf | ln -s

# Read
cat | less | head -n | tail -f | wc -l

# Search
find / -name "*.txt" | find / -perm -4000
grep -r "pattern" /path
grep -i -n -v -A3 -B3

# Text processing
awk '{print $1}' | sed 's/old/new/g'
cut -d':' -f1 | sort | uniq -c | sort -rn

# Permissions
chmod 755 | chmod +x | chown user:group
find / -perm -4000   # SUID files

# Users
id | whoami | who | last | sudo -l
useradd -m -s /bin/bash | passwd | usermod -aG

# Processes
ps aux | grep | top | htop
kill PID | kill -9 PID | killall name
```

### Bash Script Template
```bash
#!/bin/bash
set -euo pipefail

# Variables
TARGET=${1:-"default"}

# Function
usage() {
    echo "Usage: $0 <target>"
    exit 1
}

# Input validation
if [ $# -eq 0 ]; then
    usage
fi

# Main logic
echo "Processing: $TARGET"
```

### Python Requests Template
```python
import requests

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

def get(url, **kwargs):
    try:
        r = session.get(url, timeout=10, **kwargs)
        r.raise_for_status()
        return r
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
```

### Log Analysis One-Liners
```bash
# Top failed SSH IPs
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn | head

# Successful logins
grep "Accepted" /var/log/auth.log | awk '{print $9,$11}'

# Top web request IPs
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head

# 404 errors
grep " 404 " /var/log/nginx/access.log | awk '{print $7}' | sort | uniq -c | sort -rn

# Who ran sudo and what
grep "COMMAND" /var/log/auth.log | awk -F'COMMAND=' '{print $2}'
```

---

## Phase 2 Complete Checklist

- [ ] Know the Linux directory structure (`/etc`, `/var`, `/proc`, `/home`)
- [ ] Comfortable with file navigation and manipulation commands
- [ ] Understand file permissions — can read `rwxr-xr-x`, use chmod/chown
- [ ] Know SUID/SGID/Sticky bit — what they do and security implications
- [ ] Can manage users and groups (`useradd`, `usermod`, `sudo -l`)
- [ ] Comfortable with process management (`ps aux`, `kill`, `top`)
- [ ] Can install packages with apt/dnf
- [ ] Know key networking commands (`ip a`, `ss`, `netstat`, `tcpdump`)
- [ ] Can set up SSH key auth and harden sshd_config
- [ ] Understand systemd — can start/stop/enable/check services
- [ ] Can use journalctl to filter and search logs
- [ ] Can write cron jobs
- [ ] Can read and analyze `/var/log/auth.log` for attacks
- [ ] Can write bash scripts with variables, loops, functions, error handling
- [ ] Can write Python scripts using os, subprocess, socket, requests
- [ ] Can build a port scanner in both bash and Python

---

*Next → Phase 3: Cybersecurity Fundamentals + Zero Trust*

#cybersecurity #phase2 #linux #bash #scripting #python #networking #ssh #logs #permissions
