# 1
s1 = input("enter string 1\n")
s2 = input("enter string 2\n")
print(s1 + " " + s2)

# 2
n1, n2 = input("Enter two numbers: ").split()
if int(n1) + int(n2) > 10:
    print("big")
else:
    print("small")

# 3
n1, n2 = input("Enter two numbers: ").split()
s = input("enter string\n")
if int(n1) + int(n2) > len(s):
    s1 = input("enter string 1\n")
    s2 = input("enter string 2\n")
    print(s1 if len(s1) > len(s2) else s2)

# 4
n = int(input("enter number\n"))
sum_numbers = n
while n < 10:
    n = int(input("enter number\n"))
    sum_numbers += n
print(sum_numbers)
