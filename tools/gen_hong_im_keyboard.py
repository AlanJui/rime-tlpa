#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate 方音符號 keyboard images from the project key map.

Uses LXGW WenKai TC (霞鶩文楷 TC) and 3D keycaps.
Outputs:
  docs/static/img/hong_im_gian_buann.png
  docs/static/img/hong_im_gian_buann.svg
  docs/static/img/keys/key_*.png
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "static" / "img"
KEYS_DIR = OUT_DIR / "keys"

CREAM = (236, 224, 196)
CREAM_DIM = (186, 176, 154)
CREAM_WARM = (232, 168, 150)
DESK = (232, 232, 236)
# 鍵帽接近方形；英文字母與鍵面邊緣固定 6px。
CORNER_RATIO = 0.04
LABEL_INSET_PX = 6

# Dark 3D keycap faces, matching the navy sample while keeping 聲/韻/調 distinction.
PALETTE = {
    "blue": {"face": (24, 28, 56), "lip": (12, 14, 30)},   # 聲母
    "yellow": {"face": (58, 46, 18), "lip": (32, 24, 8)},  # 調號
    "peach": {"face": (46, 28, 34), "lip": (26, 14, 18)},  # 韻母
}


def _first_existing(paths: list[Path | str]) -> str:
    for path in paths:
        p = Path(path)
        if p.exists():
            return str(p)
    raise SystemExit("LXGW WenKai TC was not found. Install 霞鶩文楷 TC first.")


_USER_FONTS = Path.home() / "AppData/Local/Microsoft/Windows/Fonts"
CJK_FONT_PATH = _first_existing([
    _USER_FONTS / "LXGWWenKaiTC-Regular.ttf",
    _USER_FONTS / "LXGWWenKaiTC-Medium.ttf",
    r"C:\Windows\Fonts\LXGWWenKaiTC-Regular.ttf",
    r"C:\Windows\Fonts\LXGWWenKaiTC-Medium.ttf",
])


def face_font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(CJK_FONT_PATH, size)


