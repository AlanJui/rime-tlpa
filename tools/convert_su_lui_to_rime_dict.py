#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
convert_su_lui_to_rime_dict.py

功能：
  依《400_台羅拼音辭彙_轉換成RIME字典.md》規格，將 Excel 活頁簿
  【1956台灣白話基礎語句】ChhoeTaigi_TaioanPehoeKichhooGiku.xlsx 之
  RIME_Dict 工作表中，存放於【G 欄】（G2 起）的【台羅拼音辭彙】，
  經兩階轉換後，寫入相對映的【B 欄】（code）。

轉換規則：
  一階轉換（去除辭彙符號）：
      將辭彙符號「-」一律換成空白。
      （辭彙本身也可能已含空白，例如 "ki3 be7-tiau5"，故以空白統一切分音節。）
  二階轉換（補全調號）：
      將每個音節解構為 聲、韻、調。若【調】為空（音節結尾非數字）：
        - 若【韻】最後一個羅馬字母屬 [ptkh] 之一 → 調 = 4（陰入調）
        - 否則                                   → 調 = 1（陰平調）
      令每個音節皆「聲、韻、調」俱全。

  範例：
      i5-tiunn7        -> i5 tiunn7
      koo-tiunn7       -> koo1 tiunn7      （第1音節陽平省調，補回 1）
      a-tsik           -> a1 tsik4         （a 補 1；tsik 入聲補 4）
      ki3 be7-tiau5    -> ki3 be7 tiau5
      bin5-tsu2-tong2  -> bin5 tsu2 tong2
      beh8-a2-tsiu2    -> beh8 a2 tsiu2

設計規格：
  1. 程式語言：Python 3
  2. Excel 操作套件：xlwings（直接在已開啟的 Excel 上就地讀寫）
  3. 來源欄：G（SOURCE_COL）；目標欄：B（TARGET_COL）；工作表：RIME_Dict

使用方式：
  # 1) 純邏輯自我測試（不需 Excel / xlwings）
  python convert_su_lui_to_rime_dict.py --selftest

  # 2) 對預設檔案執行轉換（需安裝 xlwings、且本機有 Excel）
  python convert_su_lui_to_rime_dict.py

  # 3) 指定其他 xlsx
  python convert_su_lui_to_rime_dict.py "C:/path/to/your.xlsx"

  # 4) 轉換完同時匯出 RIME .dict.yaml（選用）
  python convert_su_lui_to_rime_dict.py --yaml ji_khoo_su_lui.dict.yaml
