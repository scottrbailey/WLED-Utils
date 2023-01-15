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
    with open('effects.md', 'w', encoding='utf8') as fp:
        fp.write(dedent('''\
        | ID | Effect | Description | Flags | Parms
        | ---: | --- | --- | --- | --- 
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
            line = f'| {i} | {node.effects[i]} | {desc} <br /> {img} | '
            line += f' {effect_info.print_flags()} | {effect_info.print_parameters()}\n'
            fp.write(line)


if __name__ == '__main__':
    node = WledNode('192.168.10.155')
    make_effect_md(node)
