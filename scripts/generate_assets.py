"""Generate the profile's original editorial artwork and seamless GIF loops."""

import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
CREAM = "#f7f4ed"
INK = "#17191c"
RED = "#d50920"


def write_svg(name: str, width: int, height: int, content: str) -> None:
    (ASSETS / name).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">{content}</svg>\n',
        encoding="utf-8",
    )


def generate_ticker(name: str, phrase: str, direction: int) -> None:
    # A full tile travels per cycle; the last-to-first step equals every other step.
    width, height, frame_count = 960, 48, 192
    font_path = os.environ.get("README_MONO_FONT", "C:/Windows/Fonts/consola.ttf")
    font = ImageFont.truetype(font_path, size=17)
    tile = Image.new("RGB", (width, height), INK)
    draw = ImageDraw.Draw(tile)
    draw.text((20, 14), ">>>", font=font, fill=RED)
    draw.text((70, 14), phrase, font=font, fill=CREAM)
    draw.text((width - 55, 14), ">>>", font=font, fill=RED)
    draw.line((0, 0, width, 0), fill=RED, width=2)
    frames = []
    for index in range(frame_count):
        offset = direction * index * (width // frame_count) % width
        frame = Image.new("RGB", tile.size, INK)
        frame.paste(tile, (offset, 0))
        frame.paste(tile, (offset - width, 0))
        frames.append(frame)
    frames[0].save(ASSETS / name, save_all=True, append_images=frames[1:],
                   duration=70, loop=0, optimize=True)


def flame_points(x: float, base: float, height: float, phase: float) -> list:
    """Two curving sides meet at a moving tip, with a fork in the inner side."""
    points = []
    for step in range(41):
        rise = step / 40
        sway = math.sin(rise * 4 + phase) * 25 * rise
        breadth = (1 - rise) * (11 + 6 * math.sin(rise * 5 + phase))
        points.append((x + sway - breadth, base - rise * height))
    for step in range(40, -1, -1):
        rise = step / 40
        sway = math.sin(rise * 4 + phase) * 25 * rise
        breadth = (1 - rise) * (5 + 4 * math.cos(rise * 5 + phase))
        points.append((x + sway + breadth, base - rise * height))
    return points


def generate_fire(name: str, width: int, height: int) -> None:
    palette = [0, 0, 0, 213, 9, 32, 145, 10, 27, 245, 95, 100] + [0] * 756
    frames = []
    for index in range(48):
        phase = index / 48 * math.tau
        frame = Image.new("P", (width, height), 0)
        frame.putpalette(palette)
        draw = ImageDraw.Draw(frame)
        for side in ((0, 1) if width > 200 else (0,)):
            for flame in range(7):
                x = 6 + flame * 9 if side == 0 else width - 6 - flame * 9
                flame_height = (height * .95 + 12 * math.sin(phase + flame)) * (1 - flame * .1)
                points = flame_points(x, height + 12, flame_height, phase + flame * .8)
                if flame % 3 == 0:
                    draw.polygon(points, fill=1 if flame == 0 else 2)
                else:
                    draw.line(points, fill=1 if flame % 2 else 3, width=1)
            for ember in range(5):
                rise = (index / 48 + ember / 5) % 1
                x = 18 + ember * 15 + math.sin(phase + ember) * 5
                if side:
                    x = width - x
                y = height * (1 - rise)
                draw.line((x, y, x + 2, y - 4), fill=1, width=2)
        frames.append(frame)
    frames[0].save(ASSETS / name, save_all=True, append_images=frames[1:],
                   duration=80, loop=0, transparency=0, disposal=2, optimize=False)


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    write_svg("identity.svg", 960, 240, f'''
<rect width="960" height="240" fill="{CREAM}"/>
<path d="M28 26h42" stroke="{RED}" stroke-width="3"/>
<text x="28" y="55" font-family="monospace" font-size="14" letter-spacing="4" fill="{INK}">HELLO, I'M</text>
<text x="25" y="153" font-family="Georgia,serif" font-size="110" font-weight="bold" letter-spacing="-5" fill="{INK}">TRINH LE<tspan fill="{RED}">.</tspan></text>
<text x="30" y="211" font-family="Georgia,serif" font-size="42" fill="{RED}">BUSINESS → DATA → AI.</text>
<text x="932" y="40" text-anchor="end" font-family="monospace" font-size="11" letter-spacing="2" fill="{INK}">ALWAYS A WORK IN PROGRESS</text>
''')
    write_svg("journey.svg", 960, 130, f'''
<rect width="960" height="130" fill="{CREAM}"/>
<path d="M40 65 C110 65 110 25 210 45 S350 100 390 65 S540 15 570 50 S700 100 750 60 S860 30 920 55" fill="none" stroke="{RED}" stroke-width="2"/>
{''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="{RED}"/><text x="{x}" y="110" text-anchor="middle" font-family="monospace" font-size="17" fill="{INK}">{label}</text>' for x, y, label in [(55,65,'VIETNAM'),(225,48,'BUSINESS'),(400,57,'DATA'),(570,50,'AI'),(750,60,'UK'),(910,52,'?')])}
''')
    generate_ticker("code-forward.gif", "SELECT * FROM curiosity;   >>>   learn(); build(); contribute();   >>>   human x AI", 1)
    generate_ticker("code-reverse.gif", "explore() > question() > build()   >>>   model.fit(ideas, reality)   >>>   keep(learning)", -1)
    generate_fire("fire-edges.gif", 960, 120)
    generate_fire("fire-spark.gif", 120, 90)


if __name__ == "__main__":
    main()
