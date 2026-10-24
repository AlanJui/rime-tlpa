#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
p110_建置字典資料庫.py

建置中州韻【漢字庫】SQLite 資料庫（僅 Schema，不含資料）。
依 --profile 選擇目標資料庫路徑（如 bpm2 → 台語注音二式字典.db、
tl → 台羅拼音字典.db）。

參考：docs/510_台語注音二式字典重整.md

使用方式：
  python tools/p110_建置字典資料庫.py
  python tools/p110_建置字典資料庫.py --profile bpm2
  python tools/p110_建置字典資料庫.py --profile tl
  python tools/p110_建置字典資料庫.py --db src/自訂.db
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ji_tian_db import connect, init_db, table_exists  # noqa: E402
from ji_tian_profiles import (  # noqa: E402
    DEFAULT_PROFILE_ID,
    get_profile,
    list_profile_ids,
    profile_help_text,
)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="建置中州韻漢字庫（SQLite）",
        epilog=profile_help_text(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--profile",
        default=DEFAULT_PROFILE_ID,
        choices=list_profile_ids(),
        help=f"字典設定（預設：{DEFAULT_PROFILE_ID}）",
    )
    ap.add_argument(
        "--db",
        default=None,
        help="SQLite 路徑（覆寫 profile 預設）",
    )
    args = ap.parse_args()

    try:
        profile = get_profile(args.profile)
    except KeyError as e:
        sys.exit(f"✗ {e}")

    db_path = Path(args.db) if args.db else profile.db_path
    path = init_db(db_path)
    with connect(path) as conn:
        ok = table_exists(conn)
        indexes = [
            r[0]
            for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='漢字庫'"
            ).fetchall()
        ]
        triggers = [
            r[0]
            for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='trigger' AND tbl_name='漢字庫'"
            ).fetchall()
        ]
    if not ok:
        sys.exit("✗ 建置失敗：找不到【漢字庫】資料表")
    print(f"✓ 已建置：{path}")
    print(f"  profile：{profile.id}（{profile.label}）")
    print("  資料表：漢字庫")
    print(f"  索引：{', '.join(indexes) or '(無)'}")
    print(f"  觸發器：{', '.join(triggers) or '(無)'}")


if __name__ == "__main__":
    main()
