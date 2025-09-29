def minScoreTriangulation(values):
    dp = [0] * (len(values) - 2)
    dp[0] = values[0] * values[1] * values[2]
    for i in range(1,len(values)-2):
        dp[i] = dp[i-1] + min()
    return dp[-1]


print(minScoreTriangulation(values = [4,3,4,3,5]))