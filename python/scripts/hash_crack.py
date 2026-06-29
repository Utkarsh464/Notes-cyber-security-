import hashlib

algos = {
    32: hashlib.md5,
    40: hashlib.sha1,
    56: hashlib.sha224,
    64: hashlib.sha256,
    96: hashlib.sha384,
    128: hashlib.sha512,
}

def crack_hash(target, wordlist):
    algo = algos.get(len(target))
    if algo is None:
        print("unknown hash type")
        return
    with open(wordlist, "r", errors="ignore") as f:
        for line in f:
            if target == algo(line.strip().encode()).hexdigest():
                print("found", target, "=", line.strip())
                return
    print("not found")

x = input("enter the hash :")
w = input("enter wordlist path :")
crack_hash(x, w)
