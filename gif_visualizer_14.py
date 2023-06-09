import wled
import _thread
import time
import os
import websocket
from PIL import Image, ImageDraw, ImageEnhance


class Visualizer:
    def __init__(self, node: wled.WledNode, led_size=7):
        self.node = node
        self.max_frames = 200
        self.led_size = led_size
        self.bri_adj = 3.0
        self.cols_1d = 25
        self.rows_1d = 4
        if node.is_2d:
            self.cols_2d = node.mainseg['stop'] - node.mainseg['start']
            self.rows_2d = node.mainseg['stopY'] - node.mainseg['startY']
        # array of liveview data
        self.messages = []
        # rendered gif frames
        self.frames = []
        # milliseconds between liveview messages
        self.intervals = []
        self.fx = None
        self.fp = 6 # Party
        self.last_message_time = None
        self.ws = None
        self.grid_2d = None
        self.grid_1d = None
        self.col1 = 'FF6E41' # OrangeRed Fx
        self.col2 = 'FFE369' # Yellow (Black for 2D) Bg
        self.col3 = 'FFB9B8' # Pink Cs
        # override palette, speed or intensity for given effect
        self.overrides = {0: {'frames': 1},
                          4: {'sx': 192},
                          5: {'sx': 192},
                          21: {'ix': 224},
                          23: {'sx': 224},
                          24: {'sx': 224},
                          32: {'sx': 192},
                          36: {'sx': 192},
                          44: {'sx': 192},
                          45: {'ix': 192},
                          57: {'sx': 255, 'ix': 192},
                          58: {'ix': 192},
                          64: {'ix': 240, 'bri_adj': 1.0},
                          66: {'pal': 35},
                          79: {'sx': 32, 'ix': 16, 'col2': 'FFE0A0'},
                          82: {'sx': 192},
                          83: {'frames': 1},
                          84: {'frames': 1},
                          85: {'frames': 1},
                          88: {'pal': 35},
                          90: {'sx': 192},
                          98: {'ix': 50, 'frames': 1},
                          99: {'sx': 32, 'ix': 16, 'bri_adj': 5.0},
                          122: {'c3': 192},
                          163: {'bri_adj': 5.0},
                          173: {'sx': 64, 'ix': 64},
                          176: {'sx': 96, 'ix': 64},
                          181: {'sx': 224},
                          }

    def reset(self):
        """ Reset state before rendering a new visualization """
        self.intervals = []
        self.messages = []
        self.frames = []
        self.last_message_time = None

    def save_visualization(self, mode='effect'):
        if mode == 'effect':
            fn = f'gifs/FX_{self.fx:03d}.gif'
        elif mode == 'palette':
            fn = f'gifs/PAL_{self.fp:02d}.gif'
        else:
            fn = 'gifs/test.gif'
        self.render_frames()
        self.save_gif(fn)

    def _generate_grid(self, cols, rows):
        width = cols * self.led_size
        height = rows * self.led_size
        img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        black = (0, 0, 0, 255)
        for x in range(cols + 1):
            x1 = x * self.led_size
            draw.line((x1, 0, x1, height), black, width=1)
        for y in range(rows + 1):
            y1 = y * self.led_size
            draw.line((0, y1, width, y1), black, width=1)
        return img

    def _render_1d_frame(self, message):
        byte_cnt = self.cols_1d * self.rows_1d * 3
        thumb = Image.frombytes('RGB', (self.cols_1d, self.rows_1d),
                                message[2:byte_cnt + 2])
        thumb = thumb.convert('RGBA')
        if self.bri_adj != 1.0:
            bright = ImageEnhance.Brightness(thumb)
            thumb = bright.enhance(self.bri_adj)
        img = thumb.resize((self.cols_1d * self.led_size, self.rows_1d * self.led_size),
                           resample=Image.BOX)
        if self.grid_1d is None:
            self.grid_1d = self._generate_grid(self.cols_1d, self.rows_1d)
        return Image.alpha_composite(img, self.grid_1d)

    def _render_2d_frame(self, message):
        cols = message[2]
        rows = message[3]

        box = (self.node.mainseg['start'], self.node.mainseg['startY'],
               self.node.mainseg['stop'], self.node.mainseg['stopY'])
        thumb = Image.frombytes('RGB', (cols, rows), message[4:])
        thumb = thumb.convert('RGBA')
        if self.bri_adj != 1.0:
            bright = ImageEnhance.Brightness(thumb)
            thumb = bright.enhance(self.bri_adj)
        img = thumb.resize((self.cols_2d * self.led_size, self.rows_2d * self.led_size),
                           resample=Image.BOX, box=box)
        if self.grid_2d is None:
            self.grid_2d = self._generate_grid(self.cols_2d, self.rows_2d)
        return Image.alpha_composite(img, self.grid_2d)

    def render_frames(self):
        m1 = self.messages[0]
        if m1[0] != 76:
            print('Wrong version')
            return
        if m1[1] == 1:
            for message in self.messages:
                self.frames.append(self._render_1d_frame(message))
        elif m1[1] == 2:
            for message in self.messages:
                self.frames.append(self._render_2d_frame(message))

    def save_gif(self, fn):
        img = self.frames[0]
        if len(self.frames) > 1:
            avg_dur = int(sum(self.intervals) / len(self.intervals))
            img.save(fn, format='GIF', append_images=self.frames,
                     save_all=True, duration=avg_dur, loop=0, quality=10)
        else:
            img.save(fn, format='GIF', quality=10)
        print(f'Saved visualization to {fn}')


