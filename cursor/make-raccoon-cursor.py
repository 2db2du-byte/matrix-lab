"""Raccoon cursor: classic arrow (hotspot = tip) with a 🦝 riding on its tail. Writes an Xcursor file with 24/32/48/64 px."""
import struct
from PIL import Image, ImageDraw, ImageFont

emoji_font = ImageFont.truetype("/usr/share/fonts/noto/NotoColorEmoji.ttf", 109)
big = Image.new("RGBA", (136, 128), (0, 0, 0, 0))
ImageDraw.Draw(big).text((0, 0), "🦝", font=emoji_font, embedded_color=True)
big = big.crop(big.getbbox())

def frame(n):
    S = 8                                      # draw 8x bigger, then shrink = smooth edges
    W = n * S
    im = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    u = W / 32                                 # design grid: 32 units
    arrow = [(1, 1), (1, 21), (6, 16.5), (9.5, 24), (12.5, 22.7), (9, 15.5), (16, 15.5)]
    pts = [((x + 1) * u, (y + 1) * u) for x, y in arrow]
    d.polygon(pts, fill=(255, 255, 255, 255))
    d.line(pts + [pts[0]], fill=(0, 0, 0, 255), width=max(1, int(1.6 * u)), joint="curve")
    r = big.resize((int(18 * u), int(17 * u * big.height / big.width)), Image.LANCZOS)
    im.alpha_composite(r, (int(13.5 * u), int(17 * u)))
    return im.resize((n, n), Image.LANCZOS)

sizes = [24, 32, 48, 64]
frames = {n: frame(n) for n in sizes}
frames[64].save("preview.png")
# Xcursor file format
hdr_len, chunk_hdr = 16, 36
tocs, chunks, pos = [], [], hdr_len + 12 * len(sizes)
for n in sizes:
    im = frames[n]
    px = b"".join(struct.pack("<I", (a << 24) | ((r * a // 255) << 16) | ((g * a // 255) << 8) | (b * a // 255)) for r, g, b, a in im.get_flattened_data())
    hot = max(1, round(n * 2 / 32))                # arrow tip
    chunk = struct.pack("<IIIIIIIII", chunk_hdr, 0xFFFD0002, n, 1, n, n, hot, hot, 0) + px
    tocs.append(struct.pack("<III", 0xFFFD0002, n, pos)); chunks.append(chunk); pos += len(chunk)
open("default", "wb").write(b"Xcur" + struct.pack("<III", hdr_len, 0x10000, len(sizes)) + b"".join(tocs) + b"".join(chunks))
print("ok", pos, "bytes")
