#!/usr/bin/env python3
"""Render 'Dnipro Dawn' - a 1024x1024 newspaper front page for 20 Nov 2026.

Draws everything with PIL primitives: no downloaded or copied images.
All stories are Friday 20 November 2026 news, summarised in plain words.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 34, 28)
NAVY = (16, 28, 52)
GREY = (90, 88, 82)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw a wrapped paragraph; return the y just below it."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centred(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)


def rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_skyline(draw, x0, y0, x1, y1):
    """Night sky over Kyiv: dark bands, stars, moon, towers, river, bridge."""
    # Sky bands, darker toward the top.
    bands = [(12, 20, 44), (18, 30, 58), (26, 42, 74), (36, 54, 90)]
    bh = (y1 - y0) // len(bands)
    for i, col in enumerate(bands):
        draw.rectangle([x0, y0 + i * bh, x1, y0 + (i + 1) * bh], fill=col)
    # Stars.
    stars = [(70, 165), (150, 185), (240, 160), (330, 190), (430, 158),
             (520, 180), (620, 162), (720, 188), (820, 160), (900, 182),
             (110, 210), (480, 205), (770, 215), (880, 215), (290, 215)]
    for sx, sy in stars:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(240, 238, 220))
    # Pale moon.
    draw.ellipse([860, 168, 912, 220], fill=(235, 230, 205))
    draw.ellipse([872, 178, 884, 190], fill=(210, 204, 178))
    # Distant glow of a blast on the horizon, kept small so the skyline reads.
    for r, col in [(36, (255, 140, 40)), (24, (255, 180, 70)),
                   (14, (255, 220, 130))]:
        draw.ellipse([300 - r, 300 - r, 300 + r, 300 + r], fill=col)
    # Building silhouettes.
    base = y1 - 52
    towers = [(40, 90, 120), (130, 130, 190), (200, 100, 250),
              (380, 120, 440), (450, 150, 520), (560, 95, 620),
              (640, 140, 710), (730, 105, 790), (810, 135, 880),
              (890, 100, 950)]
    for tx0, th, tx1 in towers:
        draw.rectangle([tx0, base - th, tx1, base], fill=(8, 12, 26))
        # A few lit windows.
        for wy in range(base - th + 12, base - 10, 26):
            for wx in range(tx0 + 10, tx1 - 8, 22):
                if (wx + wy) % 3 == 0:
                    draw.rectangle([wx, wy, wx + 6, wy + 8],
                                   fill=(255, 200, 90))
    # River (Dnipro) at the foot of the picture.
    draw.rectangle([x0, base, x1, y1], fill=(30, 58, 92))
    draw.line([(x0, base + 18), (x1, base + 18)], fill=(90, 130, 175), width=2)
    draw.line([(x0, base + 34), (x1, base + 34)], fill=(70, 110, 155), width=2)
    # Bridge across the river, with one span broken and tilted.
    deck = base + 6
    draw.line([(x0, deck), (x1, deck)], fill=(10, 14, 30), width=7)
    for px in range(90, 960, 110):
        draw.line([(px, deck - 44), (px, deck)], fill=(10, 14, 30), width=5)
    draw.line([(90, deck - 44), (940, deck - 44)], fill=(10, 14, 30), width=4)
    # Broken span near the blast: sagging cables and a tilted deck piece.
    draw.line([(300, deck - 44), (300, deck + 16)], fill=(10, 14, 30), width=5)
    draw.line([(300, deck + 16), (380, deck)], fill=(10, 14, 30), width=6)
    draw.line([(410, deck - 44), (410, deck)], fill=(10, 14, 30), width=5)
    # Smoke rising from the blast.
    for cx, cy, r in [(285, 245, 16), (305, 225, 20), (322, 205, 14)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 70, 80))


def story_block(draw, x, y, w, kicker, headline, body, head_size=25):
    """One boxed story: red kicker, bold headline, wrapped body text."""
    hf = font(SANS_BOLD, 15)
    draw.text((x, y), kicker, font=hf, fill=RED)
    y += 22
    y = para(draw, x, y, headline, font(SANS_BOLD, head_size), w, head_size + 6)
    y += 3
    y = para(draw, x, y, body, font(SANS, 18), w, 23)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36
    rx = W - mx

    # Masthead.
    centred(d, W // 2, 22, "THE WORLD TODAY", font(SERIF, 60))
    rule(d, mx, rx, 102, width=3)
    centred(d, W // 2, 112, "Friday, 20 November 2026  |  World news in one page",
            font(SANS, 20), fill=GREY)
    rule(d, mx, rx, 142, width=1, fill=GREY)

    # Lead illustration (shorter, so the text below has room to breathe).
    draw_skyline(d, mx, 152, rx, 382)
    d.text((mx, 358), "Kyiv at dawn: smoke over the Dnipro after the overnight strikes.",
           font=font(SANS, 14), fill=(200, 205, 215))

    # Lead headline and summary.
    d.text((mx, 392), "KYIV HIT AGAIN", font=font(SERIF, 54), fill=INK)
    para(d, mx, 454,
         "A fresh Russian missile-and-drone attack hit Kyiv overnight on "
         "Friday. Three people were killed, Kyiv mayor Vitali Klitschko said, "
         "and three bridges across the Dnipro River were damaged.",
         font(SANS, 21), rx - mx, 26)
    rule(d, mx, rx, 538, width=2)

    # Middle stories in two columns.
    col_w = 452
    left, right = mx, mx + col_w + 32
    story_block(d, left, 556, col_w, "MARKETS",
                "Markets Rout Deepens",
                "Japan's Nikkei fell 4.8% on Friday. The S&P 500 lost about 2%, "
                "its fifth straight daily loss. SoftBank dropped more than 16%, "
                "gold fell 4.2%, and Brent oil stood at $90.05.")
    story_block(d, right, 556, col_w, "MIDDLE EAST",
                "Riyadh Targeted Again",
                "Saudi Arabia intercepted another Houthi missile and five drones "
                "on Friday, with Riyadh among the reported targets, after Houthi "
                "attacks on the capital's financial district.")
    rule(d, mx, rx, 700, width=1, fill=GREY)
    story_block(d, left, 714, col_w, "GAMES",
                "GTA VI Tops $2.3 Billion",
                "Grand Theft Auto VI has topped $2.3 billion in sales at launch, "
                "expected to be the biggest entertainment launch ever.")
    story_block(d, right, 714, col_w, "UKRAINE AID",
                "UK Pledges 1,000+ Drones",
                "The UK has pledged more than 1,000 drones for Ukraine in a "
                "£260 million support package.")
    rule(d, mx, rx, 838, width=1, fill=GREY)

    # Pete Rose, full width, two short lines so the hits record stays in.
    d.text((mx, 848), "BASEBALL  •  ", font=font(SANS_BOLD, 15), fill=RED)
    d.text((mx + 108, 848), "Trump Pardons Pete Rose",
           font=font(SANS_BOLD, 22), fill=INK)
    para(d, mx, 876,
         "Donald Trump posthumously pardoned late baseball star Pete Rose, "
         "banned for betting on games and the sport's career hits record holder.",
         font(SANS, 16), rx - mx, 20)

    # Also-today strip: one short line per item, each on its own row.
    rule(d, mx, rx, 924, width=2)
    d.text((mx, 934), "ALSO TODAY", font=font(SANS_BOLD, 15), fill=RED)
    items = [
        "European youth strike in 25+ countries over living costs and militarisation.",
        "UK and EU set to agree a youth mobility scheme at Friday's Brussels summit.",
        "COP31 draft drops the call to phase out fossil fuels as talks enter their final day.",
        "Voyager 1 reaches one light-day from Earth, 49 years after launch.",
        "El Salvador's Bukele registers for a third presidential term.",
    ]
    y = 954
    for item in items:
        d.text((mx, y), "•  " + item, font=font(SANS, 13), fill=INK)
        y += 14
    img.save(OUT)
    print("saved", OUT, img.size)


if __name__ == "__main__":
    main()
