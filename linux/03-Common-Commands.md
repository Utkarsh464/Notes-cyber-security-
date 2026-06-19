# Linux Common Commands — Security Reference

> Personal notes by Utkarsh Solanki | Cybersecurity & AI Student  
> [LinkedIn](https://linkedin.com/in/utkarsh-solanki-337806252) · [GitHub](https://github.com/Utkarsh464)

---

## Table of Contents

- [Navigation](#navigation)
- [File Operations](#file-operations)
- [Viewing & Searching Files](#viewing--searching-files)
- [Process Management](#process-management)
- [Networking Commands](#networking-commands)
- [System Info](#system-info)
- [Archives & Compression](#archives--compression)
- [Redirection & Pipes](#redirection--pipes)
- [Security-Useful One-Liners](#security-useful-one-liners)

---

## Navigation

```bash
pwd                        # print working directory
ls                         # list files
ls -la                     # list all (including hidden) with details
ls -lh                     # human-readable sizes
ls -lt                     # sort by modification time
cd /path/to/dir            # change directory
cd ~                       # go home
cd -                       # go to previous directory
tree                       # visual directory tree
tree -L 2                  # limit depth to 2 levels
```

---

## File Operations

```bash
# Create
touch file.txt             # create empty file / update timestamp
mkdir dir                  # create directory
mkdir -p a/b/c             # create nested directories

# Copy
cp file.txt copy.txt       # copy file
cp -r dir/ newdir/         # copy directory recursively

# Move / Rename
mv file.txt newname.txt    # rename
mv file.txt /tmp/          # move

# Delete
rm file.txt                # delete file
rm -rf dir/                # delete directory (careful)
rmdir dir                  # delete empty directory

# Links
ln -s /path/to/file link   # create symlink
ln file hardlink           # create hard link
readlink -f link           # resolve symlink path
```

---

## Viewing & Searching Files

```bash
# View
cat file.txt               # print whole file
less file.txt              # paginated view (q to quit)
head -n 20 file.txt        # first 20 lines
tail -n 20 file.txt        # last 20 lines
tail -f /var/log/syslog    # live log watching

# Search
grep "pattern" file.txt    # search in file
grep -r "pattern" /etc/    # recursive search
grep -i "pattern" file     # case insensitive
grep -n "pattern" file     # show line numbers
grep -v "pattern" file     # invert match (exclude)
grep -l "pattern" /etc/*   # list files containing pattern

# Find files
find / -name "passwd"      # find by name
find / -type f -name "*.sh"       # all shell scripts
find / -user root -type f         # files owned by root
find / -mtime -1                  # modified in last 24h
find / -size +10M                 # files larger than 10MB
find . -name "*.conf" -exec cat {} \;   # find and read configs

# Text processing
cut -d: -f1 /etc/passwd    # cut first field (delimiter :)
awk -F: '{print $1}' /etc/passwd   # print usernames
sort file.txt              # sort lines
sort -u file.txt           # sort + unique
uniq file.txt              # remove consecutive duplicates
wc -l file.txt             # count lines
wc -w file.txt             # count words
diff file1 file2           # compare files
```

---

## Process Management

```bash
# View
ps aux                     # all running processes
ps aux | grep nginx        # filter processes
top                        # live process monitor
htop                       # better top (if installed)
pgrep nginx                # get PID of process by name

# Control
kill PID                   # send SIGTERM (graceful)
kill -9 PID                # send SIGKILL (force)
killall nginx              # kill by name
pkill -f pattern           # kill by pattern

# Background / foreground
command &                  # run in background
jobs                       # list background jobs
fg %1                      # bring job 1 to foreground
bg %1                      # send job 1 to background
nohup command &            # run immune to hangup
```

---

## Networking Commands

```bash
# Interface info
ip a                       # show all interfaces & IPs
ip r                       # show routing table
ifconfig                   # older alternative

# Connectivity
ping 8.8.8.8               # test connectivity
ping -c 4 8.8.8.8          # send only 4 packets
traceroute 8.8.8.8         # trace route to host
curl ifconfig.me           # get public IP

# DNS
dig google.com             # DNS lookup
nslookup google.com        # alternative
host google.com            # simple lookup

# Ports & connections
ss -tulpn                  # listening ports (modern)
netstat -tulpn             # listening ports (older)
ss -an | grep :80          # connections on port 80
lsof -i :80                # what's using port 80
lsof -i -P -n              # all open network connections

# Transfer
wget https://example.com/file    # download file
curl -O https://example.com/file # download file
curl -I https://example.com      # headers only
scp file.txt user@host:/path/    # secure copy
rsync -av src/ user@host:/dst/   # sync files

# Packet capture
tcpdump -i eth0            # capture on interface
tcpdump -i eth0 port 80    # filter by port
tcpdump -i eth0 -w out.pcap  # save to file
```

---

## System Info

```bash
uname -a                   # kernel + OS info
hostname                   # system hostname
uptime                     # how long running
whoami                     # current user
id                         # uid, gid, groups
env                        # environment variables
echo $PATH                 # current PATH

# Hardware
lscpu                      # CPU info
free -h                    # RAM usage
df -h                      # disk usage
lsblk                      # block devices
lsusb                      # USB devices

# Logs
journalctl -xe             # systemd logs
cat /var/log/auth.log      # auth/login logs
cat /var/log/syslog        # general system log
dmesg | tail               # kernel messages
```

---

## Archives & Compression

```bash
# tar
tar -cvf archive.tar dir/         # create
tar -xvf archive.tar              # extract
tar -czvf archive.tar.gz dir/     # create gzip compressed
tar -xzvf archive.tar.gz          # extract gzip
tar -cjvf archive.tar.bz2 dir/    # create bzip2
tar -tvf archive.tar              # list contents without extracting

# zip
zip -r archive.zip dir/           # compress directory
unzip archive.zip                 # extract
unzip -l archive.zip              # list contents

# gzip / gunzip
gzip file.txt                     # compress (replaces original)
gunzip file.txt.gz                # decompress
```

---

## Redirection & Pipes

```bash
# Output redirection
command > file.txt         # write stdout to file (overwrite)
command >> file.txt        # append stdout to file
command 2> errors.txt      # write stderr to file
command &> all.txt         # write both stdout+stderr

# Input
command < file.txt         # read stdin from file

# Pipes
command1 | command2        # pipe stdout of 1 to stdin of 2
ps aux | grep nginx        # filter process list
cat /etc/passwd | cut -d: -f1 | sort   # chain multiple

# Discard output
command > /dev/null        # discard stdout
command 2>/dev/null        # discard stderr
command &>/dev/null        # discard everything

# Tee (write to file AND stdout)
command | tee output.txt
```

---

## Security-Useful One-Liners

```bash
# Check open ports locally
ss -tulpn | grep LISTEN

# Find world-writable files
find / -perm -o+w -type f 2>/dev/null

# Find SUID binaries
find / -perm -4000 -type f 2>/dev/null

# Check cron jobs
crontab -l
cat /etc/crontab
ls /etc/cron.*

# Check running services
systemctl list-units --type=service --state=running

# Search for passwords in config files
grep -r "password" /etc/ 2>/dev/null
grep -r "passwd" /var/www/ 2>/dev/null

# Check bash history
cat ~/.bash_history
cat /root/.bash_history 2>/dev/null

# Find recently modified files
find / -mmin -60 -type f 2>/dev/null

# Check installed packages
dpkg -l                    # Debian/Ubuntu
rpm -qa                    # RHEL/CentOS

# Active network connections
ss -antp

# Who is currently logged in
w
who
last | head -20
```

---

*Last updated: June 2026*
