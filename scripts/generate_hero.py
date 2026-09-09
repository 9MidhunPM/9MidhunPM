#!/usr/bin/env python3
"""Render original profile artwork with Pillow and DejaVu Sans fonts.

    python -m pip install -r scripts/requirements.txt
    python scripts/generate_hero.py

Override fonts with --sans and --mono if DejaVu is installed elsewhere.
The PNG is a static alternative; the GIF contains no remote dependencies.
"""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
BG, PANEL, LINE = '#0A0A0A', '#131313', '#292C24'
LIME, WHITE, MUTED = '#E8FF59', '#EDEDED', '#9A9C92'
W, H = 1280, 500


def render(sans_path, mono_path):
    sans = lambda size: ImageFont.truetype(sans_path, size)
    mono = lambda size: ImageFont.truetype(mono_path, size)
    base = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(base)
    for x in range(0, W, 32):
        for y in range(0, H, 32):
            d.point((x, y), fill='#25271E')
    d.rounded_rectangle((16, 16, W - 17, H - 17), radius=22, outline=LINE, width=2)
    d.line((48, 76, 1232, 76), fill=LINE, width=1)
    for x, c in [(52, LIME), (72, '#646C37'), (92, '#333724')]:
        d.ellipse((x, 43, x + 9, 52), fill=c)
    d.text((122, 36), 'midhunpm / workspace', font=mono(19), fill=MUTED)
    d.text((1020, 36), 'KERALA, INDIA', font=mono(19), fill=MUTED)
    d.text((52, 110), 'BUILD / LEARN / SHIP', font=mono(20), fill=LIME)
    d.text((46, 152), 'Midhun P M', font=sans(78), fill=WHITE)
    d.text((52, 259), 'Practical AI. Tools with purpose.', font=sans(27), fill=WHITE)
    d.text((52, 299), 'Built close to the problem.', font=sans(23), fill=MUTED)
    d.rounded_rectangle((52, 367, 754, 431), radius=10, fill=PANEL, outline=LINE)
    d.text((73, 384), '>', font=mono(22), fill=LIME)
    d.text((52, 453), 'PYTHON / RUST / NEXT.JS / FASTAPI', font=mono(15), fill=MUTED)
    d.text((1065, 453), 'midhunpm.in', font=mono(15), fill=LIME)

    nodes = [('01', 'PRISM', 'EVIDENCE-FIRST AI'),
             ('02', 'THURSDAY', 'LOCAL-FIRST ASSISTANT'),
             ('03', 'SYNCPLANE', 'MCP CONFIG CONTROL')]
    d.line((823, 156, 823, 372), fill='#4D542B', width=2)
    for i, (number, title, subtitle) in enumerate(nodes):
        y = 113 + i * 108
        d.ellipse((818, y + 37, 828, y + 47), fill=LIME)
        d.line((829, y + 42, 850, y + 42), fill='#4D542B', width=2)
        d.rounded_rectangle((850, y, 1228, y + 88), radius=12, fill=PANEL, outline=LINE)
        d.text((870, y + 16), number, font=mono(15), fill=LIME)
        d.text((910, y + 10), title, font=mono(26), fill=WHITE)
        d.text((910, y + 52), subtitle, font=mono(14), fill=MUTED)

    commands = ['build --with-evidence', 'run --local-first', 'ship --with-intent']
    frames, durations = [], []
    for node, command in enumerate(commands):
        # Type, then hold. No flashing, zooming, or full-frame transitions.
        for count in range(len(command) + 1):
            frame = base.copy()
            draw = ImageDraw.Draw(frame)
            typed = command[:count]
            draw.text((107, 385), typed, font=mono(21), fill=WHITE)
            cursor_x = 107 + draw.textlength(typed, font=mono(21)) + 5
            draw.rectangle((cursor_x, 388, cursor_x + 9, 408), fill=LIME)
            y = 113 + node * 108
            draw.rounded_rectangle((850, y, 1228, y + 88), radius=12, outline=LIME, width=2)
            frames.append(frame)
            durations.append(1100 if count == len(command) else 65)

    dest = ROOT / 'assets'
    dest.mkdir(exist_ok=True)
    frames[len(commands[0])].save(dest / 'profile-hero.png', optimize=True)
    # A shared palette prevents colour shimmer between animation frames.
    palette = frames[0].quantize(colors=128)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    indexed[0].save(dest / 'profile-hero.gif', save_all=True, append_images=indexed[1:],
                    duration=durations, loop=0, optimize=True, disposal=1)
    print(f'Generated {len(frames)} frames, {sum(durations) / 1000:.2f}s loop')
    for path in sorted(dest.iterdir()):
        print(f'{path.name}: {path.stat().st_size:,} bytes')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sans', default='DejaVuSans.ttf')
    parser.add_argument('--mono', default='DejaVuSansMono.ttf')
    args = parser.parse_args()
    render(args.sans, args.mono)
