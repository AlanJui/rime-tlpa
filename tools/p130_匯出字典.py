#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
p130_匯出字典.py

自 SQLite【漢字庫】匯出重整後之中州韻字典檔。
依 --profile 選擇資料庫與輸出路徑。

欄位對映：
  漢字     → text
  漢字標音 → code
  常用度   → weight
  摘要說明 → stem
  時間戳記 → create

參考：docs/510_台語注音二式字典重整.md

使用方式：
  python tools/p130_匯出字典.py --profile bpm2
  python tools/p130_匯出字典.py --profile tl
  python tools/p130_匯出字典.py --db src/x.db --out y_new.dict.yaml
  python tools/p130_匯出字典.py --selftest
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ji_tian_db import connect, init_db, table_exists  # noqa: E402
from ji_tian_profiles import (  # noqa: E402
    DEFAULT_PROFILE_ID,
    DictProfile,
    get_profile,
    list_profile_ids,
    profile_help_text,
)

DICT_VERSION = "v0.1.0"


def build_header(profile: DictProfile, version: str = DICT_VERSION) -> str:
    return (
        "# Rime dictionary\n"
        "# encoding: utf-8\n"
        "#\n"
        f"# {profile.header_title}\n"
        "#\n"
        "---\n"
        f"name: {profile.dict_name}\n"
        f'version: "{version}"\n'
        "sort: by_weight\n"
        "use_preset_vocabulary: false\n"
        "columns:\n"
        "  - text #漢字／詞彙\n"
        f"  - code #{profile.code_comment}\n"
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


def export_dict(db_path: Path, out_path: Path, profile: DictProfile) -> int:
    rows = fetch_all(db_path)
    lines = [build_header(profile)]
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

    bpm2 = get_profile("bpm2")
    tl = get_profile("tl")
    check("weight", format_weight(0.8), "0.80")
    check("bpm2 header name", f"name: {bpm2.dict_name}" in build_header(bpm2), True)
    check("tl header name", f"name: {tl.dict_name}" in build_header(tl), True)
    check("tl out 檔名", tl.out_path.name, "ji_khoo_tl_HanJi_new.dict.yaml")

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
            conn.commit()
        finally:
            conn.close()
        n = export_dict(db, out, tl)
        text = out.read_text(encoding="utf-8")
        check("匯出筆數", n, 1)
        check("含 but4", "不\tbut4\t0.10\tNA\t2026-01-02 22:51" in text, True)
        check("header 標題", tl.header_title in text, True)
        check("無 [ptkh]1", re.search(r"[ptkh]1\t", text) is None, True)

    print("ALL PASS" if ok else "SOME FAILED")
    return 0 if ok else 1


def main() -> None:
    ap = argparse.ArgumentParser(
        description="SQLite 漢字庫 → 中州韻字典檔",
        epilog=profile_help_text(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--profile",
        default=DEFAULT_PROFILE_ID,
        choices=list_profile_ids(),
        help=f"字典設定（預設：{DEFAULT_PROFILE_ID}）",
    )
    ap.add_argument("--db", default=None, help="SQLite 路徑（覆寫 profile）")
    ap.add_argument("--out", default=None, help="輸出 .dict.yaml（覆寫 profile）")
    ap.add_argument("--selftest", action="store_true", help="僅執行自我測試")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    try:
        profile = get_profile(args.profile)
    except KeyError as e:
        sys.exit(f"✗ {e}")

    db_path = Path(args.db) if args.db else profile.db_path
    out_path = Path(args.out) if args.out else profile.out_path
    if not db_path.is_file():
        sys.exit(f"✗ 找不到資料庫：{db_path}（請先執行 p110／p120）")

    print(f"profile：{profile.id}（{profile.label}）")
    print(f"開啟資料庫：{db_path}")
    n = export_dict(db_path, out_path, profile)
    print(f"✓ 完成：匯出 {n} 筆 → {out_path}")


if __name__ == "__main__":
    main()
