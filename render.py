#!/usr/bin/env python3
"""Build-time renderer for the news-image-20261117 entry.

Draws entry.png: a newspaper front page summing up the world news of
Tuesday 17 November 2026. This script is a build tool only -- it is NOT
run by the grader. It uses Pillow; the shipped program (main.py) is
standard-library only and simply copies the PNG drawn here.

The day's stories (as reported on 17 November 2026):
  lead  U.S. warplanes strike Iran's Qeshm Island missile site; Iran
        fires drones at U.S. targets in Bahrain; a tanker hits a naval
        mine in the Strait of Hormuz and a gas tanker catches fire;
        24 seafarers evacuated.
  -     Ukraine strikes the Crimean Bridge with drones and missiles.
  -     Trump, Xi and Putin to hold the first U.S.-China-Russia
        trilateral summit, Thursday in Shenzhen during APEC.
  -     The United States loses its measles elimination status (PAHO).
  -     Wall Street falls as AI/tech stocks lead the losses.
  -     Winter rains flood Gaza's makeshift shelters.
  -     COP31 in Antalya: draft deal seeks a faster fossil-fuel
        phase-out and $120bn in climate finance.
  -     Quad leaders announce critical minerals pacts in Manila.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "entry.png"

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

PAPER = (247, 242, 230)
INK = (26, 24, 20)
RED = (166, 30, 38)
NAVY = (31, 52, 84)
GRAY = (94, 86, 74)
RULE = (43, 40, 35)
PANEL_BG = (252, 249, 242)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, s, path, size, max_w, min_size=10):
    """Largest font at or below `size` that keeps `s` within max_w."""
    while size > min_size:
        f = font(path, size)
        if draw.textlength(s, font=f) <= max_w:
            return f
        size -= 1
    return font(path, min_size)


def wrap(draw, s, f, max_w):
    words = s.split()
    lines, cur = [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if draw.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def center(draw, y, s, f, fill):
    w = draw.textlength(s, font=f)
    draw.text(((W - w) / 2, y), s, font=f, fill=fill)


# ---------------------------------------------------------------- icons
# Each icon draws inside the box (x, y, s, s).

def icon_bridge(d, x, y, s):
    deck_y = y + int(s * 0.66)
    top = y + int(s * 0.16)
    d.line([x + 4, deck_y, x + s - 4, deck_y], fill=INK, width=6)
    for px in (x + int(s * 0.30), x + int(s * 0.68)):
        d.line([px, top, px, deck_y], fill=INK, width=6)
        for dx in (-int(s * 0.24), -int(s * 0.12), 0, int(s * 0.12), int(s * 0.24)):
            d.line([px, top, px + dx, deck_y], fill=INK, width=2)
    # explosion burst on the deck, mid-span
    cx, cy = x + int(s * 0.49), deck_y - 4
    pts = []
    import math
    for i in range(16):
        r = 13 if i % 2 == 0 else 6
        a = math.pi * i / 8
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=(232, 116, 28))
    # water
    for wy in (deck_y + 12, deck_y + 22):
        for wx in range(x + 6, x + s - 14, 22):
            d.arc([wx, wy, wx + 14, wy + 8], 0, 180, fill=NAVY, width=3)


def icon_flags(d, x, y, s):
    pole_x = [x + int(s * 0.16), x + int(s * 0.47), x + int(s * 0.78)]
    base = y + int(s * 0.92)
    top = y + int(s * 0.10)
    fw, fh = int(s * 0.27), int(s * 0.20)
    for px in pole_x:
        d.line([px, top, px, base], fill=INK, width=4)
    # United States: stripes + blue canton
    fx, fy = pole_x[0], top
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(178, 34, 52))
    for i in range(1, 4):
        yy = fy + i * fh // 4
        d.line([fx, yy, fx + fw, yy], fill=(255, 255, 255), width=2)
    d.rectangle([fx, fy, fx + fw // 2, fy + fh // 2], fill=(60, 59, 110))
    # China: red with yellow stars
    fx = pole_x[1]
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
    d.ellipse([fx + 3, fy + 3, fx + 9, fy + 9], fill=(255, 222, 0))
    d.ellipse([fx + 12, fy + 2, fx + 16, fy + 6], fill=(255, 222, 0))
    d.ellipse([fx + 13, fy + 8, fx + 17, fy + 12], fill=(255, 222, 0))
    # Russia: white / blue / red
    fx = pole_x[2]
    d.rectangle([fx, fy, fx + fw, fy + fh // 3], fill=(245, 245, 245))
    d.rectangle([fx, fy + fh // 3, fx + fw, fy + 2 * fh // 3], fill=(0, 57, 166))
    d.rectangle([fx, fy + 2 * fh // 3, fx + fw, fy + fh], fill=(213, 43, 30))
    d.rectangle([pole_x[0], fy, pole_x[2] + fw, fy + fh], outline=INK, width=1)


def icon_virus(d, x, y, s):
    import math
    cx, cy = x + s // 2, y + s // 2
    r = int(s * 0.26)
    for i in range(8):
        a = math.pi * i / 4
        x1, y1 = cx + int(r * 0.9 * math.cos(a)), cy + int(r * 0.9 * math.sin(a))
        x2, y2 = cx + int(r * 1.45 * math.cos(a)), cy + int(r * 1.45 * math.sin(a))
        d.line([x1, y1, x2, y2], fill=RED, width=5)
        d.ellipse([x2 - 5, y2 - 5, x2 + 5, y2 + 5], fill=RED)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 84, 84))
    for dx, dy, rr in ((-10, -6, 5), (9, -12, 4), (2, 10, 5), (-13, 9, 3)):
        d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr],
                  fill=(246, 200, 200))


def icon_chart(d, x, y, s):
    ax, ay = x + int(s * 0.14), y + int(s * 0.12)
    bx, by = x + int(s * 0.90), y + int(s * 0.86)
    d.line([ax, ay, ax, by], fill=GRAY, width=4)
    d.line([ax, by, bx, by], fill=GRAY, width=4)
    pts = [(ax + 4, y + int(s * 0.24)), (x + int(s * 0.36), y + int(s * 0.38)),
           (x + int(s * 0.50), y + int(s * 0.30)), (x + int(s * 0.66), y + int(s * 0.58)),
           (x + int(s * 0.86), y + int(s * 0.80))]
    d.line(pts, fill=RED, width=7, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex + 12, ey + 2), (ex - 6, ey - 4), (ex + 2, ey + 12)], fill=RED)


def icon_tent(d, x, y, s):
    # rain cloud
    cx, cy = x + int(s * 0.50), y + int(s * 0.16)
    d.ellipse([cx - 26, cy - 10, cx + 4, cy + 12], fill=(110, 128, 150))
    d.ellipse([cx - 6, cy - 16, cx + 28, cy + 12], fill=(110, 128, 150))
    d.rectangle([cx - 26, cy + 2, cx + 28, cy + 12], fill=(110, 128, 150))
    # rain streaks
    for rx in range(x + int(s * 0.22), x + int(s * 0.82), 14):
        d.line([rx, y + int(s * 0.36), rx - 5, y + int(s * 0.50)], fill=(70, 110, 170), width=4)
    # tent
    base = y + int(s * 0.86)
    apex = (x + int(s * 0.50), y + int(s * 0.56))
    d.polygon([(x + int(s * 0.10), base), apex, (x + int(s * 0.90), base)], fill=(196, 154, 92))
    d.polygon([(x + int(s * 0.40), base), apex, (x + int(s * 0.60), base)], fill=(110, 78, 44))
    # puddle
    d.ellipse([x + int(s * 0.16), base + 4, x + int(s * 0.84), base + 14], fill=(120, 160, 200))


def icon_globe(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    r = int(s * 0.40)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=5)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=NAVY, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=NAVY, width=3)
    d.line([cx - int(r * 0.86), cy - int(r * 0.5), cx + int(r * 0.86), cy - int(r * 0.5)], fill=NAVY, width=2)
    d.line([cx - int(r * 0.86), cy + int(r * 0.5), cx + int(r * 0.86), cy + int(r * 0.5)], fill=NAVY, width=2)


def icon_gem(d, x, y, s):
    top_y = y + int(s * 0.26)
    mid_y = y + int(s * 0.44)
    bot = (x + s // 2, y + int(s * 0.88))
    left = (x + int(s * 0.10), mid_y)
    right = (x + int(s * 0.90), mid_y)
    tl = (x + int(s * 0.28), top_y)
    tr = (x + int(s * 0.72), top_y)
    d.polygon([tl, tr, right, bot, left], fill=(168, 205, 232))
    d.line([left, right], fill=NAVY, width=3)
    d.line([tl, x + int(s * 0.38), mid_y], fill=NAVY, width=2)
    d.line([tr, x + int(s * 0.62), mid_y], fill=NAVY, width=2)
    d.line([x + int(s * 0.38), mid_y, bot], fill=NAVY, width=2)
    d.line([x + int(s * 0.62), mid_y, bot], fill=NAVY, width=2)
    d.polygon([tl, tr, right, bot, left], outline=NAVY)


# ---------------------------------------------------------------- scene
def lead_scene(d, x0, y0, x1, y1):
    horizon = y0 + int((y1 - y0) * 0.62)
    # dusk sky gradient
    top = (36, 42, 68)
    low = (216, 122, 54)
    for yy in range(y0, horizon):
        t = (yy - y0) / max(1, horizon - y0)
        col = tuple(int(top[i] + (low[i] - top[i]) * t) for i in range(3))
        d.line([x0, yy, x1, yy], fill=col)
    # sea
    d.rectangle([x0, horizon, x1, y1], fill=(23, 43, 63))
    for wx in range(x0 + 190, x1 - 30, 46):
        d.line([wx, horizon + 16, wx + 22, horizon + 16], fill=(86, 120, 148), width=2)
    # island (Qeshm) on the left
    d.polygon([(x0, horizon), (x0 + 150, horizon), (x0 + 118, horizon - 26),
               (x0 + 52, horizon - 36), (x0 + 10, horizon - 14)], fill=(18, 18, 22))
    # missile launcher silhouette on the island
    d.line([x0 + 62, horizon - 32, x0 + 84, horizon - 52], fill=(8, 8, 10), width=5)
    d.polygon([(x0 + 84, horizon - 58), (x0 + 92, horizon - 50), (x0 + 80, horizon - 46)],
              fill=(8, 8, 10))
    d.text((x0 + 8, horizon + 6), "QESHM ISLAND", font=font(SANS_B, 14), fill=(220, 228, 238))
    # jets overhead
    def jet(cx, cy, sc):
        d.polygon([(cx - 26 * sc, cy), (cx + 20 * sc, cy - 5 * sc), (cx + 30 * sc, cy),
                   (cx + 20 * sc, cy + 5 * sc), (cx - 26 * sc, cy + 3 * sc)], fill=(10, 10, 14))
        d.polygon([(cx - 2 * sc, cy), (cx - 14 * sc, cy + 13 * sc), (cx + 8 * sc, cy + 2 * sc)],
                  fill=(10, 10, 14))
        d.polygon([(cx - 24 * sc, cy), (cx - 32 * sc, cy - 10 * sc), (cx - 16 * sc, cy - 1 * sc)],
                  fill=(10, 10, 14))
    jet(x0 + 330, y0 + 26, 1.0)
    jet(x0 + 470, y0 + 14, 0.8)
    # tanker, centre-right
    tx0, tx1 = x0 + 560, x0 + 884
    wl = horizon + 8
    d.rectangle([tx0 + 18, wl - 26, tx1 - 18, wl - 12], fill=(34, 34, 40))  # deck
    d.polygon([(tx0, wl - 12), (tx1, wl - 12), (tx1 - 26, wl + 12), (tx0 + 30, wl + 12)],
              fill=(14, 14, 18))  # hull
    for i, dx in enumerate((70, 140, 210)):  # tank domes
        d.pieslice([tx0 + dx, wl - 40, tx0 + dx + 56, wl - 12], 180, 360, fill=(52, 52, 60))
    d.rectangle([tx1 - 92, wl - 56, tx1 - 40, wl - 12], fill=(40, 40, 46))  # superstructure
    d.rectangle([tx1 - 74, wl - 66, tx1 - 58, wl - 56], fill=(40, 40, 46))  # funnel
    # fire amidships (kept inside the frame, below the headline)
    fx = tx0 + 168
    d.polygon([(fx - 26, wl - 26), (fx - 6, wl - 66), (fx + 4, wl - 40),
               (fx + 16, wl - 72), (fx + 30, wl - 26)], fill=(238, 110, 26))
    d.polygon([(fx - 12, wl - 26), (fx + 2, wl - 50), (fx + 16, wl - 26)], fill=(250, 186, 52))
    # smoke drifting sideways, never rising out of the frame
    for sx, sy, sr, tone in ((fx + 30, wl - 58, 9, (110, 108, 110)),
                             (fx + 54, wl - 64, 12, (96, 94, 96)),
                             (fx + 82, wl - 68, 14, (84, 82, 86))):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=tone)
    d.text((x1 - 218, y1 - 24), "STRAIT OF HORMUZ", font=font(SANS_B, 15), fill=(220, 228, 238))
    d.rectangle([x0, y0, x1, y1], outline=INK, width=3)


# ---------------------------------------------------------------- panels
def panel(d, x, y, w, h, icon, headline, sub):
    d.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=RULE, width=2)
    isz = 92
    icon(d, x + 10, y + (h - isz) // 2, isz)
    tx = x + 116
    tw = w - 130
    hf = fit(d, headline, SANS_B, 26, tw)
    lines = wrap(d, headline, hf, tw)
    sf = font(SANS, 19)
    slines = wrap(d, sub, sf, tw)
    total = len(lines) * 29 + 6 + len(slines) * 23
    ty = y + (h - total) // 2
    for ln in lines:
        d.text((tx, ty), ln, font=hf, fill=INK)
        ty += 29
    ty += 6
    for ln in slines:
        d.text((tx, ty), ln, font=sf, fill=(58, 52, 44))
        ty += 23


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 40            # page margin
    CW = W - 2 * M    # content width

    # ---- masthead
    center(d, 18, "T H E   W O R L D   I N   O N E   P A G E", font(SANS_B, 16), GRAY)
    mf = fit(d, "THE WORLD TODAY", SERIF_B, 74, CW)
    center(d, 38, "THE WORLD TODAY", mf, INK)
    d.rectangle([M, 122, W - M, 164], fill=INK)
    center(d, 130, "TUESDAY  ·  17 NOVEMBER 2026", font(SANS_B, 30), (255, 250, 238))
    d.line([M, 172, W - M, 172], fill=RED, width=3)

    # ---- lead story
    d.text((M, 184), "LEAD STORY — MIDDLE EAST", font=font(SANS_B, 20), fill=RED)
    hf = fit(d, "U.S. JETS STRIKE IRAN MISSILE SITE", SERIF_B, 56, CW)
    d.text((M, 208), "U.S. JETS STRIKE IRAN MISSILE SITE", font=hf, fill=INK)
    d.text((M, 268), "TANKER ABLAZE IN HORMUZ STRAIT", font=hf, fill=INK)
    lead_scene(d, M, 336, W - M, 458)
    dek = ("Iran fires drones at U.S. targets in Bahrain · a tanker hits a naval mine "
           "in the strait and a gas tanker catches fire · 24 seafarers evacuated")
    df = font(SANS, 22)
    ty = 468
    for ln in wrap(d, dek, df, CW):
        d.text((M, ty), ln, font=df, fill=(46, 42, 36))
        ty += 27
    d.line([M, 536, W - M, 536], fill=RULE, width=4)

    # ---- secondary grid: 3 rows of 2
    stories = [
        (icon_bridge, "UKRAINE STRIKES CRIMEAN BRIDGE",
         "Drones and missiles hit the Kerch Strait crossing"),
        (icon_flags, "FIRST U.S.–CHINA–RUSSIA SUMMIT SET",
         "Trump, Xi and Putin to meet Thursday in Shenzhen, at APEC"),
        (icon_virus, "U.S. LOSES MEASLES ELIMINATION STATUS",
         "PAHO ends the United States' measles-free standing"),
        (icon_chart, "WALL STREET FALLS AS TECH LEADS LOSSES",
         "AI and tech stocks lead a broad market sell-off"),
        (icon_tent, "WINTER RAINS FLOOD GAZA TENT CAMPS",
         "Storms soak makeshift shelters, deepening the crisis"),
        (icon_globe, "COP31 DRAFT: FASTER FOSSIL PHASE-OUT",
         "Antalya draft seeks $120bn in climate finance"),
    ]
    pw = (CW - 12) // 2
    ph = 114
    gy = 548
    for r in range(3):
        for c in range(2):
            icon, head, sub = stories[r * 2 + c]
            panel(d, M + c * (pw + 12), gy + r * (ph + 6), pw, ph, icon, head, sub)

    # ---- wide bottom panel: Quad
    wy = gy + 3 * (ph + 6) + 2
    wh = 74
    d.rectangle([M, wy, W - M, wy + wh], fill=PANEL_BG, outline=RULE, width=2)
    icon_gem(d, M + 12, wy + 8, 62)
    qh = "QUAD LEADERS SIGN CRITICAL MINERALS PACTS"
    qf = fit(d, qh, SANS_B, 26, CW - 110)
    d.text((M + 92, wy + 10), qh, font=qf, fill=INK)
    d.text((M + 92, wy + 44), "U.S., Japan, India and Australia agree supply deals at Manila summit",
           font=font(SANS, 19), fill=(58, 52, 44))

    # ---- footer: the day, named again at the foot of the page
    center(d, 992, "TUESDAY 17 NOVEMBER 2026 · COMPILED FROM THE DAY'S REPORTS",
           font(SANS_B, 14), GRAY)

    img.save(OUT)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
