#!/usr/bin/env python3
"""Generates PLACEHOLDER app icons (replace icons/icon-1024.png with your real artwork, then
re-run with --resize-only to rebuild the smaller sizes). No transparency, as Apple requires."""
import sys, math
from PIL import Image, ImageDraw

SRC = 'icons/icon-1024.png'

def draw_placeholder():
    S = 1024
    img = Image.new('RGB', (S, S))
    px = img.load()
    c1, c2 = (179, 157, 219), (232, 130, 159)          # suite purple -> pink
    for y in range(S):
        for x in range(S):
            t = (x + y) / (2 * S - 2)
            px[x, y] = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
    d = ImageDraw.Draw(img)
    # a small repeating tile motif: 3x3 four-petal flowers
    cell = S // 3
    for gy in range(3):
        for gx in range(3):
            cx, cy = gx * cell + cell // 2, gy * cell + cell // 2
            r = cell * 0.19
            for k in range(4):
                a = k * math.pi / 2 + math.pi / 4
                ox, oy = cx + math.cos(a) * r * 0.9, cy + math.sin(a) * r * 0.9
                d.ellipse([ox - r * .75, oy - r * .75, ox + r * .75, oy + r * .75], fill=(255, 250, 240))
            d.ellipse([cx - r * .38, cy - r * .38, cx + r * .38, cy + r * .38], fill=(232, 183, 79))
    img.save(SRC)

if '--resize-only' not in sys.argv:
    draw_placeholder()
base = Image.open(SRC).convert('RGB')
for size in (512, 192, 180, 167, 152):
    base.resize((size, size), Image.LANCZOS).save(f'icons/icon-{size}.png')
print('icons written')
