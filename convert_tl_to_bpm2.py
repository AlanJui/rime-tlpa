#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
convert_tl_to_bpm2.py

功能：
  1. 在同一份 Excel 檔裡，讀取「台羅轉換注音二式規則」工作表並解析規則。
  2. 建立映射字典：台羅拼音 → 注音二式。
  3. 讀取「tl_ji_khoo_phing」工作表，把「台羅拼音」欄轉換後寫回「注音二式」欄。
  4. 覆寫存檔。
"""

import pandas as pd

# 1. Excel 檔案路徑
excel_file = '漢字閩南語標音【台羅拼音】.xlsx'

# 1.1 先把規則表當純資料讀進來（不指定 header）
raw = pd.read_excel(
    excel_file,
    sheet_name='台羅轉換注音二式規則',
    header=None,
    dtype=str
)

# 1.2. 印出前 10 列，看看標頭列大概在第幾列（0-base）
print("=== raw head ===")
print(raw.head(10))

# 1.3. 假設您看到第 2 列（index=1）才是欄位名稱，就改成 header=1；若是第 3 列，就 header=2……
#    例如這裡示範用 header=1，請依您實際 raw.head() 結果做調整
header_idx = 1

df_rules = pd.read_excel(
    excel_file,
    sheet_name='台羅轉換注音二式規則',
    header=header_idx,
    dtype=str
)

# 1.4. 去除欄位前後空白，並印出最終欄位名稱確認
df_rules.columns = df_rules.columns.str.strip()
print("=== rules columns ===")
print(df_rules.columns.tolist())

# 1.5. 確定對應欄位的名稱──
#    假設欄位就叫 '台羅拼音' 跟 '注音二式'，否則改成對應出的字串
tl_col   = '台羅拼音'
bpm2_col = '注音二式'

# 1.6. 只取這兩欄並去掉空值，避免後面 mapping 出錯
df_rules = df_rules[[tl_col, bpm2_col]].dropna(how='any')

# 1.7. 再次 trim 每個值，確保沒有隱藏空白
df_rules[tl_col]   = df_rules[tl_col].str.strip()
df_rules[bpm2_col] = df_rules[bpm2_col].str.strip()

# 1.8. 建立 mapping
mapping = dict(zip(df_rules[tl_col], df_rules[bpm2_col]))
print(f"映射筆數：{len(mapping)}，前 10 筆：{list(mapping.items())[:10]}")


# 3. 讀取所有工作表
all_sheets = pd.read_excel(excel_file, sheet_name=None)

# 確認要處理的資料表名稱
data_sheet = 'tl_ji_khoo_phing'
if data_sheet not in all_sheets:
    # 若名稱有誤，可嘗試找含「hing」的
    alt = [n for n in all_sheets if 'hing' in n]
    if alt:
        data_sheet = alt[0]
    else:
        raise RuntimeError(f'找不到工作表：{data_sheet}')

df = all_sheets[data_sheet]

# 定義轉換函式
def to_bpm2(x):
    return mapping.get(x, '')

# 套用：直接寫回「注音二式」欄
df[bpm2_col] = df['台羅拼音'].apply(to_bpm2)

# 更新回字典
all_sheets[data_sheet] = df

# 4. 覆寫存回同一個檔案
with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    for name, sheet in all_sheets.items():
        sheet.to_excel(writer, sheet_name=name, index=False)

print('✅ 轉換完成，結果已寫回「注音二式」欄，並儲存回原檔案。')
