# OS Basics — What Makes a Computer Tick

> Personal notes by Utkarsh Solanki | Cybersecurity & AI Student  
> GitHub: [github.com/Utkarsh464](https://github.com/Utkarsh464) | LinkedIn: [linkedin.com/in/utkarsh-solanki-337806252](https://linkedin.com/in/utkarsh-solanki-337806252)

---

## What Even Is an Operating System?

Imagine a restaurant. You've got the kitchen (hardware — CPU, RAM, disk), the chefs (processes), and the customers (users). The OS is the **restaurant manager** — it decides who cooks when, what ingredients get used, who gets a table, and makes sure nobody sets the place on fire.

Without the OS, your CPU is just a hot rock that does nothing. The OS is the bridge between you (the human) and the machine. It handles:
- Running programs
- Managing memory
- Talking to hardware (keyboard, mouse, network card)
- Keeping things secure so one program can't mess with another

---

## The Big Three

You'll deal with three OS families in the wild:

### Windows
- Made by Microsoft, used everywhere in corporate environments
- GUI-first, but PowerShell is getting powerful
- **Security model:** UAC (User Account Control), Windows Defender, BitLocker
- **What attackers love:** SMB, RDP, Active Directory, legacy protocols
- **File system:** NTFS (default), FAT32 (USB drives)

### Linux
- Open source, tons of distributions (Ubuntu, Debian, CentOS, Arch)
- CLI-first (though desktops exist)
- **Security model:** sudo, file permissions, SELinux/AppArmor
- **What attackers love:** Misconfigured sudo, SUID binaries, weak SSH configs
- **File system:** ext4 (default), also btrfs, ZFS, xfs

### macOS
- Unix-based (like Linux), but with Apple's polish
- Found in dev shops, designers, increasingly in enterprise
- **Security model:** SIP (System Integrity Protection), Gatekeeper, FileVault
- **What attackers love:** Less malware than Windows, but growing target

> **Security takeaway:** In cybersecurity, you'll live in Linux (for attacking) and Windows (for defending / corporate environments). macOS shows up in mobile/enterprise contexts.

---

## Kernel vs User Space

The OS is split into two worlds:

### Kernel Space (The VIP Lounge)
- The kernel is the **core** of the OS — it has full access to everything
- Manages memory, CPU, devices
- If the kernel crashes, **the whole system crashes** (Blue Screen of Death)
- Kernel code runs in **ring 0** (highest privilege)

### User Space (The Peasants)
- Every app you run lives here — Chrome, Spotify, your terminal
- Apps can't directly touch hardware or each other's memory
- If a user-space app crashes, only that app dies (not the whole system)
- Runs in **ring 3** (least privilege)

```
┌──────────────────────────────┐
│       User Space (ring 3)    │
│  ┌────┐ ┌────┐ ┌──────────┐ │
│  │App │ │App │ │Terminal  │ │
│  └────┘ └────┘ └──────────┘ │
├──────────────────────────────┤
│       Kernel (ring 0)        │
│  ┌──────┐ ┌────┐ ┌───────┐ │
│  │Sched │ │Mem │ │Driver │ │
│  └──────┘ └────┘ └───────┘ │
├──────────────────────────────┤
│         Hardware             │
│   CPU  │  RAM  │  Disk      │
└──────────────────────────────┘
```

**System calls (syscalls)** are how user-space apps talk to the kernel. When you do `read()` or `write()` or `open()` — those are syscalls crossing the kernel-user boundary.

### Why This Matters for Security

The whole point of separating kernel and user space is **isolation**. If a web browser (user space) gets exploited, the attacker shouldn't automatically get kernel-level access. That's why kernel exploits are so valuable — they break through this wall.

**Privilege escalation** is literally: "I'm in user space, now I want kernel space."

---

## The Boot Process (What Happens When You Press Power)

### Linux Boot

```
Power On
   ↓
BIOS/UEFI (firmware checks hardware, finds boot device)
   ↓
Bootloader (GRUB) — lets you pick which OS/kernel to load
   ↓
Kernel loads into memory, initializes drivers
   ↓
init/systemd starts (PID 1 — the parent of all processes)
   ↓
Systemd starts services (networking, SSH, display manager)
   ↓
Login screen appears
```

### Windows Boot

```
Power On
   ↓
UEFI/BIOS
   ↓
Windows Boot Manager (bootmgr)
   ↓
winload.exe loads the kernel (ntoskrnl.exe)
   ↓
Session Manager (smss.exe) starts
   ↓
Windows subsystem starts, services load
   ↓
Login screen (winlogon.exe)
```

**Security relevance:**
- **UEFI Secure Boot** — prevents bootkits by only allowing signed bootloaders
- **Bootkits** — malware that loads before the OS, nearly invisible to antivirus
- **GRUB password** — prevents someone from booting into single-user mode (root access without password)

---

## Virtualization — Running OSes Inside OSes

Hypervisors let you run multiple OSes on one physical machine.

### Type 1 (Bare Metal)
- Runs directly on hardware
- Examples: VMware ESXi, Microsoft Hyper-V, KVM
- Used in data centers, cloud servers
- **More efficient, more secure** (smaller attack surface)

### Type 2 (Hosted)
- Runs on top of an existing OS
- Examples: VirtualBox, VMware Workstation, Parallels
- Used for labs, testing, CTFs

```
Type 1:  App  │  App  │  App
         ─────┼───────┼─────
         VM1  │ VM2   │ VM3
         ─────┼───────┼─────
         Hypervisor
         ───────────────
         Hardware

Type 2:  App │ VM1 │ VM2 │ App
         ────┼─────┼─────┼────
         Host OS
         ─────────────
         Hardware
```

**For your lab:** You'll probably use VirtualBox or VMware to run Kali Linux, Windows VMs, and vulnerable machines from TryHackMe/HTB.

---

## A Word on CPU Architecture

| Term | Meaning |
|------|---------|
| x86 | 32-bit Intel/AMD processors (old) |
| x64 / x86-64 | 64-bit (modern desktops & servers) |
| ARM | Mobile-first, power-efficient (M1/M2 Macs, Raspberry Pi, phones) |
| Endianness | Little-endian (x86) vs big-endian — matters in exploit dev |

**Why this matters in hacking:** Buffer overflow exploits need to know the architecture — x64 has different register names, calling conventions, and protection mechanisms (like NX bits, ASLR) than x86.

---

*Last updated: June 2026*
