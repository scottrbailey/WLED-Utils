import asyncio
import json
import requests
import sys
import websocket
from PIL import Image
from textwrap import dedent

RESIZE_CROP = 1
RESIZE_EXPAND = 2

from color_utils import color_distance, rgb_to_int


def _replace_defaults(i, params, defaults):
    if params[i] == '!':
        return defaults[i]
    else:
        return params[i]


class WledError(Exception):
    pass


class Effect:
    def __init__(self, id, name, info):
        meta = info.split(';')
        self.id = id
        self.name = name
        self.parameters = None
        self.colors = None
        self.palette = None
        self.flags = None
        self.defaults = None

        if len(meta) >= 1:
            self.parameters = meta[0].split(',')
        if len(meta) >= 2:
            self.colors = meta[1].split(',')
        if len(meta) >= 3:
            self.palette = meta[2].split(',')
        if len(meta) >= 4:
            self.flags = meta[3]
        if len(meta) >= 5:
            self.defaults = meta[4].split(',')

    def __str__(self):
        return dedent(f'''\
        <Effect: {self.name} ({self.id})
          Params: {self.parameters}
          Colors: {self.colors}
          Palette: {self.palette}
          Flags: {self.flags}
          Defaults: {self.defaults}
        >''')

    def print_flags(self):
        flags = {'1': '⋮', '2': '▦',
                 'v': '♪', 'f': '♫'}
        if not self.flags:
            return '⋮'
        return ' '.join([flags[f] for f in self.flags if f in flags])

    def print_colors(self):
        defaults = ['Fx', 'Bg', 'Cs']
        if self.palette and self.palette == ['!']:
            ret = '🎨 '
        else:
            ret = ''
        if self.colors is None or self.colors == ['']:
            return ret
        return ret + ', '.join([_replace_defaults(i, self.colors, defaults)
                        for i in range(len(self.colors))
                        if self.colors[i] != ''])

    def print_parameters(self):
        defaults = ['Speed', 'Intensity']
        if self.parameters is None or self.parameters == ['']:
            ''
        return ', '.join([_replace_defaults(i, self.parameters, defaults)
                         for i in range(len(self.parameters))
                            if self.parameters[i] != ''])

    @property
    def is_1d(self):
        return self.flags is None or '1' in self.flags

    @property
    def is_2d(self):
        if self.flags:
            return '2' in self.flags

    @property
    def is_3d(self):
        if self.flags:
            return '3' in self.flags

    @property
    def is_ar(self):
        if self.flags:
            return 'v' in self.flags

    @property
    def is_fft(self):
        if self.flags:
            return 'f' in self.flags


