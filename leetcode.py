def hasDuplicate(nums):
    setofnums=set(nums)
    print(setofnums)
    print(nums)
    print(len(setofnums))
    print(len(nums))
    return False if len(setofnums) == len(nums) else True
print(hasDuplicate([1,2,3,3]))