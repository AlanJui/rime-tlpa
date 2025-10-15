#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
驗證 RIME TLPA Hong Im Schema 中的 xlit 規則
"""

def validate_xlit_rules():
    """驗證 xlit 規則中的字符對映是否正確"""
    
    # 第一個 xlit 規則：注音符號對映
    source1 = "bpPmtTnlgkKwhJZCSjzcsiIuUaAOQoeExXyYFHVB@MNWRrfqv"
    target1 = "!1qa2wsxEedNcRrfvYyhnuUjJ8*iIk,<9(lL;oMO0mp/Kbtgz"
    
    # 第二個 xlit 規則：調號和功能按鍵對映
    source2 = "023579*L"
    target2 = "74365.-="
    
    print("=== RIME TLPA Hong Im Schema xlit 規則驗證 ===\n")
    
    # 驗證第一個規則
    print("1. 注音符號對映規則:")
    print(f"   源字符: {source1}")
    print(f"   目標字符: {target1}")
    print(f"   源字符數: {len(source1)}")
    print(f"   目標字符數: {len(target1)}")
    print(f"   字符數匹配: {'✅ 是' if len(source1) == len(target1) else '❌ 否'}")
    
    if len(source1) == len(target1):
        print("   對映關係:")
        for i, (s, t) in enumerate(zip(source1, target1)):
            print(f"     {s} -> {t}")
            if i >= 9:  # 只顯示前10個對映
                print(f"     ... (還有 {len(source1) - 10} 個對映)")
                break
    
    print("\n2. 調號和功能按鍵對映規則:")
    print(f"   源字符: {source2}")
    print(f"   目標字符: {target2}")
    print(f"   源字符數: {len(source2)}")
    print(f"   目標字符數: {len(target2)}")
    print(f"   字符數匹配: {'✅ 是' if len(source2) == len(target2) else '❌ 否'}")
    
    if len(source2) == len(target2):
        print("   對映關係:")
        for s, t in zip(source2, target2):
            print(f"     {s} -> {t}")
    
    # 總結
    rule1_valid = len(source1) == len(target1)
    rule2_valid = len(source2) == len(target2)
    
    print(f"\n=== 驗證結果 ===")
    print(f"規則1 (注音符號): {'✅ 有效' if rule1_valid else '❌ 無效'}")
    print(f"規則2 (調號功能): {'✅ 有效' if rule2_valid else '❌ 無效'}")
    print(f"整體狀態: {'✅ 所有規則都有效' if rule1_valid and rule2_valid else '❌ 存在無效規則'}")
    
    return rule1_valid and rule2_valid

if __name__ == "__main__":
    validate_xlit_rules()