class WledNode:
    def __init__(self, ip, connect_ws=False):
        try:
            req = requests.get(f'http://{ip}/json', timeout=3)
        except requests.exceptions.Timeout:
            print(f'Could not connect to WLED node at {ip}. Configure NODE_IP and try again.')
            sys.exit(1)
        data = req.json()
        self.ip = ip
        self.info = data['info']
        self.load_state = data['state']
        self.palettes = data['palettes']
        self.effects = data['effects']
        self.effect_info = []
        self.colors = []
        self.color_frames = []
        self.ws = None
        # Fetch and parse effect metadata if on 0.14 or greater
        if self.info['ver'] > '0.14':
            try:
                req = requests.get(f'http://{ip}/json/fxdata', timeout=3)
                data = req.json()
                for i in range(len(data)):
                    meta = data[i]
                    name = self.effects[i]
                    self.effect_info.append(Effect(i, name, meta))
            except requests.exceptions.Timeout:
                print('Could not fetch effect metadata')

    def call(self, data=None):
        if isinstance(data, dict):
            req = requests.post(f'http://{self.ip}/json', json=data)
        elif data is None:
            req = requests.get(f'http://{self.ip}/json')
        else:
            req = requests.post(f'http://{self.ip}/json', data=data)
        return req

    def on_message(self, ws, message):
        data = json.loads(message)
        state = data['state']
        info = data['info']
        if not state['on']:
            print('LEDs are off')
            return
        seg = state['seg'][state['mainseg']]
        is_rgbw = info['leds']['rgbw']
        cols = []
        for col in seg['col']:
            if is_rgbw:
                cv = (col[0] << 24) + (col[1] << 16) + (col[2] << 8) + col[3]
                cols.append(f'#{cv:08X}')
            else:
                cv = (col[0] << 16) + (col[1] << 8) + col[2]
                cols.append(f'#{cv:06X}')
        print('Got ws message')
        self.colors = cols

    def img_to_matrix(self, img_fn, aspect_mode=RESIZE_EXPAND):
        """
        Display image on a 2D matrix. The segment will be "frozen" after
        @param img_fn: name of image file
        @param aspect_mode: When aspect ratio of image doesn't match ratio of matrix
            RESIZE_EXPAND will expand the image with a black background in one dimension.
                          Original image will be smaller.
            RESIZE_CROP will crop one dimension to get the correct aspect ratio.
                          Original image will be larger, but som
        """
        global color_data, color_comp
        # change effect to solid
        self.call({'seg': {'fx': 0, 'fp': 0, 'col': [[0,0,0],[0,0,0]]}})
        # get matrix info from controller
        json_data = self.call().json()
        seg = json_data['state']['seg'][json_data['state']['mainseg']]
        if not seg.get('stopY'):
            raise WledError("Can not send image, main segment is not 2D")
        img = Image.open(img_fn)
        w = seg['stop'] - seg['start']
        h = seg['stopY'] - seg['startY']
        seg_aspect = w / h
        img_aspect = img.width / img.height

        print(f'Matrix is ({w}, {h}) Image is ({img.width}, {img.height})')
        if (w, h) != (img.width, img.height):
            if seg_aspect == img_aspect:
                # same aspect ration, just resize
                thumb = img.resize((w, h), Image.Resampling.LANCZOS)
            elif aspect_mode == RESIZE_CROP:
                # different aspect ratio, resize a portion of the image
                ratio = max([w / img.width, h / img.height])
                x1 = (img.width - (w / ratio)) // 2
                y1 = (img.height - (h / ratio)) // 2
                x2 = img.width - x1
                y2 = img.height - y1
                thumb = img.resize((w, h), Image.Resampling.LANCZOS, box=(x1, y1, x2, y2))
            else:
                ratio = min([w / img.width, h / img.height])
                nw = int(w / ratio)
                nh = int(h / ratio)
                x1 = int((nw - img.width) / 2)
                y1 = int((nh - img.height) / 2)
                expanded_img = Image.new('RGB', (nw, nh), '#000000')
                expanded_img.paste(img, (x1, y1))
                thumb = expanded_img.resize((w, h), Image.Resampling.LANCZOS)
        else:
            thumb = img.copy()
        thumb.convert('RGB')
        colors = []
        for y in range(h):
            for x in range(w):
                rgb = thumb.getpixel((x, y))
                val = rgb_to_int(*rgb[0:3])
                colors.append(val)
        color_data = colors  #
        color_comp = compress_colors(colors, 8)

        '''cd = [1] + [f'{c:06X}' for c in colors]
        self.call({'seg': {'i': color_comp}})
        return'''
        # send pixel info 256 at a time
        for i in range(0, h * w, 256):
            stop = min([i + 256, h * w])
            # cd = compress_colors(colors[i:stop], 0)
            cd = [f'{c:06X}' for c in colors[i:stop]]
            self.call({'seg': {'i': [i] + cd}})


def compress_colors(colors, tolerance=8):
    """Reduce size of color array by eliminating repeating consecutive colors"""
    col_out = []
    last_col = colors[0]
    last_col_start = 0
    col_cnt = len(colors)
    for i in range(1, col_cnt):
        col = colors[i]
        if i + 1 == col_cnt or color_distance(last_col, col) > tolerance:
            if last_col_start + 1 == i:
                col_out.extend([i - 1, f'{last_col:06X}'])
            else:
                col_out.extend([last_col_start, i - 1, f'{last_col:06X}'])
            if i + 1 == col_cnt:
                col_out.extend([i, f'{col:06X}'])
            else:
                last_col = col
                last_col_start = i
    return col_out


def on_open(ws):
    ws.send({'state': {'on': 't', 'lv': 't'}})
    print("Websocket connection opened")

def on_message(ws, message):
    state = json.loads(message)['state']
    if not state["on"]:
        print('Off')
        return
    seg = state["seg"][0]

    cols = []
    for col in seg["col"]:
        cv = (col[0] << 16) + (col[1] << 8) + col[2]
        cols.append(f'#{cv:06X}')
    display = ", ".join(cols)
    print(display)
    print(f'Bright: {state["bri"]}  Speed: {seg["sx"]} Intensity: {seg["ix"]}')


if __name__ == '__main__':
    # family room
    node = WledNode('192.168.10.203')
    color_data = []
    color_comp = []
    # living room
    # node = WledNode('192.168.10.162')
    fn = 'c:/Temp/smiley.jpg'
    flag_fn = 'c:/Temp/flag_rectangle.png'
    node.img_to_matrix(fn, aspect_mode=RESIZE_CROP)
