"""Add the talklikeachipmunk.com URL to the poster and save a print-ready copy."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "Talk like a chipmunk sign.png"
DST = ROOT / "assets" / "Talk like a chipmunk poster.png"

URL_TEXT = "talklikeachipmunk.com"

INK = (42, 42, 58, 255)        # dark navy
YELLOW = (255, 204, 51, 255)   # banner fill
ORANGE = (255, 122, 61, 255)   # accent
WHITE = (255, 255, 255, 255)

FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Chalkboard SE.ttc",
    "/System/Library/Fonts/Supplemental/Comic Sans MS Bold.ttf",
    "/System/Library/Fonts/Supplemental/Impact.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
]


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            try:
                # ttc files: Chalkboard SE has Bold at index 1
                if path.endswith(".ttc"):
                    return ImageFont.truetype(path, size, index=1)
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def main() -> None:
    src = Image.open(SRC).convert("RGBA")
    w, h = src.size

    band_h = 300
    new = Image.new("RGBA", (w, h + band_h), WHITE)
    new.paste(src, (0, 0), src)

    draw = ImageDraw.Draw(new)

    # Banner pill centered in the new strip — sized to fit comfortably with margins
    pad_x, pad_y = 70, 28
    side_margin = 120
    max_text_width = w - 2 * side_margin - 2 * pad_x
    font_size = 200
    while font_size > 60:
        font = load_font(font_size)
        bbox = draw.textbbox((0, 0), URL_TEXT, font=font)
        if (bbox[2] - bbox[0]) <= max_text_width:
            break
        font_size -= 4
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    pill_w = tw + pad_x * 2
    pill_h = th + pad_y * 2
    pill_x0 = (w - pill_w) // 2
    pill_y0 = h + (band_h - pill_h) // 2
    pill_x1 = pill_x0 + pill_w
    pill_y1 = pill_y0 + pill_h
    radius = pill_h // 2

    # Drop shadow
    shadow_offset = 12
    draw.rounded_rectangle(
        [pill_x0 + shadow_offset, pill_y0 + shadow_offset,
         pill_x1 + shadow_offset, pill_y1 + shadow_offset],
        radius=radius, fill=(0, 0, 0, 60),
    )

    # Outlined yellow pill
    draw.rounded_rectangle(
        [pill_x0, pill_y0, pill_x1, pill_y1],
        radius=radius, fill=YELLOW, outline=INK, width=10,
    )

    # URL text centered in pill
    text_x = pill_x0 + (pill_w - tw) // 2 - bbox[0]
    text_y = pill_y0 + (pill_h - th) // 2 - bbox[1]
    draw.text((text_x, text_y), URL_TEXT, font=font, fill=INK)

    # Tiny accent dots on each side of the pill
    dot_r = 14
    cy = (pill_y0 + pill_y1) // 2
    for dx in (-60, -30):
        draw.ellipse([pill_x0 + dx - dot_r, cy - dot_r,
                      pill_x0 + dx + dot_r, cy + dot_r], fill=ORANGE)
    for dx in (30, 60):
        draw.ellipse([pill_x1 + dx - dot_r, cy - dot_r,
                      pill_x1 + dx + dot_r, cy + dot_r], fill=ORANGE)

    new.convert("RGB").save(DST, "PNG", optimize=True)
    print(f"Wrote {DST} ({new.size[0]}x{new.size[1]})")


if __name__ == "__main__":
    main()
