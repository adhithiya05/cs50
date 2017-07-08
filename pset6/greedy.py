while True:
    print("How much change is owed ?")
    a = float(input())
    if a > 0:
        break
    
b = round(a * 100)
print(b)
quarter = b // 25
balance = b % 25
dimes = balance // 10
balance = balance % 10
nickel = balance // 5
balance = balance % 5
coins = quarter + dimes + nickel + balance
print(coins)