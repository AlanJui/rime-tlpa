#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ji_tian_profiles.py

中州韻字典重整作業之【字典設定檔】（profile）。
同一套 p110／p120／p130 可依 profile 處理不同拼音系統之字典。

參考：docs/510_台語注音二式字典重整.md
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class DictProfile:
    """一種中州韻字典重整目標。"""

    id: str
    label: str  # 顯示名稱，如「台語注音二式」
    dict_path: Path  # 來源 .dict.yaml
    db_path: Path  # SQLite 資料庫
    out_path: Path  # 重整後輸出 .dict.yaml
    dict_name: str  # Rime name:
    header_title: str  # 檔頭註解標題
    code_comment: str  # columns code 註解


# 內建 profile：可再擴充
PROFILES: dict[str, DictProfile] = {
    "bpm2": DictProfile(
        id="bpm2",
        label="台語注音二式",
        dict_path=ROOT / "ji_khoo_bpm2.dict.yaml",
        db_path=ROOT / "src" / "台語注音二式字典.db",
        out_path=ROOT / "ji_khoo_bpm2_new.dict.yaml",
        dict_name="ji_khoo_bpm2",
        header_title="台語注音二式字典（重整後）",
        code_comment="漢字標音（台語注音二式）",
    ),
    "tl": DictProfile(
        id="tl",
        label="台羅拼音",
        dict_path=ROOT / "ji_khoo_tl_HanJi.dict.yaml",
        db_path=ROOT / "src" / "台羅拼音字典.db",
        out_path=ROOT / "ji_khoo_tl_HanJi_new.dict.yaml",
        dict_name="ji_khoo_tl_HanJi",
        header_title="台羅拼音字典（重整後）",
        code_comment="漢字標音（台羅拼音）",
    ),
}

DEFAULT_PROFILE_ID = "bpm2"


def list_profile_ids() -> list[str]:
    return sorted(PROFILES.keys())


def get_profile(profile_id: str | None = None) -> DictProfile:
    pid = (profile_id or DEFAULT_PROFILE_ID).strip().lower()
    if pid not in PROFILES:
        known = ", ".join(list_profile_ids())
        raise KeyError(f"未知 profile：{profile_id!r}（可用：{known}）")
    return PROFILES[pid]


def profile_help_text() -> str:
    lines = ["可用 --profile："]
    for pid in list_profile_ids():
        p = PROFILES[pid]
        lines.append(
            f"  {pid:6} {p.label}  dict={p.dict_path.name}  db={p.db_path.name}"
        )
    return "\n".join(lines)
