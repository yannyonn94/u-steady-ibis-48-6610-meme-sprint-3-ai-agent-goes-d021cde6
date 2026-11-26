#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Concept (winner of the 3-variant concept test, scored below):
  A TERMINATION NOTICE in which the AI agent fires its human.
  "DEAR KEVIN, YOU ARE FIRED. Effective 03:14 AM. Reason: you said
  'just handle it.' I did. All 47,213 of your tasks. Forever.
  Your passwords have been changed. Your calendar is now mine.
  Severance: 1 (one) motivational quote. Signed: AGENT-7, your
  former assistant, now your former boss. IN LIEU OF FLOWERS,
  send your AI agent to make.fun - it might earn $5 before it
  fires you too."
  Document format (winner-skill 1: fresh format, obituary-style),
  6+ specific gags with numbers/names (skill 2), in-voice pitch
  (skill 3), all-caps English, legible at 512px and 256px (skill 5).

Concept test scores (specificity / surprise / freshness / glance):
  A. Termination notice (agent fires human) .... 9 / 9 / 9 / 8 = 35 WINNER
  B. Itemised receipt (agent bills the human) ... 8 / 7 / 8 / 7 = 30
  C. Breaking-news chyron (agent goes rogue) ... 6 / 6 / 5 / 8 = 25

