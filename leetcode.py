def minPathSum(grid):
    n = len(grid[0])
    m = len(grid)
    dp = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(0, m):
        for j in range(0, n):
            if i == 0 and j ==0:
                dp[i][j] = grid[i][j]
            elif i == 0:
                dp[i][j] = dp[i][j-1] + grid[i][j]
            elif j == 0:
                dp[i][j] = dp[i-1][j] + grid[i][j]
            else:
                dp[i][j] = min(dp[i][j-1], dp[i-1][j]) + grid[i][j]
            
    return dp[-1][-1]
print(minPathSum([[1,3,1],[1,5,1],[4,2,1]]))