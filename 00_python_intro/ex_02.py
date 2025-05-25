# 1
lst = [4, "hello", [True, "avi", [5, 1, 9, 3]]]
num_lst = lst[2][2]
print(sum(num_lst) / len(num_lst))

# 2
arr = [17, 1, 12, 54, 23, 9, 21]
print(sum(filter(lambda x: 3 < x < 20, arr)))

# 3
arr = [17, 1, 12, 54, 23, 9, 21, 4, 87, 11, 36]
print(sum(filter(lambda x: x % 2, arr)))

# 4
arr = [17, 1, 12, 54, 23, 9, 21, 4, 87, 11, 36]
half_arr = arr[:int(len(arr) / 2)]
print(sum(half_arr) / len(half_arr))

# 5
mat = [[32, 15], [1, 7, 12], [8, 14, 6, 11]]
print(max([sum(arr) for arr in mat]))

# 6
strct = {
    "nums1": [4, 1, 2, 5],
    "nums2": [6, 1, 8, 3],
    "Student": {
        "Name": "Avi",
        "ID": 111111,
        "Grades": {
            "nums3": [4, 1, 9, 3]
        }
    }
}

nums1 = strct["nums1"]
nums3 = strct["Student"]["Grades"]["nums3"]
print(max(sum(nums1) / len(nums1), sum(nums3) / len(nums3)))
