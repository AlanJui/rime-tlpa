# -*- coding: utf-8 -*-
"""
從梁烱輝《臺灣閩南語傳統語文教育文讀音系統之調查與研究》
資料篇附表三（D-403～D-500）抽「漢字 + 台羅拼音」試作字典。

規則（依使用者 2026-09-17）：
- 漢字：【單字出現次數】如 蓬0003 → 蓬
- 標音字母：【發音人文讀音（聲調取調值）】
- 調值→調號：55=1, 53=2, 11=3, 30=4, 13=5, 33=7, 50=8
- 調值讀不到或非上列七種 → 改用彙集雅俗通【聲調】
- 論文 TLPA → 台羅：ch→tsh，再 c→ts
"""
from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np
import pymupdf
from opencc import OpenCC
from rapidocr_onnxruntime import RapidOCR

PDF = Path(r"c:\Users\AlanJui\OneDrive\漢語\804592428-梁烱輝-臺灣閩南語傳統語文教育文讀音系統之調查與研究.pdf")
OUT_DIR = Path(__file__).resolve().parent
# D-n 的 PDF 頁碼 = 528 + n（D-1 = p.529）
D_FIRST, D_LAST = 403, 500

TONE_VALUE = {
    "55": 1,
    "53": 2,
    "11": 3,
    "30": 4,
    "13": 5,
    "33": 7,
    "50": 8,
}
SNI_TONE = {
    "上平": 1,
    "上上": 2,
    "上去": 3,
    "上入": 4,
    "下平": 5,
    "下去": 7,
    "下入": 8,
}
SNI_FIX = (
    ("下至", "下平"),
    ("下卒", "下平"),
    ("下乎", "下平"),
    ("上卒", "上平"),
    ("上乎", "上平"),
    ("上李", "上平"),
    ("上平", "上平"),
    ("地上去", "上去"),
)

HAN_COUNT = re.compile(r"([\u4e00-\u9fff])0?(\d{3,4})")
ROMAN = re.compile(r"\b([a-z]{1,8})([0-9]{2})?\b", re.I)
TONE_TAIL = re.compile(r"([a-z]{1,8})\s*([0-9]{2})", re.I)
ZI_XU = re.compile(r"^\d+(?:-\d+){1,3}$")
SKIP_ROW = re.compile(r"內轉|外轉|附表|字序|單字|出現|文讀")
_CC = OpenCC("s2t")


def d_to_index(d_page: int) -> int:
    return 527 + d_page  # D-403 → index 930


def pixmap_to_array(pix: pymupdf.Pixmap) -> np.ndarray:
    arr = np.frombuffer(pix.samples, dtype=np.uint8)
    arr = arr.reshape(pix.height, pix.width, pix.n)
    if pix.n == 4:
        arr = arr[:, :, :3]
    return arr


def to_tailo(roman: str) -> str:
    s = roman.lower()
    s = s.replace("ch", "tsh")
    s = s.replace("c", "ts")
    return s


def sni_tone_of(text: str) -> int | None:
    t = text
    for a, b in SNI_FIX:
        t = t.replace(a, b)
    for name, num in SNI_TONE.items():
        if name in t:
            return num
    return None


def parse_tone_value(text: str) -> int | None:
    """只接受黏在羅馬字後的兩位調值（hong13、bong55#）。"""
    compact = re.sub(r"[^a-z0-9#]", "", text.lower())
    m = re.search(r"^[a-z]{1,10}(55|53|11|30|13|33|50)#?$", compact)
    if m:
        return TONE_VALUE[m.group(1)]
    return None


def cluster_rows(items: list, y_tol: float = 18.0) -> list[list]:
    """items: (y, x, text)"""
    if not items:
        return []
    items = sorted(items, key=lambda t: (t[0], t[1]))
    rows: list[list] = []
    cur = [items[0]]
    y0 = items[0][0]
    for it in items[1:]:
        if abs(it[0] - y0) <= y_tol:
            cur.append(it)
        else:
            rows.append(cur)
            cur = [it]
            y0 = it[0]
    rows.append(cur)
    return rows


