#/usr/bin/env python3

""" """

import argparse
import requests
import sys
import time
import xml.etree.ElementTree as ET

from color_utils import split_rgb
from PIL import Image, ImageDraw


LED_COLS = 20
LED_ROWS = 3
LED_SIZE = 7
SPACE_SIZE = 2
LED_COUNT = LED_COLS * LED_ROWS
FRAME_COUNT = LED_COLS * LED_ROWS
NODE_IP = '192.168.10.208'

# Palette used when rendering effects
EFFECT_PALETTE = 6
# Effect used when rendering palettes
PALLET_EFFECT = 65

image_size = (LED_COLS * (LED_SIZE + SPACE_SIZE),
              (LED_ROWS * (LED_SIZE + SPACE_SIZE)))

color_1 = 'FF6E41'   # redorange
color_2 = 'FFE369'   # yellow
color_3 = 'FFB9B8'   # pink


class Node:
    """ WLED node used to render palette and effects. """
    def __init__(self, ip):
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
        self.initialize()

    def initialize(self):
        # Set segment bounds and colors
        api_cmd = {"on": True, "bri": 127,
                   "col": [list(split_rgb(color_1)),
                           list(split_rgb(color_2)),
                           list(split_rgb(color_3))],
                   "seg": [{"start": 0, "stop": LED_COUNT,
                            "pal": 5, "fx": 84, "sx": 127, "ix": 127}]}
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
        draw.rectangle((x1, y1, x1 + LED_SIZE, y1 + LED_SIZE), fill=split_rgb(int(leds[i], 16)))
    return image


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


def render_effect(fx=0, fp=None, frame_cnt=None):
    # Set effect to fx and palette to Party
    if fp is None:
        # use fire palette for fire 2012 effect
        fp = EFFECT_PALETTE if fx != 66 else 35
    # long periods where these effects do nothing - so speed up and capture longer
    slow_effects = [4, 5, 32, 36, 44, 57, 58, 82, 90]
    if fx in slow_effects:
        sx = 255
        frame_cnt = frame_cnt if frame_cnt is not None else 160
    else:
        sx = 127
        frame_cnt = frame_cnt if frame_cnt is not None else 80
    node.win(fx, fp, sx)
    print(f'rendering effect {fx} {node.effects[fx]}')
    time.sleep(0.3)
    frames = []
    for number in range(frame_cnt):
        time.sleep(0.02)
        frames.append(draw_frame())
    frame_one = frames[0]
    frame_one.save(f'gifs/FX_{fx:03d}.gif', format="GIF", append_images=frames,
                   save_all=True, duration=30, loop=0, quality=10)


def render_all_effects():
    for i in range(0, node.effect_cnt):
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
    draw.rectangle((1, 1, 14, 14), fill=split_rgb(int(leds[0], 16)))
    image.save('gifs/color_1.gif', format="GIF")
    draw.rectangle((1, 1, 14, 14), fill=split_rgb(int(leds[1], 16)))
    image.save('gifs/color_2.gif', format="GIF")
    draw.rectangle((1, 1, 14, 14), fill=split_rgb(int(leds[2], 16)))
    image.save('gifs/color_3.gif', format="GIF")

    with open('effects.md', 'w') as fp:
        fp.write(f'''### Effects
To aid in showing where colors vs palettes are used, all effects are rendered with the _{node.palettes[EFFECT_PALETTE]}_ palette  
and the colors
![](gifs/color_1.gif) primary
![](gifs/color_2.gif) secondary
![](gifs/color_3.gif) tertiary colors

| ID | Effect | New Visual | Old Visual 
| ---: | --- | --- | --- 
''')
        for i in range(node.effect_cnt):
            fp.write(f'| {i} | {node.effects[i]} | ![](gifs/FX_{i:03d}.gif) | ![]({old_url}/FX_{i}.gif)\n')

    with open('palettes.md', 'w') as fp:
        fp.write(f'### Palettes\nPalettes are rendered with the {node.effects[PALLET_EFFECT]} effect\n')
        fp.write('| ID | Palette | New Vis | Old Vis \n| ---: | --- | --- | ---\n')
        for i in range(node.palette_cnt):
            fp.write(f'| {i} | {node.palettes[i]} | ![](gifs/PAL_{i:02d}.gif) | ![]({old_url}/PAL_{i}.gif)\n')


if __name__ == "__main__":
    node = Node(NODE_IP)

    parser = argparse.ArgumentParser(description='Render effects and/or palettes as animated GIFs')
    parser.add_argument('-md', action='store_true', help='generate effect/palette markdown files')
    parser.add_argument('--effect', dest='effect', type=int,
                        help='Render effect (-1 for all)')
    parser.add_argument('--palette', dest='palette', type=int,
                        help='Render palette (-1 for all)')

    args = parser.parse_args()

    if args.effect == -1:
        render_all_effects()
    elif args.effect is not None:
        render_effect(args.effect)

    if args.palette == -1:
        render_all_palettes()
    elif args.palette is not None:
        render_palette()

    if args.md:
        make_md()
