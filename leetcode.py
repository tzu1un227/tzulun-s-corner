s = "42"
UNDERZERO = False
result = ""

for c in range(len(s)):
    if s[c] != " ":
        s=s[c:]
        break

if s:
    if s[0]=="-":
        UNDERZERO = True
        s=s.replace("-","")
    elif s[0]=="+":
        s=s.replace("+","")

for c in range(len(s)+1):
    
    if c == len(s) or not s[c].isdigit():
        result = s[:c]
        if result and UNDERZERO:
            result = "-"+result
        break

result = int(result) if result else 0

if result < -(2**31):
    result = -2**31
elif result > 2**31:
    result = 2**31 - 1

print(result)