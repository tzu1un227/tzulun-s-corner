import os
os.system('cls')

strA='babad'
strB='cbbd'
strC='a'
s=strA
result=''
for i in range(len(s)+1):
    for j in range(i+1,len(s)+1):
        temp=s[i:j]
        if temp==temp[::-1] and len(temp)>len(result):
            result=temp


print(result)