"""
convert_tlpa_to_mps2_for_rime_dict.py

將【台語音標（TLPA+）】轉換成【台語注音二式（MPS2）】。
用法：
    python convert_tlpa_to_mps2_for_rime_dict.py tl_ji_khoo_peh_ue.dict.yaml output.dict.yaml
"""

import re
import sys

# 聲母轉換對照表（【索引】字串排序，需由長到短）
SIANN_BU_TNG_UANN_PIAU = {
    "tsh": "c",
    "ts": "z",
    # 二字母
    "ph": "p",  # ㄆ → p (雙唇音/清音：塞音/送氣)
    "th": "t",  # ㄊ → t (齒齦音/清音：塞音/送氣)
    "kh": "k",  # ㄎ → k（軟顎音/清音：塞音/送氣）
    "ng": "ggn",  # ㄫ → ng（軟顎音/濁音：鼻音）
    # 一字母
    # 雙唇音
    "p": "b",  # ㄅ → b（雙唇音/清音：塞音不送氣）
    "b": "bb",  # ㆠ → bb（雙唇音/濁音：塞音不送氣）
    "m": "bbn",  # ㄇ → m（雙唇音/濁音：鼻音）
    # ------------------------------
    # 齒齦音
    "t": "d",  # ㄉ → d（齒齦音/清音：塞音/不送氣）
    "l": "l",  # ㄌ → l（齒齦音/濁音：邊音）
    "n": "ln",  # ㄋ → n（齒齦音/濁音：鼻音）
    # ------------------------------
    # 軟顎音
    "k": "g",  # ㄍ → g（軟顎音/清音：塞音/不送氣）
    "g": "gg",  # ㆣ → gg（軟顎音/濁音：塞音/不送氣）
    # ------------------------------
    # 齒齦音
    "z": "z",  # ㄗ → z (齒齦音/清音：塞音/不送氣)
    "j": "zz",  # ㆡ → zz（齒齦音/濁音：塞擦音/不送氣）
    "c": "c",  # ㄘ → c (齒齦音/清音：塞音/送氣)
    "s": "s",  # ㄙ → s（齒齦音/清音：擦音）
    # ------------------------------
    # 聲門音
    "h": "h",  # ㄏ → h（聲門音／擦音：聲門音／清音）
}

# 【齒音聲母+i】轉換對照表
# 【齒音聲母】：TLPA: 舌尖前音/TL: 舌齒音
CI_IM_TNG_UANN_PIAU = {
    # "zzi": "zzii",  # ㆢ：ji → jj+i
    # "zi": "ji",  # ㄐ：z+i → j+i
    # "ci": "ci",  # ㄑ：c+i → ch+i
    # "si": "si",  # ㄒ：s+i → sh+i
}

# 韻母轉換對照表（【索引】字串排序，需由長到短）
UN_BU_TNG_UANN_PIAU = {
    "ainn": "nai",
    "aunn": "nao",
    "ennh": "naeh",
    "onnh": "nooh",
    "oonn": "noo",
    "onn": "noo",
    "ann": "na",
    "inn": "ni",
    "unn": "nu",
    "enn": "ne",
    # "ang": "ang",
    # "ong": "ong",
    # "ing": "ing",
    # "ionn": "N/A",
    # "ioh": "ioh",
    # "iok": "iok",
    # "io": "io",
    # "ooh": "ooh",
    # "oo": "oo",
    # "oh": "oh",
    # "op": "op",
    # "ok": "ok",
    # "om": "N/A",
    # "ik": "ik",
    # "ai": "ai",
    "au": "ao",
    # "an": "an",
    # "en": "en",
    # "ir": "ir",
    # "am": "am",
    # "a": "a",
    # "i": "i",
    # "u": "u",
    # "e": "e",
    # "o": "o",  # ㄜ
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
    print(f"轉換完成，結果已寫入 {outfile}")


if __name__ == "__main__":
    # 設定預設檔案名稱
    default_infile = "tl_ji_khoo_peh_ue.dict.yaml"
    default_outfile = "bp.dict.yaml"

    # 解析命令列參數
    infile = sys.argv[1] if len(sys.argv) > 1 else default_infile
    outfile = sys.argv[2] if len(sys.argv) > 2 else default_outfile

    print(f"輸入檔案：{infile}")
    print(f"輸出檔案：{outfile}")

    main(infile, outfile)
