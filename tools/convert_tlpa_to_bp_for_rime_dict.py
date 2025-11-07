"""
convert_tlpa_to_bp_for_rime_dict.py

將【台語音標（TLPA+）】轉換成【台語注音二式（bp）】。

用法：
    python convert_tlpa_to_bp_for_rime_dict.py [input_file] [output_file]

參數：
    input_file  (可選): 輸入檔案路徑
                       預設值：專案根目錄下的 tl_ji_khoo_peh_ue.dict.yaml
    output_file (可選): 輸出檔案路徑
                       預設值：專案根目錄下的 bp_ji_khoo.dict.yaml

範例：
    # 使用預設檔案
    python convert_tlpa_to_bp_for_rime_dict.py

    # 指定輸入檔案，使用預設輸出檔案
    python convert_tlpa_to_bp_for_rime_dict.py custom_input.dict.yaml

    # 指定輸入和輸出檔案
    python convert_tlpa_to_bp_for_rime_dict.py input.dict.yaml output.dict.yaml
"""

import re
import sys

# RIME 字典名稱
JI_KHOO_NAME = "bp_ji_khoo"

# 聲母轉換對照表（【索引】字串排序，需由長到短）
SIANN_BU_TNG_UANN_PIAU = {
    "tsh": "c",
    "ts": "z",
    # 二字母
    "ph": "p",  # ㄆ → p (雙唇音/清音：塞音/送氣)
    "th": "t",  # ㄊ → t (齒齦音/清音：塞音/送氣)
    "kh": "k",  # ㄎ → k（軟顎音/清音：塞音/送氣）
    "ng": "ggn", # ㄫ → ng（軟顎音/濁音：鼻音）
    # 一字母
    # 雙唇音
    "p": "b",  # ㄅ → b（雙唇音/清音：塞音不送氣）
    "b": "bb",  # ㆠ → bb（雙唇音/濁音：塞音不送氣）
    "m": "bbn",  # ㄇ → m（雙唇音/濁音：鼻音）
    # ------------------------------
    # 齒齦音
    "t": "d",  # ㄉ → d（齒齦音/清音：塞音/不送氣）
    "n": "ln",  # ㄋ → n（齒齦音/濁音：鼻音）
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
CI_IM_TNG_UANN_PIAU: dict[str, str] = {
    # "zzi": "jji",  # ㆢ：ji → jj+i
    # "zi": "ji",  # ㄐ：z+i → j+i
    # "ci": "chi",  # ㄑ：c+i → ch+i
    # "si": "shi",  # ㄒ：s+i → sh+i
}

# 韻母轉換對照表（【索引】字串排序，需由長到短）
# （1）複合韻母：
# ai, au/ao, ia, iu, io, ua, ui, ue, iau/iao, uai
# （2）鼻化韻母：
# ann, inn, enn, onn, ainn, iann, iunn/ionn, uann, uainn, iaunn/iaonn
# （3）鼻音韻尾：
# am, an, ang, im, in, ing, un, ong, iam, ian, iang, iong, uan, uang
UN_BU_TNG_UANN_PIAU = {
    # （1）鼻化韻母
    "iaunn": "niao",
    "uainn": "nuai",
    "uann": "nua",
    "iunn": "niu",
    "ionn": "nio",
    "iann": "nia",
    "ainn": "nai",
    "oonn": "no",
    "onn": "no",
    "enn": "ne",
    "inn": "ni",
    # （2）複合韻母
    # "uai": "uai",
    "iau": "iao",
    "ue": "ue",
    "ui": "ui",
    "ua": "ua",
    "io": "io",
    "iu": "iu",
    "ia": "ia",
    "au": "ao",
    "ai": "ai",
    # （3）鼻音韻尾：
    # am, an, ang, im, in, ing, un, ong, iam, ian, iang, iong, uan, uang
    "uang": "uang",
    "uan": "uan",
    "iong": "iong",
    "iang": "iang",
    "ian": "ian",
    "iam": "iam",
    "ong": "ong",
    "un": "un",
    "ing": "ing",
    "in": "in",
    "im": "im",
    "ang": "ang",
    "an": "an",
    "am": "am",
    # （1）元音及方音
    # "ir": "ir",
    # "ee": "ee",
    # "a": "a",
    # "i": "i",
    # "u": "u",
    # "e": "e",
    # "oo": "oo",
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
    將一個 TLPA（台語音標）詞條轉換為注音二式（BP/MPS2）格式。
    輸入格式：小寫英文字母組成的拼音部分後接一或多位數字聲調，例如 "tsiann1"。
    若輸入不符合正規表達式 ^([a-z]+)(\\d+)$，則原樣回傳。

    轉換步驟（概要）：
    1. 以正規表達式分離拼音（聲母+韻母）與聲調數字。
    2. 以 SIANN_BU_TNG_UANN_PIAU 做最長前綴比對轉換聲母，剩餘為韻母。
    3. 若剩餘韻母整段能在 UN_BU_TNG_UANN_PIAU 找到對應，則以對應值取代。
    4. 處理零聲母且韻母以 i 或 u 起頭的介音情形：
       - i 為介音且後一字為母音時：聲母設為 "y"，刪去韻母首 i。
       - i 為介音但後一字非母音時：聲母設為 "y"，韻母保留。
       - u 為介音且後一字為母音時：聲母設為 "w"，刪去韻母首 u。
       - u 為介音但後一字非母音時：聲母設為 "w"，韻母保留。
    5. 以 TLPA_TIAU_HO_PIAU 與 BP_TIAU_HO_PIAU 做聲調名稱與編碼之對應轉換。
    6. 回傳 "<聲母><韻母><聲調>"。

    參數：
    - TLPA_piau_im (str): 要轉換的 TLPA 詞條，如 "tsiann1"、"iao2" 等。

    回傳值：
    - str: 轉換後的 BP 詞條；若輸入格式不符則回傳原字串。
    """
    # 確認傳入之【台語音標】符合格式=聲母+韻母+聲調=英文字母+數字
    m = re.match(r"^([a-z]+)(\d+)$", TLPA_piau_im)
    if not m:
        # 如果不符合「全英文字母+數字」格式，就原樣回傳
        return TLPA_piau_im

    # 提取：【無調號標音】（聲母+韻母）和【聲調】
    mo_tiau_piau_im, tiau = m.group(1), m.group(2)

    # 1. 轉聲母：從長到短比對 prefix
    # 特殊處理：韻化聲母 m、ng（後面直接接聲調，不轉換）
    siann = ""
    un = mo_tiau_piau_im

    # 檢查是否為韻化聲母：m 或 ng 後面沒有韻母（整個無調號標音就是 m 或 ng）
    if mo_tiau_piau_im == "m":
        # 韻化聲母 m：毋 [m7] 保持為 m，不轉換成 bbn
        siann = ""
        un = "m"
    elif mo_tiau_piau_im == "ng":
        # 韻化聲母 ng：黃 [ng5] 保持為 ng，不轉換成 ggn
        siann = ""
        un = "ng"
    else:
        # 正常聲母轉換邏輯
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
            # i 為【介音】，聲母變更為：[y]，韻母的首羅馬字 [i] 將之刪除。
            # 【例】：腰 [iao] ==> [yao]，鞅 [iang] ==> [yang]，央 [iong] ==> [yong]
            # i 後面是母音：移到聲母 y，刪掉韻母開頭 i（1.2）
            if len(un) >= 2 and un[1] in VOWELS:
                siann = "y"
                un = un[1:]
            else:
                # i 為【元音】韻母，聲母變更為：[y]，韻母維持不變。
                # 【例】：伊 [i] ==> [yi]，音 [im] ==> [yim]，益 [ik] ==> [yik]
                # i 後面不是母音：移到聲母 y，但韻母保留 i（1.1）
                siann = "y"
                # un 保持以 i 起頭，例如 i / in / inn

        elif first_lo_ma_ji_bu == "u":
            # u 為【介音】，聲母變更為：[w]，韻母的首羅馬字 [u] 將之刪除。
            # 【例】：彎 [uan] ==> [wan]，歪 [uai] ==> [wai]，位 [ui] ==> [wi]
            # u 後面是母音：移到聲母 w，刪掉韻母開頭 u（2.2）
            if len(un) >= 2 and un[1] in VOWELS:
                siann = "w"
                un = un[1:]
            else:
                # u 為【元音】韻母，聲母變更為：[w]，韻母維持不變。
                # 【例】：有 [u] ==> [wu]，溫 [un] ==> [wun]，鬱 [ut] ==> [wut]
                # u 後面不是母音：移到聲母 w，但韻母保留 u（2.1）
                siann = "w"
                # un 保持以 u 起頭，例如 u / un / unn

    # 4. 【台語音標】調號轉換成【閩拼音標】調號
    tiau_mia = TLPA_TIAU_HO_PIAU.get(tiau, tiau)
    tiau = BP_TIAU_HO_PIAU.get(tiau_mia, tiau_mia)
    return f"{siann}{un}{tiau}"


def main(infile: str, outfile: str):
    """
    將 TLPA 編碼的 Rime 字典檔轉換為注音（Bopomofo，BP）形式並寫入輸出檔案。
    行為概述
    - 以 UTF-8 開啟輸入檔與輸出檔。
    - 假設輸入檔為典型的 Rime 字典文字檔，包含標頭區與詞條區；詞條區由一行僅含 "..."（去除空白後相等）開始。
    - 在標頭區：
        - 保留原始行內容不變，但若某行在去除前後空白後以 "name:" 開頭，則用模組層級變數 JI_KHOO_NAME 的值取代整行，格式為 "name: {JI_KHOO_NAME}\n"。
    - 在詞條區：
        - 保留空白行與以 "#" 開頭的註解行原樣不動。
        - 假設詞條行為以 tab 分隔的欄位（欄位1\t欄位2\t...）。若某行至少有兩個欄位，則會將第二欄（index 1）交由 convert_TLPA_to_BP(original) 轉換，並以轉換後的結果取代，再以 tab 重新組合寫出。
        - 若欄位數少於兩個，則保留原行不變。
    - 所有輸出行的行尾統一為 "\n"。
    副作用與輸出
    - 會將轉換後的內容寫入指定的 outfile 路徑（若存在則覆寫）。
    - 轉換完成後會印出訊息："轉換完成，結果已寫入 {outfile}"。
    相依與前置條件
    - 模組層級需定義 JI_KHOO_NAME（字串）以供標頭替換使用。
    - 需提供函式 convert_TLPA_to_BP(s: str) -> str：接受 TLPA 字串並回傳對應的注音字串。
    - 輸入檔應為可由 UTF-8 解碼的文字檔。
    例外與錯誤處理
    - 可能會拋出 FileNotFoundError、OSError 或其他 I/O 相關錯誤，若讀寫檔案失敗將向上傳播。
    - 若 convert_TLPA_to_BP 在處理某些字串時拋例外，該例外會向上傳播。
    回傳值
    - None。此函式以檔案 I/O 與列印為副作用。
    """
    with open(infile, "r", encoding="utf-8") as fin:
        lines = fin.readlines()

    out_lines = []
    in_entries = False
    for line in lines:
        # name 欄位自動更換
        if line.strip().startswith("name:"):
            out_lines.append(f"name: {JI_KHOO_NAME}\n")
            continue
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
    import os

    # 取得專案根目錄（假設此工具在 tools/ 目錄下）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # 上一層目錄即為專案根目錄

    # 設定預設檔案路徑（相對於專案根目錄）
    default_infile = os.path.join(project_root, "tl_ji_khoo_peh_ue.dict.yaml")
    default_outfile = os.path.join(project_root, "bp_ji_khoo.dict.yaml")

    # 解析命令列參數
    infile = sys.argv[1] if len(sys.argv) > 1 else default_infile
    outfile = sys.argv[2] if len(sys.argv) > 2 else default_outfile

    # 顯示使用的檔案路徑
    print(f"輸入檔案：{infile}")
    print(f"輸出檔案：{outfile}")

    # 檢查輸入檔案是否存在
    if not os.path.exists(infile):
        print(f"錯誤：輸入檔案不存在 - {infile}")
        sys.exit(1)

    main(infile, outfile)
