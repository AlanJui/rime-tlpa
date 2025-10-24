# 測試 Unicode 字元 F8F4
decimal_code = 63732
hex_code = 0xF8F4

print(f"十進位: {decimal_code}")
print(f"十六進位: {hex_code}")
print(f"十六進位 (格式化): F8F4")

# 檢查這個 Unicode 字元
char = chr(decimal_code)
print(f"字元: {repr(char)}")
print(f"字元表示法: \\u{hex_code:04X}")
print(f"UTF-8 編碼: {char.encode('utf-8')}")

# 檢查是否在 Private Use Area
if 0xE000 <= decimal_code <= 0xF8FF:
    print("✅ 此字元在 Private Use Area (U+E000-U+F8FF)")
elif 0xF0000 <= decimal_code <= 0xFFFFD:
    print("✅ 此字元在 Private Use Area A (U+F0000-U+FFFFD)")
elif 0x100000 <= decimal_code <= 0x10FFFD:
    print("✅ 此字元在 Private Use Area B (U+100000-U+10FFFD)")
else:
    print("❌ 此字元不在 Private Use Area")

# 測試在不同情境下的顯示
print(f"\n實際字元顯示: '{char}'")
print(f"在字串中的表示: 'ㄥ{char}ㄚ'")

# 測試 RIME xform 的可能用法
print(f"\n=== RIME xform 測試 ===")
print(f"直接使用字元: xform/{char}//")
print(f"使用 Unicode 轉義: xform/\\u{hex_code:04X}//")
print(f"使用 UTF-8 編碼: {char.encode('utf-8')}")