def parse_row(cells: list[tuple]) -> dict | None:
    texts = [t for _, _, t in sorted(cells, key=lambda c: c[1])]
    joined = " ".join(texts)
    if SKIP_ROW.search(joined) and not HAN_COUNT.search(joined):
        return None

    han = None
    count = None
    for t in texts:
        m = HAN_COUNT.search(t)
        if m:
            han, count = m.group(1), int(m.group(2))
            break
    if not han:
        return None
    han = _CC.convert(han)

    # 文讀音在「單字」右側、反切（如 2-36）左側
    roman = None
    tone_from_value = None
    for t in texts:
        tl = t.lower().replace("#", "").replace("＃", "")
        tl = tl.replace("'", "").replace('"', "")
        m = re.fullmatch(r"([a-z]{1,10})(\d{2})?", tl)
        if m and not ZI_XU.fullmatch(t):
            roman = m.group(1)
            if m.group(2) and m.group(2) in TONE_VALUE:
                tone_from_value = TONE_VALUE[m.group(2)]
            break
        m = TONE_TAIL.search(tl)
        if m:
            roman = m.group(1)
            if m.group(2) in TONE_VALUE:
                tone_from_value = TONE_VALUE[m.group(2)]
            break

    if not roman:
        # 退而求：列中第一個純字母 token
        for t in texts:
            tl = re.sub(r"[^a-z]", "", t.lower())
            if 1 <= len(tl) <= 10 and not ZI_XU.fullmatch(t):
                roman = tl
                break
    if not roman:
        return None

    if tone_from_value is None:
        for t in texts:
            # 不可拿字序／反切的數字當調值
            if ZI_XU.fullmatch(t) or re.fullmatch(r"\d+-\d+", t):
                continue
            if re.search(r"[\u4e00-\u9fff]", t) and not re.search(r"[a-zA-Z]", t):
                continue
            tv = parse_tone_value(t)
            if tv:
                tone_from_value = tv
                break

    tone_from_sni = None
    sni_label = ""
    for t in texts:
        st = sni_tone_of(t)
        if st:
            tone_from_sni = st
            t2 = t
            for a, b in SNI_FIX:
                t2 = t2.replace(a, b)
            for name in SNI_TONE:
                if name in t2:
                    sni_label = name
                    break
            break

    # 上標調值幾乎都會被 OCR 吃掉；讀不到或非七種調值 → 十五音聲調
    if tone_from_value is not None:
        tone, tone_src = tone_from_value, "調值"
    elif tone_from_sni is not None:
        tone, tone_src = tone_from_sni, "十五音聲調"
    else:
        return None

    code = f"{to_tailo(roman)}{tone}"
    return {
        "han": han,
        "count": count or 0,
        "roman_raw": roman,
        "code": code,
        "tone": tone,
        "tone_src": tone_src,
        "sni": sni_label,
        "raw": joined,
    }


def ocr_d_page(ocr: RapidOCR, doc: pymupdf.Document, d_page: int) -> list[dict]:
    page = doc[d_to_index(d_page)]
    clip = pymupdf.Rect(0, 40, page.rect.width * 0.56, page.rect.height - 28)
    pix = page.get_pixmap(matrix=pymupdf.Matrix(3.0, 3.0), clip=clip, alpha=False)
    img = pixmap_to_array(pix)
    result, _ = ocr(img)
    if not result:
        return []
    items = []
    for box, text, _score in result:
        if not text or not str(text).strip():
            continue
        y = min(p[1] for p in box)
        x = min(p[0] for p in box)
        items.append((y, x, str(text).strip()))
    rows = cluster_rows(items, y_tol=22.0)
    out = []
    for cells in rows:
        rec = parse_row(cells)
        if rec:
            rec["d_page"] = d_page
            out.append(rec)
    return out


def looks_like_syllable(code: str) -> bool:
    m = re.fullmatch(r"([a-z]+)([1-8])", code)
    if not m:
        return False
    r = m.group(1)
    if r in {"a", "e", "i", "o", "u", "m", "ng", "oo", "ai", "au", "ia", "iu", "io", "ua", "ui", "ue"}:
        return True
    if not re.search(r"[aeiou]", r):
        return False
    return len(r) >= 2


