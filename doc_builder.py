"""
Generate Effect and Palette markdown files
"""
import json
import os

from textwrap import dedent
from wled import WledNode


def make_effect_md(node:WledNode):
    with open('effect_descriptions.json') as ed:
        effect_desc = json.load(ed)
    # verify effects haven't changed
    for fx in range(len(node.effects)):
        effect = node.effects[fx]
        effect_info = effect_desc[fx]
        if effect != effect_info['name']:
            raise Exception(f"Effect name has changed from {effect_info['name']} to {effect}.")

    with open('effects.md', 'w', encoding='utf8') as fp:
        fp.write(dedent('''\
        ### Effects
        
        To aid in showing where colors vs palettes are used, all effects are rendered with the 
        _Party_ palette ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/PAL_06.gif) 
        and the colors: <br />
        ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/color_1.gif) primary _Fx_<br />
        ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/color_2.gif) secondary _Bg_<br />
        ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/color_3.gif) tertiary _Cs.<br />
        For 2D effects the background (secondary) color is set to black.

        | ID | Effect | Description | Flags | Colors | Parms
        | ---: | --- | --- | --- | --- | --- 
        '''))
        for i in range(len(node.effects)):
            if node.effects[i] == 'RSVD':
                continue
            if node.effects[i] != effect_desc[i]['name']:
                print(f'Warning, the name of effect {i} has changed to {node.effects[i]}.')
                print('Update effect_descriptions.json')
                continue
            effect_info = node.effect_info[i]
            desc = effect_desc[i]["description"]
            img_fn = f'gifs/FX_{i:03d}.gif'
            if os.path.exists(img_fn):
                img = f'![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/FX_{i:03d}.gif)'
            else:
                img = ''
            line = f'| {i} | {node.effects[i]} | {desc} <br /> {img} |  {effect_info.print_flags()} '
            line += f'| {effect_info.print_colors} | {effect_info.print_parameters()}\n'
            fp.write(line)
        print('Updated effects.md')


def make_pallete_md(node:WledNode):
    with open('palette_descriptions.json') as tmp:
        palette_desc = json.load(tmp)
    for i in range(len(node.palettes)):
        name = palette_desc[i]['name']
        if node.palettes[i].replace('* ', '') != name:
            raise Exception(f"The palette {i} name has changed from {name} to {node.palettes[i]}.")
    with open('palettes.md', 'w') as fp:
        fp.write(dedent('''\
        ### Palettes
        
        | ID | Name | Description
        | ---: | --- | ---
        '''))
        for i in range(len(node.palettes)):
            pal_info = palette_desc[i]
            img = f'![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/PAL_{i:02d}.gif)'
            fp.write(f"| {i} | {pal_info['name']} | {pal_info['description']}<br />{img}\n")
    print('Updated palettes.md')


if __name__ == '__main__':
    node = WledNode('192.168.10.154')
    make_effect_md(node)
    make_pallete_md(node)
