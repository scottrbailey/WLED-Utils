import colors
import math


def split_rgb(col):
    if isinstance(col, str):
        col = int(col, 16)
    r = (col & (255 << 16)) >> 16
    g = (col & (255 << 8)) >> 8
    b = col & 255
    return r, g, b


def to_hex(r, g, b):
    return f'{r:02X}{g:02X}{b:02X}'


def color_distance(c1, c2):
    r1 = (c1 & 255 << 16) >> 16
    r2 = (c2 & 255 << 16) >> 16
    g1 = (c1 & 255 << 8) >> 8
    g2 = (c2 & 255 << 8) >> 8
    b1 = (c1 & 255)
    b2 = (c2 & 255)
    return math.sqrt((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2)


def closest_color(c1):
    min_d = 1000.0
    closest_col = ''
    for k, v in nc.items():
        d = color_distance(c1, v)
        if d < min_d:
            min_d = d
            closest_col = k
    return closest_col


if __name__ == '__main__':
    nc = {k: int(v, 16) for k, v in colors.named_colors.items()}
