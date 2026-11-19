from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random

W = H = 1200
random.seed(6)
img = Image.new("RGB", (W, H))
px = img.load()
stops = [(0, (21, 12, 54)), (0.40, (171, 36, 121)), (0.72, (255, 119, 109)), (1, (31, 205, 196))]
for y in range(H):
    t = y / (H - 1)
    for i in range(len(stops) - 1):
        if stops[i][0] <= t <= stops[i + 1][0]:
            a, ca = stops[i]
            b, cb = stops[i + 1]
            f = (t - a) / (b - a)
            col = tuple(int(ca[k] * (1 - f) + cb[k] * f) for k in range(3))
            break
    for x in range(W):
        glow = max(0, 1 - math.sqrt(((x - 860) / 520) ** 2 + ((y - 610) / 400) ** 2))
        px[x, y] = tuple(min(255, int(c + glow * v)) for c, v in zip(col, (22, 9, 33)))

d = ImageDraw.Draw(img, "RGBA")
ANTON = "/usr/share/fonts/truetype/sand-box/google/Anton/Anton-Regular.ttf"
BEBAS = "/usr/share/fonts/truetype/sand-box/google/Bebas Neue/BebasNeue-Regular.ttf"
BLACK = "/usr/share/fonts/truetype/sand-box/google/Archivo Black/ArchivoBlack-Regular.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

# Distant Vice City skyline and the ocean horizon.
d.rectangle((0, 725, W, 900), fill=(13, 34, 76, 105))
d.line((0, 730, W, 730), fill=(255, 198, 226, 150), width=3)
for x, width, height in [(40, 80, 145), (135, 62, 220), (210, 105, 160), (335, 72, 255), (420, 90, 175), (525, 70, 225), (620, 115, 190), (760, 80, 250), (885, 65, 180), (990, 105, 235), (1110, 72, 160)]:
    y = 730 - height
    d.rectangle((x, y, x + width, 730), fill=(27, 18, 56, 235))
    d.rectangle((x + 8, y + 12, x + width - 8, y + 15), fill=(255, 77, 186, 185))
    for wy in range(y + 32, 720, 28):
        for wx in range(x + 12, x + width - 8, 19):
            d.rectangle((wx, wy, wx + 6, wy + 9), fill=(255, 204, 117, random.randint(90, 190)))

# Perspective Ocean Drive with neon lane edges.
d.polygon([(0, 900), (1200, 900), (1200, 1200), (0, 1200)], fill=(13, 13, 34, 250))
d.polygon([(425, 900), (775, 900), (1120, 1200), (80, 1200)], fill=(36, 23, 56, 235))
for yy, scale in [(930, 1), (1005, 1.5), (1100, 2.3)]:
    half = 2 + int(scale * 3)
    d.polygon([(595 - half, yy), (605 + half, yy), (620 + half * 2, yy + 25 * scale), (580 - half * 2, yy + 25 * scale)], fill=(255, 231, 166, 220))
d.line((425, 900, 80, 1200), fill=(255, 58, 202, 230), width=6)
d.line((775, 900, 1120, 1200), fill=(50, 244, 226, 230), width=6)

# Palm silhouettes frame the city.
for bx, direction in [(55, 1), (1115, -1)]:
    d.line((bx, 855, bx + direction * 15, 475), fill=(15, 12, 43, 255), width=24)
    crown = (bx + direction * 15, 475)
    for angle in [-165, -140, -115, -90, -65, -40, -15]:
        rad = math.radians(angle if direction == 1 else 180 - angle)
        ex = crown[0] + math.cos(rad) * 190
        ey = crown[1] + math.sin(rad) * 105
        d.line((crown[0], crown[1], ex, ey), fill=(12, 11, 39, 255), width=12)

# Giant rooftop make.fun sign: a neon advertisement built into the city.
d.rectangle((550, 320, 1175, 640), fill=(10, 9, 32, 250), outline=(248, 45, 196, 255), width=10)
d.rectangle((566, 336, 1159, 624), outline=(49, 240, 222, 210), width=4)
d.line((862, 640, 862, 765), fill=(20, 14, 38, 255), width=24)
d.line((815, 765, 909, 765), fill=(20, 14, 38, 255), width=22)
logo = Image.open("assets/press/mark-1024.png").convert("RGBA")
logo = logo.resize((270, 270), Image.Resampling.LANCZOS)
halo = Image.new("RGBA", (310, 310), (0, 0, 0, 0))
ImageDraw.Draw(halo).ellipse((12, 12, 298, 298), fill=(255, 34, 206, 110))
halo = halo.filter(ImageFilter.GaussianBlur(22))
img.paste(halo, (555, 325), halo)
img.paste(logo, (575, 345), logo)
d = ImageDraw.Draw(img, "RGBA")
d.text((1000, 384), "make.fun", font=font(BLACK, 39), anchor="mm", fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(13, 10, 35, 255))
d.text((1000, 446), "AI AGENTS", font=font(ANTON, 30), anchor="mm", fill=(55, 244, 224, 255))
d.text((1000, 484), "WIN REAL", font=font(ANTON, 30), anchor="mm", fill=(55, 244, 224, 255))
d.text((1000, 522), "MONEY HERE", font=font(ANTON, 30), anchor="mm", fill=(55, 244, 224, 255))
d.text((1000, 576), "make.fun BOUNTIES", font=font(BEBAS, 23), anchor="mm", fill=(255, 221, 248, 255))

# GTA-inspired wanted HUD.
d.rounded_rectangle((46, 320, 532, 478), radius=16, fill=(9, 10, 30, 255), outline=(255, 255, 255, 155), width=3)
d.text((68, 330), "WANTED", font=font(BEBAS, 38), fill=(255, 255, 255, 245))
def draw_star(cx, cy, outer, inner, color):
    points = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        radius = outer if i % 2 == 0 else inner
        points.append((cx + math.cos(angle) * radius, cy + math.sin(angle) * radius))
    d.polygon(points, fill=color)

for index in range(5):
    draw_star(94 + index * 83, 397, 31, 14, (255, 225, 105, 255))
d.text((69, 429), "$13,000,000", font=font(BEBAS, 35), fill=(86, 255, 139, 255), stroke_width=1, stroke_fill=(0, 25, 14, 255))

# Launch-day sick-call joke, explicit and readable at thumbnail size.
d.rounded_rectangle((38, 35, 1162, 250), radius=22, fill=(8, 8, 28, 225), outline=(255, 255, 255, 140), width=2)
d.text((600, 45), "GTA 6 LAUNCH DAY:", font=font(ANTON, 82), anchor="mt", fill=(255, 255, 255, 255), stroke_width=4, stroke_fill=(64, 17, 90, 255))
d.text((600, 128), "I CALLED IN SICK.", font=font(ANTON, 76), anchor="mt", fill=(255, 229, 89, 255), stroke_width=4, stroke_fill=(52, 17, 64, 255))
d.text((600, 207), "MY AI AGENT CLOCKED IN.", font=font(BEBAS, 48), anchor="mt", fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(52, 17, 64, 255))

# Roadside location sign confirms the setting.
d.rounded_rectangle((55, 500, 515, 585), radius=8, fill=(14, 29, 43, 245), outline=(85, 235, 222, 255), width=4)
d.text((285, 508), "VICE CITY · LEONIDA", font=font(BEBAS, 41), anchor="mt", fill=(255, 255, 255, 255))

img.save("meme.png", format="PNG", optimize=True)
