#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import xlwings as xw

# ========= 使用者可調整 =========
SHEET_NAME    = "韻母轉換"
SOURCE_RANGE  = "A2:A85"          # 第一個迴圈的資料來源
# PIPELINE      = [1, 2, 3, 4, 5]   # 要按順序執行的規則組，可自由擴充
PIPELINE      = [1, 2, 3]   # 要按順序執行的規則組，可自由擴充

# 僅在這些組別「限定字尾」比對（自動加上 $）
SUFFIX_ONLY_GROUPS = {4, 5}

# 這些組別的 pattern 視為「正規式」原樣使用（不 re.escape、不自動加 $）
REGEX_GROUPS = {3}

# 各組替換規則（大小寫有區分）
# 注意：第1/5組不要自己加 $，程式會自動加；第4組可用正規式（^...$）
MAPPING_GROUPS = {
    1: [
        ("iong", "iOW"),
        ("iooh", "iOh"),
        ("nooh", "nOh"),
        ("ooh",  "Oh"),
        ("iok",  "iOk"),
        ("oo",   "O"),
        ("ong",  "OW"),
        ("op",   "Op"),
        ("ok",   "Ok"),
        ("oM",   "OM"),
    ],
    2: [
        ("ai", "x"),
        ("ao", "y"),    # ao
        ("am", "V"),    # am
        ("an", "@"),    # an
    ],
    3: [
        ("^nO$", "Q"),
        ("^nx$", "X"),
        ("^ny$", "Y"),
        ("^ni$", "I"),
        ("^nu$", "U"),
        ("^na$", "A"),
        ("^ne$", "E"),
    ],
    4: [
        # ("aW", "P"),    # ang
        ("iang", "iaW"),
        ("ng", "W"),
        ("n",  "N"),
        ("m",  "M"),
    ],
    # 5: [
    #     ("p", "r"),
    #     ("t", "f"),
    #     ("k", "q"),
    #     ("h", "v"),
    # ],
}

# ========= 核心函式 =========
def build_regex_pairs(group_id, group_rules):
    """
    將 (pattern, repl) 轉為 regex：
    - 長字串優先（避免 'ng' 被 'n' 先吃掉）
    - group 在 SUFFIX_ONLY_GROUPS：字面比對並自動加 '$'（只吃尾端）
    - group 在 REGEX_GROUPS：pattern 視為正規式原樣使用（^...$ 可生效）
    - 其餘組：做「字形等價」的字面子字串比對：
        * 'a' -> '[aɑ]'（同時吃 ASCII a 與 ɑ U+0251）
        * 'g' -> '[gɡ]'（同時吃 ASCII g 與 ɡ U+0261）
      其餘字元做 re.escape
    """
    # 依原始 pattern 長度排序（穩定排序，長字串優先）
    sorted_rules = sorted(group_rules, key=lambda kv: len(kv[0]), reverse=True)

    def escape_with_equiv(pat: str) -> str:
        out = []
        for ch in pat:
            if ch == "a":
                out.append("[aɑ]")   # a or ɑ
            elif ch == "g":
                out.append("[gɡ]")   # g or ɡ
            else:
                out.append(re.escape(ch))
        return "".join(out)

    pairs = []
    suffix_only = group_id in SUFFIX_ONLY_GROUPS
    regex_mode  = group_id in REGEX_GROUPS

    for pat, repl in sorted_rules:
        if regex_mode:
            pattern = pat  # 使用者提供的是正規式（如 ^...$）
        else:
            pattern = escape_with_equiv(pat)
            if suffix_only:
                pattern += r"$"  # 只比對字尾
        rx = re.compile(pattern)
        pairs.append((rx, repl))
    return pairs

def apply_one_group_once(text, group_id):
    """
    單一組規則：命中第一條就替換一次（避免連鎖意外），否則原樣返回。
    """
    rules = MAPPING_GROUPS.get(group_id, [])
    for rx, repl in build_regex_pairs(group_id, rules):
        if rx.search(text):
            return rx.sub(repl, text, count=1)
    return text

def next_column(col_idx, steps=1):
    return col_idx + steps

def apply_pipeline_column_by_column(sheet, source_range_addr, pipeline):
    """
    每一組一個迴圈，逐欄輸出：
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

        src_addr = sheet.range((first_row, current_src_col), (last_row, current_src_col)).address
        dst_addr = sheet.range((first_row, dst_col), (last_row, dst_col)).address

        src_vals = sheet.range(src_addr).value
        if not isinstance(src_vals, list):
            src_vals = [src_vals]
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
            out_vals.append(apply_one_group_once(s, gid))

        sheet.range(dst_addr).value = [[x] for x in out_vals]

        print(f"第 {i} 個迴圈（組 {gid}）：{src_addr} -> {dst_addr}")
        current_src_col = dst_col  # 下一組的來源改成這一組的目的欄

# ========= 執行 =========
wb = xw.apps.active.books.active
sheet = wb.sheets[SHEET_NAME]

apply_pipeline_column_by_column(sheet, SOURCE_RANGE, PIPELINE)

print("全部完成 ✅")
