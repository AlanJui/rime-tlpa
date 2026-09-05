#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
convert_kam_ji_tian_to_rime_dict.py

功能：
  依《410_甘字典轉換指引.md》規格，將 Excel 活頁簿
  【甘字典】ChhoeTaigi_KamJitian.xlsx 之【甘字典】工作表，
  轉換後寫入【RIME】工作表（text / code / weight / stem / create）。

來源欄位（【甘字典】工作表）：
  A：DictWordID        字典識別碼
  D：HanLoTaibunPoj    漢字
  H：KaisoehHanLoPoj   漢字解釋（漢羅混寫白話字）
  J：KipInput          白話音／文白同音之台羅標音
  L：HanbunImKipInput  文讀音台羅標音

轉換規則：
  1. text   = D 欄漢字（空值或「-」者，整列略過）
  2. code   = J 欄（及 L 欄，若有值則另立一筆）之台羅拼音
       - 一律轉為小寫
       - 補全調號：音節結尾非數字時，
           韻尾屬 [ptkh] → 補調號 4（陰入調）
           其餘         → 補調號 1（陰平調）
  3. weight = 依音節首字母大小寫判讀：
       - 首字母大寫 → 文讀音 → 0.80
       - 首字母小寫 → 白話音 → 0.60
  4. stem   = 【<DictWordID>】<KaisoehHanLoPoj>
  5. create = 程式執行時刻，格式 yyyy-mm-dd hh:mm

使用方式：
  # 1) 純邏輯自我測試（不需 Excel / xlwings）
  python tools/convert_kam_ji_tian_to_rime_dict.py --selftest

  # 2) 對預設檔案執行轉換（需安裝 xlwings、且本機有 Excel）
  python tools/convert_kam_ji_tian_to_rime_dict.py

  # 3) 指定其他 xlsx
  python tools/convert_kam_ji_tian_to_rime_dict.py "C:/path/to/your.xlsx"

  # 4) 轉換完同時匯出 RIME .dict.yaml（選用）
  python tools/convert_kam_ji_tian_to_rime_dict.py --yaml ji_khoo_kam_ji_tian.dict.yaml
