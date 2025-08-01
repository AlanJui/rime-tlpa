#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
convert_tl_to_bpm2_openpyxl.py

功能：
  1. 讀取同一支 Excel（漢字閩南語標音【台羅拼音】.xlsx）
  2. 解析「台羅轉換注音二式規則」工作表，建立台羅音節的子項（聲母、韻母）→注音二式片段的對應字典
  3. 讀取「tl_ji_khoo_phing」工作表，把「台羅拼音」欄切割成  (聲母 + 韻母 + 聲調)，
     分別對應再組回「注音二式」字串
  4. 只儲存回原檔，其餘工作表與格式不變
"""

import re

import openpyxl

# 1. 載入活頁簿
excel_file = '漢字閩南語標音【台羅拼音】.xlsx'
wb = openpyxl.load_workbook(excel_file)

# 2. 解析規則表，建立 mapping
rules_ws = wb['台羅轉換注音二式規則']

# 2.1 找 header 列（第一列出現「台羅拼音」）
header_row = None
for row in rules_ws.iter_rows(min_row=1, max_row=20):
    if any(cell.value == '台羅拼音' for cell in row):
        header_row = row[0].row
        break
if header_row is None:
    raise RuntimeError('找不到「台羅拼音」欄位標頭')

# 2.2 抓出「台羅拼音」與「注音二式」兩欄的欄號
col_idx = {}
for cell in rules_ws[header_row]:
    if cell.value in ('台羅拼音', '注音二式'):
        col_idx[cell.value] = cell.column  # openpyxl 1-based

if '台羅拼音' not in col_idx or '注音二式' not in col_idx:
    raise RuntimeError('規則表缺少「台羅拼音」或「注音二式」欄')

tl_col_idx   = col_idx['台羅拼音']
bpm2_col_idx = col_idx['注音二式']

# 2.3 讀 mapping：只要聲母或韻母片段不為空，就建立字典
mapping = {}
for row in rules_ws.iter_rows(min_row=header_row+1, max_row=rules_ws.max_row):
    k = row[tl_col_idx-1].value
    v = row[bpm2_col_idx-1].value
    if k and v:
        k = str(k).strip()
        v = str(v).strip()
        mapping[k] = v

print(f'>>> 共建立 {len(mapping)} 筆子項對應規則')

# 2.4 為了拆聲母，我們把所有 mapping key 依長度由大到小排序
map_keys_sorted = sorted(mapping.keys(), key=lambda x: len(x), reverse=True)

# 3. 處理 tl_ji_khoo_phing 表
data_ws = wb['tl_ji_khoo_phing']

# 3.1 找 header row（假設在第 1 列）
header = next(data_ws.iter_rows(min_row=1, max_row=1))
data_cols = {cell.value: cell.column for cell in header}
if '台羅拼音' not in data_cols or '注音二式' not in data_cols:
    raise RuntimeError('資料表缺少「台羅拼音」或「注音二式」欄')

data_tl_col   = data_cols['台羅拼音']
data_bpm2_col = data_cols['注音二式']

def convert_syllable(tl_syl: str) -> str:
    """將 tl_syl（如 'kau2'）拆成 聲母/韻母/聲調，分別對應後再組合回去。"""
    if not tl_syl:
        return ''
    s = str(tl_syl).strip()
    # 分離尾端的數字聲調
    m = re.match(r'^([a-z]+?)([0-9])$', s)
    if m:
        body, tone = m.group(1), m.group(2)
    else:
        body, tone = s, ''

    # 找出最長匹配的聲母（mapping key）
    init = ''
    for k in map_keys_sorted:
        if body.startswith(k):
            init = k
            break
    finals = body[len(init):]  # 剩下就是韻母
    # 對應
    init_mapped  = mapping.get(init, '')
    final_mapped = mapping.get(finals, '') if finals else ''

    return init_mapped + final_mapped + tone

# 3.2 逐列寫回
for row in data_ws.iter_rows(min_row=2, max_row=data_ws.max_row):
    src = row[data_tl_col-1].value
    result = convert_syllable(src)
    row[data_bpm2_col-1].value = result
    # 可以開 debug
    print(f'{src} → {result}')

# 4. 儲存回原檔
wb.save(excel_file)
print('✅ 轉換完成，已寫回「注音二式」欄，並儲存回原檔。')
