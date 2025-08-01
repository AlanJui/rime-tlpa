#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
convert_tl_to_bpm2_openpyxl.py

功能：
  1. 讀取同一支 Excel（漢字閩南語標音【台羅拼音】.xlsx）
  2. 解析「台羅轉換注音二式規則」工作表，建立 台羅拼音 → 注音二式 的對應字典
  3. 逐列讀取「tl_ji_khoo_phing」工作表，把「台羅拼音」轉換後寫回「注音二式」欄
  4. 只儲存回原檔案，其餘工作表與格式不變
"""

import openpyxl

# Excel 檔案名稱（與此 script 放同一目錄，或改成絕對路徑）
excel_file = '漢字閩南語標音【台羅拼音】.xlsx'

# 1. 載入活頁簿
wb = openpyxl.load_workbook(excel_file)

# 2. 解析規則表，建立 mapping 字典
rules_ws = wb['台羅轉換注音二式規則']

# 2.1 找到 header 列（第一個包含「台羅拼音」字樣的那一列）
header_row = None
for row in rules_ws.iter_rows(min_row=1, max_row=20):
    if any(cell.value == '台羅拼音' for cell in row):
        header_row = row[0].row
        break
if header_row is None:
    raise RuntimeError('在「台羅轉換注音二式規則」裡找不到欄位標頭「台羅拼音」')

# 2.2 讀出 header 那列所有欄位，找出「台羅拼音」與「注音二式」的欄編號
col_idx = {}
for cell in rules_ws[header_row]:
    if cell.value in ('台羅拼音', '注音二式'):
        col_idx[cell.value] = cell.column  # 1-based

if '台羅拼音' not in col_idx or '注音二式' not in col_idx:
    raise RuntimeError('規則表缺少「台羅拼音」或「注音二式」欄')

tl_col_idx  = col_idx['台羅拼音']
bpm2_col_idx = col_idx['注音二式']

# 2.3 逐列讀取 mapping
mapping = {}
for row in rules_ws.iter_rows(min_row=header_row+1, max_row=rules_ws.max_row):
    tl = row[tl_col_idx-1].value
    bp = row[bpm2_col_idx-1].value
    if tl and bp:
        tl = str(tl).strip()
        bp = str(bp).strip()
        mapping[tl] = bp

# （可選）印出映射數量，確認有多少筆
print(f'共讀取 {len(mapping)} 筆對應規則')

# 3. 處理 tl_ji_khoo_phing 表
data_ws = wb['tl_ji_khoo_phing']

# 3.1 假設 header 在第一列，取出欄位編號
header = next(data_ws.iter_rows(min_row=1, max_row=1))
data_cols = {cell.value: cell.column for cell in header}

if '台羅拼音' not in data_cols or '注音二式' not in data_cols:
    raise RuntimeError('資料表「tl_ji_khoo_phing」缺少「台羅拼音」或「注音二式」欄')

data_tl_col   = data_cols['台羅拼音']
data_bpm2_col = data_cols['注音二式']

# 3.2 逐列轉換：從第 2 列到最後一列
for row in data_ws.iter_rows(min_row=2, max_row=data_ws.max_row):
    cell_tl   = row[data_tl_col-1]
    cell_dest = row[data_bpm2_col-1]
    val = cell_tl.value
    key = str(val).strip() if val is not None else ''
    cell_dest.value = mapping.get(key, '')

# 4. 儲存回原檔
wb.save(excel_file)
print('✅ 轉換完成，只修改「tl_ji_khoo_phing」的注音二式欄，並已儲存回原檔。')
