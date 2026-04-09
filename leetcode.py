def topKFrequent(nums,k):
    fdict={}
    for num in nums:
        fdict[num]=fdict.get(num,0)+1

    return sorted(fdict.items(),key=lambda x: x[1], reverse=True)[:k]
    
print(topKFrequent(nums = [1,2,2,3,3,3], k = 2))