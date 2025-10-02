#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convert_TLPA_to_BP.py

將【台語音標（TLPA+）】轉換成【閩拼方案（BP）】。
用法：
    python convert_TLPA_to_BP.py <輸入檔> <輸出檔>
"""

import re
import sys

# 聲母轉換對照表（【索引】字串排序，需由長到短）
SIANN_BU_TNG_UANN_PIAU = {
    # 羅馬拼音
    "tsh": "c",
    "ts": "z",
    # 二字母
    "ph": "p",   # ㄆ → p (雙唇音/清音：塞音/送氣)
    "th": "t",   # ㄊ → t (齒齦音/清音：塞音/送氣)
    "kh": "k",   # ㄎ → k（軟顎音/清音：塞音/送氣）
    "ng": "ggn", # ㄫ → ng（軟顎音/濁音：鼻音）
    # 一字母
    # 雙唇音
    "p": "b",    # ㄅ → b（雙唇音/清音：塞音不送氣）
    "b": "bb",   # ㆠ → bb（雙唇音/濁音：塞音不送氣）
    "m": "bbn",  # ㄇ → m（雙唇音/濁音：鼻音）
    #------------------------------
    # 齒齦音
    "t": "d",    # ㄉ → d（齒齦音/清音：塞音/不送氣）
    "n": "ln",   # ㄋ → n（齒齦音/濁音：鼻音）
    "l": "l",    # ㄌ → l（齒齦音/濁音：邊音）
    #------------------------------
    # 齒齦音
    "z": "z",    # ㄗ → z (齒齦音/清音：塞音/不送氣)
    "c": "c",    # ㄘ → c (齒齦音/清音：塞音/送氣)
    "j": "zz",   # ㆡ → zz（齒齦音/濁音：塞擦音/不送氣）
    "s": "s",    # ㄙ → s（齒齦音/清音：擦音）
    #------------------------------
    # 軟顎音
    "k": "g",    # ㄍ → g（軟顎音/清音：塞音/不送氣）
    "g": "gg",   # ㆣ → gg（軟顎音/濁音：塞音/不送氣）
    #------------------------------
    # 聲門音
    "h": "h",    # ㄏ → h（聲門音／擦音：聲門音／清音）
}
# 【齒音聲母+i】轉換對照表
# 【齒音聲母】：TLPA: 舌尖前音/TL: 舌齒音
CI_IM_TNG_UANN_PIAU = {
    # "ji": "zzi",   # ㄗ：j -> zz
    "zzi": "zzi",    # ㆡㄧ：ji → ㆢㄧ：zz+i
}

# 韻母轉換對照表（【索引】字串排序，需由長到短）
UN_BU_TNG_UANN_PIAU = {
    "oonn": "noo",
    "ainn": "nai",
    "aunn": "nao",
    "ann": "na",
    "inn": "ni",
    "unn": "nu",
    "enn": "ne",
    # "ang": "ang",
    # "ong": "ong",
    # "ing": "ing",
    "oo": "oo",
    "ik": "ik",
    # "ai": "ai",
    "au": "ao",
    # "an": "an",
    # "en": "en",
    # "ir": "ir",
    # "am": "am",
    # "om": "om",
    # "a": "a",
    # "i": "i",
    # "u": "u",
    # "e": "e",
    "o": "o",  # ㄜ
}

VOWELS = set("aeiou")  # 用於判斷「i/u 後是否接母音」

TLPA_TIAU_HO_PIAU = {
    "1": "陰平",
    "2": "陰上",
    "3": "陰去",
    "4": "陰入",
    "5": "陽平",
    "6": "陽上",
    "7": "陽去",
    "8": "陽入",
}
BP_TIAU_HO_PIAU = {
    "陰平": "1",
    "陽平": "2",
    "陰上": "3",
    "陽上": "3",
    "陰去": "5",
    "陽去": "6",
    "陰入": "7",
    "陽入": "8",
}

def convert_TLPA_to_BP(TLPA_piau_im: str) -> str:
    """
    將一個【台語音標/TLPA】（如 'tsiann1'）轉成【閩拼/BP】（例如 'ziann1'）。
    保留後面的數字（聲調）。
    """
    # 確認傳入之【台語音標】符合格式=聲母+韻母+聲調=英文字母+數字
    m = re.match(r"^([a-z]+)(\d+)$", TLPA_piau_im)
    if not m:
        # 如果不符合「全英文字母+數字」格式，就原樣回傳
        return TLPA_piau_im

    # 提取：【無調號標音】（聲母+韻母）和【聲調】
    mo_tiau_piau_im, tiau = m.group(1), m.group(2)

    # 1. 轉聲母：從長到短比對 prefix
    siann = ""
    un = mo_tiau_piau_im
    for key in sorted(SIANN_BU_TNG_UANN_PIAU.keys(), key=lambda x: -len(x)):
        if mo_tiau_piau_im.startswith(key):
            siann = SIANN_BU_TNG_UANN_PIAU[key]
            un = mo_tiau_piau_im[len(key) :]
            break

    # 2. 轉韻母：整段比對
    if un in UN_BU_TNG_UANN_PIAU:
        un = UN_BU_TNG_UANN_PIAU[un]

    # 3.【零聲母連i/u】特殊處理
    if siann == "" and un:
        first_lo_ma_ji_bu = un[0]

        if first_lo_ma_ji_bu == "i":
            # i 後面是母音：移到聲母 y，刪掉韻母開頭 i（1.2）
            if len(un) >= 2 and un[1] in VOWELS:
                siann = "y"
                un = un[1:]
            else:
                # i 後面不是母音：移到聲母 y，但韻母保留 i（1.1）
                siann = "y"
                # un 保持以 i 起頭，例如 i / in / inn

        elif first_lo_ma_ji_bu == "u":
            # u 後面是母音：移到聲母 w，刪掉韻母開頭 u（2.2）
            if len(un) >= 2 and un[1] in VOWELS:
                siann = "w"
                un = un[1:]
            else:
                # u 後面不是母音：移到聲母 w，但韻母保留 u（2.1）
                siann = "w"
                # un 保持以 u 起頭，例如 u / un / unn
    # 4. 【台語音標】調號轉換成【閩拼音標】調號
    tiau_mia = TLPA_TIAU_HO_PIAU.get(tiau, tiau)
    tiau = BP_TIAU_HO_PIAU.get(tiau_mia, tiau_mia)

    return f"{siann}{un}{tiau}"


def main(infile: str, outfile: str):
    with open(infile, "r", encoding="utf-8") as fin:
        lines = fin.readlines()

    out_lines = []
    in_entries = False
    for line in lines:
        # 找到「...」之後即進入詞條區
        if not in_entries:
            out_lines.append(line)
            if line.strip() == "...":
                in_entries = True
            continue

        # 在詞條區，跳過空行或註解
        if not line.strip() or line.startswith("#"):
            out_lines.append(line)
            continue

        # 假設詞條以「欄位1\t欄位2\t...」格式，至少要有兩欄
        parts = line.rstrip("\n").split("\t")
        if len(parts) >= 2:
            parts[1] = convert_TLPA_to_BP(parts[1])
            out_lines.append("\t".join(parts) + "\n")
        else:
            out_lines.append(line)

    with open(outfile, "w", encoding="utf-8") as fout:
        fout.writelines(out_lines)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法：python convert_TLPA_to_BP.py <輸入檔> <輸出檔>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
