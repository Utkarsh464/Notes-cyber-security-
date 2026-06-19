# networking-and-os

Networking & OS cheatsheets written from a security perspective — not just how things work, but how to abuse and detect misuse of them.

> **Utkarsh Solanki** — Cybersecurity & AI Student  
> [LinkedIn](https://linkedin.com/in/utkarsh-solanki-337806252) · [GitHub](https://github.com/Utkarsh464)

---

## Contents

| File | Topics |
|------|--------|
| [01-TCPIP-DNS-HTTP-Subnetting.md](./01-TCPIP-DNS-HTTP-Subnetting.md) | OSI model, TCP/UDP, 3-way handshake, TCP flags, DNS records, HTTP methods & status codes, subnetting, CIDR, common ports |
| [02-Wireshark-Packet-Analysis.md](./02-Wireshark-Packet-Analysis.md) | Capture filters, display filters, protocol analysis, detecting port scans, ARP spoofing, DNS tunneling, tcpdump |
| [03-OS-Basics.md](./03-OS-Basics.md) | What is an OS, kernel vs user space, Windows/Linux/macOS, boot process, virtualization, CPU architecture |
| [04-File-Systems.md](./04-File-Systems.md) | NTFS, ext4, FAT32, exFAT, inodes, MBR vs GPT, mounting, forensics & data recovery |
| [05-Process-Memory.md](./05-Process-Memory.md) | Processes vs threads, virtual memory, paging, memory layout, CPU scheduling, NX/ASLR |
| [06-OS-Security.md](./06-OS-Security.md) | UAC, sudo, patch management, secure boot, hardening checklists, logging, common vulns |

---

## Tools Referenced

| Tool | Purpose |
|------|---------|
| `nmap` | Port scanning and service detection |
| `dig` / `nslookup` | DNS enumeration |
| `subfinder` / `amass` | Subdomain recon |
| `Wireshark` | GUI packet analysis |
| `tcpdump` | CLI packet capture |
| `ipcalc` | Subnet calculator |
| `ps` / `top` / `htop` | Process monitoring |
| `vmstat` / `free` | Memory & swap analysis |
| `stat` / `lsblk` / `fdisk` | File system & disk inspection |
| `journalctl` | System log analysis |

---

## Related Repos

| Repo | What's inside |
|------|--------------|
| [python](https://github.com/Utkarsh464/python) | Python fundamentals, study notes, and security scripts |
| [linux-notes](https://github.com/Utkarsh464/linux-notes) | Permissions, users, groups, commands, bash one-liners |
| [cybersecurity-notes](https://github.com/Utkarsh464/cybersecurity-notes) | Fundamentals, ethical hacking, web application security, roadmap |

---

*Last updated: June 2026*
