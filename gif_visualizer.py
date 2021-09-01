#/usr/bin/env python3

""" """

import argparse
import requests
import time

from color_utils import split_rgb
from PIL import Image, ImageDraw


LED_COLS = 20
LED_ROWS = 3
LED_SIZE = 7
SPACE_SIZE = 2
FRAME_COUNT = LED_COLS * LED_ROWS
NODE_IP = '192.168.10.208'
OLD_URL = 'https://raw.githubusercontent.com/photocromax/WLED-live-visualizations/master/GIF/'
# Palette used when rendering effects
EFFECT_PALETTE = 6
# Effect used when rendering palettes
PALLET_EFFECT = 65

image_size = (LED_COLS * (LED_SIZE + SPACE_SIZE),
              (LED_ROWS * (LED_SIZE + SPACE_SIZE)))
# populated from [NODE_IP]/json
effect_cnt = 0
palette_cnt = 0
effects = []
palettes = []
color_1 = 'FF6E41'
color_2 = 'FFE369'
color_3 = 'FFB9B8'


def draw_frame():
    req = requests.get(f'http://{NODE_IP}/json/live')
    image = Image.new("P", image_size, "black")
    draw = ImageDraw.Draw(image)
    leds = req.json()['leds']
    for i in range(LED_COLS * LED_ROWS):
        row = i // LED_COLS
        col = LED_COLS - 1 - (i % LED_COLS) if row % 2 else i % LED_COLS
        x1 = col * (LED_SIZE + SPACE_SIZE) + 1
        y1 = row * (LED_SIZE + SPACE_SIZE) + 1
        # print(f'{i}({col},{row}) - rectangle({x1}, {y1}, #{colors[i]})')
        draw.rectangle((x1, y1, x1 + LED_SIZE, y1 + LED_SIZE), fill=split_rgb(int(leds[i], 16)))
    return image


def render_palette(fp=0):
    # Set effect to Palette and palette fp
    req = requests.get(f'http://{NODE_IP}/win&FX={PALLET_EFFECT}&FP={fp}&TT=0')
    print(f'rendering palette {fp} {palettes[fp]}')
    time.sleep(0.3)
    frames = []
    for number in range(LED_COLS * LED_ROWS):
        time.sleep(0.02)
        frames.append(draw_frame())
    frame_one = frames[0]
    frame_one.save(f'gifs/PAL_{fp:02d}.gif', format="GIF", append_images=frames,
                   save_all=True, duration=100, loop=0, quality=10)


def render_effect(fx=0, fp=None, frame_cnt=60):
    # Set effect to fx and palette to Party
    if fp is None:
        # use fire palette for fire 2012 effect
        fp = EFFECT_PALETTE if fx != 66 else 35
    req = requests.get(f'http://{NODE_IP}/win&FX={fx}&FP={fp}&TT=0&CL=h{color_1}&C2=h{color_2}&C3={color_3}')
    print(f'rendering effect {fx} {effects[fx]}')
    time.sleep(0.3)
    frames = []
    for number in range(frame_cnt):
        time.sleep(0.02)
        frames.append(draw_frame())
    frame_one = frames[0]
    frame_one.save(f'gifs/FX_{fx:03d}.gif', format="GIF", append_images=frames,
                   save_all=True, duration=100, loop=0, quality=10)


def render_all_effects():
    for i in range(0, len(node_info['effects'])):
        render_effect(i)


def render_all_palettes():
    for i in range(0, len(node_info['palettes'])):
        render_palette(i)


def make_md():
    with open('effects.md', 'w') as fp:
        fp.write(f'### Effects\nTo aid in showing where colors vs palettes are used, all effects are rendered with the _{palettes[EFFECT_PALETTE]}_ palette  \n')
        fp.write(f'and these colors: primary <span style="background-color:#{color_1}; padding:5px; border-radius: 10px">{color_1}</span>, ')
        fp.write(f'secondary <span style="background-color:#{color_2}; padding:5px; border-radius: 10px">{color_2}</span>, ')
        fp.write(f' and tertiary <span style="background-color:#{color_3}; padding:5px; border-radius: 10px">{color_3}</span>\n')
        fp.write('| ID | Effect | New Vis | Old Vis \n| ---: | --- | --- | ---\n')
        for i in range(len(effects)):
            fp.write(f'| {i} | {effects[i]} | ![](gifs/FX_{i:03d}.gif) | ![]({OLD_URL}/FX_{i}.gif)\n')
    with open('palettes.md', 'w') as fp:
        fp.write(f'### Palettes\nPalettes are rendered with the {effects[PALLET_EFFECT]} effect\n')
        fp.write('| ID | Palette | New Vis | Old Vis \n| ---: | --- | --- | ---\n')
        for i in range(len(palettes)):
            fp.write(f'| {i} | {palettes[i]} | ![](gifs/PAL_{i:02d}.gif) | ![]({OLD_URL}/PAL_{i}.gif)\n')


if __name__ == "__main__":
    try:
        req = requests.get(f'http://{NODE_IP}/json')
        node_info = req.json()
    except:
        print(f'Could not connect to WLED node at http://{NODE_IP}. Please configure NODE_IP.')
    effects = node_info['effects']
    palettes = node_info['palettes']
    effect_cnt = node_info['info']['fxcount']
    palette_cnt = node_info['info']['palcount']

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
