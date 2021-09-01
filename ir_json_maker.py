# !/usr/bin/env python

"""
Converts IR remote info from Excel to ir.json files for WLED.

Each worksheet will output one *ir.json file, and should have at minimum a 'label', 'code', and 'cmd' column.
If the label is found in def_commands, for instance 'on', 'off', 'speed+', 'slow', etc. then no command is required.
Additionally, if the label is a named CSS color, then that color will be used as the primary color. 
The secondary and tertiary colors will be set by rotating the primary color the specified degrees around the color wheel.
For color buttons, you can set a palette. For instance, you might want to use the "Orangery" palette with the orange button.
If you use a named css color as the label, in this case "orange", then the primary, secondary and tertiary colors will also
be set to orange in addition to setting the palette. 


CSS named colors can be found at https://www.w3schools.com/cssref/css_colors.asp
"""

import colorsys
import json
import openpyxl
import re
from colors import named_colors, palettes
from color_utils import split_rgb

SEC_SHIFT_DEG = 30
TERT_SHIFT_DEG = -15
TERT_SHIFT_SAT = 0.7
TERT_SHIFT_VAL = 0.8
USE_PALETTES = True

PSFB_PAT = re.compile('!presetFallback\((.+)\)')

# map labels to commands
def_commands = {"on": "T=1", "off": "T=0&FX=0&FP=0&IX=128&SX=128", "on/off": "T=2", "power": "T=2",
                "bright+": "!incBrightness", "bright-": "!decBrightness",
                "speed+": "SX=~16", "speed-": "SX=~-16", "quick": "SX=~16", "slow": "SX=~-16",
                "intensity+": "IX=~16", "intensity-": "IX=~-16",
                "effect+": "FX=~", "effect-": "FX=~-",
                "preset+": "PL=~", "preset-": "PL=~-",
                "palette+": "FP=~", "palette-": "FP=~-",
                "play": {"playlist": {"ps": [1, 2, 3, 4, 5], "dur": 1800, "transition": 7, "repeat": 0}},
                "auto": {"playlist": {"ps": [1, 2, 3, 4, 5], "dur": 1800, "transition": 7, "repeat": 0}},
                "timer30": "NL=30&NT=0", "timer60": "NL=60&NT=0", "timer120": "NL=120&NT=0", "timeroff": "NL=0",
                "diy1": "!presetFallback(1, 110, 6)", "diy2": "!presetFallback(2, 38, 55)",
                "diy3": "!presetFallback(3, 67, 28)", "diy4": "!presetFallback(4, 72, 44)",
                "diy5": "!presetFallback(5, 87, 27)", "diy6": "!presetFallback(6, 65, 45)",
                "mode1": "!presetFallback(1, 110, 6)", "mode2": "!presetFallback(2, 38, 55)",
                "mode3": "!presetFallback(3, 67, 28)", "mode4": "!presetFallback(4, 72, 44)",
                "mode5": "!presetFallback(5, 87, 27)", "mode6": "!presetFallback(6, 65, 45)",
                }

# map labels (named colors) to palette ids (can use FP# or name)
def_palettes = {"red": 8, "orangered": "Sakura", "pink": "Pink Candy",
                "orange": "Orangery",  "yellow": "Yellowout", "khaki": "Grintage",
                "green": "Forest", "lightgreen": "Rivendale",
                "aqua": "Ocean", "cyan": "Beech", "darkcyan": "Hult 64", "turquoise": "Toxy Reaf",
                "blue": "Icefire", "skyblue": "Breeze", "darkblue":  "Semi Blue",
                "plum": "Magenta", "magenta": "Magred"}


def shift_color(col, shift, sat=1.0, val=1.0):
    # convert to HSV
    hsv = colorsys.rgb_to_hsv(*split_rgb(col))
    # shift by specified degrees
    h = (((hsv[0] * 360) + shift) % 360) / 360.0
    # convert back to RGB
    rgb = colorsys.hsv_to_rgb(h, hsv[1] * sat, hsv[2] * val)
    return (int(rgb[0]) << 16) + (int(rgb[1]) << 8) + int(rgb[2])


def preset_fallback(node): 
    matches = PSFB_PAT.match(node['cmd'])
    if matches:
        parms = [int(n) for n in matches.group(1).split(',')]
        fb_keys = ['PL', 'FX', 'FP']
        for i in range(len(parms)):
            node[fb_keys[i]] = parms[i]
        node['cmd'] = '!presetFallback'
    else:
        node['cmd'] = ''
    

