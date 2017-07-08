import sys

while True:
    if len(sys.argv) != 2:
        print("Usage: caesar.py k")
        exit(1)
    else:
        break

a = int(sys.argv[1])
plain = input()

for p in plain:
    if (str.isupper(p)):
        cipher_val = ((((ord(p) - 65) + a) % 26) + 65)
        cipher = chr(cipher_val)
        print(cipher, end="")
        
    elif (str.islower(p)):
        cipher_val = ((((ord(p) - 97) + a) % 26) + 97)
        cipher = chr(cipher_val)
        print(cipher, end="")
        
    else:
        print(p, end="")
print()