# kind: pair | single | tone | empty | coda
# bg: blue=聲母, yellow=調號, peach=韻母
KEYS = [
    dict(id="1", label="1", shift="!", bg="blue", kind="pair",
         top=("ㆠ", "b"), bottom=("ㄅ", "p")),
    dict(id="2", label="2", shift="@", bg="blue", kind="single",
         top=("ㄉ", "t")),
    dict(id="3", label="3", shift="#", bg="yellow", kind="tone",
         name="陰去", mark="`"),
    dict(id="4", label="4", shift="$", bg="yellow", kind="tone",
         name="上声", mark="ˋ"),
    dict(id="5", label="5", shift="%", bg="yellow", kind="tone",
         name="陽去", mark="´"),
    dict(id="6", label="6", shift="^", bg="yellow", kind="tone",
         name="陽平", mark="·"),
    dict(id="7", label="7", shift="&", bg="yellow", kind="tone",
         name="入声", mark="˙"),
    dict(id="8", label="8", shift="*", bg="peach", kind="pair",
         top=("ㆩ", "ann"), bottom=("ㄚ", "a")),
    dict(id="9", label="9", shift="(", bg="peach", kind="pair",
         top=("ㆮ", "ainn"), bottom=("ㄞ", "ai")),
    dict(id="0", label="0", shift=")", bg="peach", kind="single",
         top=("ㄢ", "an")),
    dict(id="minus", label="-", shift="_", bg="peach", kind="single",
         top=("ñ", "*nn")),
    dict(id="equal", label="=", shift="+", bg="peach", kind="single",
         top=("ㄥ", "*a")),
    dict(id="q", label="Q", shift="", bg="blue", kind="single",
         top=("ㄆ", "ph")),
    dict(id="w", label="W", shift="", bg="blue", kind="single",
         top=("ㄊ", "th")),
    dict(id="e", label="E", shift="", bg="blue", kind="pair",
         top=("ㆣ", "g"), bottom=("ㄍ", "k")),
    dict(id="r", label="R", shift="", bg="blue", kind="pair",
         top=("ㆢ", "j"), bottom=("ㄐ", "z")),
    dict(id="t", label="T", shift="", bg="blue", kind="single",
         top=("ㆵ", "t0")),
    dict(id="y", label="Y", shift="", bg="blue", kind="pair",
         top=("ㆡ", "j"), bottom=("ㄗ", "z")),
    dict(id="u", label="U", shift="", bg="peach", kind="pair",
         top=("ㆪ", "inn"), bottom=("ㄧ", "i")),
    dict(id="i", label="I", shift="", bg="peach", kind="pair",
         top=("ㆧ", "onn"), bottom=("ㆦ", "oo")),
    dict(id="o", label="O", shift="", bg="peach", kind="pair",
         top=("ㆱ", "om"), bottom=("ㆲ", "ong")),
    dict(id="p", label="P", shift="", bg="peach", kind="single",
         top=("ㄣ", "-n")),
    dict(id="lbracket", label="[", shift="{", bg="peach", kind="empty"),
    dict(id="rbracket", label="]", shift="}", bg="peach", kind="empty"),
    dict(id="backslash", label="\\", shift="|", bg="peach", kind="empty"),
    dict(id="a", label="A", shift="", bg="blue", kind="single",
         top=("ㄇ", "m")),
    dict(id="s", label="S", shift="", bg="blue", kind="single",
         top=("ㄋ", "n")),
    dict(id="d", label="D", shift="", bg="blue", kind="single",
         top=("ㄎ", "kh")),
    dict(id="f", label="F", shift="", bg="blue", kind="single",
         top=("ㄑ", "c")),
    dict(id="g", label="G", shift="", bg="blue", kind="single",
         top=("ㆶ", "k0")),
    dict(id="h", label="H", shift="", bg="blue", kind="single",
         top=("ㄘ", "c")),
    dict(id="j", label="J", shift="", bg="peach", kind="pair",
         top=("ㆫ", "unn"), bottom=("ㄨ", "u")),
    dict(id="k", label="K", shift="", bg="peach", kind="pair",
         top=("ㆨ", "ir"), bottom=("ㄜ", "or")),
    dict(id="l", label="L", shift="", bg="peach", kind="pair",
         top=("ㆯ", "aunn"), bottom=("ㄠ", "au")),
    dict(id="semicolon", label=";", shift=":", bg="peach", kind="single",
         top=("ㄤ", "ang")),
    dict(id="quote", label="'", shift='"', bg="peach", kind="coda",
         top=("入", "ptkh")),
    dict(id="z", label="Z", shift="", bg="blue", kind="single",
         top=("ㆷ", "h0")),
    dict(id="x", label="X", shift="", bg="blue", kind="single",
         top=("ㄌ", "l")),
    dict(id="c", label="C", shift="", bg="blue", kind="single",
         top=("ㄏ", "h")),
    dict(id="v", label="V", shift="", bg="blue", kind="single",
         top=("ㄒ", "s")),
    dict(id="b", label="B", shift="", bg="blue", kind="single",
         top=("ㆴ", "p0")),
    dict(id="n", label="N", shift="", bg="blue", kind="pair",
         top=("ㄫ", "ng"), bottom=("ㄙ", "s")),
    dict(id="m", label="M", shift="", bg="peach", kind="pair",
         top=("ㆰ", "am"), bottom=("ㆬ", "-m")),
    dict(id="comma", label=",", shift="<", bg="peach", kind="pair",
         top=("ㆥ", "enn"), bottom=("ㆤ", "e")),
    dict(id="period", label=".", shift=">", bg="peach", kind="coda",
         top=("入", "ptkh")),
    dict(id="slash", label="/", shift="?", bg="peach", kind="single",
         top=("ㆭ", "-ng")),
]

