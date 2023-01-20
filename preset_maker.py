#!/usr/env python
"""
Creates random presets for WLED based on your selection of favorite palettes and effects.



"""

import copy
import json
import requests
import random
import sys
import time
from . import color_utils
from .wled import Node


class WNode(Node):
    def __init__(self, ip):
        super().__init__(ip)
        seg = self.state['seg'][self.state['mainseg']]
        self.col1_pos = seg['start']
        self.col2_pos = ((seg['start'] - seg['stop']) // 2) // (1 + self.info['leds']['count'] // 180)

    def initialize(self):
        # turn on and set transition time to 0
        self.win(TT=0, T=1)

    def __enter__(self):
        pass

    def __exit__(self):
        # set transition time and on back to original values
        tt = self.state['transition']
        t = 1 if self.state['on'] else 0
        self.win(TT=tt, T=t)



def grab_live_colors(fx):
    req = requests.get(f'http://{ip}/json/live')
    leds = req.json['leds']

def find_fav_fx():
    fx_names = js['effects']
    print(f"""This will cycle through {len(fx_names)} effects to determine if you want to use it to make a preset.
    If you like it, enter 1
    If you want to skip it, enter 0
    If you want to quit at any time, enter Q.""")
    cont = input("This will clear your previous favorites. \nWould you like to continue?  Y/N")
    
    if cont.upper() == 'Y':
        favs = []
        # be sure lights are on, set palette to Party and shorten transition time
        hr = requests.get(f'http://{ip}/win&TT=50&T=1&FP=6')
        
        for i in range(len(js['effects'])):
            hr = requests.get(f'http://{ip}/win&FX={i}')
            ans = input(f'Favorite {fx_names[i]}? 0: No, 1: Yes\t')
            if ans == '1':
                favs.append(i)
            elif ans in ['Q', 'q']:
                return
        return favs
    

def find_fav_pal():
    pal_names = js['palettes']
    print(f"""This will cycle through {len(pal_names) - 4} palettes to determine if you want to use it to make a preset.
    If you like it, enter 1
    If you want to skip it, enter 0
    If you want to quit at any time, enter Q. Favorites will not be saved.""")
    # turn lights on set effect to Palette
    hr = requests.get(f'{ip}/win&TT=50&T=1&FX=65')
    fav_pals = []
    fav_pal_cols = {}

    for i in range(5, len(pal_names)):
        hr = requests.get(f'{ip}/win&FP={i}')
        name = pal_names[i]
        # Strip extra info from names in SR
        ai = name.find('@')
        if ai:
            name = name[0:ai]
        ans = input(f'Favorite {name}? 0: No, 1: Yes, Q: Quit\t')
        if ans == '1':
            fav_pals.append(i)

        elif ans in ['Q', 'q']:
            return
    return fav_pals
    

def build_presets():
    random.shuffle(fav_pal)
    random.shuffle(fav_fx)
    pal_len = len(fav_pal)
    presets = {0: {}}
    cols = js['state']['seg'][0]['col']
    segment = {'id': 0, 'grp': 1, 'spc': 0, 'on': True,
               'bri': 255, 
               'fx': 1, 'sx': 128, 'ix': 128, 'pal': 1, 'sel': True, 'rev': False, 'mi': False}
    preset = {'n': 'Preset 2', 'on': True, 'bri': 128, 'transition': 7,
          'mainseg': 0, 'seg': []}
    segment_bounds = [(seg['start'], seg['stop']) for seg in js['state']['seg']]
    for i in range(len(fav_fx)):
        pal_id = fav_pal[i % pal_len]
        fx_id = fav_fx[i]
        pal_name = js['palettes'][pal_id]
        fx_name = js['effects'][fx_id]
        ps = copy.deepcopy(preset)
        ps['n'] = f'{fx_name} - {pal_name}' if i else '_boot_'                 
        for j in range(len(segment_bounds)):
            seg = copy.deepcopy(segment)
            if i == 0:
                seg['start'] = segment_bounds[j][0]
                seg['stop'] = segment_bounds[j][1]
                seg['col'] = cols
            seg['id'] = j    
            seg['fx'] = fx_id
            seg['pal'] = pal_id
            ps['seg'].append(seg)
        presets[i+1] = ps
    fp = open('presets.json', 'w')
    json.dump(presets, fp)
    fp.close()
    print('done')


def save_favs(favs):
    with open('favorites.json', 'w') as fp:
        json.dump(favs, fp, indent=2)


if __name__ == '__main__':
    ip = '192.168.10.51'
    fav_pal = [38, 15, 46, 20, 51, 44, 29, 22, 42, 45, 49, 30, 27, 50,
               55, 12, 19, 11, 36, 28, 37, 6, 33, 41]
    fav_fx = [99, 72, 112, 110, 60, 64, 111, 73, 78, 87, 41, 101, 81, 71, 74,
              91, 79, 16, 109, 38, 67, 105, 89, 57, 80, 75, 70, 93, 106]

    with open('favorites.json') as fp:
        favorites = json.load(fp)

    node = WNode(ip)
    js = {}
