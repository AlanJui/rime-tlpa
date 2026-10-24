#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ji_tian_db.py

中州韻漢字庫（SQLite）共用模組。
同一 Schema 可服務多種拼音系統之字典重整（見 ji_tian_profiles）。

參考：docs/510_台語注音二式字典重整.md
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_SQL = ROOT / "sql" / "ji_tian_schema.sql"

# 向後相容：未指定 profile 時之預設路徑
DEFAULT_DB = ROOT / "src" / "台語注音二式字典.db"


def connect(db_path: str | os.PathLike | None = None) -> sqlite3.Connection:
    path = Path(db_path) if db_path else DEFAULT_DB
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: str | os.PathLike | None = None) -> Path:
    """依 schema DDL 建置／更新【漢字庫】。"""
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
