import random
import os
os.system("cls")
# 定義顏色和數量
colors = ['白色'] * 6 + ['黑色'] * 6 + ['綠色'] * 5 + ['藍色'] * 5 + ['紅色'] * 5 + ['黃色'] * 5

# 隨機打亂顏色列表
random.shuffle(colors)

# 打印結果
print(colors)
