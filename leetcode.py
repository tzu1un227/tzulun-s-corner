def climbStairs(n):
    steps = 0
    def DFS(temp,step ,n)->int:
        temp += step
        if temp + step >= n:
            return 1
        DFS(temp , 2, n)
        DFS(temp , 1, n)

    steps += DFS(steps, 0, n)
    return steps

print(climbStairs(3))