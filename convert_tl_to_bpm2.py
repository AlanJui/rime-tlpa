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

# 2. 先把規則表當純資料讀進來，找出真正的標頭列
raw = pd.read_excel(excel_file,
                    sheet_name='台羅轉換注音二式規則',
                    header=None)

header_idx = None
for i, row in raw.iterrows():
    if row.astype(str).str.contains('台羅拼音').any():
        header_idx = i
        break
if header_idx is None:
    raise RuntimeError('在「台羅轉換注音二式規則」找不到「台羅拼音」標頭')

# 重新以正確標頭讀
df_rules = pd.read_excel(excel_file,
                         sheet_name='台羅轉換注音二式規則',
                         header=header_idx)

# 自動抓「台羅」來源欄與「注音二式」目標欄
src_cols = [c for c in df_rules.columns if '台羅' in c]
dst_cols = [c for c in df_rules.columns if '注音二式' in c]
if not src_cols or not dst_cols:
    raise RuntimeError('無法在規則表找到「台羅」或「注音二式」欄位')
tl_col    = src_cols[0]
bpm2_col  = dst_cols[0]

# 建映射字典
mapping = pd.Series(df_rules[bpm2_col].values,
                    index=df_rules[tl_col]).to_dict()

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
