#!/usr/bin/env python3
"""Draw the news-image-20261121 entry: a one-page newspaper front page
summing up world news of Saturday 21 November 2026. PIL only, no network.
Data: research/20261121.json (45 stories). Output: 1024x1024 PNG < 1 MiB."""
import json
import math
from datetime import date
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (20, 20, 20)
WHITE = (255, 255, 255)
RED = (176, 30, 36)
NAVY = (31, 58, 95)
TEAL = (14, 107, 107)
GREEN = (0, 120, 80)
GOLD = (176, 120, 0)
GREY = (90, 88, 80)
LIGHT = (238, 232, 214)
BROWN = (122, 74, 22)
MAROON = (128, 32, 48)
PURPLE = (90, 60, 140)
PINK = (200, 60, 120)
DARKGREEN = (46, 110, 46)

REGION_COLOR = {
    "EUROPE": NAVY, "UNITED STATES": DARKGREEN, "MIDDLE EAST": RED,
    "ASIA": TEAL, "MARKETS": GOLD, "AMERICAS": BROWN, "AFRICA": MAROON,
    "SPORT": (60, 60, 60), "CLIMATE": GREEN, "SCIENCE": PURPLE,
    "HEALTH": PINK,
}

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_block(draw, x, y, lines, fnt, color, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def icon_burst(d, x, y, s, c):
    cx, cy = x + s / 2, y + s / 2
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        d.line([cx + 12 * math.cos(a), cy + 12 * math.sin(a),
                cx + (s / 2 - 2) * math.cos(a), cy + (s / 2 - 2) * math.sin(a)],
               fill=(255, 170, 60), width=5)
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(255, 210, 90))


def icon_chart(d, x, y, s, c):
    pts = [(x + 4, y + s * 0.25), (x + s * 0.35, y + s * 0.4),
           (x + s * 0.55, y + s * 0.3), (x + s - 8, y + s * 0.8)]
    d.line(pts, fill=c, width=5, joint="curve")
    d.polygon([(x + s - 14, y + s * 0.62), (x + s - 2, y + s * 0.72),
               (x + s - 12, y + s * 0.86)], fill=c)


def icon_globe(d, x, y, s, c):
    d.ellipse([x + 4, y + 4, x + s - 4, y + s - 4], outline=c, width=4)
    d.line([x + s / 2, y + 6, x + s / 2, y + s - 6], fill=c, width=3)
    d.line([x + 6, y + s / 2, x + s - 6, y + s / 2], fill=c, width=3)


LEAD_ICONS = [icon_burst, icon_chart, icon_globe]

# Rough continent outlines in (lon, lat), equirectangular projection.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 71), (-100, 72), (-85, 70), (-75, 62),
     (-60, 55), (-70, 45), (-80, 32), (-85, 25), (-95, 20), (-105, 20),
     (-115, 28), (-125, 40), (-140, 60), (-160, 58)],
    [(-80, 10), (-60, 5), (-45, -5), (-35, -10), (-40, -25), (-55, -35),
     (-65, -45), (-70, -30), (-75, -15), (-80, 0)],
    [(-10, 36), (0, 38), (10, 38), (20, 40), (28, 45), (30, 55), (20, 60),
     (10, 62), (0, 58), (-5, 50), (-10, 45)],
    [(-15, 15), (-10, 30), (0, 35), (10, 35), (20, 32), (30, 30), (35, 25),
     (40, 15), (45, 10), (50, 0), (40, -10), (35, -20), (25, -30),
     (15, -35), (10, -25), (5, -15), (0, 0), (-8, 5)],
    [(35, 35), (45, 40), (55, 45), (65, 50), (75, 55), (90, 60), (110, 65),
     (130, 70), (150, 68), (170, 65), (160, 55), (140, 45), (130, 35),
     (120, 30), (110, 20), (100, 10), (95, 5), (85, 10), (75, 15),
     (65, 20), (55, 25), (45, 28), (40, 30)],
    [(113, -22), (125, -15), (140, -12), (150, -20), (153, -28),
     (145, -38), (135, -35), (125, -32), (115, -30)],
]

MAP_DOTS = [  # (lon, lat, label, label dx, label dy)
    (30.5, 50.5, "KYIV", 7, -16), (34.5, 31.5, "GAZA", -36, 6),
    (46.7, 24.6, "RIYADH", 7, 4), (-77.0, -12.0, "LIMA", 7, -6),
    (30.7, 36.9, "ANTALYA", 8, -18), (-74.0, 40.7, "", 0, 0),
    (-0.1, 51.5, "LONDON", -60, -6), (51.4, 35.7, "", 0, 0),
]

TIMELINE = [  # (UTC time, label)
    ("00:09", "Peru quake"), ("01:17", "COP31 draft"),
    ("02:26", "Haiti toll rises"), ("05:05", "FBI hack reported"),
    ("06:54", "Zelensky interview"), ("08:30", "Kutaisi blast"),
]