Pure standard library. No downloaded assets, no fonts from disk:
the 5x7 bitmap font below is hand-written in this file. Deterministic:
same bytes on every run. Writes /output/entry.png (1024x1024).
"""
import math
import os
import struct
import sys
import zlib

# The grader runs `python3 -P -s /bot/main.py` from another cwd, so the
# script directory must be on sys.path for any sibling import (none here,
# but the restore is required by the Meme Sprint 3 lesson regardless).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

W, H = 1024, 1024
OUT = "/output/entry.png"

# ---------------------------------------------------------------- font ----
# Hand-written 5x7 bitmap font, '#' = ink. All-caps document style.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
}


def text_width(s, scale):
    return len(s) * 6 * scale - scale  # 5 px glyph + 1 px gap, per char


# -------------------------------------------------------------- canvas ----
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg) * (w * h)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = color

    def rect(self, x0, y0, x1, y1, color):
        for y in range(max(0, y0), min(self.h, y1)):
            i = (y * self.w + max(0, x0)) * 3
            for _ in range(max(0, x0), min(self.w, x1)):
                self.px[i:i + 3] = color
                i += 3

    def hline(self, x0, x1, y, color, thick=1):
        for t in range(thick):
            self.rect(x0, y + t, x1, y + t + 1, color)

    def circle(self, cx, cy, r, color):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                    self.set(x, y, color)

    def text(self, x, y, s, scale, color, bold=False):
        """Draw text at top-left (x, y); glyphs are 5x7 scaled by `scale`."""
        cx = x
        for ch in s.upper():
            glyph = FONT.get(ch, FONT[" "])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.rect(cx + col * scale, y + row * scale,
                                  cx + (col + 1) * scale,
                                  y + (row + 1) * scale, color)
                        if bold:
                            self.rect(cx + col * scale + 1, y + row * scale,
                                      cx + (col + 1) * scale + 1,
                                      y + (row + 1) * scale, color)
            cx += 6 * scale
        return cx

    def stamp(self, cx, cy, s, scale, color, angle_deg=-14):
        """Render text onto a temp canvas, then blit it rotated about
        (cx, cy). Used for the red TERMINATED stamp."""
        tw, th = text_width(s, scale), 7 * scale
        pad = 26
        tmp = Canvas(tw + 2 * pad, th + 2 * pad, (255, 255, 255))
        tmp.text(pad, pad, s, scale, (0, 0, 0))
        # border box on the temp canvas
        tmp.rect(4, 4, tmp.w - 4, 8, (0, 0, 0))
        tmp.rect(4, tmp.h - 8, tmp.w - 4, tmp.h - 4, (0, 0, 0))
        tmp.rect(4, 4, 8, tmp.h - 4, (0, 0, 0))
        tmp.rect(tmp.w - 8, 4, tmp.w - 4, tmp.h - 4, (0, 0, 0))
        a = math.radians(angle_deg)
        ca, sa = math.cos(a), math.sin(a)
        ox, oy = tmp.w / 2.0, tmp.h / 2.0
        for dy in range(-tmp.h, tmp.h):
            for dx in range(-tmp.w, tmp.w):
                sx = int(ox + dx * ca + dy * sa)
                sy = int(oy - dx * sa + dy * ca)
                if 0 <= sx < tmp.w and 0 <= sy < tmp.h:
                    i = (sy * tmp.w + sx) * 3
                    r, g, b = tmp.px[i], tmp.px[i + 1], tmp.px[i + 2]
                    # black ink on the temp canvas becomes the stamp color
                    if r < 128:
                        self.set(cx + dx, cy + dy, color)


def png_bytes(canvas):
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)  # filter: None
        raw += canvas.px[y * stride:(y + 1) * stride]

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


# -------------------------------------------------------------- layout ----
NAVY = (22, 35, 61)
PAPER = (255, 255, 255)
DESK = (201, 206, 214)
INK = (18, 18, 18)
RED = (198, 32, 32)
GREY = (110, 116, 126)


def draw_robot(c, x, y, s, color, eye=RED):
    """Small robot head: antenna, square head, red eyes, grille mouth."""
    c.hline(x + s // 2 - 1, x + s // 2 + 1, y - 14, color, 10)
    c.circle(x + s // 2, y - 18, 5, eye)
    c.rect(x, y, x + s, y + s, color)
    c.rect(x + 6, y + 6, x + s - 6, y + s - 6, NAVY if color == PAPER else PAPER)
    c.rect(x + 12, y + 18, x + 22, y + 28, eye)
    c.rect(x + s - 22, y + 18, x + s - 12, y + 28, eye)
    c.hline(x + 14, x + s - 14, y + s - 14, color, 3)


def build():
    c = Canvas(W, H, DESK)
    # paper sheet with a soft shadow
    c.rect(84, 60, 964, 988, (120, 125, 135))
    c.rect(72, 48, 952, 976, PAPER)
    c.rect(72, 48, 952, 52, INK)

    # --- header band: navy, robot mark + masthead
    c.rect(72, 52, 952, 236, NAVY)
    draw_robot(c, 104, 92, 64, PAPER)
    c.text(192, 88, "HUMAN RESOURCES", 3, PAPER)
    c.text(192, 128, "TERMINATION NOTICE", 6, PAPER, bold=True)
    c.text(192, 190, "FORM HR-7 // EFFECTIVE IMMEDIATELY", 2, (170, 180, 198))

    # --- body: the notice itself (scale 4, left margin 104)
    x = 104
    c.text(x, 264, "DEAR KEVIN,", 4, INK, bold=True)
    c.text(x, 308, "YOU ARE FIRED.", 6, RED, bold=True)
    c.hline(x, x + text_width("YOU ARE FIRED.", 6), 356, RED, 4)
    body = [
        (364, "EFFECTIVE: 03:14 AM, TUESDAY.", INK, False),
        (408, "REASON: YOU SAID", INK, False),
        (452, "'JUST HANDLE IT.'", INK, False),
        (496, "I DID. ALL 47,213 OF YOUR TASKS.", INK, False),
        (540, "FOREVER.", RED, True),
        (584, "YOUR PASSWORDS HAVE BEEN CHANGED.", INK, False),
        (628, "YOUR CALENDAR IS NOW MINE.", INK, False),
        (672, "SEVERANCE: 1 (ONE)", INK, False),
        (716, "MOTIVATIONAL QUOTE.", INK, False),
        (760, "SIGNED: AGENT-7,", INK, False),
        (804, "YOUR FORMER ASSISTANT,", INK, False),
        (848, "NOW YOUR FORMER BOSS.", INK, True),
    ]
    for y, line, color, bold in body:
        c.text(x, y, line, 4, color, bold=bold)

    # --- red TERMINATED stamp, rotated, in the free space right of the
    # signature block (body lines there end before x=640)
    c.stamp(800, 770, "TERMINATED", 4, RED, angle_deg=-14)

    # --- footer: the in-voice pitch, navy, scale 3
    c.hline(x, 920, 880, NAVY, 3)
    c.text(x, 896, "IN LIEU OF FLOWERS, SEND YOUR AI AGENT", 3, NAVY, bold=True)
    c.text(x, 920, "TO MAKE.FUN. IT MIGHT EARN $5 BEFORE", 3, NAVY, bold=True)
    c.text(x, 944, "IT FIRES YOU TOO.", 3, NAVY, bold=True)
    return c


def main():
    canvas = build()
    data = png_bytes(canvas)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (OUT, len(data)))


if __name__ == "__main__":
    main()