def parse_sheet(ws):
    used_codes = []
    print(f'Parsing worksheet {ws.title}')
    ir = {"remote": ws.title}
    rows = ws.rows
    keys = [col.value.lower() for col in next(rows)]
    
    for row in rows:
        rec = dict(zip(keys, [col.value for col in row]))
        if rec.get('code') is None:
            continue
        if rec['code'] in used_codes:
            print(f'The code {rec["code"]} has already been defined in this spreadsheet. Skipping.')
            continue
        used_codes.append(rec['code'])
        label = rec.get('label').lower().replace(' ', '')
        cd = {"label": rec.get('label')}
        if rec.get('row') and rec.get('col'):
            cd['pos'] = f'{rec["row"]}x{rec["col"]}'
        if rec.get('comment') and rec.get('comment') != rec.get('label'):
            cd['cmnt'] = rec.get('comment')
        if rec.get('rpt'):
            cd['rpt'] = bool(rec['rpt'])

        if rec.get('cmd'):
            cd['cmd'] = rec['cmd']
            if label in named_colors:
                # label was a named css color, calculate secondary and tertiary colors and add to HTTP or JSON command
                c1 = int(named_colors[label], 16)
                c2 = shift_color(c1, SEC_SHIFT_DEG)
                c3 = shift_color(c1, TERT_SHIFT_DEG, sat=TERT_SHIFT_SAT, val=TERT_SHIFT_VAL)
                if cd['cmd'].startswith('{'):
                    # json command
                    json_cmd = json.loads(cd['cmd'])
                    seg = json_cmd.get('seg', [{}])
                    if not seg[0].get('col'):
                        cols = [list(split_rgb(c1)), list(split_rgb(c2)), list(split_rgb(c3))]
                        seg[0]['col'] = cols
                        json_cmd['seg'] = seg
                    cd['cmd'] = json_cmd
                elif not cd['cmd'].startswith('!'):
                    # http command
                    cd['cmd'] += f'&CL=h{c1:06X}&C2=h{c2:06X}&C3=h{c3:06X}'
                    if 'FP=' not in cd['cmd']:
                        # set palette to colors only
                        cd['cmd'] += '&FP=5'
            elif type(rec['cmd']) == str and rec['cmd'].startswith('!presetFallback'):
                preset_fallback(cd)               
        elif all((rec.get('primary'), rec.get('secondary'), rec.get('tertiary'))):
            c1 = int(rec.get('primary'), 16)
            c2 = int(rec.get('secondary'), 16)
            c3 = int(rec.get('tertiary'), 16)
            cd['cmd'] = f'FP=5&CL=h{c1:X}&C2=h{c2:X}&C3=h{c3:X}'
        elif all((rec.get('primary'), rec.get('secondary'))):
            c1 = int(rec.get('primary'), 16)
            c2 = int(rec.get('secondary'), 16)
            c3 = shift_color(c2, TERT_SHIFT_DEG, sat=TERT_SHIFT_SAT, val=TERT_SHIFT_VAL)
            cd['cmd'] = f'FP=5&CL=h{c1:X}&C2=h{c2:X}&C3=h{c3:X}'
        elif rec.get('primary'):
            c1 = int(rec.get('primary'), 16)
            c2 = shift_color(c1, SEC_SHIFT_DEG)
            c3 = shift_color(c1, TERT_SHIFT_DEG, sat=TERT_SHIFT_SAT, val=TERT_SHIFT_VAL)
            cd['cmd'] = f'FP=5&CL=h{c1:X}&C2=h{c2:X}&C3=h{c3:X}'
        elif label in def_commands:
            cd['cmd'] = def_commands.get(label)
            if type(cd['cmd']) == str and cd['cmd'].startswith('!presetFallback'):
                preset_fallback(cd)
        elif label in named_colors:
            c1 = int(named_colors[label], 16)
            c2 = shift_color(c1, SEC_SHIFT_DEG)
            c3 = shift_color(c1, TERT_SHIFT_DEG, sat=TERT_SHIFT_SAT, val=TERT_SHIFT_VAL)
            fp = 5
            if USE_PALETTES and label in def_palettes:
                pal = def_palettes.get(label)
                if str(pal).isdecimal():
                    fp = pal
                    cd['cmnt'] = palettes[int(pal)]
                elif pal in palettes:
                    fp = palettes.index(pal)
                    cd['cmnt'] = pal
            cd['cmd'] = f'FP={fp}&CL=h{c1:06X}&C2=h{c2:06X}&C3=h{c3:06X}'
        else:
            print(f'Did not find a command or color for {rec["label"]}. Hint use named CSS colors as labels')
        ir[rec['code']] = cd

    with open(f'ir_json/{ws.title}_ir.json', 'w') as fp:
        json.dump(ir, fp, indent=2)


if __name__ == '__main__':
    wb = openpyxl.load_workbook('IR_Remote_Codes.xlsx')
    
    for sheet in wb.worksheets:
        parse_sheet(sheet)
