import hashlib
x = input("enter the hash :")
with open("../passwords/rockyou.txt", "r", errors= "ignore") as f:
    for line in f:
        if x == hashlib.md5(line.strip().encode()).hexdigest():
            print("found", x, "=", line.strip()) 
    else:
            print("not found")
