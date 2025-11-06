#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 BP 處理邏輯
驗證零聲母 BP 格式是否能正確被包裝和處理
"""

import re

def simulate_bp_processing(input_text):
    """模擬 bp_libs.yaml 的處理流程"""
    print(f"輸入: {input_text}")
    
    # 步驟1：拆解聲母+韻母+聲調（模擬第314行）
    # 有聲母處理
    result = re.sub(r'^((?:bb|ln|ggn|gg|zz|[bpmtdlgkzcsjh]).*\d)$', r'〔〉Ø\1〕', input_text)
    if result != input_text:
        print(f"有聲母處理: {result}")
        input_text = result
    
    # 步驟2：零聲母 BP 格式處理（模擬第318行，我們新加的規則）
    result = re.sub(r'^([yw].*\d)$', r'〔〉\1〕', input_text)
    if result != input_text:
        print(f"零聲母BP處理: {result}")
        input_text = result
    
    # 步驟3：清除零聲母標記Ø（模擬第324行）
    result = re.sub(r'〔〉Ø', '〔〉', input_text)
    if result != input_text:
        print(f"清除Ø標記: {result}")
        input_text = result
    
    # 步驟4：處理鼻化韻母（模擬第330行）
    result = re.sub(r'n([iu]?(ai|ao|oo|[aiue]))', r'ⁿ\1', input_text)
    if result != input_text:
        print(f"鼻化韻母處理: {result}")
        input_text = result
    
    # 步驟5：其他零聲母保持原樣（移除〔〉標記）
    result = re.sub(r'〔〉', '〔', input_text)
    if result != input_text:
        print(f"移除〉標記: {result}")
        input_text = result
    
    print(f"最終結果: {input_text}")
    print("-" * 50)
    return input_text

# 測試案例
test_cases = [
    "yong2",     # 楊 - 零聲母複合韻母
    "yi1",       # 伊 - 零聲母單純韻母  
    "wu6",       # 有 - 零聲母單純韻母
    "yin1",      # 因 - 零聲母+鼻尾音
    "wun2",      # 溫 - 零聲母+鼻尾音
    "kong1",     # 公 - 有聲母
    "thinn1",    # 聽 - 有聲母+鼻化韻母
]

print("=== BP 處理邏輯測試 ===")
for case in test_cases:
    simulate_bp_processing(case)