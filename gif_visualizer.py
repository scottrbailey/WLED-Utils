import requests
import time

from PIL import Image, ImageDraw


LED_COLS = 20
LED_ROWS = 3
LED_SIZE = 7
SPACE_SIZE = 2
FRAME_COUNT = LED_COLS * LED_ROWS
NODE_IP = '192.168.10.208'
image_size = (LED_COLS * LED_SIZE + (LED_COLS + 1 * SPACE_SIZE),
             (LED_ROWS * LED_SIZE + (LED_ROWS + 1) * SPACE_SIZE))


def draw_frame():
    req = requests.get(f'http://{NODE_IP}/json/liveview')
    image = Image.new("RGB", image_size, "black")
    draw = ImageDraw.Draw(image)
    colors = req.json()['leds']
    for i in range(LED_COLS * LED_ROWS):
        row = i // LED_COLS
        col = LED_COLS - 1 - (i % LED_COLS) if row % 2 else i % LED_COLS
        #col = i % LED_COLS
        x1 = col * (LED_SIZE + SPACE_SIZE) + SPACE_SIZE
        y1 = row * (LED_SIZE + SPACE_SIZE) + SPACE_SIZE
        # print(f'{i}({col},{row}) - rectangle({x1}, {y1}, #{colors[i]})')
        draw.rectangle((x1, y1, x1 + LED_SIZE, y1 + LED_SIZE), fill=int(colors[i], 16))
    return image


def render_palette(fp=0):
    # Set effect to Palette and palette fp
    req = requests.get(f'http://{NODE_IP}/win&FX=65&FP={fp}&TT=0&CL=hFF6E41&C2=hFFE369')
    time.sleep(0.3)
    frames = []
    for number in range(LED_COLS * LED_ROWS):
        time.sleep(0.02)
        frames.append(draw_frame())
    frame_one = frames[0]
    frame_one.save(f'gifs/PAL_{fp:02d}.gif', format="GIF", append_images=frames,
                   save_all=True, duration=60, loop=0)

def render_effect(fx=0):
    # Set effect to fx and palette to Party
    req = requests.get(f'http://{NODE_IP}/win&FX={fx}&FP=6&TT=0&CL=hFF6E41&C2=hFFE369')
    time.sleep(0.3)
    frames = []
    for number in range(LED_COLS * LED_ROWS):
        time.sleep(0.02)
        frames.append(draw_frame())
    frame_one = frames[0]
    frame_one.save(f'gifs/FX_{fx:02d}.gif', format="GIF", append_images=frames,
                   save_all=True, duration=60, loop=0)

def render_all_effects():
    for i in range(len(node_info['effects'])):
        print(f'rendering {node_info["effects"][i]}')
        render_effect(i)


def render_all_palettes():
    for i in range(0, len(node_info['palettes'])):
        print(f'rendering {node_info["palettes"][i]}')
        render_palette(i)


if __name__ == "__main__":
    req = requests.get(f'http://{NODE_IP}/json')
    node_info = req.json()
    render_all_effects()