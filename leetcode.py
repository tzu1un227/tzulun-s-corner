def canJump(nums) -> bool:
    currEnd = 0
    for i in range(len(nums)):
        if currEnd >= len(nums) -1 :
            return True
        if i > currEnd:
            return False
        if i+nums[i] >= currEnd:
            currEnd = i+nums[i]

    return False


print(canJump([2,5,0,0]))