#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Draws the winning concept -- a cheerful household robot blasting its owner
point-blank with a fire hose, captioned "YOU SAID DRINK MORE WATER" --
as a 1024x1024 PNG, stdlib only (zlib + struct PNG encoder, glyph bitmaps
from glyphs.py). Writes /output/entry.png. Deterministic: same bytes
every run. No network, no secrets, no imports beyond the stdlib.
"""
import binascii
import math
import os
import struct
import sys
import zlib

from glyphs import GLYPHS

W = H = 1024

# ---- palette (flat, high contrast; no gradients, no blur) ----
SKY = (168, 220, 240)
GROUND = (140, 192, 132)
GRASS_DARK = (74, 140, 74)
PANEL = (255, 255, 255)
NAVY = (20, 33, 61)
TEAL = (42, 157, 143)
TEAL_LIGHT = (138, 207, 199)
RED = (214, 40, 40)
ORANGE = (228, 87, 46)
YELLOW = (255, 201, 60)
WATER = (30, 136, 229)
WATER_LIGHT = (91, 168, 232)
SKIN = (242, 194, 155)
HAIR = (58, 46, 42)
GREY = (107, 114, 128)

SPACE_ADV = {100: 29, 64: 18}

buf = bytearray(W * H * 3)


def px(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i], buf[i + 1], buf[i + 2] = color


def hline(x0, x1, y, color):
    if y < 0 or y >= H:
        return
    x0 = max(0, x0)
    x1 = min(W - 1, x1)
    if x0 > x1:
        return
    i = (y * W + x0) * 3
    for x in range(x0, x1 + 1):
        buf[i], buf[i + 1], buf[i + 2] = color
        i += 3


def fill_rect(x0, y0, x1, y1, color):
    for y in range(max(0, y0), min(H, y1 + 1)):
        hline(x0, x1, y, color)


def fill_circle(cx, cy, r, color):
    for dy in range(-r, r + 1):
        dx = int(math.sqrt(max(0, r * r - dy * dy)))
        hline(cx - dx, cx + dx, cy + dy, color)


def fill_ellipse(cx, cy, rx, ry, color):
    for dy in range(-ry, ry + 1):
        t = 1.0 - (dy * dy) / float(ry * ry)
        dx = int(rx * math.sqrt(max(0.0, t)))
        hline(cx - dx, cx + dx, cy + dy, color)


def fill_rr(x0, y0, x1, y1, r, color):
    fill_rect(x0 + r, y0, x1 - r, y1, color)
    fill_rect(x0, y0 + r, x1, y1 - r, color)
    fill_circle(x0 + r, y0 + r, r, color)
    fill_circle(x1 - r, y0 + r, r, color)
    fill_circle(x0 + r, y1 - r, r, color)
    fill_circle(x1 - r, y1 - r, r, color)


def fill_triangle(p0, p1, p2, color):
    (x0, y0), (x1, y1), (x2, y2) = p0, p1, p2
    ymin, ymax = min(y0, y1, y2), max(y0, y1, y2)
    for y in range(ymin, ymax + 1):
        xs = []
        for (ax, ay), (bx, by) in (((x0, y0), (x1, y1)),
                                   ((x1, y1), (x2, y2)),
                                   ((x2, y2), (x0, y0))):
            if ay == by:
                continue
            if min(ay, by) <= y < max(ay, by):
                xs.append(ax + (y - ay) * (bx - ax) / (by - ay))
        if len(xs) >= 2:
            hline(int(min(xs)), int(max(xs)), y, color)


def thick_line(x0, y0, x1, y1, width, color):
    steps = max(abs(x1 - x0), abs(y1 - y0)) // 4 + 1
    r = width // 2
    for i in range(steps + 1):
        t = i / steps
        fill_circle(int(x0 + (x1 - x0) * t), int(y0 + (y1 - y0) * t), r, color)


def bezier_thick(p0, c, p1, r0, r1, color, steps=70):
    for i in range(steps + 1):
        t = i / steps
        u = 1.0 - t
        x = int(u * u * p0[0] + 2 * u * t * c[0] + t * t * p1[0])
        y = int(u * u * p0[1] + 2 * u * t * c[1] + t * t * p1[1])
        r = int(r0 + (r1 - r0) * t)
        fill_circle(x, y, r, color)


def text_width(size, text):
    total = 0
    for ch in text:
        if ch == " ":
            total += SPACE_ADV[size]
        else:
            total += GLYPHS[(size, ch)][0]
    return total


def draw_text(size, x, y, text, color):
    """Draw text with draw origin (x, y) at anchor 'la' (left, ascender)."""
    cx = x
    for ch in text:
        if ch == " ":
            cx += SPACE_ADV[size]
            continue
        adv, xoff, yoff, w, h, hx = GLYPHS[(size, ch)]
        raw = bytes.fromhex(hx)
        rowbytes = (w + 7) // 8
        for gy in range(h):
            row = raw[gy * rowbytes:(gy + 1) * rowbytes]
            for gx in range(w):
                if row[gx // 8] >> (7 - gx % 8) & 1:
                    px(cx + xoff + gx, y + yoff + gy, color)
        cx += adv
    return cx


def draw_centered(size, cx, y, text, color):
    draw_text(size, cx - text_width(size, text) // 2, y, text, color)


# ---- scene ----
def draw_scene():
    # Sky and ground.
    fill_rect(0, 0, W - 1, 899, SKY)
    fill_rect(0, 900, W - 1, H - 1, GROUND)

    # Clouds (white, flat).
    for cx, cy, rx, ry in ((700, 348, 62, 22), (735, 338, 48, 18),
                           (665, 340, 44, 16), (940, 344, 58, 20),
                           (972, 334, 42, 16), (908, 336, 40, 15)):
        fill_ellipse(cx, cy, rx, ry, PANEL)

    # Top caption panel: the agent's line, huge and centred.
    fill_rr(24, 24, 1000, 300, 22, PANEL)
    draw_centered(100, 512, 44, "YOU SAID DRINK", NAVY)
    draw_centered(100, 512, 169, "MORE WATER", NAVY)

    # Speech bubble from the robot: "I'M HELPING!"
    fill_rr(24, 322, 620, 420, 24, PANEL)
    fill_triangle((300, 418), (380, 418), (330, 452), PANEL)
    draw_centered(64, 322, 339, "I'M HELPING!", NAVY)

    # Robot antenna: sticks out to the left of the head, clear of the
    # speech bubble above (a top antenna would collide with its tail).
    thick_line(182, 500, 150, 500, 10, NAVY)
    fill_circle(142, 500, 10, RED)

    # Robot head: white shell, dark face screen, happy eyes, smile.
    fill_rr(180, 450, 400, 600, 28, PANEL)
    fill_rr(200, 470, 380, 580, 18, NAVY)
    fill_ellipse(255, 515, 9, 15, PANEL)
    fill_ellipse(325, 515, 9, 15, PANEL)
    bezier_thick((252, 545), (290, 566), (328, 545), 5, 5, PANEL, steps=24)

    # Robot neck and body.
    fill_rect(270, 600, 310, 614, NAVY)
    fill_rr(170, 610, 410, 880, 24, TEAL)
    fill_rr(200, 640, 380, 762, 16, TEAL_LIGHT)
    fill_circle(245, 700, 14, RED)
    fill_circle(290, 700, 14, YELLOW)
    fill_circle(335, 700, 14, PANEL)

    # Robot legs and feet.
    fill_rect(200, 880, 240, 922, NAVY)
    fill_rect(340, 880, 380, 922, NAVY)
    fill_ellipse(220, 926, 32, 12, NAVY)
    fill_ellipse(360, 926, 32, 12, NAVY)

    # Robot arm reaching out to the hose.
    thick_line(408, 680, 520, 640, 30, TEAL)
    fill_circle(525, 638, 18, TEAL)

    # Red fire hose, curving to the nozzle.
    bezier_thick((520, 640), (600, 575), (645, 580), 15, 13, RED)
    fill_rect(640, 566, 676, 594, GREY)
    fill_circle(678, 580, 12, GREY)

    # The water: one big arc from the nozzle onto the user.
    bezier_thick((678, 580), (810, 390), (888, 638), 30, 18, WATER)
    bezier_thick((678, 580), (810, 390), (888, 638), 16, 9, WATER_LIGHT)
    # Splash where the water hits the user (kept off the face so the
    # shocked expression stays readable at thumbnail size).
    for cx, cy, r in ((866, 612, 16), (916, 600, 13), (886, 584, 11),
                      (850, 648, 12), (924, 636, 10), (896, 668, 9)):
        fill_circle(cx, cy, r, WATER)
    # Flying droplets along the arc.
    for cx, cy, r in ((742, 470, 9), (800, 430, 8), (850, 470, 9),
                      (720, 520, 7), (830, 540, 8), (770, 400, 7),
                      (880, 520, 7), (700, 600, 8), (760, 600, 7)):
        fill_circle(cx, cy, r, WATER)

    # The user: soaked, arms thrown up, hair plastered down.
    # Legs and feet first, then body, then head.
    fill_rect(872, 860, 900, 920, NAVY)
    fill_rect(922, 860, 950, 920, NAVY)
    fill_ellipse(886, 926, 28, 11, NAVY)
    fill_ellipse(936, 926, 28, 11, NAVY)
    fill_rr(860, 700, 950, 862, 20, ORANGE)
    # Raised arms.
    thick_line(868, 716, 828, 640, 22, SKIN)
    thick_line(942, 716, 982, 640, 22, SKIN)
    fill_circle(826, 636, 12, SKIN)
    fill_circle(984, 636, 12, SKIN)
    # Head: hair cap, then face, shocked eyes and "o" mouth.
    fill_ellipse(905, 598, 43, 30, HAIR)
    fill_circle(905, 625, 40, SKIN)
    fill_ellipse(905, 598, 43, 26, HAIR)
    fill_circle(891, 620, 4, NAVY)
    fill_circle(919, 620, 4, NAVY)
    fill_circle(905, 646, 6, NAVY)
    # Water dripping off the user.
    for cx, cy, r in ((872, 700, 7), (940, 720, 7), (905, 700, 6),
                      (860, 780, 6), (948, 800, 6), (905, 830, 7)):
        fill_circle(cx, cy, r, WATER)

    # Puddle under the user.
    fill_ellipse(905, 938, 92, 16, WATER_LIGHT)
    fill_ellipse(905, 936, 70, 11, WATER)

    # Grass tufts.
    for bx, by in ((60, 1000), (500, 1006), (990, 996)):
        fill_triangle((bx - 16, by), (bx + 16, by), (bx, by - 34), GRASS_DARK)


# ---- minimal PNG writer (stdlib only) ----
def _chunk(tag, data):
    out = struct.pack(">I", len(data)) + tag + data
    out += struct.pack(">I", binascii.crc32(tag + data) & 0xFFFFFFFF)
    return out


def write_png(path, width, height, rgb):
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)  # filter: none
        raw += rgb[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", ihdr)
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += _chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "/output/entry.png"
    draw_scene()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    n = write_png(out, W, H, buf)
    print("wrote %s (%d bytes, %dx%d)" % (out, n, W, H))


if __name__ == "__main__":
    main()
