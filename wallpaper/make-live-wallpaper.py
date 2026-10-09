"""Seamless Matrix rain loop for the ASUS (1366x768). Every drop moves a whole number of laps per loop,
and glyph changes tick on a beat that divides the loop, so frame N == frame 0."""
import random, os
from PIL import Image, ImageDraw, ImageFont
W, H, FPS, SECS = 1366, 768, 20, 20
N = FPS * SECS
CELL = 18
font = ImageFont.truetype("/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc", 16)
G = "ｦｱｳｴｵｶｷｹｺｻｼｽｾｿﾀﾂﾃﾅﾆﾇﾈﾊﾋﾎﾏﾐﾑﾒﾓﾔﾕﾗﾘﾜ0123456789Z:.=*+-<>|"
rnd = random.Random(7)
cols = W // CELL + 1
rows = H // CELL + 1
LOOP = rows + 30                                     # a drop travels rows + tail space per lap
drops = []
for c in range(cols):
    for _ in range(rnd.choice([1, 1, 2])):
        laps = rnd.choice([1, 2, 2, 3, 3, 4])          # whole laps per loop = seamless
        drops.append((c, rnd.randrange(LOOP), laps, rnd.randint(8, 26)))
glyph_seed = [[rnd.randrange(10**6) for _ in range(rows + 1)] for _ in range(cols)]
def glyph(c, r, t):
    beat = (t // 5) % (N // 5)                         # changes every 5 frames, wraps with the loop
    return G[(glyph_seed[c][r % (rows + 1)] + beat * (c * 7 + r * 13 + 1)) % len(G)]
for t in range(N):
    img = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(img)
    for c, off, laps, tail in drops:
        head = (off + t * laps * LOOP // N) % LOOP
        for i in range(tail):
            r = head - i
            if 0 <= r < rows:
                fade = 1 - i / tail
                col = (190, 255, 205) if i == 0 else (0, int(50 + 190 * fade), int(15 + 45 * fade))
                d.text((c * CELL, r * CELL), glyph(c, r, t), font=font, fill=col)
    img.save(f"frames/{t:04d}.png")
print("frames", N)
