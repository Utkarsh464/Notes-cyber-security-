import hashlib
def hasher(password):
    return hashlib.md5(password.strip().encode()).hexdigest()
word = input("enter the password :")
print(hasher(word))