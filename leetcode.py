def triangularSum(nums):
    if len(nums) == 1:
        return nums[0]
    for i in range(len(nums)-1):
            nums[i]=nums[i]+nums[i+1]
    return triangularSum(nums[:-1]) % 10
print(triangularSum([1,2,3,4,5]))