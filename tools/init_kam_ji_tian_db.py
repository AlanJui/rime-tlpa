#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
init_kam_ji_tian_db.py

建置【甘字典漢字庫】SQLite 資料庫（僅建立 Schema，不含資料）。

使用方式：
  python tools/init_kam_ji_tian_db.py
  python tools/init_kam_ji_tian_db.py --db src/Kam_Ji_Tian.db
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kam_ji_tian_db import DEFAULT_DB, connect, init_db, table_exists  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description="建置甘字典漢字庫（SQLite）")
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
    print(f"  資料表：漢字庫")
    print(f"  索引：{', '.join(indexes) or '(無)'}")
    print(f"  觸發器：{', '.join(triggers) or '(無)'}")


if __name__ == "__main__":
    main()
