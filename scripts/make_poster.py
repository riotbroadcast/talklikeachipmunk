"""Add the talklikeachipmunk.com URL to the poster and save a print-ready copy.

The URL is rendered in the same multi-coloured outlined style as the title
(orange / yellow / green / blue / purple), so it reads as part of the artwork
rather than a separate sticker.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "Talk like a chipmunk sign.png"
DST = ROOT / "assets" / "Talk like a chipmunk poster.png"

URL_TEXT = "talklikeachipmunk.com"

# Colours sampled from the title in the original artwork
INK = (42, 42, 58)
PALETTE = [
    (255, 122, 61),   # orange
    (255, 204, 51),   # yellow
    (108, 194, 74),   # green
    (52, 182, 228),   # blue
    (139, 92, 246),   # purple
]

FONT_CANDIDATES = [
    # (path, ttc_index_or_None) — heaviest, roundest first
    ("/System/Library/Fonts/Supplemental/Comic Sans MS Bold.ttf", None),
    ("/System/Library/Fonts/Supplemental/Chalkboard SE.ttc", 1),
    ("/System/Library/Fonts/Supplemental/Impact.ttf", None),
]


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for path, idx in FONT_CANDIDATES:
        if Path(path).exists():
            try:
                if idx is not None:
                    return ImageFont.truetype(path, size, index=idx)
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def color_for(ch: str, idx: int) -> tuple[int, int, int]:
    """Pick a palette colour, but skip yellow for the dot so it stays legible."""
    color = PALETTE[idx % len(PALETTE)]
    if ch == "." and color == PALETTE[1]:
        return PALETTE[0]
    return color


def measure(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont,
            stroke: int) -> tuple[int, int, int]:
    """Return (total visual width, max ascent above baseline, max descent below).

    Letters are drawn at consecutive pen positions; their outline strokes overlap
    cleanly between neighbours since they share the same stroke colour. The
    visual width is therefore the sum of glyph advances plus one stroke of
    padding at each end of the word.
    """
    ascent = descent = 0
    width = 0
    for ch in text:
        bbox = draw.textbbox((0, 0), ch, font=font, stroke_width=stroke,
                             anchor="ls")
        ascent = max(ascent, -bbox[1])
        descent = max(descent, bbox[3])
        width += int(draw.textlength(ch, font=font))
    return width + 2 * stroke, ascent, descent


def main() -> None:
    src = Image.open(SRC).convert("RGBA")
    w, h = src.size

    # Extra space at the bottom for the URL band
    band_h = 320
    canvas = Image.new("RGBA", (w, h + band_h), (255, 255, 255, 255))
    canvas.paste(src, (0, 0), src)

    # We render the URL at a generous size, auto-shrinking until it fits with margins
    side_margin = 110
    max_width = w - 2 * side_margin
    stroke = 14
    font_size = 230

    draw = ImageDraw.Draw(canvas)
    while font_size > 60:
        font = load_font(font_size)
        tw, ascent, descent = measure(draw, URL_TEXT, font, stroke)
        if tw <= max_width:
            break
        font_size -= 6

    # Vertical placement: centre the cap-height inside the band
    band_top = h
    band_center_y = band_top + band_h // 2
    baseline_y = band_center_y + (ascent - descent) // 2

    # First letter's left outline starts at the visual-left edge of the word
    word_left = (w - tw) // 2
    pen_start = word_left + stroke

    # --- Soft drop shadow under the whole word (single pass, blurred) ---
    shadow_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_layer)
    x_cursor = pen_start
    for i, ch in enumerate(URL_TEXT):
        sdraw.text((x_cursor + 8, baseline_y + 10), ch, font=font,
                   fill=(0, 0, 0, 110), stroke_width=stroke,
                   stroke_fill=(0, 0, 0, 110), anchor="ls")
        x_cursor += int(draw.textlength(ch, font=font))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(6))
    canvas.alpha_composite(shadow_layer)

    # --- The actual letters: outlined, alternating palette colours ---
    x_cursor = pen_start
    color_idx = 0
    for ch in URL_TEXT:
        if ch == ".":
            fill = INK
        else:
            fill = color_for(ch, color_idx)
            color_idx += 1
        draw.text((x_cursor, baseline_y), ch, font=font, fill=fill,
                  stroke_width=stroke, stroke_fill=INK, anchor="ls")
        x_cursor += int(draw.textlength(ch, font=font))

    # --- Decorative stars on either side of the URL, like the confetti above ---
    star_y = band_center_y
    for cx, color in [
        (word_left - 60, PALETTE[2]),
        (word_left + tw + 60, PALETTE[0]),
    ]:
        draw_star(draw, cx, star_y, r=32, fill=color, outline=INK, width=8)

    canvas.convert("RGB").save(DST, "PNG", optimize=True)
    print(f"Wrote {DST} ({canvas.size[0]}x{canvas.size[1]}) at font size {font_size}")


def draw_star(draw: ImageDraw.ImageDraw, cx: int, cy: int, r: int,
              fill, outline, width: int) -> None:
    """Draw a chunky 5-point star centred on (cx, cy)."""
    import math
    points = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        radius = r if i % 2 == 0 else r * 0.45
        points.append((cx + radius * math.cos(angle),
                       cy + radius * math.sin(angle)))
    draw.polygon(points, fill=fill, outline=outline, width=width)


if __name__ == "__main__":
    main()
