import hashlib

algos = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha224": hashlib.sha224,
    "sha256": hashlib.sha256,
    "sha384": hashlib.sha384,
    "sha512": hashlib.sha512,
}

def hasher(algo, password):
    return algo(password.strip().encode()).hexdigest()

word = input("enter the password :")
choice = input("choose algo (md5/sha1/sha224/sha256/sha384/sha512): ")
func = algos.get(choice)
if func is None:
    print("unknown algo")
else:
    print(hasher(func, word))
