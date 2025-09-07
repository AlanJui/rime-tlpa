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
    "ng": "ng", # ㄫ → ng（軟顎音/濁音：鼻音）
    # 一字母
    # 雙唇音
    "p": "b",  # ㄅ → b（雙唇音/清音：塞音不送氣）
    "b": "bb", # ㆠ → bb（雙唇音/濁音：塞音不送氣）
    "m": "m",  # ㄇ → m（雙唇音/濁音：鼻音）
    # ------------------------------
    # 齒齦音
    "t": "d",  # ㄉ → d（齒齦音/清音：塞音/不送氣）
    "n": "n",  # ㄋ → n（齒齦音/濁音：鼻音）
    "l": "l",  # ㄌ → l（齒齦音/濁音：邊音）
    # ------------------------------
    # 齒齦音
    "z": "z",  # ㄗ → z (齒齦音/清音：塞音/不送氣)
    "j": "zz",  # ㆡ → zz（齒齦音/濁音：塞擦音/不送氣）
    "c": "c",  # ㄘ → c (齒齦音/清音：塞音/送氣)
    "s": "s",  # ㄙ → s（齒齦音/清音：擦音）
    # ------------------------------
    # 軟顎音
    "k": "g",  # ㄍ → g（軟顎音/清音：塞音/不送氣）
    "g": "gg",  # ㆣ → gg（軟顎音/濁音：塞音/不送氣）
    # ------------------------------
    # 聲門音
    "h": "h",  # ㄏ → h（聲門音／擦音：聲門音／清音）
}

# 【齒音聲母+i】轉換對照表
# 【齒音聲母】：TLPA: 舌尖前音/TL: 舌齒音
CI_IM_TNG_UANN_PIAU = {
    "zzi": "jji",  # ㆢ：ji → jj+i
    "zi": "ji",  # ㄐ：z+i → j+i
    "ci": "chi",  # ㄑ：c+i → ch+i
    "si": "shi",  # ㄒ：s+i → sh+i
}

# 韻母轉換對照表（【索引】字串排序，需由長到短）
UN_BU_TNG_UANN_PIAU = {
    "oonn": "oonn",
    # "ainn": "ainn",
    # "aunn": "aunn",
    # "ang": "ang",
    # "ann": "ann",
    # "inn": "inn",
    # "unn": "unn",
    # "enn": "enn",
    # "ong": "ong",
    # "ing": "ing",
    "ionn": "ioonn",
    "ioh": "iorh",
    "iok": "iook",
    "io": "ior",
    "onnh": "oonnh",
    "onn": "oonn",
    "ooh": "ooh",
    "oo": "oo",
    "oh": "orh",
    "op": "oop",
    "ok": "ook",
    "om": "oom",
    "ik": "iek",
    # "ai": "ai",
    # "au": "au",
    # "an": "an",
    # "en": "en",
    # "ir": "ir",
    # "am": "am",
    # "a": "a",
    # "i": "i",
    # "u": "u",
    # "e": "e",
    "o": "or",  # ㄜ
}


def convert_TLPA_to_MPS2(TLPA_piau_im: str) -> str:
    """
    將一個【台語音標/TLPA】（如 'tsiann1'）轉成【注音二式/MPS2】（'ziann1'）。
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
    # else:
    #     # 若末尾是「o」卻不在 FINAL_MAP，做一次 o→or
    #     if rest.endswith("o"):
    #         rest = rest[:-1] + "or"

    # 3. 處理【齒音連i】的特殊狀況：【齒音聲母】+ i（【韻母】首拼音字母）
    if siann in ("z", "c", "s", "zz") and un.startswith("i"):
        ci_im_lian_i = f"{siann}i"
        if ci_im_lian_i in CI_IM_TNG_UANN_PIAU:
            ci_im_result = CI_IM_TNG_UANN_PIAU[ci_im_lian_i]
            siann = ci_im_result[:-1]  # 去掉最後的 i

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
            parts[1] = convert_TLPA_to_MPS2(parts[1])
            out_lines.append("\t".join(parts) + "\n")
        else:
            out_lines.append(line)

    with open(outfile, "w", encoding="utf-8") as fout:
        fout.writelines(out_lines)
    print(f"轉換完成，結果已寫入 {outfile}")


if __name__ == "__main__":
    # 設定預設檔案名稱
    default_infile = "tl_ji_khoo_peh_ue.dict.yaml"
    default_outfile = "zu_im_2.dict.yaml"

    # 解析命令列參數
    infile = sys.argv[1] if len(sys.argv) > 1 else default_infile
    outfile = sys.argv[2] if len(sys.argv) > 2 else default_outfile

    print(f"輸入檔案：{infile}")
    print(f"輸出檔案：{outfile}")

    main(infile, outfile)
