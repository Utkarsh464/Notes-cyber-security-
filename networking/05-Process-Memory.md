# Processes, Memory & the CPU — How Programs Actually Run

> Personal notes by Utkarsh Solanki | Cybersecurity & AI Student  
> GitHub: [github.com/Utkarsh464](https://github.com/Utkarsh464) | LinkedIn: [linkedin.com/in/utkarsh-solanki-337806252](https://linkedin.com/in/utkarsh-solanki-337806252)

---

## Programs vs Processes — Not the Same Thing

A **program** is a file on disk (like `chrome.exe`). A **process** is that program **loaded into memory and running**.

Think of a program as a recipe book, and a process as someone actually cooking that recipe. You can have 5 people cooking the same recipe (5 Chrome tabs) — each is a separate process.

```bash
# See all running processes
ps aux
# Every line is a process with its own PID, memory, and state
```

---

## Processes — The OS's To-Do List

### Process States

Every process goes through these states:

```
Start → Ready → Running → Waiting (I/O, disk, network)
                  ↓
                Terminated
```

- **Ready** — process has everything it needs except CPU time
- **Running** — CPU is actually executing this process right now
- **Waiting** — process is blocked waiting for something (keyboard input, disk read, network packet)

When you open a big file in a text editor, the process goes into "Waiting" state until the disk finishes reading. The CPU uses that time to work on other processes.

### Context Switching

The CPU can only run one process at a time per core. But a modern CPU does **context switching** — it runs Process A for a few milliseconds, saves its state, runs Process B, saves its state, then goes back to A. This happens thousands of times per second, making it look like everything is running simultaneously.

```bash
# Watch context switches in real-time
vmstat 1
# Look at the 'cs' (context switch) column
```

**Security angle:** Context switches are invisible to users, but kernel exploits can manipulate them to escalate privileges or bypass security checks.

---

### Process Control Block (PCB)

For every process, the OS keeps a data structure called the PCB. It contains:

```
PID (Process ID)              — unique number
State                         — running, waiting, etc.
Program Counter               — next instruction to execute
CPU registers                 — saved state for context switching
Memory limits                 — what address space this process can access
Open files list               — every file descriptor this process has
Priority                      — how important is this process?
Parent process (PPID)         — who started this process
```

You can see some of this info on Linux:
```bash
ls /proc/1234/    # everything about PID 1234
cat /proc/1234/status   # human-readable PCB info
cat /proc/1234/fd/      # open file descriptors
```

---

### Zombies and Orphans

**Zombie process:** A process that has finished executing but still has an entry in the process table (because the parent hasn't read its exit status yet). It's dead but not cleaned up.

```bash
# Zombies show with status Z in ps output
ps aux | grep Z
```

**Orphan process:** A process whose parent has died. The OS adopts it — `init` (PID 1) becomes its new parent.

---

## Threads — Lightweight Processes

A process can have multiple **threads** — parallel execution paths within the same process. Threads share the same memory space (so they can communicate easily), but each has its own stack and registers.

```
Process (1 Chrome tab)
├── Thread 1 — main UI
├── Thread 2 — network request
├── Thread 3 — rendering
└── Thread 4 — JavaScript engine
```

Threads are cheaper to create than processes because they share memory (no need to copy everything).

```bash
# See threads in a process
ps -eLf | grep chrome
# Look at NLWP (Number of Light-Weight Processes) = threads
```

---

## Virtual Memory — The Con That Makes Everything Work

Here's the problem: programs need memory, but there's not enough RAM for everything at once. And even if there were, one program shouldn't be able to read another's memory.

**Virtual memory** solves both problems with a clever trick.

### How It Works

Each process gets its own **virtual address space** (on 64-bit systems: a massive 256 TB). The process thinks it has all this memory to itself. But the OS is mapping these virtual addresses to **physical RAM** pages behind the scenes.

```
Process A's view:          Physical reality:
┌──────────────┐          ┌──────────────┐
│ 0x0000-0xFFF │          │  RAM page 0  │ ← Process A
│   (virtual)  │          ├──────────────┤
├──────────────┤          │  RAM page 1  │ ← Process B
│ 0x1000-0x1FFF│          ├──────────────┤
│   (virtual)  │          │  RAM page 2  │ ← Process A
└──────────────┘          ├──────────────┤
                          │  RAM page 3  │ ← Kernel
                          └──────────────┘
```

The **Memory Management Unit (MMU)** is hardware that translates virtual addresses to physical addresses on the fly. Each process has a **page table** that maps its virtual pages to physical frames.

### Benefits

1. **Isolation** — Process A can't see Process B's memory (unless they explicitly share it)
2. **Efficiency** — unused parts of a program can be swapped to disk
3. **Simplicity** — every program sees a clean, contiguous address space

### Paging and Swapping

When RAM gets full, the OS moves some memory pages to disk (swap space on Linux, pagefile.sys on Windows). This is **swapping**.

```bash
# Check swap usage
free -h
swapon --show

# Set swapiness (how aggressively to swap)
cat /proc/sys/vm/swappiness
# Default: 60 (higher = more swapping)
```

**Security note:** When a process is swapped out, its data is written to disk in plaintext (unless encrypted). An attacker with disk access could read swapped memory containing passwords or encryption keys.

---

## Memory Layout of a Process

When a process loads into memory, it gets this layout:

```
High addresses
┌──────────────────────┐
│       Stack          │ ← Local variables, function calls, return addresses
│         ↓            │
│                      │
│         ↑            │
│       Heap           │ ← Dynamic allocation (malloc, new)
├──────────────────────┤
│    Data (BSS)        │ ← Uninitialized global variables
│    Data (init)       │ ← Initialized global variables
├──────────────────────┤
│       Text           │ ← Program code (instructions)
└──────────────────────┘
Low addresses
```

**Stack:**
- Grows downward
- Stores: function parameters, return addresses, local variables
- Each function call pushes a "stack frame"
- **Buffer overflow target** — write past a local variable to overwrite the return address

**Heap:**
- Grows upward
- Stores: dynamically allocated memory (malloc, new)
- **Heap overflow target** — corrupt adjacent heap objects or metadata

**Text:**
- Read-only (usually) — the CPU fetches instructions from here
- Patching this region means modifying the program's code (code injection)

---

## CPU Scheduling — Who Gets the CPU When

The OS scheduler decides which process runs next.

### Scheduling Algorithms

| Algorithm | How it works | Used in |
|-----------|-------------|---------|
| Round Robin | Each process gets a fixed time slice | General-purpose OS |
| Priority-based | Higher priority processes run first | Real-time systems |
| Completely Fair (CFS) | Fair share of CPU time | Linux |
| Multilevel Queue | Different queues for different types | Windows |

You can influence scheduling on Linux:
```bash
# See process priority (-20 = highest, 19 = lowest)
nice -n -10 ./important_program

# Change priority of running process
renice -5 -p 1234
```

### The Five-Minute Rule

Here's a way to think about relative speed:

```
CPU cache          → 1 nanosecond    (5 minutes)
RAM                → 100 nanoseconds (8 hours)
SSD                → 10 microseconds (1 month)
HDD                → 10 milliseconds (2 years)
Network request    → 100 milliseconds (20 years)
```

*(The parenthetical is what each step feels like if CPU time is compressed to 5 minutes.)*

When your program reads from disk, the CPU could have executed millions of instructions in that time. That's why caching is everything.

---

## Security Implications

### Process Isolation
The OS prevents one process from reading another's memory. But bugs in the OS (kernel exploits) can break this — that's how privilege escalation works.

### Memory Protection

Modern CPUs provide:

| Feature | What it does | Bypassed by |
|---------|-------------|-------------|
| **NX / DEP** | Marks stack/heap as non-executable | ROP (Return-Oriented Programming) |
| **ASLR** | Randomizes where code loads | Info leak first, then calculate offsets |
| **Stack canaries** | Value on stack before return address | Info leak or brute force |
| **SMEP** | Kernel can't execute user-space code | ROP chains in kernel |

### What Attackers Look For

- **Process listing** — what's running, what version, what's vulnerable
- **Open file handles** — what files does a process have access to?
- **Memory dumps** — `procdump`, `/proc/PID/mem` can leak credentials
- **Unquoted service paths** — Windows service with spaces in path
- **DLL injection** — inject code into a running process

---

*Last updated: June 2026*
