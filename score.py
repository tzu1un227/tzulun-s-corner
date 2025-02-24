'''
事前準備:
1.準備一個excel檔，第一個colume放全部學生的學號，第二個colume放全部學生的姓名
2.填試算表檔名
3.填工作表名稱
4.填班級總人數
'''
excel_name = 'score.xlsx'
sheet_name = '工作表1'
total_num = 155 #填總人數，
# 導入函式庫
import openpyxl

# 清空terminal。非必要，但有了看了很舒服
import os
os.system('cls')

# 讀取excel，這裡放試算表檔名
wb = openpyxl.load_workbook(excel_name)

# 讀取工作表，這裡放工作表名稱
sh = wb[sheet_name]

# main

while(True):
    id = input("學號 > ")
    if id == 'q':
        break
    for i in range(1,int(total_num)+2):
        if str(sh[f'A{i}'].value) == id:
            print("姓名:",sh[f'B{i}'].value)
            score = input("分數 > ")
            sh[f'C{i}'].value = score
            break
        elif sh[f'A{i}'].value == None:
            print("學號錯誤")
    

# 儲存excel
wb.save('score.xlsx')