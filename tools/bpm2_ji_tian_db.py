#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
bpm2_ji_tian_db.py

向後相容轉接：請改用 ji_tian_db / ji_tian_profiles。
"""

from __future__ import annotations

from ji_tian_db import DEFAULT_DB, SCHEMA_SQL, connect, init_db, table_exists  # noqa: F401
from ji_tian_profiles import DEFAULT_PROFILE_ID, get_profile  # noqa: F401

# 舊路徑別名（Schema 已改名為 ji_tian_schema.sql）
_ = SCHEMA_SQL