def main():
    data = json.load(open(
        "/home/hatch/workspace/make-fun/news-image-20261121/research/20261121.json"))
    stories = sorted(data["stories"], key=lambda s: s["rank"])
    assert len(stories) == 45, len(stories)
    day = date(2026, 11, 21)
    weekday = day.strftime("%A").upper()  # computed in code: SATURDAY
    date_str = f"{weekday}  •  21 NOVEMBER 2026"

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 26

    # ---- Masthead ----
    y = 16
    tf = font(SERIF, 56)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, y), title, font=tf, fill=INK)
    y += 72
    d.line([mx, y, W - mx, y], fill=INK, width=3)
    y += 7
    band_h = 46
    d.rectangle([mx, y, W - mx, y + band_h], fill=RED)
    df = font(SANS_B, 30)
    band = date_str + "   —   45 STORIES"
    dw = d.textlength(band, font=df)
    d.text(((W - dw) / 2, y + 7), band, font=df, fill=WHITE)
    y += band_h + 12  # y = 153

    # ---- 3 leads, side by side ----
    leads = stories[:3]
    gap = 12
    col_w = (W - 2 * mx - 2 * gap) // 3
    lead_h = 178
    for i, st in enumerate(leads):
        cx = mx + i * (col_w + gap)
        col = REGION_COLOR[st["region"]]
        d.rectangle([cx, y, cx + col_w, y + lead_h], fill=WHITE,
                    outline=INK, width=2)
        d.rectangle([cx, y, cx + col_w, y + 6], fill=col)
        d.text((cx + 12, y + 14), f"LEAD {i + 1}  —  {st['region']}",
               font=font(SANS_B, 14), fill=col)
        icon = LEAD_ICONS[i]
        d.ellipse([cx + col_w - 52, y + 10, cx + col_w - 6, y + 56],
                  fill=LIGHT)
        icon(d, cx + col_w - 50, y + 12, 42, col)
        hl = wrap(d, st["headline"], font(SERIF, 23), col_w - 24)
        assert len(hl) <= 3, (st["headline"], hl)
        yy = draw_block(d, cx + 12, y + 40, hl, font(SERIF, 23), INK, 28)
        dl = wrap(d, st["deck"], font(SANS, 13), col_w - 24)
        assert len(dl) <= 2, (st["deck"], dl)
        draw_block(d, cx + 12, yy + 4, dl, font(SANS, 13), (50, 50, 50), 17)
    y += lead_h + 10  # y = 341

    # ---- Story list: remaining 42, 3 columns x 14 rows ----
    rest = stories[3:]
    assert len(rest) == 42
    list_top = y
    row_h = 36
    for j, st in enumerate(rest):
        c, r = divmod(j, 14)
        cx = mx + c * (col_w + gap)
        cy = list_top + r * row_h
        col = REGION_COLOR[st["region"]]
        d.ellipse([cx + 2, cy + 5, cx + 12, cy + 15], fill=col)
        hl = wrap(d, st["headline"], font(SANS_B, 14), col_w - 22)
        assert len(hl) <= 2, (st["headline"], hl)
        draw_block(d, cx + 18, cy, hl, font(SANS_B, 14), INK, 17)
    y = list_top + 14 * row_h + 8  # y = 853

    # ---- Bottom band: world map (left) + UTC timeline (right) ----
    band_h = 150
    map_x0, map_y0 = mx, y
    map_w, map_h2 = 480, band_h
    d.rectangle([map_x0, map_y0, map_x0 + map_w, map_y0 + band_h],
                fill=WHITE, outline=(180, 172, 150), width=1)
    d.text((map_x0 + 10, map_y0 + 6), "WHERE IT HAPPENED",
           font=font(SANS_B, 13), fill=GREY)

    def proj(lon, lat):
        return (map_x0 + 8 + (lon + 180) / 360 * (map_w - 16),
                map_y0 + 24 + (80 - lat) / 140 * (band_h - 30))
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=(210, 205, 190), outline=(150, 142, 122))
    for lon, lat, label, dx, dy in MAP_DOTS:
        px, py = proj(lon, lat)
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED,
                  outline=WHITE, width=1)
        if label:
            d.text((px + dx, py + dy), label, font=font(SANS_B, 11),
                   fill=INK)

    # UTC timeline, right of the map: 2 columns x 3 rows
    tl_x = mx + map_w + 16
    tl_w = W - mx - tl_x
    d.text((tl_x, y + 6), "THE DAY IN UTC", font=font(SANS_B, 13),
           fill=GREY)
    d.line([tl_x, y + 26, W - mx, y + 26], fill=(180, 172, 150), width=2)
    tcol_w = tl_w // 2
    for i, (t, label) in enumerate(TIMELINE):
        tc, tr = divmod(i, 3)
        ex = tl_x + tc * tcol_w
        ey = y + 36 + tr * 42
        d.ellipse([ex + 2, ey + 4, ex + 12, ey + 14], fill=NAVY)
        d.text((ex + 18, ey), t, font=font(SANS_B, 14), fill=INK)
        d.text((ex + 18, ey + 19), label, font=font(SANS, 12), fill=GREY)
    y += band_h + 8  # y = 1011

    # ---- Footer ----
    foot = "45 stories  •  All stories reported on Saturday 21 November 2026 (UTC)"
    ff = font(SANS, 13)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, y - 6), foot, font=ff, fill=GREY)

    out = "/home/hatch/workspace/make-fun/news-image-20261121/entry.png"
    img.save(out, "PNG", optimize=True)
    print("saved", out)


if __name__ == "__main__":
    main()
