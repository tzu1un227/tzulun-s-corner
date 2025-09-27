def findMedianSortedArrays(nums1, nums2):
    MedianIndex = (len(nums1) + len(nums2)) // 2
    sorted_nums = []
    while nums1 and nums2:
        if nums1[0] > nums2[0]:
            sorted_nums.append(nums2[0])
            nums2.pop(0)
        else:
            sorted_nums.append(nums1[0])
            nums1.pop(0)
    sorted_nums += nums1 if nums1 else nums2
    return float(sorted_nums[MedianIndex]) if len(sorted_nums) % 2 != 0 else (float(sorted_nums[MedianIndex]) + float(sorted_nums[MedianIndex-1])) / 2.0

print(findMedianSortedArrays([1,2,3,4,5], [6,7,8,9,10,11,12,13,14,15,16,17]))