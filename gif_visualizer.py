#!/usr/bin/env python3
"""
Render WLED visualizations by connecting to a WLED node and pulling colors from /json/live
"""

import argparse
import requests
import sys
import time

from color_utils import split_rgb
from PIL import Image, ImageDraw


LED_COLS = 20
LED_ROWS = 3
LED_SIZE = 7                      # size in pixels for each LED
SPACE_SIZE = 2                    # space in pixels between each LED
LED_COUNT = LED_COLS * LED_ROWS   # Do not exceed 100. That is all json/live displays
NODE_IP = '192.168.10.50'
AC_EFFECT_CNT = 118

# Palette used when rendering effects
EFFECT_PALETTE = 6
# Effect used when rendering palettes
PALLET_EFFECT = 65

image_size = (LED_COLS * (LED_SIZE + SPACE_SIZE),
              (LED_ROWS * (LED_SIZE + SPACE_SIZE)))

color_1 = 'FF6E41'   # OrangeRed
color_2 = 'FFE369'   # Yellow
color_3 = 'FFB9B8'   # Pink
slow_effects = [4, 5, 32, 36, 44, 57, 58, 82, 90]


class Node:
    """ WLED node used to render palette and effects. """
    def __init__(self, ip, static_mode=False):
        self.ip = ip
        try:
            req = requests.get(f'http://{ip}/json', timeout=3)
        except requests.exceptions.Timeout:
            print(f'Could not to WLED node at {ip}. Configure NODE_IP and try again.')
            sys.exit(1)

        self.json = req.json()
        self.palettes = self.json['palettes']
        self.effects = self.json['effects']
        self.palette_cnt = len(self.palettes)
        self.effect_cnt = len(self.effects)
        #
        self.initialize(static_mode)

    def initialize(self, static_mode=False):
        # Set segment bounds and colors
        bg_col = [0,0,0] if static_mode else list(split_rgb(color_2))
        api_cmd = {"on": True, "bri": 255,
                   "col": [list(split_rgb(color_1)),
                           bg_col,
                           list(split_rgb(color_3))],
                   "seg": [{"start": 0, "stop": LED_COUNT, "sel": True,
                            "col": [list(split_rgb(color_1)),
                                bg_col,
                                list(split_rgb(color_3))]}]}
        req = requests.put(f'http://{self.ip}/json', json=api_cmd)

    def initialize_matrix(self):
        api_cmd = {"on": True, "bri": 127,
                   "col": [list(split_rgb(color_1)),
                           list(split_rgb(color_2)),
                           list(split_rgb(color_3))],
                   "seg": []}
        for i in range(LED_ROWS):
            api_cmd["seg"].append({"start": i * LED_COLS, "stop": (i+1) * LED_COLS, "sel": True, "rev": bool(i % 2)})
        req = requests.put(f'http://{self.ip}/json', json=api_cmd)

    def led_colors(self):
        # return array of colors from live view.
        req = requests.get(f'http://{self.ip}/json/live')
        return req.json()['leds']

    def win(self, fx, fp, sx=127, ix=127):
        # HTTP Request API call
        req = requests.get(f'http://{self.ip}/win&FP={fp}&FX={fx}&SX={sx}&IX={ix}&TT=0')

    def __str__(self):
        return f'WLED Node ver: {self.json["info"]["ver"]} at {self.ip}'


def draw_frame():
    image = Image.new("P", image_size, "black")
    draw = ImageDraw.Draw(image)
    leds = node.led_colors()
    for i in range(LED_COUNT):
        row = i // LED_COLS
        col = LED_COLS - 1 - (i % LED_COLS) if row % 2 else i % LED_COLS
        x1 = col * (LED_SIZE + SPACE_SIZE) + 1
        y1 = row * (LED_SIZE + SPACE_SIZE) + 1
        draw.rectangle((x1, y1, x1 + LED_SIZE, y1 + LED_SIZE), fill=split_rgb(leds[i]))
    return image


def add_frame_(img, x):
    # renders frame at 1 pixel per LED along y axis
    leds = node.led_colors()
    for y in range(LED_COUNT):
        img.putpixel((x, y), split_rgb(leds[y]))
    return img


