# ex1
from functools import reduce

names = ["Yoav", "Ron", "Aviva", "Ronen", "Dan", "Galit"]
lens = map(lambda n: len(n), names)
shorts = filter(lambda x: x > 4, lens)
total = reduce(lambda x, y: x + y, shorts)
print(total)


# ex2
def pub_sub(n1, n2, funcs):
    for func in funcs:
        print(func(n1, n2))


pub_sub(2, 5, [lambda x, y: x + y, lambda x, y: x - y, lambda x, y: x * y])

# ex3
nums = [6, 2, 8, 12, 4]
minNum = reduce(lambda x, y: min(x, y), nums)
print(minNum)

# פתרון של המנחה
# יוצאים מנקודת הנחה שהראשון הוא הכי נמוך ומחזירים את הבא רק אם הוא יותר קטן
nums = [6, 2, 8, 12, 4]
minNum = reduce(lambda x, y: x if x < y else y, nums)
print(minNum)


# ex4
def pow_mul(num):
    def pow(num):
        return num**2

    return pow(num * 2)


print(pow_mul(10))
