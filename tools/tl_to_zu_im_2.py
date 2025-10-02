#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convert_TL_to_bopomofo2.py

將 Rime 字典中第二欄的台羅拼音（TL）轉換成注音二式。
用法：
    python convert_TL_to_bopomofo2.py tl_ji_khoo_peh_ue.dict.yaml output.dict.yaml
"""

import re
import sys

# 聲母（初聲）映射表，注意要從長到短比對 prefix
INITIAL_MAP = {
    # 四字母（如果有更長的 key，也放最前面）
    "tshi": "ci",  # ㄑ → ci
    # 三字母
    "tsi": "zi",  # ㄐ → zi
    # 二字母
    "tsh": "c",  # ㄘ → c
    "ts": "z",  # ㄗ → z
    "ph": "p",  # ㄆ → p
    "th": "t",  # ㄊ → t
    "kh": "k",  # ㄎ → k
    "ji": "zzi",  # ㆢ → zzi
    "si": "si",  # ㄒ → si
    # 一字母
    "b": "bb",  # ㆠ → bb
    "p": "b",  # ㄅ → b
    "m": "m",  # ㄇ → m
    "t": "d",  # ㄉ → d
    "n": "n",  # ㄋ → n
    "l": "l",  # ㄌ → l
    "k": "g",  # ㄍ → g
    "g": "gg",  # ㆣ → gg
    "h": "h",  # ㄏ → h
    "j": "zz",  # ㆡ → zz
    "s": "s",  # ㄙ → s
}

# 韻母（襯聲）映射表，台羅→注音二式（多數相同，唯「o」→「or」需要特別處理）
FINAL_MAP = {
    "i": "i",
    "inn": "inn",
    "u": "u",
    "unn": "unn",
    "a": "a",
    "ann": "ann",
    "oo": "oo",
    "oonn": "oonn",
    "o": "or",  # ㄜ
    "e": "e",
    "enn": "enn",
    "ai": "ai",
    "ainn": "ainn",
    "au": "au",
    "aunn": "aunn",
    "an": "an",
    "en": "en",
    "ang": "ang",
    "ir": "ir",
    "am": "am",
    "om": "om",
    "ong": "ong",
    # 如果你的字典裡有「-ng」或「-ing」「-m」等，也可加進來：
    "-ng": "-ng",
    "ing": "ing",
    "m": "m",
}


def convert_TL_to_bopomofo2(code: str) -> str:
    """
    將一個 TL code（如 'tsiann1'）轉成注音二式（'ziann1'）。
    保留後面的數字（聲調）。
    """
    m = re.match(r"^([a-z]+)(\d+)$", code)
    if not m:
        # 如果不符合「全英文字母+數字」格式，就原樣回傳
        return code

    body, tone = m.group(1), m.group(2)

    # 1. 轉聲母：從長到短比對 prefix
    onset = ""
    rest = body
    for key in sorted(INITIAL_MAP.keys(), key=lambda x: -len(x)):
        if body.startswith(key):
            onset = INITIAL_MAP[key]
            rest = body[len(key) :]
            break

    # 2. 轉韻母：整段比對
    if rest in FINAL_MAP:
        rest = FINAL_MAP[rest]
    else:
        # 若末尾是「o」卻不在 FINAL_MAP，做一次 o→or
        if rest.endswith("o"):
            rest = rest[:-1] + "or"

    return f"{onset}{rest}{tone}"


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
            parts[1] = convert_TL_to_bopomofo2(parts[1])
            out_lines.append("\t".join(parts) + "\n")
        else:
            out_lines.append(line)

    with open(outfile, "w", encoding="utf-8") as fout:
        fout.writelines(out_lines)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法：python convert_TL_to_bopomofo2.py <輸入檔> <輸出檔>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