def render_palette(fp=0):
    # Set effect to Palette and palette fp
    node.win(PALLET_EFFECT, fp)
    print(f'rendering palette {fp} {node.palettes[fp]}')
    time.sleep(0.3)
    frames = []
    for number in range(80):
        time.sleep(0.02)
        frames.append(draw_frame())
    frame_one = frames[0]
    frame_one.save(f'gifs/PAL_{fp:02d}.gif', format="GIF", append_images=frames,
                   save_all=True, duration=30, loop=0, quality=10)


def render_effect_static(fx, fp=None, ix=127, frame_cnt=None):
    if fp is None:
        # use fire palette for fire 2012 effect
        fp = EFFECT_PALETTE if fx != 66 else 35
    if fx in slow_effects:
        sx = 255
        frame_cnt = frame_cnt or 160
    else:
        sx = 127
        frame_cnt = frame_cnt or 160

    node.win(fx, fp, sx, ix)
    image = Image.new("RGB", (frame_cnt, LED_COUNT), "black")
    print(f'rendering effect {fx} {node.effects[fx]}')
    time.sleep(0.3)
    for i in range(frame_cnt):
        add_frame_(image, i)
        time.sleep(0.02)
    image.save(f'gifs/FX_static_{fx:03d}.gif', format="GIF", quality=10)


def render_effect(fx=0, fp=None, ix=None, frame_cnt=None):
    # Set effect to fx and palette to Party
    if fp is None:
        # use fire palette for fire 2012 effect
        fp = EFFECT_PALETTE if fx != 66 else 35
    # long periods where these effects do nothing - so speed up and capture longer

    if fx in slow_effects:
        sx = 255
        frame_cnt = frame_cnt if frame_cnt is not None else 160
    else:
        sx = 127
        frame_cnt = frame_cnt if frame_cnt is not None else 80
    if ix is None:
        ix = 127
    node.win(fx, fp, sx, ix)
    print(f'rendering effect {fx} {node.effects[fx]}')
    time.sleep(0.3)
    frames = []
    for number in range(frame_cnt):
        time.sleep(0.02)
        frames.append(draw_frame())
    frame_one = frames[0]
    frame_one.save(f'gifs/FX_{fx:03d}.gif', format="GIF", append_images=frames,
                   save_all=True, duration=30, loop=0, quality=10)


def decode_sr_parms(info):
    # Convert "Fade rate,Puddle size,,Select bin,Volume (minimum);!,!;!" to something sensible
    desc = ''
    parms = ['Speed', 'Intensity', 'FFT Low', 'FFT High', 'FFT Custom']
    labels = info.split(';')
    labels = labels[0].split(',')
    for i in range(len(labels)):
        label = labels[i]
        if label == '!':
            desc += f'**{parms[i]}** <br /> '
        elif label != '':
            desc += f'**{parms[i]}**: {label} <br />'
    return desc


def render_all_effects(static_mode=False, min_fx=0, max_fx=AC_EFFECT_CNT):
    for i in range(min_fx, max_fx):
        name = node.effects[i]
        if 'Reserved' in name:  # '♪' in name or '♫' in name or
            continue
        if static_mode:
            render_effect_static(i)
        else:
            render_effect(i)


def render_all_palettes():
    for i in range(0, node.palette_cnt):
        render_palette(i)


