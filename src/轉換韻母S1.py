#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import xlwings as xw

# ========= 使用者可調整 =========
SHEET_NAME    = "韻母轉換"
SOURCE_RANGE  = "A2:A85"     # 第一個迴圈的資料來源
PIPELINE      = [1, 2, 3, 4, 5]    # 要按順序執行的規則組，可自由擴充，例如 [1,2,3,4,5]

# 各組替換規則（只會比對「字尾」；自動做長字串優先）
# 可自由增刪、改寫；大小寫有區分
MAPPING_GROUPS = {
    1: [
        ("ng$", "W"),
        ("n$",  "N"),
        ("m$",  "M"),
    ],
    2: [
        ("ioW", "iOW"),
        ("iooh", "iOh"),
        ("nooh", "nOh"),
        ("ooh",  "Oh"),
        ("iok",  "iOk"),
        ("oo",   "O"),
        ("oW",   "OW"),  # 注意大小寫
        ("op",   "Op"),
        ("ok",   "Ok"),
        ("om",   "Om"),
    ],
    3: [
        ("aW", "P"),
        ("ai", "x"),
        ("ao", "y"),
        ("am", "V"),
        ("an", "@"),
    ],
    4: [
        ("nO", "Q"),
        ("nx", "X"),
        ("ny", "Y"),
        ("ni", "I"),
        ("nu", "U"),
        ("na", "A"),
        ("ne", "E"),
    ],
    5: [
        ("p$", "r"),
        ("t$", "f"),
        ("k$", "q"),
        ("h$", "v"),
    ],
}

# ========= 核心函式 =========
def build_regex_pairs(group_rules):
    """將 (pattern, repl) 轉為只比對字尾的 regex，並依 pattern 長度由長到短排序。"""
    sorted_rules = sorted(group_rules, key=lambda kv: len(kv[0]), reverse=True)
    pairs = []
    for pat, repl in sorted_rules:
        rx = re.compile(re.escape(pat) + r"$")  # 僅字尾
        pairs.append((rx, repl))
    return pairs

def apply_one_group_once(text, group_id):
    """
    對單一組規則做「一次替換」：
    依長字串優先逐條測試，命中第一條就替換並返回；未命中則原樣返回。
    """
    rules = MAPPING_GROUPS.get(group_id, [])
    for rx, repl in build_regex_pairs(rules):
        if rx.search(text):
            return rx.sub(repl, text, count=1)
    return text

def next_column(col_idx, steps=1):
    """傳回往右 steps 欄的欄號（1-based）。"""
    return col_idx + steps

def apply_pipeline_column_by_column(sheet, source_range_addr, pipeline):
    """
    逐組迴圈、逐欄輸出：
      第1組：來源 = SOURCE_RANGE，目的 = 往右一欄
      第2組：來源 = 上一組目的欄，目的 = 再往右一欄
      ...
    """
    src_rng = sheet.range(source_range_addr)
    first_row = src_rng.row
    last_row  = src_rng.last_cell.row
    src_col   = src_rng.column

    current_src_col = src_col

    for i, gid in enumerate(pipeline, start=1):
        dst_col = next_column(current_src_col, 1)

        # 組出來源與目的 Range（同列數）
        src_addr = sheet.range((first_row, current_src_col), (last_row, current_src_col)).address
        dst_addr = sheet.range((first_row, dst_col), (last_row, dst_col)).address

        src_vals = sheet.range(src_addr).value  # 可能是 list(列) 或 單欄陣列
        # 統一成 Python list（逐列）
        if not isinstance(src_vals, list):
            src_vals = [src_vals]
        # 如果是 2D list（如 [[val],[val],...]），攤平成 1D
        if src_vals and isinstance(src_vals[0], list):
            src_vals = [row[0] for row in src_vals]

        out_vals = []
        for v in src_vals:
            if v is None:
                out_vals.append(None)
                continue
            s = str(v).strip()
            if not s:
                out_vals.append("")
                continue
            converted = apply_one_group_once(s, gid)
            out_vals.append(converted)

        # 寫回目的欄（以 2D 陣列形式一次寫入較快）
        sheet.range(dst_addr).value = [[x] for x in out_vals]

        print(f"第 {i} 個迴圈（組 {gid}）：{src_addr} -> {dst_addr}")
        current_src_col = dst_col  # 下一組的來源改成這一組的目的欄

# ========= 執行 =========
wb = xw.apps.active.books.active
sheet = wb.sheets[SHEET_NAME]

apply_pipeline_column_by_column(sheet, SOURCE_RANGE, PIPELINE)

print("全部完成 ✅")
