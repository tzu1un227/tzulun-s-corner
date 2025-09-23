n = 3
parentheses_list = ["()"] * n*2
result_list = []
temp = []

def BT(index):
    if len(temp) == n * 2:
        result_list.append("".join(temp))
        return
    
    for c in parentheses_list[index]:
        if (temp.count("(") == temp.count(")") and c == ")") or (temp.count("(") == n and c == "("):
            continue

        temp.append(c)
        BT(index+1)
        temp.pop()

BT(0)

print(parentheses_list)
print(result_list)