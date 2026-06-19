# File Systems — How Your OS Stores Stuff

> Personal notes by Utkarsh Solanki | Cybersecurity & AI Student  
> GitHub: [github.com/Utkarsh464](https://github.com/Utkarsh464) | LinkedIn: [linkedin.com/in/utkarsh-solanki-337806252](https://linkedin.com/in/utkarsh-solanki-337806252)

---

## The Big Picture

A file system is basically **a giant spreadsheet that tracks where every file's bytes live on disk**. Without it, your hard drive is just a big block of magnetic goo with no structure.

Think of a library:
- The **file system** is the catalog system
- **Files** are books
- **Directories** are shelves/sections
- **Metadata** (permissions, timestamps) is the card catalog info

---

## Common File Systems

### NTFS (Windows — Default)
- **Journaled** — keeps a log of changes before making them (helps recover from crashes)
- Supports: permissions (ACLs), encryption (EFS), compression, disk quotas
- Max file size: 16 EB (that's enormous)
- **Security:** File permissions per-user, audit logging, alternate data streams

**Alternate Data Streams (ADS):** NTFS can hide data inside other files using `:` syntax.
```powershell
# Hide a payload in a legitimate file
echo "malicious code" > readme.txt:hidden.txt

# Read it back
more < readme.txt:hidden.txt

# This is how attackers hide data — it won't show in normal file listing
```
Only shows up if you use `dir /r` or tools like `streams.exe`.

### FAT32 (USB Drives, Old Windows)
- **No journaling** — corruption is very possible
- Max file size: 4 GB (can't store a movie)
- No permissions, no encryption
- Universal compatibility — every OS can read it

### exFAT (Modern USB Drives)
- FAT32 without the 4GB limit
- No journaling, simple
- Best for external drives you share between Windows/macOS/Linux

### ext4 (Linux — Default)
- **Journaled** — very reliable
- Supports: permissions (rwx), extended attributes, large files
- Uses **inodes** (explained below)
- No built-in encryption (use LUKS for that)

### APFS (macOS — Default)
- **Copy-on-write** — making a copy doesn't duplicate data until you change it
- Built-in encryption, snapshots, space sharing
- Optimized for SSDs

---

## Inodes — The Linux File System Heart

In ext4 (and other Unix file systems), every file has an **inode** (index node). The inode stores **everything about the file except its name and data**.

```
Inode contains:
├── File type (regular, directory, symlink)
├── Permissions (rwxr-xr-x)
├── Owner (UID) and Group (GID)
├── File size
├── Timestamps (access, modify, change)
├── Link count (how many names point to this inode)
└── Pointers to data blocks on disk
```

The **filename** is stored in the **directory entry**, which maps a name to an inode number.

```bash
# See inode numbers
ls -li file.txt
# Output: 123456 -rw-r--r-- 1 user user 1024 Jun 10 file.txt
#         ^^^^^^
#         inode number

# Get detailed inode info
stat file.txt
```

**Hard links:** Multiple filenames pointing to the same inode (same data).
```bash
ln file.txt hardlink.txt    # both names, same data
# Delete one, data survives until all links are deleted
```

**Soft links (symlinks):** A file that points to another filename.
```bash
ln -s /path/to/real/file symlink.txt
# If original is deleted, symlink breaks (dead link)
```

---

## MBR vs GPT — Partition Tables

Before a disk can hold file systems, it needs a **partition table** — a map of how the disk is divided.

### MBR (Master Boot Record)
- Old standard (1983)
- Supports up to **2 TB** disks
- Max **4 primary partitions** (or 3 primary + extended)
- Boot code stored in first 512 bytes

### GPT (GUID Partition Table)
- New standard, part of UEFI
- Supports disks **larger than 2 TB**
- Unlimited partitions (theoretically)
- Stores backup partition table at end of disk (recovery-friendly)
- Required for UEFI boot

```bash
# Check partition table type on Linux
sudo fdisk -l /dev/sda
# Look for "Disklabel type: gpt" or "Disklabel type: dos" (MBR)
```

### Which One?

| You're using... | Use |
|----------------|-----|
| Old BIOS + Windows/Linux | MBR |
| UEFI + Windows/Linux | GPT |
| Disk > 2 TB | GPT |
| Dual boot with UEFI | GPT |

---

## Mounting — Making Drives Accessible

On Linux, everything is a file. When you plug in a USB or add a disk, you need to **mount** it — attach it to a directory in the file tree.

```bash
# Find the device
lsblk
# sda      8:0    0  disk
# ├─sda1   8:1    0  /boot
# └─sda2   8:2    0  /

# Mount a USB drive
sudo mount /dev/sdb1 /mnt/usb

# Unmount
sudo umount /mnt/usb

# See all mounted filesystems
df -h
mount

# Mount with specific permissions
sudo mount -o noexec,nosuid /dev/sdb1 /mnt/usb
```

**The `noexec` flag** — prevents ANY file on that drive from being executed. Good for /tmp, /home, and external drives. Attackers can't run their downloaded binaries.

---

## Windows Drive Letters

Windows uses drive letters instead of a unified tree:
- `C:\` — system drive (Windows + programs)
- `D:\` — usually optical drive or recovery partition
- `E:\` — USB drive
- `\\SERVER\share` — network shares (UNC paths)

```powershell
# List drives
Get-PSDrive

# Mount a network share
net use Z: \\192.168.1.100\shared

# Check disk info
fsutil fsinfo drives
```

---

## Forensics Angle — What Attackers and Investigators Look For

**Deleted files** are not really gone — the OS just marks the space as available. Until it's overwritten, the data is recoverable.

```bash
# Recover deleted files on Linux (ext4)
extundelete /dev/sda2 --restore-all

# Create a disk image for forensics
dd if=/dev/sda of=disk_image.img bs=4M

# Analyze with tools like Autopsy, FTK Imager
```

**What investigators check:**
- **$MFT** (Master File Table on NTFS) — records every file that ever existed on the drive
- **Timestamps** — created, modified, accessed, and **$MFT modified** timestamps
- **Unallocated space** — deleted files that haven't been overwritten
- **Slack space** — leftover bytes between end of file and end of sector

**Timestomping** — attackers deliberately change file timestamps to hide their tracks.
```bash
# Linux: change timestamp of a file to match another
touch -r legitimate.log backdoor.exe

# Windows: use PowerShell
(Get-Item backdoor.exe).CreationTime = (Get-Item legit.dll).CreationTime
```

---

*Last updated: June 2026*
