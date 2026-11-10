def longestConsecutive(nums):
    set_nums = set(nums)
    sorted_num = sorted(set_nums)
    result = 1
    temp_result = 1
    for i in range(len(sorted_num)-1):
        if sorted_num[i] == sorted_num[i+1] - 1:
            temp_result += 1
        else:
            temp_result = 1
        if temp_result > result:
            result = temp_result
    return result
    
print(longestConsecutive([2,20,4,10,3,4,5]))

print(longestConsecutive([0,3,2,5,4,6,1,1]))

print(longestConsecutive([0,-1]))