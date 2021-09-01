#!/usr/env python
"""
Creates random presets for WLED
"""

import copy
import json
import requests
import random
import time
from . import colors


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
        hr = requests.get(f'{url}/win&TT=50&T=1&FP=6')
        
        for i in range(len(js['effects'])):
            hr = requests.get(f'{url}/win&FX={i}')
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
    If you want to quit at any time, enter Q.""")
    # turn lights on set effect to Palette
    hr = requests.get(f'{url}/win&TT=50&T=1&FX=65')
    favs = []
    for i in range(5, len(pal_names)):
        hr = requests.get(f'{url}/win&FP={i}')
        ans = input(f'Favorite {pal_names[i]}? 0: No, 1: Yes\t')
        if ans == '1':
            favs.append(i)
        elif ans in ['Q', 'q']:
            return
    return favs
        


def color_distance(c1, c2):
    r1 = (c1 & 255 << 16) >> 16
    r2 = (c2 & 255 << 16) >> 16
    g1 = (c1 & 255 << 8) >> 8
    g2 = (c2 & 255 << 8) >> 8
    b1 = (c1 & 255)
    b2 = (c2 & 255)
    return math.sqrt((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2)
    

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
    for i in range(len(fav_fx)): #
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

if __name__ == '__main__':
    url = 'http://192.168.10.55'
    fav_pal = [38, 15, 46, 20, 51, 44, 29, 22, 42, 45, 49, 30, 27, 50,
               55, 12, 19, 11, 36, 28, 37, 6, 33, 41]
    fav_fx = [99, 72, 112, 110, 60, 64, 111, 73, 78, 87, 41, 101, 81, 71, 74,
              91, 79, 16, 109, 38, 67, 105, 89, 57, 80, 75, 70, 93, 106]
    
    req = requests.get(f'{url}/json')
    js = req.json()

        
        
        
