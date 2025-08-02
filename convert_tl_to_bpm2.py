#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convert_tl_to_bpm2.py

功能：
  1. 讀取「漢字閩南語標音【台羅拼音】.xlsx」同一支活頁簿
  2. 從「台羅轉換注音二式規則」表解析聲母、韻母對應
  3. 定義 oo／o 韻母的特殊 override 規則（發 [ɔ] 與發 [o] 區別）
  4. 逐列讀「tl_ji_khoo_phing」工作表，把「台羅拼音」轉成「注音二式」
     – 若未成功轉換，會在「訂正說明」欄寫入缺規則
  5. 儲存回同一支活頁簿，其餘工作表與格式不受影響
"""

import re

import openpyxl

# 檔名放在同目錄或自行改成絕對路徑
excel_file = '漢字閩南語標音【台羅拼音】.xlsx'

# 1. 載入活頁簿
wb = openpyxl.load_workbook(excel_file)

# 2. 解析「台羅轉換注音二式規則」表
rules_ws = wb['台羅轉換注音二式規則']

# 2.1 找到標頭列：第一個出現「台羅拼音」的列
header_row = None
for row in rules_ws.iter_rows(min_row=1, max_row=20):
    if any(cell.value == '台羅拼音' for cell in row):
        header_row = row[0].row
        break
if header_row is None:
    raise RuntimeError('規則表無法找到「台羅拼音」欄位標頭')

# 2.2 取得「台羅拼音」「注音二式」「音標種類」三欄的欄號
cols = {cell.value: cell.column for cell in rules_ws[header_row]}
tl_col_idx   = cols['台羅拼音']
bpm2_col_idx = cols['注音二式']
kind_col_idx = cols['音標種類']

# 2.3 建立聲母與韻母對應字典
initial_map = {}
final_map   = {}
for r in rules_ws.iter_rows(min_row=header_row+1, max_row=rules_ws.max_row):
    key  = r[tl_col_idx-1].value
    val  = r[bpm2_col_idx-1].value
    kind = r[kind_col_idx-1].value
    if key and val and kind:
        k = str(key).strip()
        v = str(val).strip()
        if str(kind).strip() == '聲母':
            initial_map[k] = v
        elif str(kind).strip() == '韻母':
            final_map[k] = v

# 2.4 為 Longest‐match，將聲母鍵依長度由大到小排序
initial_keys = sorted(initial_map.keys(), key=len, reverse=True)

# 3. 定義 oo ／ o 的特殊 override 規則
final_override_map = {
    # 發 [ɔ] 的 oo 群
    'oo':  'oo',   'onn':  'oonnh', 'ooh':  'ooh',  'onnh': 'oonnh',
    'om':  'oom',  'ong':  'ong',   'op':   'oop',  'ok':   'ook',
    'ioo': 'ioo',  'ionn': 'ioonn','iooh':'iooh','iong': 'iong','iok':'iook',
    # 發 [o] 的 o 群
    'o':   'or',   'oh':   'orh',  'io':  'ior',  'ioh':  'iorh',
}

# 4. 定義轉換函式
def convert_one(syl):
    """將單音節台羅（如 'hiaunn2'）拆 init+final+tone，並轉成注音二式拼音字母＋數字聲調。"""
    if syl is None:
        return ''
    s = str(syl).strip()
    # 4.1 把尾端一位數字的聲調分離
    m = re.match(r'^(.+?)([0-9])$', s)
    body, tone = (m.group(1), m.group(2)) if m else (s, '')

    # 4.2 找最長匹配聲母
    init = ''
    for k in initial_keys:
        if body.startswith(k):
            init = k
            break
    finals = body[len(init):]

    # 4.3 聲母對應
    init_p = initial_map.get(init, init)

    # 4.4 韻母 override → 規則表 → fallback
    if finals in final_override_map:
        final_p = final_override_map[finals]
    else:
        final_p = final_map.get(finals, finals)

    # 4.5 debug 訊息：指明哪邊沒對到
    missing = []
    if init not in initial_map:
        missing.append('聲母未轉換')
    if finals not in final_override_map and finals not in final_map:
        missing.append('韻母未轉換')
    if missing:
        note = '、'.join(missing)
        print(f'⚠️ {note}：{s} → init:{init}->{init_p}, final:{finals}->{final_p}, tone:{tone}')

    return init_p + final_p + tone

# 5. 處理「tl_ji_khoo_phing」工作表
ws = wb['tl_ji_khoo_phing']
# 5.1 取 header
hdr = next(ws.iter_rows(min_row=1, max_row=1))
header_cols = {cell.value: cell.column for cell in hdr}
if '台羅拼音' not in header_cols or '注音二式' not in header_cols:
    raise RuntimeError('tl_ji_khoo_phing 表缺少「台羅拼音」或「注音二式」欄')
src_col  = header_cols['台羅拼音']
dst_col  = header_cols['注音二式']

# 5.2 「訂正說明」欄：若不存在就新增
if '訂正說明' not in header_cols:
    note_col = ws.max_column + 1
    ws.cell(row=1, column=note_col, value='訂正說明')
else:
    note_col = header_cols['訂正說明']

# 5.3 逐列轉換：從第2列到最後一列
for r in range(2, ws.max_row + 1):
    src = ws.cell(row=r, column=src_col).value
    res = convert_one(src)
    ws.cell(row=r, column=dst_col, value=res)
    if not res:
        ws.cell(row=r, column=note_col,
                value=f'缺規則：{src}')

# 6. 儲存回原檔
wb.save(excel_file)
print('✅ 轉換完成：所有列已處理，「注音二式」與「訂正說明」皆已更新並儲存回原檔。')