def on_message(ws, message):
    global vis # threads
    if isinstance(message, bytes):
        t = time.time()
        if vis.last_message_time:
            vis.intervals.append(int((t - vis.last_message_time) * 1000))
        vis.last_message_time = t
        vis.messages.append(message)

        if len(vis.messages) >= vis.max_frames:
            ws.close()


def on_open(ws):
    print('Opened websocket, recording effect')

    def run(*args):
        ws.send("{'lv': true}")
    _thread.start_new_thread(run, ())


def on_close(ws):
    print('Capture complete')
    ws.thread.join()


def render_effect(vis: Visualizer, fx):
    vis.reset()
    vis.fx = fx
    effect = vis.node.effect_info[fx]
    if effect.colors and len(effect.colors) >= 2 and effect.colors[1] == '!':
        bg_color = '000000'
    else:
        bg_color = vis.col2
    config = {'fx': fx, 'pal': vis.fp, 'sx': 127, 'si': 127,
              'col1': vis.col1, 'col2': bg_color,
              'col3': vis.col3, 'frames': 200,
              'bri_adj': 3.0}
    if fx in vis.overrides:
        config.update(vis.overrides[fx])
    vis.max_frames = config['frames']

    vis.node.call({'bri': 255,
                   'seg': {'fx': fx, 'pal': config['pal'], 'si': config['si'],
                           'sx': config['sx'],
                           'col': [config['col1'], config['col2'], config['col3']]}})
    effect_info = vis.node.effect_info[fx]
    print(f'Rendering {effect_info.name} FX: {fx}')
    time.sleep(0.3)
    ws = websocket.WebSocketApp(f'ws://{vis.node.ip}/ws',
                                     on_open=on_open,
                                     on_message=on_message,
                                     on_close=on_close)
    ws.run_forever()
    vis.render_frames()
    vis.save_gif(f'images/FX_{fx:03d}.gif')


def make_compare_file(node: wled.WledNode):
    gh_link = 'https://raw.githubusercontent.com/scottrbailey/WLED-Utils/master'
    with open('compare.md', 'w', encoding='utf8') as fp:
        fp.write('| ID | Effect | Flags | Master | Branch | New\n')
        fp.write('| ---: | --- | --- | --- | --- | ----\n')
        for i in range(len(node.effects)):
            effect = node.effect_info[i]
            if effect.name != 'RSVD':
                gh_img = f'![]({gh_link}/gifs/FX_{i:03d}.gif)'
                line = f'| {i} | {effect.name} | {effect.print_flags()} | {gh_img} | ![](gifs/FX_{i:03d}.gif) | ![](images/FX_{i:03d}.gif)\n'
                fp.write(line)


def visualize_all(vis: Visualizer, skip_existing=False):
    """ Render all effects that match node's configuration (1d or 2d) """
    for i in range(len(node.effects)):
        effect = node.effect_info[i]
        if effect.name == 'RSVD':
            continue
        if skip_existing and os.path.exists(f'images/FX_{i:03d}.gif'):
            continue
        if node.is_2d and effect.is_2d:
            if i in vis.overrides:
                render_effect(vis, i)
        elif not node.is_2d and not effect.is_2d:
            if effect.is_fft:
                render_effect(vis, i)


if __name__ == '__main__':
    node = wled.WledNode('192.168.10.56')
    node.call({'transition': 0})
    vis = Visualizer(node, led_size=8)
    if node.is_2d:
        vis.led_size = 5

    # make_compare_file(node)
    # visualize_all(vis)