ROWS = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "minus", "equal"],
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "lbracket", "rbracket", "backslash"],
    ["a", "s", "d", "f", "g", "h", "j", "k", "l", "semicolon", "quote"],
    ["z", "x", "c", "v", "b", "n", "m", "comma", "period", "slash"],
]


def key_by_id(key_id: str) -> dict:
    return next(k for k in KEYS if k["id"] == key_id)


def _lerp(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _vertical_gradient(size: tuple[int, int], top: tuple[int, int, int], bot: tuple[int, int, int]) -> Image.Image:
    w, h = size
    strip = Image.new("RGB", (1, max(h, 1)))
    px = strip.load()
    last = max(h - 1, 1)
    for y in range(h):
        px[0, y] = _lerp(top, bot, y / last)
    return strip.resize((w, h), Image.Resampling.BILINEAR)


def _rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def make_keycap(size: tuple[int, int], face: tuple[int, int, int], lip: tuple[int, int, int], scale: float):
    """Return (keycap RGBA, face_box in keycap coords, pad)."""
    w, h = size
    radius = max(6, int(min(w, h) * CORNER_RATIO))
    pad = int(max(8, 10 * scale))
    lip_h = int(max(6, 9 * scale))
    inset = int(max(3, 4 * scale))
    canvas_w, canvas_h = w + pad * 2, h + pad * 2 + int(4 * scale)
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

    shadow = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (pad + int(2 * scale), pad + int(6 * scale), pad + w + int(2 * scale), pad + h + int(8 * scale)),
        radius=radius,
        fill=(0, 0, 0, 110),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=max(2, int(4.5 * scale))))
    canvas = Image.alpha_composite(canvas, shadow)

    body = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    ImageDraw.Draw(body).rounded_rectangle(
        (pad, pad, pad + w, pad + h), radius=radius, fill=lip + (255,)
    )

    fx0, fy0 = pad + inset, pad + inset
    fx1, fy1 = pad + w - inset, pad + h - lip_h
    fw, fh = max(fx1 - fx0, 1), max(fy1 - fy0, 1)
    face_r = max(4, radius - max(1, inset // 2))

    top = _lerp(face, (255, 255, 255), 0.18)
    bot = _lerp(face, (0, 0, 0), 0.10)
    grad = _vertical_gradient((fw, fh), top, bot)
    fmask = _rounded_mask((fw, fh), face_r)
    face_rgba = Image.new("RGBA", (fw, fh))
    face_rgba.paste(grad, mask=fmask)

    sheen = Image.new("RGB", (fw, fh), (255, 255, 255))
    sheen_a = Image.new("L", (fw, fh), 0)
    spx = sheen_a.load()
    fade = max(int(fh * 0.42), 1)
    for y in range(fade):
        alpha = int(48 * (1 - y / fade))
        for x in range(fw):
            spx[x, y] = alpha
    sheen_a = ImageChops.multiply(sheen_a, fmask)
    face_rgba = Image.alpha_composite(face_rgba, Image.merge("RGBA", (*sheen.split(), sheen_a)))

    body.paste(face_rgba, (fx0, fy0), face_rgba)
    canvas = Image.alpha_composite(canvas, body)
    return canvas, (fx0, fy0, fx1, fy1), pad


def draw_legend(draw: ImageDraw.ImageDraw, box, spec, scale: float) -> None:
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    kind = spec["kind"]
    inset = LABEL_INSET_PX

    f_lbl = face_font(max(20, int(24 * scale)))
    f_big = face_font(max(32, int(42 * scale)))
    f_sym = face_font(max(24, int(30 * scale)))
    f_rom = face_font(max(14, int(17 * scale)))
    f_tone = face_font(max(20, int(24 * scale)))
    f_mark = face_font(max(24, int(30 * scale)))

    draw.text((x0 + inset, y0 + inset), spec["label"], font=f_lbl, fill=CREAM, anchor="lt")
    if spec.get("shift"):
        draw.text((x1 - inset, y0 + inset), spec["shift"], font=f_lbl, fill=CREAM_DIM, anchor="rt")

    cx, rx = x0 + w * 0.38, x0 + w * 0.78
    top_y, bot_y, mid_y = y0 + h * 0.48, y0 + h * 0.80, y0 + h * 0.58

    if kind == "empty":
        return
    if kind == "tone":
        draw.text((x0 + w * 0.5, y0 + h * 0.52), spec["name"], font=f_tone, fill=CREAM, anchor="mm")
        draw.text((x0 + w * 0.5, y0 + h * 0.80), spec["mark"], font=f_mark, fill=CREAM, anchor="mm")
        return
    if kind == "pair":
        ts, tr = spec["top"]
        bs, br = spec["bottom"]
        draw.text((cx, top_y), ts, font=f_big, fill=CREAM, anchor="mm")
        draw.text((rx, top_y), tr, font=f_rom, fill=CREAM_DIM, anchor="mm")
        draw.text((cx, bot_y), bs, font=f_sym, fill=CREAM_WARM, anchor="mm")
        draw.text((rx, bot_y), br, font=f_rom, fill=CREAM_DIM, anchor="mm")
        return

    ts, tr = spec["top"]
    color = CREAM_WARM if kind == "coda" else CREAM
    draw.text((cx, mid_y), ts, font=f_big, fill=color, anchor="mm")
    draw.text((rx, mid_y), tr, font=f_rom, fill=CREAM_DIM, anchor="mm")


def render_key_image(spec: dict, width: int, height: int, scale: float) -> Image.Image:
    colors = PALETTE[spec["bg"]]
    cap, face, _pad = make_keycap((width, height), colors["face"], colors["lip"], scale)
    draw_legend(ImageDraw.Draw(cap), face, spec, scale)
    return cap


def layout_board(key_w=168, key_h=148, gap=16, pad=36):
    indents = [0, int(key_w * 0.28), int(key_w * 0.48), int(key_w * 0.72)]
    boxes = {}
    y = pad
    max_x = 0
    for r, row in enumerate(ROWS):
        x = pad + indents[r]
        for kid in row:
            boxes[kid] = (x, y, x + key_w, y + key_h)
            x += key_w + gap
            max_x = max(max_x, x)
        y += key_h + gap
    return boxes, max_x + pad - gap, y + pad - gap


def render_board(scale=1.0) -> Image.Image:
    key_w, key_h, gap, pad = (int(v * scale) for v in (168, 148, 16, 40))
    boxes, width, height = layout_board(key_w, key_h, gap, pad)
    img = Image.new("RGBA", (width, height), DESK + (255,))
    for kid, (x0, y0, x1, y1) in boxes.items():
        cap = render_key_image(key_by_id(kid), x1 - x0, y1 - y0, scale)
        extra = (cap.size[0] - (x1 - x0)) // 2
        img.alpha_composite(cap, (x0 - extra, y0 - extra))
    return img.convert("RGB")


def svg_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_svg(key_w=168, key_h=148, gap=16, pad=40) -> str:
    boxes, width, height = layout_board(key_w, key_h, gap, pad)
    fills = {
        "blue": ("#2a3058", "#14182e"),
        "yellow": ("#6a5428", "#2a1e08"),
        "peach": ("#5a3840", "#221016"),
    }
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<defs>",
        '<filter id="keyShadow" x="-20%" y="-20%" width="140%" height="160%">'
        '<feDropShadow dx="2" dy="6" stdDeviation="4" flood-color="#000" flood-opacity="0.35"/>'
        "</filter>",
    ]
    for name, (top, bot) in fills.items():
        parts.append(
            f'<linearGradient id="g-{name}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0%" stop-color="{top}"/>'
            f'<stop offset="100%" stop-color="{bot}"/>'
            "</linearGradient>"
        )
    parts += [
        "</defs>",
        '<style>text{font-family:"LXGW WenKai TC","霞鶩文楷 TC",serif}</style>',
        f'<rect width="{width}" height="{height}" fill="#e8e8ec"/>',
    ]
    for kid, (x0, y0, x1, y1) in boxes.items():
        spec = key_by_id(kid)
        w, h = x1 - x0, y1 - y0
        rx = max(6, int(min(w, h) * CORNER_RATIO))
        lip = 8
        face_x, face_y = x0 + 4, y0 + 4
        parts.append(
            f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="{rx}" fill="#0c0e1e" filter="url(#keyShadow)"/>'
        )
        parts.append(
            f'<rect x="{face_x}" y="{face_y}" width="{w - 8}" height="{h - lip - 4}" rx="{max(4, rx - 2)}" '
            f'fill="url(#g-{spec["bg"]})"/>'
        )
        parts.append(
            f'<text x="{face_x + LABEL_INSET_PX}" y="{face_y + LABEL_INSET_PX + 14}" font-size="15" fill="#bab09a">{svg_escape(spec["label"])}</text>'
        )
        if spec.get("shift"):
            parts.append(
                f'<text x="{x1 - 4 - LABEL_INSET_PX}" y="{face_y + LABEL_INSET_PX + 14}" font-size="15" fill="#bab09a" text-anchor="end">'
                f'{svg_escape(spec["shift"])}</text>'
            )
        cx, rx_t = x0 + w * 0.36, x0 + w * 0.76
        if spec["kind"] == "tone":
            parts.append(
                f'<text x="{x0 + w / 2}" y="{y0 + h * 0.55}" font-size="20" text-anchor="middle" fill="#ece0c4">{spec["name"]}</text>'
            )
            parts.append(
                f'<text x="{x0 + w / 2}" y="{y0 + h * 0.80}" font-size="24" text-anchor="middle" fill="#ece0c4">{spec["mark"]}</text>'
            )
        elif spec["kind"] == "pair":
            ts, tr = spec["top"]
            bs, br = spec["bottom"]
            parts.append(
                f'<text x="{cx}" y="{y0 + h * 0.50}" font-size="32" text-anchor="middle" fill="#ece0c4">{ts}</text>'
            )
            parts.append(
                f'<text x="{rx_t}" y="{y0 + h * 0.50}" font-size="15" text-anchor="middle" fill="#bab09a">{svg_escape(tr)}</text>'
            )
            parts.append(
                f'<text x="{cx}" y="{y0 + h * 0.80}" font-size="24" text-anchor="middle" fill="#e8a896">{bs}</text>'
            )
            parts.append(
                f'<text x="{rx_t}" y="{y0 + h * 0.80}" font-size="15" text-anchor="middle" fill="#bab09a">{svg_escape(br)}</text>'
            )
        elif spec["kind"] in ("single", "coda"):
            ts, tr = spec["top"]
            fill_c = "#e8a896" if spec["kind"] == "coda" else "#ece0c4"
            parts.append(
                f'<text x="{cx}" y="{y0 + h * 0.62}" font-size="32" text-anchor="middle" fill="{fill_c}">{svg_escape(ts)}</text>'
            )
            parts.append(
                f'<text x="{rx_t}" y="{y0 + h * 0.62}" font-size="15" text-anchor="middle" fill="#bab09a">{svg_escape(tr)}</text>'
            )
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    KEYS_DIR.mkdir(parents=True, exist_ok=True)

    board = render_board(scale=1.25)
    board_path = OUT_DIR / "hong_im_gian_buann.png"
    board.save(board_path, "PNG", optimize=True)

    svg_path = OUT_DIR / "hong_im_gian_buann.svg"
    svg_path.write_text(render_svg(), encoding="utf-8")

    for spec in KEYS:
        img = render_key_image(spec, 320, 320, scale=2.0)
        img.save(KEYS_DIR / f"key_{spec['id']}.png", "PNG", optimize=True)

    print(f"font:  {CJK_FONT_PATH}")
    print(f"board: {board_path} {board.size}")
    print(f"svg:   {svg_path}")
    print(f"keys:  {KEYS_DIR} ({len(KEYS)} files)")


if __name__ == "__main__":
    main()
