while True:
    print("Height: ",end="")
    a = int(input())
    if 1 < a < 23:
        break
    
for i in range(a):
    print(" " * (a - 1 - i), end="") 
    print("#" * (i + 1), end="")
    print(" " * 2, end="")
    print("#" * (i + 1), end="")
    print()