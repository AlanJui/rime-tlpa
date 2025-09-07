#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
convert_tlpa_to_mps2_for_excel.py

功能：
  1. 讀取同一份 Excel 中的兩個工作表：
     - tl_ji_khoo_phing（來源資料，含「台羅拼音」欄位）
     - 台羅轉換注音二式規則（對應表，含「台羅拼音」與「注音二式」欄位）
  2. 建立映射字典，將台羅拼音轉換為注音二式。
  3. 對 tl_ji_khoo_phing 工作表的每一列，將「台羅拼音」轉換後寫入「台語注音二式音標」欄位。
  4. 將轉換後的結果寫入新的 Excel 檔案。

使用方式：
  1. 將本檔與 Excel 放在同一目錄，或自行修改 input_file 與 output_file 變數為絕對路徑。
  2. 執行：python convert_tlpa_to_mps2_for_excel.py
  3. 可選參數 -out 指定輸出檔案名稱，若不指定則覆寫原檔案。
      python convert_tlpa_to_mps2_for_excel.py <輸入檔案> -out <輸出檔案>
"""

import os
import sys

import pandas as pd

from convert_tlpa_to_mps2 import convert_TLPA_to_MPS2

# 1. 設定輸入與輸出檔案名稱
# input_file = None
input_file = './src/tl_phing_im.xlsx'  # 預設輸入檔案
output_file = None  # 預設為 None，表示直接覆寫原檔案
SOURCE_SHEET = 'tl_ji_khoo'  # 來源資料工作表名稱

# 解析命令列參數
if len(sys.argv) > 1:
    input_file = sys.argv[1]  # 第一個參數為輸入檔案
    if len(sys.argv) > 3 and sys.argv[2] == '-out':
        output_file = sys.argv[3]  # 若有 -out 選項，則設定輸出檔案

# 確保 input_file 為字串類型
if not isinstance(input_file, str):
    print("輸入檔案名稱無效，請提供正確的檔案路徑。")
    sys.exit(1)

# 檢查檔案是否存在
if not os.path.isfile(input_file):
    print(f"檔案不存在：{input_file}")
    sys.exit(1)

# 檢查檔案格式
if not input_file.endswith('.xlsx'):
    print(f"檔案格式錯誤，請提供有效的 .xlsx 檔案：{input_file}")
    sys.exit(1)

try:
    # 確保使用 openpyxl 引擎讀取 Excel 檔案
    excel_file = pd.ExcelFile(input_file, engine='openpyxl')
    sheet_names = excel_file.sheet_names
except Exception as e:
    print(f"無法讀取 Excel 檔案，請確認檔案是否損壞或格式正確：{e}")
    sys.exit(1)

if not sheet_names:
    print("Excel 檔案中沒有可見的工作表，請檢查檔案內容。")
    sys.exit(1)

df_data = pd.read_excel(input_file, sheet_name=SOURCE_SHEET)

# 3. 修改轉換函式：直接使用 convert_TLPA_to_MPS2
def convert_to_mps2(tlpa_im_piau):
    """
    將單一台羅拼音字串轉為注音二式。
    tl_value：字串，如 'khua1'
    回傳：對應的注音二式，如 'khua1' → 'ㄎㄨㄚ1'
    """
    return convert_TLPA_to_MPS2(tlpa_im_piau)

# 4. 套用到原始資料
#    將台羅拼音逐一轉換為注音二式
df_data['注音二式'] = df_data['台羅拼音'].apply(convert_to_mps2)

# 5. 輸出結果
if output_file:
    # 若指定輸出檔案，則另存
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for sheet_name in sheet_names:
            if sheet_name == SOURCE_SHEET:
                df_data.to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                # 保留原始格式，避免新增 Unnamed 欄位
                original_sheet = pd.read_excel(input_file, sheet_name=sheet_name, engine='openpyxl')
                original_sheet.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
    print(f'轉換完成，結果已儲存至：{output_file}')
else:
    # 否則覆寫原檔案
    with pd.ExcelWriter(input_file, engine='openpyxl') as writer:
        for sheet_name in sheet_names:
            if sheet_name == SOURCE_SHEET:
                df_data.to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                # 保留原始格式，避免新增 Unnamed 欄位
                original_sheet = pd.read_excel(input_file, sheet_name=sheet_name, engine='openpyxl')
                original_sheet.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
    print(f'轉換完成，結果已覆寫至原檔案：{input_file}')

