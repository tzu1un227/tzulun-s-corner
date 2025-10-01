def uniquePaths(m, n):
    dp = [[1 for _ in range(n)] for _ in range(m)]
    dp[0][0] = 0
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[-1][-1]
print(uniquePaths(m = 3, n = 7))