def write_dict(rows: list[dict], path: Path) -> None:
    # 同漢字同音碼：保留較大出現次數
    merged: dict[tuple[str, str], dict] = {}
    for r in rows:
        if not looks_like_syllable(r["code"]):
            continue
        key = (r["han"], r["code"])
        if key not in merged or r["count"] > merged[key]["count"]:
            merged[key] = r
    items = sorted(merged.values(), key=lambda r: (-r["count"], r["code"], r["han"]))
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# Rime dictionary",
        "# encoding: utf-8",
        "#",
        "# 梁烱輝（2001）《臺灣閩南語傳統語文教育文讀音系統之調查與研究》",
        "# 資料篇附表三 發音人文讀音試作（D-403–D-500；D-5000 視為 D-500）",
        "# 字母：論文 TLPA（先 ch→tsh，再 c→ts）",
        "# 調號：上標調值 OCR 不穩，本試作以彙集雅俗通【聲調】為準",
        "# 漢字為掃描 OCR，須人工校對後才能匯入正式字庫",
        "#",
        "---",
        "name: ji_khoo_tl_LiangBunThak",
        'version: "v0.0.1-proto"',
        "sort: by_weight",
        "use_preset_vocabulary: false",
        "columns:",
        "  - text",
        "  - code",
        "  - weight",
        "  - stem",
        "  - create",
        "...",
        "",
    ]
    for r in items:
        if not looks_like_syllable(r["code"]):
            continue
        stem = f"D-{r['d_page']} {r['tone_src']} n={r['count']}"
        lines.append(f"{r['han']}\t{r['code']}\t{r['count']}\t{stem}\t{today}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def regen_from_tsv() -> None:
    tsv = OUT_DIR / "fubiao3_extract.tsv"
    rows = []
    with tsv.open(encoding="utf-8", newline="") as f:
        for rec in csv.DictReader(f, delimiter="\t"):
            rec["d_page"] = int(rec["d_page"])
            rec["count"] = int(rec["count"] or 0)
            rec["tone"] = int(rec["tone"] or 0)
            rows.append(rec)
    dict_path = OUT_DIR / "ji_khoo_tl_LiangBunThak.dict.yaml"
    write_dict(rows, dict_path)
    kept = [r for r in rows if looks_like_syllable(r["code"])]
    print("tsv", len(rows), "syllable_ok", len(kept), "unique", len({(r["han"], r["code"]) for r in kept}))
    print("wrote", dict_path)


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--from-tsv":
        regen_from_tsv()
        return
    d0 = int(sys.argv[1]) if len(sys.argv) > 1 else D_FIRST
    d1 = int(sys.argv[2]) if len(sys.argv) > 2 else D_LAST
    print(f"PDF={PDF}")
    print(f"pages D-{d0} .. D-{d1}")
    ocr = RapidOCR()
    doc = pymupdf.open(str(PDF))
    all_rows: list[dict] = []
    tsv = OUT_DIR / "fubiao3_extract.tsv"
    with tsv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["d_page", "han", "count", "roman_raw", "code", "tone", "tone_src", "sni", "raw"],
            delimiter="\t",
        )
        w.writeheader()
        for d in range(d0, d1 + 1):
            recs = ocr_d_page(ocr, doc, d)
            all_rows.extend(recs)
            for r in recs:
                w.writerow(r)
            print(f"D-{d:03d}  rows={len(recs):3d}  total={len(all_rows)}")
            f.flush()
    doc.close()
    dict_path = OUT_DIR / "ji_khoo_tl_LiangBunThak.dict.yaml"
    write_dict(all_rows, dict_path)
    src = defaultdict(int)
    for r in all_rows:
        src[r["tone_src"]] += 1
    print("tone_src", dict(src))
    print("unique", len({(r['han'], r['code']) for r in all_rows}))
    print("wrote", tsv)
    print("wrote", dict_path)


if __name__ == "__main__":
    main()
