import hashlib

def crack_hash(target, wordlist):
    with open(wordlist, "r", errors="ignore") as f:
        for line in f:
            if target == hashlib.md5(line.strip().encode()).hexdigest():
                print("found", target, "=", line.strip())
                return
    print("not found")

x = input("enter the hash :")
crack_hash(x, "../passwords/rockyou.txt")
