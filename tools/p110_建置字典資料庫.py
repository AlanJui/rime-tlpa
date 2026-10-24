#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
p110_建置字典資料庫.py

建置【台語注音二式字典】SQLite 資料庫（僅建立 Schema，不含資料）。

參考：docs/510_台語注音二式字典重整.md

使用方式：
  python tools/p110_建置字典資料庫.py
  python tools/p110_建置字典資料庫.py --db src/台語注音二式字典.db
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bpm2_ji_tian_db import DEFAULT_DB, connect, init_db, table_exists  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description="建置台語注音二式字典（SQLite）")
    ap.add_argument("--db", default=str(DEFAULT_DB), help="SQLite 資料庫路徑")
    args = ap.parse_args()

    path = init_db(args.db)
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
    print("  資料表：漢字庫")
    print(f"  索引：{', '.join(indexes) or '(無)'}")
    print(f"  觸發器：{', '.join(triggers) or '(無)'}")


if __name__ == "__main__":
    main()
