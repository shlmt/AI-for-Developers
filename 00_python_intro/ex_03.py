# 1
def func1(s1, s2):
    print(s1 if len(s1) > len(s2) else s2)


func1("hello!!!", "world")


# 2
def func2(flag, n1, n2):
    if flag:
        print(n1 + n2)
    else:
        return n1 * n2


print(func2(False, 1, 2))


# 3
def func3(arr_nums):
    return sum(arr_nums)


print(func3([1, 2, 3, 4, 5]))


# 4
def func4(arr_str):
    for s in arr_str:
        func5(s)


def func5(str):
    print(str)


func4(["aaa", "bbb", "ccc"])
