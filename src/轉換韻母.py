import re

import xlwings as xw


def replace_final(text):
    if re.search(r"m$", text):
        return re.sub(r"m$", "W", text)
    elif re.search(r"ng$", text):
        return re.sub(r"ng$", "N", text)
    elif re.search(r"n$", text):
        return re.sub(r"n$", "M", text)
    return text

# 連到【目前作用中的 Excel】
wb = xw.apps.active.books.active
# sheet = wb.sheets.active   # 目前作用中的工作表
sheet = wb.sheets["韻母轉換"]


# 假設要處理 A 欄 (A2 ~ A100)
for cell in sheet.range("A2:A100"):
    if cell.value:
        un_before = str(cell.value)
        cell.value = replace_final(str(cell.value))
        un_after = str(cell.value)
        print(f"{un_before} => {un_after}")