#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
p130_匯出字典.py

自 SQLite【台語注音二式字典】匯出新中州韻字典檔：ji_khoo_bpm2_new.dict.yaml。

欄位對映：
  漢字     → text
  漢字標音 → code
  常用度   → weight
  摘要說明 → stem
  時間戳記 → create

參考：docs/510_台語注音二式字典重整.md

使用方式：
  python tools/p130_匯出字典.py
  python tools/p130_匯出字典.py --db src/台語注音二式字典.db
  python tools/p130_匯出字典.py --out ji_khoo_bpm2_new.dict.yaml
  python tools/p130_匯出字典.py --selftest
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from bpm2_ji_tian_db import DEFAULT_DB, connect, init_db, table_exists  # noqa: E402

DEFAULT_OUT = ROOT / "ji_khoo_bpm2_new.dict.yaml"
DICT_NAME = "ji_khoo_bpm2"
DICT_VERSION = "v0.1.0"


def build_header(name: str = DICT_NAME, version: str = DICT_VERSION) -> str:
    return (
        "# Rime dictionary\n"
        "# encoding: utf-8\n"
        "#\n"
        "# 台語注音二式字典（重整後）\n"
        "#\n"
        "---\n"
        f"name: {name}\n"
        f'version: "{version}"\n'
        "sort: by_weight\n"
        "use_preset_vocabulary: false\n"
        "columns:\n"
        "  - text #漢字／詞彙\n"
        "  - code #漢字標音（台語注音二式）\n"
        "  - weight #常用度（優先顯示度）\n"
        "  - stem #用法舉例\n"
        "  - create #時間戳記\n"
        "...\n"
        "#漢字\t漢字標音\t常用度\t用法舉例\t時間戳記\n"
    )


def format_weight(weight) -> str:
    try:
        w = float(weight)
    except (TypeError, ValueError):
        w = 0.1
    return f"{w:.2f}"


def format_create(value) -> str:
    if value is None:
        return ""
    s = str(value).strip()
    if len(s) >= 16 and s[4] == "-" and s[10] == " ":
        return s[:16]
    return s


def fetch_all(db_path: Path) -> list[tuple]:
    conn = connect(db_path)
    try:
        if not table_exists(conn):
            sys.exit(f"✗ 資料庫尚無【漢字庫】資料表，請先執行 p110／p120：{db_path}")
        rows = conn.execute(
            """
            SELECT 漢字, 漢字標音, 常用度, 摘要說明, 時間戳記
              FROM 漢字庫
             ORDER BY 漢字 COLLATE BINARY, 漢字標音 COLLATE BINARY, 識別號
            """
        ).fetchall()
        return [
            (
                r["漢字"],
                r["漢字標音"],
                r["常用度"],
                r["摘要說明"] if r["摘要說明"] is not None else "NA",
                r["時間戳記"],
            )
            for r in rows
        ]
    finally:
        conn.close()


def export_dict(db_path: Path, out_path: Path) -> int:
    rows = fetch_all(db_path)
    lines = [build_header()]
    for text, code, weight, stem, create in rows:
        lines.append(
            f"{text}\t{code}\t{format_weight(weight)}\t{stem}\t{format_create(create)}"
        )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        "".join(line if line.endswith("\n") else line + "\n" for line in lines),
        encoding="utf-8",
    )
    return len(rows)


def selftest() -> int:
    import tempfile

    ok = True

    def check(desc, got, exp):
        nonlocal ok
        mark = "OK  " if got == exp else "FAIL"
        if got != exp:
            ok = False
        print(f"{mark} {desc}: {got!r} (expect {exp!r})")

    check("weight 0.8 → 0.80", format_weight(0.8), "0.80")
    check("create 截斷", format_create("2026-07-05 21:19:00"), "2026-07-05 21:19")
    check("header 含 name", "name: ji_khoo_bpm2" in build_header(), True)

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        db = Path(tmp) / "t.db"
        out = Path(tmp) / "out.dict.yaml"
        init_db(db)
        conn = connect(db)
        try:
            conn.execute(
                "INSERT INTO 漢字庫 (漢字, 漢字標音, 常用度, 摘要說明, 時間戳記) "
                "VALUES (?, ?, ?, ?, ?)",
                ("不", "but4", 0.10, "NA", "2026-01-02 22:51:07"),
            )
            conn.execute(
                "INSERT INTO 漢字庫 (漢字, 漢字標音, 常用度, 摘要說明, 時間戳記) "
                "VALUES (?, ?, ?, ?, ?)",
                ("人", "lang5", 0.60, "【12996】大人.", "2026-07-05 21:19:00"),
            )
            conn.commit()
        finally:
            conn.close()
        n = export_dict(db, out)
        text = out.read_text(encoding="utf-8")
        check("匯出筆數", n, 2)
        check(
            "含 but4",
            "不\tbut4\t0.10\tNA\t2026-01-02 22:51" in text,
            True,
        )
        check(
            "含 lang5",
            "人\tlang5\t0.60\t【12996】大人.\t2026-07-05 21:19" in text,
            True,
        )
        check("無 [ptkh]1", bool(re_search_bad(text)), False)

    print("ALL PASS" if ok else "SOME FAILED")
    return 0 if ok else 1


def re_search_bad(text: str) -> bool:
    import re

    return re.search(r"[ptkh]1\t", text) is not None


def main() -> None:
    ap = argparse.ArgumentParser(description="台語注音二式字典 → 中州韻字典檔")
    ap.add_argument("--db", default=str(DEFAULT_DB), help="SQLite 資料庫路徑")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="輸出 .dict.yaml 路徑")
    ap.add_argument("--selftest", action="store_true", help="僅執行自我測試")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    db_path = Path(args.db)
    out_path = Path(args.out)
    if not db_path.is_file():
        sys.exit(f"✗ 找不到資料庫：{db_path}（請先執行 p110／p120）")

    print(f"開啟資料庫：{db_path}")
    n = export_dict(db_path, out_path)
    print(f"✓ 完成：匯出 {n} 筆 → {out_path}")


if __name__ == "__main__":
    main()
