import wled
import _thread
import time
import websocket
from PIL import Image, ImageDraw, ImageEnhance


def on_message(ws, message):
    global vis
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

def render_effect(vis, fx, pal=6):
    vis.intervals = []
    vis.messages = []
    vis.frames = []
    vis.last_message_time = None
    vis.fx = fx
    vis.node.call({'bri': 255,
                   'seg': {'fx': fx, 'pal': pal, 'si': 127, 'sx': 127,
                           'col': [vis.color_1, vis.color_2, vis.color_3]}})
    effect_info = vis.node.effect_info[fx]
    print(f'Rendering {effect_info.name} FX: {fx}')
    time.sleep(1)
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
        fp.write('| ID | Effect | GitHub | Old | New\n')
        fp.write('| ---: | --- | --- | --- | ---\n')
        for i in range(len(node.effects)):
            effect = node.effect_info[i]
            if effect.is_2d or effect.is_fft or effect.is_ar:
                gh_img = f'![]({gh_link}/gifs/FX_{i:03d}.gif)'
                line = f'| {i} | {effect.name} | {gh_img} | ![](gifs/FX_{i:03d}.gif) | ![](images/FX_{i:03d}.gif)\n'
                fp.write(line)


class Visualizer:
    def __init__(self, node: wled.WledNode, max_frames=200, led_size=7):
        self.node = node
        self.max_frames = max_frames
        self.led_size = led_size
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
        self.color_1 = 'FF6E41' # OrangeRed Fx
        self.color_2 = '000000' # Black Bg
        self.color_3 = 'FFB9B8' # Pink Cs

    def save_visualization(self, mode='effect'):
        if mode == 'effect':
            fn = f'gifs/FX_{self.fx:03d}.gif'
        elif mode == 'palette':
            fn = f'gifs/PAL_{self.fp:02d}.gif'
        else:
            fn = 'gifs/test.gif'
        self.render_frames()
        self.save_gif(fn)

    def on_open(self, ws):
        print('Opening websocket')

        def run(*args):
            ws.send("{'lv': true}")
        _thread.start_new_thread(run, ())

    def on_message(self, ws, message):
        if isinstance(message, bytes):
            t = time.time()
            if self.last_message_time:
                self.intervals.append(int((t - self.last_message_time) * 1000))
            self.last_message_time = t
            self.messages.append(message)
            if len(self.messages) >= self.max_frames:
                ws.close()

    def on_close(self, ws):
        self.node.call("{'lv': false}")
        self.save_visualization()

    def generate_grid(self, cols, rows):
        width = cols * self.led_size
        height = rows * self.led_size
        img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        black = (0, 0, 0, 255)
        for x in range(cols):
            x1 = x * self.led_size
            draw.line((x1, 0, x1, width), black, width=1)
        for y in range(rows):
            y1 = y * self.led_size
            draw.line((0, y1, height, y1), black, width=1)
        return img

    def render_2d_frame(self, message, brightness=3.0):
        cols = message[2]
        rows = message[3]
        thumb = Image.frombytes('RGB', (cols, rows), message[4:])
        thumb = thumb.convert('RGBA')
        bright = ImageEnhance.Brightness(thumb)
        thumb = bright.enhance(brightness)
        img = thumb.resize((cols * self.led_size, rows * self.led_size),
                           resample=Image.BOX)
        return Image.alpha_composite(img, self.grid_2d)

    def render_frames(self):
        m1 = self.messages[0]
        if m1[0] != 76 or m1[1] != 2:
            print('Not a matrix. Bummer')
            return
        cols = m1[2]
        rows = m1[3]
        self.grid_2d = self.generate_grid(cols, rows)
        for message in self.messages:
            self.frames.append(self.render_2d_frame(message))

    def save_gif(self, fn):
        img = self.frames[0]
        dur = 60
        avg_dur = int(sum(self.intervals) / len(self.intervals))
        img.save(fn, format='GIF', append_images=self.frames,
                 save_all=True, duration=avg_dur, loop=0, quality=10)
        print(f'Saved visualization to {fn}')


if __name__ == '__main__':
    node = wled.WledNode('192.168.10.154')
    vis = Visualizer(node, max_frames=200, led_size=6)

    # Render all 2D effects

    for i in range(len(node.effects)):
        effect = node.effect_info[i]
        if effect.is_ar or effect.is_fft:
            render_effect(vis, i, 6)

    # make_compare_file(node)

