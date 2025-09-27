def mergeTwoLists(list1, list2):
    result = []
    while list1 or list2:
        if not list1 or list1[0] > list2[0]:
            result.append(list2[0])
            list2.pop(0)
        elif not list2 or list1[0] <= list2[0]:
            result.append(list1[0])
            list1.pop(0)
    return result

print(mergeTwoLists(list1 = [1,2,4], list2 = [1,3,4]))