"""

import argparse
import os
import re
import sys

# ──────────────────────────────────────────────────────────────────────────
# 參數設定
# ──────────────────────────────────────────────────────────────────────────
DEFAULT_XLSX = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "src",
    "【1956台灣白話基礎語句】ChhoeTaigi_TaioanPehoeKichhooGiku.xlsx",
)
SHEET_NAME = "RIME_Dict"
SOURCE_COL = "G"      # 台羅拼音辭彙來源欄
TARGET_COL = "B"      # 轉換結果（code）目標欄
ANCHOR_COL = "A"      # 用以偵測資料末列的連續欄（text）
START_ROW = 2         # 資料起始列（第 1 列為標題）

TONE_DIGITS = set("0123456789")
PTKH = set("ptkhPTKH")


# ──────────────────────────────────────────────────────────────────────────
# 核心轉換邏輯（純函式，不依賴 Excel，便於測試）
# ──────────────────────────────────────────────────────────────────────────
def complete_one_syllable(syllable: str) -> str:
    """二階轉換：對單一音節補全調號。"""
    s = syllable.strip()
    if not s:
        return s
    if s[-1] in TONE_DIGITS:          # 已有調號，原樣保留
        return s
    if s[-1] in PTKH:                 # 韻尾為 p/t/k/h → 陰入調 4
        return s + "4"
    return s + "1"                    # 否則 → 陰平調 1


def convert_tailo(tailo: str) -> str:
    """將一個台羅拼音辭彙完成一階＋二階轉換。"""
    if tailo is None:
        return ""
    # 一階：辭彙符號「-」換成空白，再以任意空白切分音節
    text = str(tailo).replace("-", " ")
    parts = [p for p in re.split(r"\s+", text) if p]
    # 二階：逐音節補全調號後，以單一空白重組
    return " ".join(complete_one_syllable(p) for p in parts)


# ──────────────────────────────────────────────────────────────────────────
# Excel 處理（xlwings）
# ──────────────────────────────────────────────────────────────────────────
def run_convert(xlsx_path: str, yaml_out: str | None = None) -> None:
    try:
        import xlwings as xw
    except ImportError:
        sys.exit("✗ 未安裝 xlwings，請先執行：pip install xlwings")

    if not os.path.isfile(xlsx_path):
        sys.exit(f"✗ 找不到檔案：{xlsx_path}")

    print(f"開啟活頁簿：{xlsx_path}")
    book = xw.Book(xlsx_path)            # 若已在 Excel 開啟則自動接上
    try:
        try:
            sht = book.sheets[SHEET_NAME]
        except Exception:
            sys.exit(f"✗ 找不到工作表：{SHEET_NAME}")

        # 以 ANCHOR_COL（A 欄，text）偵測資料末列
        last_row = sht.range(f"{ANCHOR_COL}1").end("down").row
        if last_row < START_ROW:
            sys.exit("✗ 無資料可轉換。")
        n = last_row - START_ROW + 1
        print(f"工作表：{SHEET_NAME}，資料列：{START_ROW}~{last_row}（共 {n} 列）")

        # 一次批次讀取來源欄（較逐格快）
        src_rng = sht.range(f"{SOURCE_COL}{START_ROW}:{SOURCE_COL}{last_row}")
        src_vals = src_rng.value
        if not isinstance(src_vals, list):     # 只有一列時 xlwings 回傳純量
            src_vals = [src_vals]

        # 逐列轉換
        out_vals, converted, skipped = [], 0, 0
        for v in src_vals:
            if v is None or str(v).strip() == "":
                out_vals.append([None])
                skipped += 1
            else:
                out_vals.append([convert_tailo(v)])
                converted += 1

        # 一次批次寫回目標欄
        sht.range(f"{TARGET_COL}{START_ROW}:{TARGET_COL}{last_row}").value = out_vals
        book.save()
        print(f"✓ 完成：已轉換 {converted} 列，略過空白 {skipped} 列，寫入 {TARGET_COL} 欄並存檔。")

        if yaml_out:
            export_rime_yaml(sht, START_ROW, last_row, yaml_out)
    finally:
        # 不關閉活頁簿，保留給使用者檢視
        pass


def export_rime_yaml(sht, start_row: int, last_row: int, yaml_out: str) -> None:
    """選用：依模版另存一份 RIME .dict.yaml。"""
    header = (
        "# Rime dictionary\n"
        "# encoding: utf-8\n"
        "#\n"
        "# 台語白話音日常辭庫\n"
        "#\n"
        "---\n"
        "name: ji_khoo_su_lui\n"
        'version: "v0.1.0"\n'
        "sort: by_weight\n"
        "use_preset_vocabulary: false\n"
        "columns:\n"
        "  - text    # 漢字\n"
        "  - code    # 台灣音標（TLPA）拼音\n"
        "  - weight  # 常用度（優先顯示度）\n"
        "  - stem    # 用法舉例\n"
        "  - create  # 建立時間\n"
        "...\n"
    )
    rng = sht.range(f"A{start_row}:E{last_row}").value
    lines = [header]
    for row in rng:
        text, code, weight, stem, create = (list(row) + [None] * 5)[:5]
        if not text or not code:
            continue
        weight = "" if weight is None else weight
        stem = "" if stem is None else stem
        create = "" if create is None else create
        lines.append(f"{text}\t{code}\t{weight}\t{stem}\t{create}")
    with open(yaml_out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"✓ 已匯出 RIME 字典：{yaml_out}")


# ──────────────────────────────────────────────────────────────────────────
# 自我測試
# ──────────────────────────────────────────────────────────────────────────
def selftest() -> int:
    cases = [
        ("i5-tiunn7",       "i5 tiunn7"),
        ("koo-tiunn7",      "koo1 tiunn7"),
        ("a-tsik",          "a1 tsik4"),
        ("ki3 be7-tiau5",   "ki3 be7 tiau5"),
        ("bin5-tsu2-tong2", "bin5 tsu2 tong2"),
        ("beh8-a2-tsiu2",   "beh8 a2 tsiu2"),
        ("a-tsoo2",         "a1 tsoo2"),
    ]
    ok = True
    for src, exp in cases:
        got = convert_tailo(src)
        mark = "OK  " if got == exp else "FAIL"
        if got != exp:
            ok = False
        print(f"{mark} {src:18s} -> {got:20s} (expect {exp})")
    print("ALL PASS" if ok else "SOME FAILED")
    return 0 if ok else 1


# ──────────────────────────────────────────────────────────────────────────
# 進入點
# ──────────────────────────────────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(description="台羅拼音辭彙 → RIME 字庫（B 欄 code）轉換")
    ap.add_argument("xlsx", nargs="?", default=DEFAULT_XLSX, help="輸入 .xlsx（預設為專案 src 內檔案）")
    ap.add_argument("--yaml", metavar="OUT", help="同時匯出 RIME .dict.yaml")
    ap.add_argument("--selftest", action="store_true", help="僅執行純邏輯自我測試（不需 Excel）")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    run_convert(args.xlsx, args.yaml)


if __name__ == "__main__":
    main()
