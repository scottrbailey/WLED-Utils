#!/usr/bin/env python3
"""
Render WLED visualizations by connecting to a WLED node and pulling colors from /json/live
"""

import argparse
import asyncio
import json
import queue
import requests
import sys
import time
import websockets

from color_utils import split_rgb
from PIL import Image, ImageDraw, ImageFilter


LED_COLS = 20
LED_ROWS = 3
LED_SIZE = 7                      # size in pixels for each LED
SPACE_SIZE = 2                    # space in pixels between each LED
LED_COUNT = LED_COLS * LED_ROWS   # Do not exceed 100. That is all json/live displays
STATIC_LED_COUNT = 96
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
        self.frames = []
        #
        self.initialize(static_mode)

    def initialize(self, static_mode=False):
        # Set segment bounds and colors
        bg_col = [0,0,0] if static_mode else list(split_rgb(color_2))
        api_cmd = {"on": True, "bri": 255, "transition": 0,
                   "col": [list(split_rgb(color_1)),
                           bg_col,
                           list(split_rgb(color_3))],
                   "seg": [{"start": 0, "stop": STATIC_LED_COUNT, "sel": True,
                            "col": [list(split_rgb(color_1)),
                                bg_col,
                                list(split_rgb(color_3))]}]}
        req = requests.put(f'http://{self.ip}/json', json=api_cmd)

    def led_colors(self):
        # return array of colors from live view.
        req = requests.get(f'http://{self.ip}/json/live')
        return req.json()['leds']

    def win(self, fx, fp, sx=127, ix=127):
        # HTTP Request API call
        req = requests.get(f'http://{self.ip}/win&FP={fp}&FX={fx}&SX={sx}&IX={ix}&TT=0')

    async def run_and_record(self, fx, pal, sx=127, ix=127, frame_cnt=160):
        # switch to effect/palette, connect websocket and capture live data
        frames = []
        cnt = 0
        print(f'Recording {self.effects[fx]} - {self.palettes[pal]}')
        async with websockets.connect(f'ws://{self.ip}/ws') as ws:
            parms = {"transition": 0, "bri": 255,
                     "seg": [{"fx": fx, "pal": pal, "sx": sx, "ix": ix}]}
            await ws.send(json.dumps(parms))
            time.sleep(0.3)
            await ws.send('{"lv": true}')
            while cnt < frame_cnt:
                data = await ws.recv()
                jd = json.loads(data)
                if 'leds' in jd:
                    leds = [int(c, 16) for c in jd.get('leds')]
                    frames.append(leds)
                    cnt += 1
        self.frames = frames

    def __str__(self):
        return f'WLED Node ver: {self.json["info"]["ver"]} at {self.ip}'


class Renderer:
    ANIMATED_MODE = 1
    STATIC_MODE = 2
    MULTI_MODE = 3               # render animated and static

    slow_effects = [4, 5, 32, 36, 44, 57, 58, 82, 90]

    def __init__(self, wled, cols, rows, led_size, space_size, mode=ANIMATED_MODE):
        self.wled = wled
        self.cols = cols
        self.rows = rows
        self.led_size = led_size
        self.space_size = space_size
        self.combined_size = led_size + space_size
        self.mode = mode
        self.led_count = rows * cols
        self.image_size = (cols * self.combined_size,
                           rows * self.combined_size)
        self.frame_cnt = 0

    def _render_animated_frame(self, frame_no):
        data = self.wled.frames[frame_no]
        if data:
            image = Image.new("P", self.image_size)
            draw = ImageDraw.Draw(image)
            for i in range(self.led_count):
                row = i // self.cols
                col = self.cols - 1 - (i % self.cols) if row % 2 else i % self.cols
                x1 = col * self.combined_size
                y1 = row * self.combined_size
                draw.rectangle((x1, y1, x1+self.led_size, y1 + self.led_size), fill=split_rgb(data[i]))
            return image

    def _render_animated(self, fname):
        #
        frames = []
        for i in range(len(self.wled.frames)):
            frames.append(self._render_animated_frame(i))
        frame_one = frames[0]
        frame_one.save(f'gifs/animated/{fname}.gif', format="GIF", append_images=frames, save_all=True,
                       duration=30, loop=0, quality=10)

    def _render_static(self, fname):
        #
        lm = STATIC_LED_COUNT - 1
        pixel_size = 2
        image = Image.new("RGB", (self.frame_cnt * pixel_size, STATIC_LED_COUNT * pixel_size), "black")
        draw = ImageDraw.Draw(image)
        for x in range(len(self.wled.frames)):
            data = self.wled.frames[x]
            if data is None:
                continue
            for i in range(STATIC_LED_COUNT):
                y = lm - i
                x1 = x * pixel_size
                y1 = y * pixel_size
                x2 = x1 + pixel_size - 1
                y2 = y1 + pixel_size - 1
                draw.rectangle((x1, y1, x2, y2), fill=split_rgb(data[i]))
                # image.putpixel((x, y), split_rgb(data[i]))
        image.filter(ImageFilter.GaussianBlur(radius=2))
        image.save(f'gifs/static/{fname}.png', format="PNG", quality=10)

    def render(self, fname, fx, pal, sx=127, ix=127, frame_cnt=160, mode=None):
        self.frame_cnt = frame_cnt
        asyncio.run(self.wled.run_and_record(fx, pal, sx, ix, self.frame_cnt))
        print('Rendering')
        if mode is None:
            mode = self.mode
        if mode & self.ANIMATED_MODE:
            self._render_animated(fname)
        if mode & self.STATIC_MODE:
            self._render_static(fname)


def render_effect(renderer, fx=0, pal=None, ix=None, frame_cnt=None):
    # Set effect to fx and palette to Party
    if pal is None:
        # use fire palette for fire 2012 effect
        pal = EFFECT_PALETTE if fx != 66 else 35
    # long periods where these effects do nothing - so speed up and capture longer

    if frame_cnt is None:
        frame_cnt = 160
    if fx in Renderer.slow_effects:
        sx = 255
    else:
        sx = 127
    if ix is None:
        ix = 127
    node.win(fx, pal, sx, ix)
    print(f'rendering effect {fx} {node.effects[fx]}')
    fname = f'FX_{fx:03d}'
    renderer.render(fname, fx, pal, sx, ix, frame_cnt)


def render_palette(renderer, pal):
    #
    fname = f'PAL_{pal:02d}.gif'
    renderer.render(fname, PALLET_EFFECT, pal, frame_cnt=1, mode=renderer.ANIMATED_MODE)


def render_all_effects(r, min_fx=0, max_fx=AC_EFFECT_CNT):
    for i in range(min_fx, max_fx):
        name = node.effects[i]
        if 'Reserved' in name:  # '♪' in name or '♫' in name or
            continue
        render_effect(r, i)


def render_all_palettes(r):
    for i in range(0, node.palette_cnt):
        render_palette(r, i)


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
    renderer = Renderer(node, LED_COLS, LED_ROWS, LED_SIZE, SPACE_SIZE, 3)

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
            render_effect(args.effect)
        else:
            render_effect(args.effect)

    if args.palette == -1:
        render_all_palettes()
    elif args.palette is not None:
        render_palette()

    if args.md:
        make_md()

