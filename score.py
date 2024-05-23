'''
事前準備:
準備一個excel檔，第一個colume放全部學生的學號
'''
# 導入函式庫
import openpyxl

# 清空terminal
import os
os.system('cls')

# 讀取excel
wb = openpyxl.load_workbook('score.xlsx')

# 讀取工作表
sh = wb['工作表1']

# main
total_num = input("學生總共有多少人") #計算機數學 35 人/電機專題 156 人
while(True):
    id = input("學號 > ")
    if id == 'q':
        break
    for i in range(1,total_num):
        if str(sh[f'A{i}'].value) == id:
            score = input("分數 > ")
            sh[f'B{i}'].value = score
            break
        elif sh[f'A{i}'].value == None:
            print("學號錯誤")
    

# 儲存excel
wb.save('score.xlsx')