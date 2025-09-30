def triangleNumber(nums):
    nums = sorted(nums,reverse=1)
    result = 0
    for i in range(len(nums) - 2):
        if nums[i] > 0:
            for j in range(i+1, len(nums) - 1):
                left = j + 1
                right = len(nums) - 1
                while left < right:
                    mid = (left + right) // 2
                    if nums[mid] + nums[j] <= nums[i]:
                        right = mid - 1
                    elif nums[mid] + nums[j] > nums[i]:
                        left = mid + 1
                mid = max(left, right)
                if mid < len(nums)-1 and nums[mid + 1] + nums[j] > nums[i]:
                    result += mid - j + 1
                elif nums[mid] + nums[j] > nums[i]:
                    result += mid - j
                else:
                    result += mid - j - 1
        else:
            continue
    return result
print(triangleNumber([7,0,0,0]))