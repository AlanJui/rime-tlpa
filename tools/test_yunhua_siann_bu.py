#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試韻化聲母轉換功能
"""

import os
import sys

# 添加 tools 目錄到路徑，以便導入轉換函數
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from convert_tlpa_to_bp_for_rime_dict import convert_TLPA_to_BP


def test_yunhua_siann_bu():
    """測試韻化聲母轉換"""
    print("=== 韻化聲母轉換測試 ===")

    # 測試案例：韻化聲母（韻母保持原樣，但聲調會轉換）
    # TLPA 7 → BP 6 (陽去), TLPA 5 → BP 2 (陽平)
    yunhua_cases = [
        ("m7", "m6", "毋 - 韻化聲母 m (TLPA 7→BP 6)"),
        ("ng5", "ng2", "黃 - 韻化聲母 ng (TLPA 5→BP 2)"),
    ]

    print("\n1. 韻化聲母測試（應保持原樣）：")
    for tlpa, expected, description in yunhua_cases:
        result = convert_TLPA_to_BP(tlpa)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {tlpa} → {result} (期望: {expected}) - {description}")

    # 測試案例：正常聲母（應該轉換，聲調也會轉換）
    # TLPA 2→BP 3, TLPA 5→BP 2, TLPA 1→BP 1
    normal_cases = [
        ("mi2", "bbni3", "米 - 正常聲母 m (TLPA 2→BP 3)"),
        ("ngoo5", "ggnoo2", "吳 - 正常聲母 ng (TLPA 5→BP 2)"),
        ("ma1", "bbna1", "媽 - 正常聲母 m (TLPA 1→BP 1)"),
        ("nga2", "ggna3", "雅 - 正常聲母 ng (TLPA 2→BP 3)"),
    ]

    print("\n2. 正常聲母測試（應該轉換）：")
    for tlpa, expected, description in normal_cases:
        result = convert_TLPA_to_BP(tlpa)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {tlpa} → {result} (期望: {expected}) - {description}")

    # 測試案例：零聲母（驗證原有功能，聲調也會轉換）
    # TLPA 1→BP 1, TLPA 2→BP 3, TLPA 3→BP 5
    zero_cases = [
        ("i1", "yi1", "伊 - 零聲母 i (TLPA 1→BP 1)"),
        ("iong2", "yong3", "楊 - 零聲母 iong (TLPA 2→BP 3)"),
        ("u3", "wu5", "有 - 零聲母 u (TLPA 3→BP 5)"),
        ("uan2", "wan3", "彎 - 零聲母 uan (TLPA 2→BP 3)"),
    ]

    print("\n3. 零聲母測試（驗證原有功能）：")
    for tlpa, expected, description in zero_cases:
        result = convert_TLPA_to_BP(tlpa)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {tlpa} → {result} (期望: {expected}) - {description}")

    # 測試案例：其他正常聲母（驗證沒有破壞原有功能）
    other_cases = [
        ("tsiann1", "znia1", "正 - 正常聲母轉換 (韻母 iann→nia)"),
        ("siok8", "siok8", "俗 - 正常聲母保持"),
        ("kong1", "gong1", "公 - 正常聲母轉換"),
    ]

    print("\n4. 其他聲母測試（驗證原有功能）：")
    for tlpa, expected, description in other_cases:
        result = convert_TLPA_to_BP(tlpa)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {tlpa} → {result} (期望: {expected}) - {description}")

if __name__ == "__main__":
    test_yunhua_siann_bu()