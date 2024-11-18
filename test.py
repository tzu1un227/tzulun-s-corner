s="jbpnbwwd"

temp = ""
result = 0
# for c in s:
#     if c in temp:
#         temp = ""
#     else:
#         temp = temp + c
#         if len(temp)>result:
#             result=len(temp)
for i in range(0,len(s)):
    for j in range(i,len(s)):
        if s[j] in temp:
            temp = ""
            break
        else:
            temp = temp + s[j]
            if len(temp)>result:
                result=len(temp)

print(result)