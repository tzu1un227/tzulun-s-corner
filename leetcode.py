nums = [-1,0,1,2,-1,-4]
result = []
for x in nums:
    copy_nums = nums.copy()
    copy_nums.remove(x)
    y, z = 0, len(copy_nums) - 1
    while y != z:
        if copy_nums[y] + copy_nums[z] == -x:
            result.append([x, y, z])

print(result)