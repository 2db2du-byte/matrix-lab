"""Matrix digital rain wallpapers for the ASUS (1366x768 screen, drawn at 2x)."""
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
CJK, MONO = "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc", "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Bold.ttf"
W, H = 2732, 1536
GLYPHS = "ｦｱｳｴｵｶｷｹｺｻｼｽｾｿﾀﾂﾃﾅﾆﾇﾈﾊﾋﾎﾏﾐﾑﾒﾓﾔﾕﾗﾘﾜ0123456789Z:.\"=*+-<>¦|"

def rain(seed, density, caption=None):
    rnd = random.Random(seed)
    img = Image.new("RGB", (W, H), (0, 0, 0))
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    size = 34
    font = ImageFont.truetype(CJK, size)
    d, g = ImageDraw.Draw(img), ImageDraw.Draw(glow)
    for x in range(0, W, size):
        if rnd.random() > density: continue
        head = rnd.randint(-H // 3, H + H // 2)
        length = rnd.randint(8, 40)
        for i in range(length):
            y = head - i * size
            if y < -size or y > H: continue
            ch = rnd.choice(GLYPHS)
            fade = 1 - i / length
            if i == 0:
                col = (210, 255, 220)                         # bright white-green head
                g.text((x, y), ch, font=font, fill=(0, 255, 70))
            else:
                col = (0, int(60 + 195 * fade), int(20 + 45 * fade))
            d.text((x, y), ch, font=font, fill=col)
    img = Image.composite(img, img, Image.new("L", (W, H), 255))
    img.paste(Image.blend(img, glow.filter(ImageFilter.GaussianBlur(10)), 0.0), (0, 0))
    img = Image.eval(Image.merge("RGB", [Image.blend(c, gc, 0) for c, gc in zip(img.split(), glow.filter(ImageFilter.GaussianBlur(10)).split())]), lambda v: v)
    from PIL import ImageChops
    img = ImageChops.add(img, glow.filter(ImageFilter.GaussianBlur(12)))
    if caption:
        f2 = ImageFont.truetype(MONO, 64)
        box = ImageDraw.Draw(img).textbbox((0, 0), caption, font=f2)
        tw, th = box[2] - box[0], box[3] - box[1]
        x0, y0 = (W - tw) // 2, (H - th) // 2
        ImageDraw.Draw(img).rectangle((x0 - 60, y0 - 40, x0 + tw + 60, y0 + th + 50), fill=(0, 0, 0))
        tg = Image.new("RGB", (W, H)); ImageDraw.Draw(tg).text((x0, y0), caption, font=f2, fill=(0, 255, 65))
        img = ImageChops.add(img, tg.filter(ImageFilter.GaussianBlur(6)))
        ImageDraw.Draw(img).text((x0, y0), caption, font=f2, fill=(0, 255, 65))
    return img

rain(1, 0.85, "Wake up, Rabbid...").save("1-wake-up-rabbid.png")
rain(2, 0.95).save("2-digital-rain.png")
rain(3, 0.45).save("3-quiet-rain.png")
print("ok")
