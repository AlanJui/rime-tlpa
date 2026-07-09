#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
kam_ji_tian_db.py

甘字典漢字庫（SQLite）共用模組。
參考：docs/420_甘字典漢字庫指引.md
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = ROOT / "src" / "Kam_Ji_Tian.db"
SCHEMA_SQL = ROOT / "sql" / "kam_ji_tian_schema.sql"


def connect(db_path: str | os.PathLike | None = None) -> sqlite3.Connection:
    path = Path(db_path) if db_path else DEFAULT_DB
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: str | os.PathLike | None = None) -> Path:
    """依 schema DDL 建置／更新【甘字典漢字庫】。"""
    path = Path(db_path) if db_path else DEFAULT_DB
    if not SCHEMA_SQL.is_file():
        raise FileNotFoundError(f"找不到 Schema：{SCHEMA_SQL}")

    ddl = SCHEMA_SQL.read_text(encoding="utf-8")
    conn = connect(path)
    try:
        conn.executescript(ddl)
        conn.commit()
    finally:
        conn.close()
    return path


def table_exists(conn: sqlite3.Connection) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='漢字庫'"
    ).fetchone()
    return row is not None
