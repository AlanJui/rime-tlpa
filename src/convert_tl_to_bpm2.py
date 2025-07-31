#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
convert_tl_to_bpm2.py

功能：
  1. 讀取同一份 Excel 中的兩個工作表：
     - tl_ji_khoo_phing（來源資料，含「台羅拼音」欄位）
     - 台羅轉換注音二式規則（對應表，含「台羅拼音」與「注音二式」欄位）
  2. 建立映射字典，將台羅拼音轉換為注音二式。
  3. 對 tl_ji_khoo_phing 工作表的每一列，將「台羅拼音」轉換後寫入「台語注音二式音標」欄位。
  4. 將轉換後的結果寫入新的 Excel 檔案。

使用方式：
  1. 將本檔與 Excel 放在同一目錄，或自行修改 input_file 與 output_file 變數為絕對路徑。
  2. 執行：python convert_tl_to_bpm2.py
"""

import pandas as pd

# 1. 設定輸入與輸出檔案名稱
# input_file  = '漢字閩南語標音【台羅拼音】.xlsx'       # 原始檔案，內含兩個工作表
# output_file = '漢字閩南語標音_轉換後.xlsx'          # 轉換完畢後的輸出檔案
input_file  = 'tl_phing_im.xlsx'       # 原始檔案，內含兩個工作表
output_file = '漢字閩南語標音_轉換後.xlsx'          # 轉換完畢後的輸出檔案

# 2. 讀取工作表
#    sheet_name 可用名稱或索引（0, 1, …）
df_data  = pd.read_excel(input_file, sheet_name='tl_ji_khoo_phing')
df_rules = pd.read_excel(input_file, sheet_name='台羅轉換注音二式規則')

# 3. 建立映射字典：鍵為「台羅拼音」，值為「注音二式」
#    假設規則表中「台羅拼音」與「注音二式」欄位名稱正確無誤
mapping = pd.Series(
    df_rules['注音二式'].values,
    index=df_rules['台羅拼音']
).to_dict()

# 4. 定義轉換函式：若對應表中無此拼音，預設回傳空字串
def convert_to_bpm2(tl_value):
    """
    將單一台羅拼音字串轉為注音二式。
    tl_value：字串，如 'khua1'
    回傳：對應的注音二式，如 'khua1' → 'ㄎㄨㄚ1' (視規則表而定)
    """
    return mapping.get(tl_value, '')

# 5. 套用到原始資料
df_data['台語注音二式音標'] = df_data['台羅拼音'].apply(convert_to_bpm2)

# 6. 輸出結果到新的 Excel
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # 只將轉換後的 tl_ji_khoo_phing 寫入同名工作表
    df_data.to_excel(writer, sheet_name='tl_ji_khoo_phing', index=False)

print(f'轉換完成，結果已儲存至：{output_file}')

