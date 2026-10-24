#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
p120_匯入字典.py

將【中州韻字典檔】ji_khoo_bpm2.dict.yaml 逐筆寫入 SQLite。

處理規則：
  1. 入聲韻尾標音 ([ptkh])1 → \\14（改為陰入調 4）
  2. 遇【漢字+漢字標音】重複時略過，不中止

參考：docs/510_台語注音二式字典重整.md

使用方式：
  python tools/p120_匯入字典.py
  python tools/p120_匯入字典.py --dict ji_khoo_bpm2.dict.yaml
  python tools/p120_匯入字典.py --db src/台語注音二式字典.db --replace
  python tools/p120_匯入字典.py --selftest
"""

from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from bpm2_ji_tian_db import DEFAULT_DB, connect, init_db  # noqa: E402

DEFAULT_DICT = ROOT / "ji_khoo_bpm2.dict.yaml"

# 入聲韻尾 p/t/k/h 後接錯誤調號 1 → 改為 4
_ENTERING_TONE_RE = re.compile(r"([ptkh])1$", re.IGNORECASE)


def fix_entering_tone(code: str) -> str:
    """jip1 / but1 / siok1 / bbeh1 → …4"""
    return _ENTERING_TONE_RE.sub(r"\g<1>4", code.strip())


def parse_dict_line(line: str) -> tuple[str, str, float, str, str | None] | None:
    """
    解析字典檔一列（tab 分隔）。
    回傳 (漢字, 漢字標音, 常用度, 摘要說明, 時間戳記|None)；無效列回傳 None。
    """
    s = line.strip()
    if not s or s.startswith("#"):
        return None
    if s in ("---", "..."):
        return None
    # YAML header 鍵值列
    if ":" in s and "\t" not in s:
        return None

    parts = line.rstrip("\n\r").split("\t")
    if len(parts) < 2:
        return None

    text = parts[0].strip()
    code = fix_entering_tone(parts[1].strip())
    if not text or not code:
        return None

    weight = 0.1
    if len(parts) >= 3 and parts[2].strip():
        try:
            weight = float(parts[2].strip())
        except ValueError:
            weight = 0.1

    stem = parts[3].strip() if len(parts) >= 4 and parts[3].strip() else "NA"
    create = parts[4].strip() if len(parts) >= 5 and parts[4].strip() else None
    return text, code, weight, stem, create


def import_dict(
    dict_path: Path,
    db_path: Path,
    *,
    replace: bool = False,
) -> tuple[int, int, int]:
    """
    寫入【漢字庫】。
    回傳 (寫入筆數, 略過重複筆數, 入聲調號修正筆數)。
    遇 UNIQUE(漢字, 漢字標音) 衝突時略過，不中止。
    """
    init_db(db_path)
    inserted = skipped = tone_fixed = 0
    conn = connect(db_path)
    try:
        if replace:
            conn.execute("DELETE FROM 漢字庫")
            conn.commit()

        sql = """
            INSERT INTO 漢字庫 (漢字, 漢字標音, 常用度, 摘要說明, 時間戳記)
            VALUES (?, ?, ?, ?, COALESCE(?, DATETIME('now', 'localtime')))
        """

        if not dict_path.is_file():
            sys.exit(f"✗ 找不到字典檔：{dict_path}")

        in_body = False
        with dict_path.open(encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                if not in_body:
                    if line.strip() == "...":
                        in_body = True
                    continue
                s = line.strip()
                if not s or s.startswith("#"):
                    continue
                parts = line.rstrip("\n\r").split("\t")
                if len(parts) < 2:
                    continue
                text = parts[0].strip()
                raw_code = parts[1].strip()
                if not text or not raw_code:
                    continue
                code = fix_entering_tone(raw_code)
                if code != raw_code:
                    tone_fixed += 1

                weight = 0.1
                if len(parts) >= 3 and parts[2].strip():
                    try:
                        weight = float(parts[2].strip())
                    except ValueError:
                        weight = 0.1
                stem = (
                    parts[3].strip()
                    if len(parts) >= 4 and parts[3].strip()
                    else "NA"
                )
                create = (
                    parts[4].strip()
                    if len(parts) >= 5 and parts[4].strip()
                    else None
                )

                try:
                    conn.execute(sql, (text, code, weight, stem, create))
                    inserted += 1
                except sqlite3.IntegrityError:
                    skipped += 1
                print(
                    f"\r寫入 行={line_no} 漢字={text} 標音={code}  "
                    f"寫入={inserted} 略過={skipped} 調號修正={tone_fixed}",
                    end="",
                    flush=True,
                )
        print()
        conn.commit()
    finally:
        conn.close()

    return inserted, skipped, tone_fixed


def selftest() -> int:
    import tempfile

    ok = True

    def check(desc, got, exp):
        nonlocal ok
        mark = "OK  " if got == exp else "FAIL"
        if got != exp:
            ok = False
        print(f"{mark} {desc}: {got!r} (expect {exp!r})")

    check("jip1 → jip4", fix_entering_tone("jip1"), "jip4")
    check("but1 → but4", fix_entering_tone("but1"), "but4")
    check("siok1 → siok4", fix_entering_tone("siok1"), "siok4")
    check("bbeh1 → bbeh4", fix_entering_tone("bbeh1"), "bbeh4")
    check("heh1 → heh4", fix_entering_tone("heh1"), "heh4")
    check("lang5 不變", fix_entering_tone("lang5"), "lang5")
    check("jit8 不變", fix_entering_tone("jit8"), "jit8")
    check("ki1 不變（非入聲韻尾）", fix_entering_tone("ki1"), "ki1")

    check(
        "解析 + 調號",
        parse_dict_line("不\tbut1\t0.1\tNA\t2026-01-02 22:51:07"),
        ("不", "but4", 0.1, "NA", "2026-01-02 22:51:07"),
    )
    check("註解列 → None", parse_dict_line("# 註解"), None)

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        tmp_path = Path(tmp)
        db = tmp_path / "t.db"
        dict_file = tmp_path / "t.dict.yaml"
        dict_file.write_text(
            "# Rime dictionary\n"
            "---\n"
            "name: t\n"
            "...\n"
            "嚇\theh1\t0.1\tNA\t2026-01-02 22:51:07\n"
            "嚇\theh4\t0.01\tNA\t2025-02-11 11:16:04\n"
            "不\tbut1\t0.1\tNA\t2026-01-02 22:51:07\n"
            "人\tlang5\t0.6\t【12996】大人.\t2026-07-05 21:19:00\n",
            encoding="utf-8",
        )
        ins, sk, fixed = import_dict(dict_file, db, replace=True)
        check("寫入筆數（heh1→heh4 與既有 heh4 去重）", ins, 3)
        check("略過重複", sk, 1)
        check("調號修正次數", fixed, 2)

        conn = connect(db)
        try:
            codes = [
                r[0]
                for r in conn.execute(
                    "SELECT 漢字標音 FROM 漢字庫 WHERE 漢字='嚇' ORDER BY 漢字標音"
                ).fetchall()
            ]
            n = conn.execute("SELECT COUNT(*) FROM 漢字庫").fetchone()[0]
        finally:
            conn.close()
        check("嚇 僅保留一筆 heh4", codes, ["heh4"])
        check("總筆數", n, 3)

    print("ALL PASS" if ok else "SOME FAILED")
    return 0 if ok else 1


def main() -> None:
    ap = argparse.ArgumentParser(description="中州韻字典 → 台語注音二式字典（SQLite）")
    ap.add_argument("--dict", default=str(DEFAULT_DICT), help="輸入 .dict.yaml")
    ap.add_argument("--db", default=str(DEFAULT_DB), help="SQLite 資料庫路徑")
    ap.add_argument(
        "--replace",
        action="store_true",
        help="匯入前清空【漢字庫】後全量寫入",
    )
    ap.add_argument("--selftest", action="store_true", help="僅執行自我測試")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    dict_path = Path(args.dict)
    db_path = Path(args.db)
    print(f"讀取字典：{dict_path}")
    print(f"寫入資料庫：{db_path}")
    inserted, skipped, tone_fixed = import_dict(
        dict_path, db_path, replace=args.replace
    )
    mode = "全量重建" if args.replace else "增量（略過重複）"
    print(
        f"✓ 完成（{mode}）：寫入 {inserted} 筆，略過重複 {skipped} 筆，"
        f"入聲調號修正 {tone_fixed} 筆 → {db_path}"
    )


if __name__ == "__main__":
    main()