def make_md():
    # url of previous effect / palette renderings
    old_url = 'https://raw.githubusercontent.com/photocromax/WLED-live-visualizations/master/GIF/'
    image = Image.new("P", (16, 16), "black")
    draw = ImageDraw.Draw(image)
    # set fx to Solid Pattern Tri - pal to * Colors Only - speed to 0
    node.win(84, 5, ix=0)
    time.sleep(0.2)
    leds = node.led_colors()
    draw.rectangle((1, 1, 14, 14), fill=split_rgb(leds[0]))
    image.save('gifs/color_1.gif', format="GIF")
    draw.rectangle((1, 1, 14, 14), fill=split_rgb(leds[1]))
    image.save('gifs/color_2.gif', format="GIF")
    draw.rectangle((1, 1, 14, 14), fill=split_rgb(leds[2]))
    image.save('gifs/color_3.gif', format="GIF")

    with open('effects.md', 'w', encoding='utf8') as fp:
        fp.write(f'''### Effects
To aid in showing where colors vs palettes are used, all effects are rendered with the _{node.palettes[EFFECT_PALETTE]}_ palette  
and the colors
![](gifs/color_1.gif) primary
![](gifs/color_2.gif) secondary
![](gifs/color_3.gif) tertiary colors. For static renders the background (secondary) color is set to black.

| ID | Effect | Animated Visual | Static Visual | Parms
| ---: | --- | --- | --- | ---
''')
        for i in range(0, AC_EFFECT_CNT):
            if '@' in node.effects[i]:
                name, det = node.effects[i].split('@')
                if ';' in det:
                    info = decode_sr_parms(det)
                else:
                    info = det
            else:
                name = node.effects[i]
                info = '-'
            fp.write(f'| {i} | {name} | ![](gifs/FX_{i:03d}.gif) | ![](gifs/FX_static_{i:03d}.gif) | {info}\n')

    with open('palettes.md', 'w') as fp:
        fp.write(f'### Palettes\nPalettes are rendered with the {node.effects[PALLET_EFFECT]} effect\n')
        fp.write('| ID | Palette | New Vis | Old Vis \n| ---: | --- | --- | ---\n')
        for i in range(node.palette_cnt):
            fp.write(f'| {i} | {node.palettes[i]} | ![](gifs/PAL_{i:02d}.gif) | ![]({old_url}/PAL_{i}.gif)\n')

    if node.effect_cnt > AC_EFFECT_CNT:
        tab_head = '| ID | Effect | Visual | Settings \n| ---: | --- | --- | --- \n'
        sr1 = f'#### Volume Reactive Effects\n{tab_head}'
        sr2 = f'#### Frequency Reactive Effects\n{tab_head}'
        sr3 = f'#### Matrix Effects\n{tab_head}'
        sr4 = f'#### Misc SR Effects\n{tab_head}'
        with open('effects_sr.md', 'w', encoding='utf8') as fp:
            fp.write('''### SR Effects\nAll effects are rendered with the Party palette and, of course, _Thunderstruck_ \n''')
            for i in range(AC_EFFECT_CNT, node.effect_cnt):
                if '@' in node.effects[i]:
                    name, det = node.effects[i].split('@')
                    if ';' in det:
                        info = decode_sr_parms(det)
                    else:
                        info = det
                else:
                    name, info = node.effects[i], ''
                row = f'| {i} | {name} | ![](gifs/FX_{i:03d}.gif) | {info} \n'
                if '♪' in name:
                    sr1 += row
                elif '♫' in name:
                    sr2 += row
                elif name.startswith('2D '):
                    sr3 += row
                elif 'Reserved' not in name:
                    sr4 += row
            fp.write(sr1)
            fp.write(sr2)
            fp.write(sr3)
            fp.write(sr4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Render effects and/or palettes as animated GIFs')
    parser.add_argument('-md', action='store_true', help='generate effect/palette markdown files')
    parser.add_argument('-s', action='store_true', help='Static mode - render static GIFs')
    parser.add_argument('--effect', dest='effect', type=int,
                        help='Render effect (-1 for all, -2 all AC effects, -3 all SR effects)')
    parser.add_argument('--palette', dest='palette', type=int,
                        help='Render palette (-1 for all)')
    parser.add_argument('--ip', dest='ip', help='Override IP address of WLED node')

    args = parser.parse_args()

    ip = args.ip or NODE_IP
    node = Node(ip, args.s)

    if args.effect == -1:
        render_all_effects(args.s)
    elif args.effect == -2:
        # AC only effects
        render_all_effects(args.s, 0, AC_EFFECT_CNT)
    elif args.effect == -3:
        # AC only effects
        render_all_effects(args.s, AC_EFFECT_CNT, node.effect_cnt)
    elif args.effect is not None:
        if args.s:
            render_effect_static(args.effect)
        else:
            render_effect(args.effect)

    if args.palette == -1:
        render_all_palettes()
    elif args.palette is not None:
        render_palette()

    if args.md:
        make_md()

