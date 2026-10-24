#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
p120_匯入字典.py

將【中州韻字典檔】逐筆寫入 SQLite。
依 --profile 選擇來源字典與目標資料庫。

處理規則：
  1. 入聲韻尾標音 ([ptkh])1 → \\14（改為陰入調 4）
  2. 遇【漢字+漢字標音】重複時略過，不中止

參考：docs/510_台語注音二式字典重整.md

使用方式：
  python tools/p120_匯入字典.py --profile bpm2 --replace
  python tools/p120_匯入字典.py --profile tl --replace
  python tools/p120_匯入字典.py --dict path.dict.yaml --db src/x.db --replace
  python tools/p120_匯入字典.py --selftest
"""

from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ji_tian_db import connect, init_db  # noqa: E402
from ji_tian_profiles import (  # noqa: E402
    DEFAULT_PROFILE_ID,
    get_profile,
    list_profile_ids,
    profile_help_text,
)

# 入聲韻尾 p/t/k/h 後接錯誤調號 1 → 改為 4（BPM2／台羅皆適用）
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
    check("ki1 不變", fix_entering_tone("ki1"), "ki1")

    bpm2 = get_profile("bpm2")
    tl = get_profile("tl")
    check("bpm2 db 檔名", bpm2.db_path.name, "台語注音二式字典.db")
    check("tl db 檔名", tl.db_path.name, "台羅拼音字典.db")
    check("tl 來源字典", tl.dict_path.name, "ji_khoo_tl_HanJi.dict.yaml")

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
        check("寫入筆數", ins, 3)
        check("略過重複", sk, 1)
        check("調號修正", fixed, 2)

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
        check("嚇 僅 heh4", codes, ["heh4"])
        check("總筆數", n, 3)

    print("ALL PASS" if ok else "SOME FAILED")
    return 0 if ok else 1


def main() -> None:
    ap = argparse.ArgumentParser(
        description="中州韻字典 → SQLite 漢字庫",
        epilog=profile_help_text(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--profile",
        default=DEFAULT_PROFILE_ID,
        choices=list_profile_ids(),
        help=f"字典設定（預設：{DEFAULT_PROFILE_ID}）",
    )
    ap.add_argument("--dict", default=None, help="輸入 .dict.yaml（覆寫 profile）")
    ap.add_argument("--db", default=None, help="SQLite 路徑（覆寫 profile）")
    ap.add_argument(
        "--replace",
        action="store_true",
        help="匯入前清空【漢字庫】後全量寫入",
    )
    ap.add_argument("--selftest", action="store_true", help="僅執行自我測試")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    try:
        profile = get_profile(args.profile)
    except KeyError as e:
        sys.exit(f"✗ {e}")

    dict_path = Path(args.dict) if args.dict else profile.dict_path
    db_path = Path(args.db) if args.db else profile.db_path

    print(f"profile：{profile.id}（{profile.label}）")
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
