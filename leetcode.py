def maximumTotalDamage(power):
    power_sorted = sorted(power)
    power_set_list = list(set(power_sorted))
    dp = [0] * len(power_set_list)
    for i in range(len(power_set_list)):
        dp[i] = sum([j for j in power_sorted if abs(j-power_set_list[i])==0 or abs(j-power_set_list[i]) > 2])

    return max(dp)
print(maximumTotalDamage([1,1,3,4]))