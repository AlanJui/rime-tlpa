#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convert_phing.py

將台羅拼音轉成注音二式，預設讀取 tl_phing_im.txt，輸出到 zu_im_2_phing_im.txt。
也可執行時指定：
    python convert_phing.py 輸入檔.txt 輸出檔.txt
"""

import re
import sys

# 預設檔名
DEFAULT_INPUT = "tl_phing_im.txt"
DEFAULT_OUTPUT = "zu_im_2_phing_im.txt"

# 聲母（初聲）映射表，從長到短比對 prefix
INITIAL_MAP = {
    "tshi": "ci",  # ㄑ → ci
    "tsi": "zi",  # ㄐ → zi
    "tsh": "c",  # ㄘ → c
    "ts": "z",  # ㄗ → z
    "ph": "p",  # ㄆ → p
    "th": "t",  # ㄊ → t
    "kh": "k",  # ㄎ → k
    "ji": "zzi",  # ㆢ → zzi
    "si": "si",  # ㄒ → si
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

# 韻母（襯聲）映射表
FINAL_MAP = {
    "i": "i",
    "inn": "inn",
    "u": "u",
    "unn": "unn",
    "a": "a",
    "ann": "ann",
    "oo": "oo",
    "oonn": "oonn",
    "o": "or",
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
    "-ng": "-ng",
    "ing": "ing",
    "m": "m",
}


def convert_TL_to_BoPoMo2(code: str) -> str:
    """
    將 TLPA code（如 'tshainn1'）轉成注音二式（'cainn1'）。
    保留末尾數字（聲調）。
    """
    m = re.match(r"^([a-z]+)(\d+)$", code)
    if not m:
        return code  # 不符合格式就原樣回傳

    body, tone = m.group(1), m.group(2)

    # 1. 轉聲母
    onset = ""
    rest = body
    for key in sorted(INITIAL_MAP, key=lambda x: -len(x)):
        if body.startswith(key):
            onset = INITIAL_MAP[key]
            rest = body[len(key) :]
            break

    # 2. 轉韻母
    if rest in FINAL_MAP:
        rest = FINAL_MAP[rest]
    else:
        # 若末尾是「o」卻不在 FINAL_MAP，就換成 or
        if rest.endswith("o"):
            rest = rest[:-1] + "or"

    return f"{onset}{rest}{tone}"


def main(infile: str, outfile: str):
    with open(infile, "r", encoding="utf-8") as fin:
        lines = fin.readlines()

    out_lines = []
    in_entries = False
    for line in lines:
        if not in_entries:
            out_lines.append(line)
            if line.strip() == "...":
                in_entries = True
            continue

        if not line.strip() or line.startswith("#"):
            out_lines.append(line)
            continue

        parts = line.rstrip("\n").split("\t")
        if len(parts) >= 2:
            parts[1] = convert_TL_to_BoPoMo2(parts[1])
            out_lines.append("\t".join(parts) + "\n")
        else:
            out_lines.append(line)

    with open(outfile, "w", encoding="utf-8") as fout:
        fout.writelines(out_lines)
    print(f"已輸出：{outfile}")


if __name__ == "__main__":
    # 允許用命令列指定，否則採用預設
    if len(sys.argv) == 3:
        inp = sys.argv[1]
        out = sys.argv[2]
    else:
        inp = DEFAULT_INPUT
        out = DEFAULT_OUTPUT
        print(f"未指定檔名，使用預設：輸入={inp}，輸出={out}")
    main(inp, out)
