"""
Generate Effect and Palette markdown files
"""
import json
import os

from textwrap import dedent
from wled import WledNode


def make_effect_md(node:WledNode, outfn=None, skip_validation=False):
    with open('effect_descriptions.json') as ed:
        effect_desc = json.load(ed)
    # verify effects haven't changed
    if not skip_validation:
        for fx in range(len(node.effects)):
            effect = node.effects[fx]
            effect_info = effect_desc[fx]
            if effect != effect_info['name']:
                msg = f"Effect {fx} name has changed from {effect_info['name']} to {effect}."
                raise Exception(msg)
    if outfn is None:
        outfn = 'effects.md'
    with open(outfn, 'w', encoding='utf8') as fp:
        fp.write(dedent('''\
        ### Effects
        
        To aid in showing where colors vs palettes are used, all effects are rendered with the 
        _Party_ palette ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/PAL_06.gif) 
        and the colors: <br />
        ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/color_1.gif) primary _Fx_<br />
        ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/color_2.gif) secondary _Bg_<br />
        ![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/color_3.gif) tertiary _Cs.<br />
        For 2D effects the background (secondary) color is set to black.

        |  ID | Effect                   | Description                                                                                    | Flags | Colors                                  | Parms                                                                         |
        |----:|--------------------------|------------------------------------------------------------------------------------------------|-------|-----------------------------------------|-------------------------------------------------------------------------------|
        '''))
        for name in sorted(node.effects):
            if name == 'RSVD':
                continue
            idx = node.effects.index(name)
            effect_info = node.effect_info[idx]
            if idx < len(effect_desc) and name == effect_desc[idx]["name"]:
                desc = effect_desc[idx]["description"]
            else:
                desc = ''
            if '☾' in name:
                img_fn = f'gifs/FX_MM{idx:03d}.gif'
            else:
                img_fn = f'gifs/FX_{idx:03d}.gif'
            if os.path.exists(img_fn):
                # img = f'![]({img_fn})'
                img = f'![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/{img_fn})'
            else:
                img = ''
            line = f'| {idx:3} | {node.effects[idx]:26} | {desc} <br /> {img} |  {effect_info.print_flags()} '
            line += f'| {effect_info.print_colors()} | {effect_info.print_parameters():30} |\n'
            fp.write(line)
        print(f'Updated {outfn}')


def make_pallete_md(node:WledNode):
    with open('palette_descriptions.json') as tmp:
        palette_desc = json.load(tmp)
    for i in range(len(node.palettes)):
        name = palette_desc[i]['name']
        if node.palettes[i].replace('* ', '') != name:
            msg = f'Palette {i} name has changed from {name} to {node.palettes[i]}.'
            raise Exception(msg)
    with open('palettes.md', 'w') as fp:
        fp.write(dedent('''\
        ### Palettes
        
        |  ID | Name           | Description                                                                                                                                                                                           |
        |----:|----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
        '''))
        for i in range(len(node.palettes)):
            pal_info = palette_desc[i]
            img = f'![](https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master/gifs/PAL_{i:02d}.gif)'
            fp.write(f"| {i} | {pal_info['name']} | {pal_info['description']}<br />{img} |\n")
    print('Updated palettes.md')


if __name__ == '__main__':
    node = WledNode('192.168.10.140')
    # Need to skip validation of effect name when building MM effect.md page
    make_effect_md(node, 'effects_mm.md', True)
    #make_effect_md(node)
    #make_pallete_md(node)