"""

import argparse
import os
import sys
from datetime import datetime

# ──────────────────────────────────────────────────────────────────────────
# 參數設定
# ──────────────────────────────────────────────────────────────────────────
DEFAULT_XLSX = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "src",
    "【甘字典】ChhoeTaigi_KamJitian.xlsx",
)
SOURCE_SHEET = "【甘字典】"
TARGET_SHEET = "RIME"
START_ROW = 2                 # 資料起始列（第 1 列為標題）

WEIGHT_BUN = 0.80             # 文讀音
WEIGHT_PEH = 0.60             # 白話音

TONE_DIGITS = set("0123456789")
PTKH = set("ptkh")


# ──────────────────────────────────────────────────────────────────────────
# 核心轉換邏輯（純函式，不依賴 Excel，便於測試）
# ──────────────────────────────────────────────────────────────────────────
def complete_tone(syllable: str) -> str:
    """補全調號：陰平調（1）與陰入調（4）省略者補回。"""
    s = syllable.strip()
    if not s:
        return s
    if s[-1] in TONE_DIGITS:      # 已有調號，原樣保留
        return s
    if s[-1] in PTKH:             # 韻尾為 p/t/k/h → 陰入調 4
        return s + "4"
    return s + "1"                # 否則 → 陰平調 1


def to_code(tailo: str) -> str:
    """台羅標音 → code 欄值：小寫化＋補全調號。"""
    return complete_tone(str(tailo).strip().lower())


def to_weight(tailo: str) -> float:
    """依首字母大小寫判讀文讀（0.80）／白話（0.60）。"""
    s = str(tailo).strip()
    return WEIGHT_BUN if s and s[0].isupper() else WEIGHT_PEH


def convert_row(dict_word_id, text, kaisoeh, kip_input, hanbun_im) -> list[tuple]:
    """
    將來源一列轉為 0~2 筆 RIME 紀錄 (text, code, weight, stem)。
    - text 空值、「-」或「?」：略過（回傳空 list）
    - J 欄（kip_input）一筆；L 欄（hanbun_im）有值再一筆
    - 同列 code 重複者只留一筆
    """
    t = "" if text is None else str(text).strip()
    if not t or t in ("-", "?", "？"):
        return []

    wid = "" if dict_word_id is None else str(dict_word_id).strip()
    if wid.endswith(".0"):                     # Excel 數值可能帶 .0
        wid = wid[:-2]
    k = "" if kaisoeh is None else str(kaisoeh).strip()
    stem = f"【{wid}】{k}"

    records, seen = [], set()
    for raw in (kip_input, hanbun_im):
        if raw is None or str(raw).strip() == "":
            continue
        code = to_code(raw)
        if code in seen:
            continue
        seen.add(code)
        records.append((t, code, to_weight(raw), stem))
    return records


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
    book = xw.Book(xlsx_path)                  # 若已在 Excel 開啟則自動接上
    try:
        src = book.sheets[SOURCE_SHEET]
    except Exception:
        sys.exit(f"✗ 找不到來源工作表：{SOURCE_SHEET}")
    try:
        dst = book.sheets[TARGET_SHEET]
    except Exception:
        dst = book.sheets.add(TARGET_SHEET, after=src)
        print(f"（新建標的工作表：{TARGET_SHEET}）")

    # 以 A 欄（DictWordID）偵測資料末列
    last_row = src.range("A1").end("down").row
    if last_row < START_ROW:
        sys.exit("✗ 來源工作表無資料可轉換。")
    n = last_row - START_ROW + 1
    print(f"來源工作表：{SOURCE_SHEET}，資料列：{START_ROW}~{last_row}（共 {n} 列）")

    # 分批讀取 A~L 欄並轉換，於同一列回報處理進度
    create_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    out, skipped = [], 0
    CHUNK = 1000
    for chunk_start in range(START_ROW, last_row + 1, CHUNK):
        chunk_end = min(chunk_start + CHUNK - 1, last_row)
        rows = src.range(f"A{chunk_start}:L{chunk_end}").value
        if chunk_start == chunk_end:
            rows = [rows]
        for i, row in enumerate(rows):
            # A=0, D=3, H=7, J=9, L=11
            recs = convert_row(row[0], row[3], row[7], row[9], row[11])
            if not recs:
                skipped += 1
            for text, code, weight, stem in recs:
                out.append([text, code, weight, stem, create_str])
        print(f"\r目前處理 row no：{chunk_end}/{last_row}", end="", flush=True)
    print()  # 進度列結束，換行

    # 清除標的工作表舊資料後，批次寫入
    print("寫入標的工作表中…", flush=True)
    dst.clear_contents()
    dst.range("A1").value = ["text", "code", "weight", "stem", "create"]
    if out:
        dst.range(f"A{START_ROW}").value = out
    print("存檔中…", flush=True)
    book.save()
    print(f"✓ 完成：來源 {n} 列 → 寫入 {len(out)} 筆（略過無漢字 {skipped} 列），已存檔。")

    if yaml_out:
        export_rime_yaml(out, yaml_out)


def export_rime_yaml(records: list[list], yaml_out: str) -> None:
    """選用：依模版另存一份 RIME .dict.yaml。"""
    header = (
        "# Rime dictionary\n"
        "# encoding: utf-8\n"
        "#\n"
        "# 台語白話音日常辭庫\n"
        "#\n"
        "---\n"
        "name: ji_khoo_kam_ji_tian\n"
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
    lines = [header]
    for text, code, weight, stem, create in records:
        lines.append(f"{text}\t{code}\t{weight:.2f}\t{stem}\t{create}")
    with open(yaml_out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"✓ 已匯出 RIME 字典：{yaml_out}")


# ──────────────────────────────────────────────────────────────────────────
# 自我測試
# ──────────────────────────────────────────────────────────────────────────
def selftest() -> int:
    ok = True

    def check(desc, got, exp):
        nonlocal ok
        mark = "OK  " if got == exp else "FAIL"
        if got != exp:
            ok = False
        print(f"{mark} {desc}: {got!r} (expect {exp!r})")

    # code：小寫化＋補全調號
    check("Un5 → code", to_code("Un5"), "un5")
    check("goo7 → code", to_code("goo7"), "goo7")
    check("Ngoo2 → code", to_code("Ngoo2"), "ngoo2")
    check("a → code（補陰平）", to_code("a"), "a1")
    check("ak → code（補陰入）", to_code("ak"), "ak4")
    check("Sip → code（補陰入）", to_code("Sip"), "sip4")
    check("ann → code（補陰平）", to_code("ann"), "ann1")

    # weight：首字母大小寫判讀
    check("Un5 → weight", to_weight("Un5"), WEIGHT_BUN)
    check("goo7 → weight", to_weight("goo7"), WEIGHT_PEH)

    # convert_row：整列轉換
    check(
        "云（僅 J 欄，文讀）",
        convert_row(25121, "云", "山川 ê 氣, 雲霧.", "Un5", None),
        [("云", "un5", WEIGHT_BUN, "【25121】山川 ê 氣, 雲霧.")],
    )
    check(
        "五（J＋L 兩欄 → 兩筆）",
        convert_row(4478, "五", "五月, 五穀.", "goo7", "Ngoo2"),
        [
            ("五", "goo7", WEIGHT_PEH, "【4478】五月, 五穀."),
            ("五", "ngoo2", WEIGHT_BUN, "【4478】五月, 五穀."),
        ],
    )
    check("無漢字（-）→ 略過", convert_row(15, "-", "a-ka.", "a", None), [])
    check("無漢字（?）→ 略過", convert_row(15, "?", "a-ka.", "a", None), [])
    check("無漢字（全形？）→ 略過", convert_row(15, "？", "a-ka.", "a", None), [])
    check("漢字空值 → 略過", convert_row(15, None, "a-ka.", "a", None), [])
    check(
        "同列 J/L 同音 → 只留一筆",
        convert_row(1, "水", "解說.", "Sui2", "sui2"),
        [("水", "sui2", WEIGHT_BUN, "【1】解說.")],
    )
    check(
        "DictWordID 帶 .0 → 去除",
        convert_row(1440.0, "井", "水堀 ê 空.", "Tsing2", None),
        [("井", "tsing2", WEIGHT_BUN, "【1440】水堀 ê 空.")],
    )

    print("ALL PASS" if ok else "SOME FAILED")
    return 0 if ok else 1


# ──────────────────────────────────────────────────────────────────────────
# 進入點
# ──────────────────────────────────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(description="【甘字典】→ RIME 字典（RIME 工作表）轉換")
    ap.add_argument("xlsx", nargs="?", default=DEFAULT_XLSX, help="輸入 .xlsx（預設為專案 src 內檔案）")
    ap.add_argument("--yaml", metavar="OUT", help="同時匯出 RIME .dict.yaml")
    ap.add_argument("--selftest", action="store_true", help="僅執行純邏輯自我測試（不需 Excel）")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    run_convert(args.xlsx, args.yaml)


if __name__ == "__main__":
    main()
