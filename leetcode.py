def jump(nums):

    dp = [len(nums)] * len(nums)
    dp[0] = 0
    
    for i in range(0, len(nums) - 1):
        for j in range(1, nums[i]+1):
            if i + j >= len(nums) :
                continue
            if dp[i+j] > dp[i] + 1:
                dp[i+j] = dp[i] + 1

    return dp[-1]

nums = [1,3,2]
print(jump(nums))