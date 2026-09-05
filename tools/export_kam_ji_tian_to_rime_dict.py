#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
export_kam_ji_tian_to_rime_dict.py

功能：
  依《420_甘字典漢字庫指引.md》規格，自 SQLite【甘字典漢字庫】
  匯出中州韻字典子檔（ji_khoo_kam_ji_tian.dict.yaml）。

欄位對映：
  漢字     → text
  台羅音標 → code
  常用度   → weight
  摘要說明 → stem
  時間戳記 → create

使用方式：
  python tools/export_kam_ji_tian_to_rime_dict.py
  python tools/export_kam_ji_tian_to_rime_dict.py --db src/Kam_Ji_Tian.db
  python tools/export_kam_ji_tian_to_rime_dict.py --out ji_khoo_kam_ji_tian.dict.yaml
  python tools/export_kam_ji_tian_to_rime_dict.py --selftest
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from kam_ji_tian_db import DEFAULT_DB, connect, init_db, table_exists  # noqa: E402

DEFAULT_OUT = ROOT / "ji_khoo_kam_ji_tian.dict.yaml"
DICT_NAME = "ji_khoo_kam_ji_tian"
DICT_VERSION = "v0.1.0"


def build_header(name: str = DICT_NAME, version: str = DICT_VERSION) -> str:
    return (
        "# Rime dictionary\n"
        "# encoding: utf-8\n"
        "#\n"
        "# 甘字典\n"
        "#\n"
        "---\n"
        f"name: {name}\n"
        f'version: "{version}"\n'
        "sort: by_weight\n"
        "use_preset_vocabulary: false\n"
        "columns:\n"
        "  - text #漢字／詞彙\n"
        "  - code #台羅音標\n"
        "  - weight #常用度（優先顯示度）\n"
        "  - stem #用法舉例\n"
        "  - create #時間戳記\n"
        "...\n"
        "#漢字\t台羅音標\t常用度\t用法舉例\t時間戳記\n"
    )


def format_weight(weight) -> str:
    try:
        w = float(weight)
    except (TypeError, ValueError):
        w = 0.1
    # 與既有字典風格一致：兩位小數
    return f"{w:.2f}"


def format_create(value) -> str:
    if value is None:
        return ""
    s = str(value).strip()
    # 匯出時可縮成 YYYY-MM-DD HH:MM（與 420 範例一致）
    if len(s) >= 16 and s[4] == "-" and s[10] == " ":
        return s[:16]
    return s


def fetch_all(db_path: Path) -> list[tuple]:
    conn = connect(db_path)
    try:
        if not table_exists(conn):
            sys.exit(f"✗ 資料庫尚無【漢字庫】資料表，請先執行匯入：{db_path}")
        rows = conn.execute(
            """
            SELECT 漢字, 台羅音標, 常用度, 摘要說明, 時間戳記
              FROM 漢字庫
             ORDER BY 漢字 COLLATE BINARY, 台羅音標 COLLATE BINARY, 識別號
            """
        ).fetchall()
        return [
            (
                r["漢字"],
                r["台羅音標"],
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
    out_path.write_text("".join(line if line.endswith("\n") else line + "\n" for line in lines), encoding="utf-8")
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
    check("weight 0.60 → 0.60", format_weight(0.60), "0.60")
    check("create 截斷", format_create("2026-07-05 21:19:00"), "2026-07-05 21:19")
    check("header 含 name", "name: ji_khoo_kam_ji_tian" in build_header(), True)

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        db = Path(tmp) / "t.db"
        out = Path(tmp) / "out.dict.yaml"
        init_db(db)
        conn = connect(db)
        try:
            conn.execute(
                "INSERT INTO 漢字庫 (漢字, 台羅音標, 常用度, 摘要說明, 時間戳記) "
                "VALUES (?, ?, ?, ?, ?)",
                ("九", "kau2", 0.60, "【9257】二九.", "2026-07-05 21:19:00"),
            )
            conn.execute(
                "INSERT INTO 漢字庫 (漢字, 台羅音標, 常用度, 摘要說明, 時間戳記) "
                "VALUES (?, ?, ?, ?, ?)",
                ("九", "kiu2", 0.80, "【10316】容器.", "2026-07-05 21:19:00"),
            )
            conn.commit()
        finally:
            conn.close()
        n = export_dict(db, out)
        text = out.read_text(encoding="utf-8")
        check("匯出筆數", n, 2)
        check("含 kau2", "九\tkau2\t0.60\t【9257】二九.\t2026-07-05 21:19" in text, True)
        check("含 kiu2", "九\tkiu2\t0.80\t【10316】容器.\t2026-07-05 21:19" in text, True)
        check("無 import_tables", "import_tables" not in text, True)

    print("ALL PASS" if ok else "SOME FAILED")
    return 0 if ok else 1


def main() -> None:
    ap = argparse.ArgumentParser(description="甘字典漢字庫 → 中州韻字典子檔")
    ap.add_argument("--db", default=str(DEFAULT_DB), help="SQLite 資料庫路徑")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="輸出 .dict.yaml 路徑")
    ap.add_argument("--selftest", action="store_true", help="僅執行自我測試")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    db_path = Path(args.db)
    out_path = Path(args.out)
    if not db_path.is_file():
        sys.exit(f"✗ 找不到資料庫：{db_path}（請先執行 import_kam_ji_tian_from_excel.py）")

    print(f"開啟資料庫：{db_path}")
    n = export_dict(db_path, out_path)
    print(f"✓ 完成：匯出 {n} 筆 → {out_path}")


if __name__ == "__main__":
    main()
