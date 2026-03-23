#!/usr/bin/env python3
"""Generate all pixel art sprites for KFS Easter Egg game.
Output: 48x48 PNG files with transparency in assets/textures/
Working resolution: 16x16, scaled 3x to 48x48 (chunky pixel art look).
"""

from PIL import Image, ImageDraw, ImageFilter
import os, random

OUT = "assets/textures"
os.makedirs(OUT, exist_ok=True)

# Scale factor: work at 16x16, output 48x48
S = 16
SCALE = 3

# Color palette
T = (0, 0, 0, 0)          # transparent
BK = (20, 20, 20, 255)     # black outline
WH = (255, 255, 255, 255)  # white
WH2 = (240, 240, 235, 255) # off-white
PK = (255, 150, 170, 255)  # pink
PK2 = (255, 180, 190, 255) # light pink
RD = (200, 50, 50, 255)    # red
RD2 = (220, 70, 70, 255)   # light red
BN = (140, 90, 50, 255)    # brown
BN2 = (170, 110, 60, 255)  # light brown
BN3 = (100, 65, 35, 255)   # dark brown
GR = (80, 170, 50, 255)    # green grass
GR2 = (60, 140, 40, 255)   # darker grass
GR3 = (100, 190, 65, 255)  # lighter grass
DG = (30, 80, 25, 255)     # dark green (bush)
DG2 = (40, 100, 30, 255)   # medium dark green
YL = (255, 220, 60, 255)   # yellow
YL2 = (220, 190, 50, 255)  # dark yellow
GD = (255, 200, 0, 255)    # gold
GD2 = (220, 170, 0, 255)   # dark gold
GD3 = (255, 230, 100, 255) # light gold
OR = (240, 160, 40, 255)   # orange
PP = (150, 60, 200, 255)   # purple
PP2 = (180, 100, 230, 255) # light purple
PP3 = (120, 40, 170, 255)  # dark purple
GY = (100, 100, 100, 255)  # gray
GY2 = (70, 70, 70, 255)    # dark gray
GY3 = (140, 140, 140, 255) # light gray
BL = (60, 60, 60, 255)     # near-black
MU = (110, 80, 45, 255)    # mud
MU2 = (90, 65, 35, 255)    # dark mud
MU3 = (130, 100, 60, 255)  # light mud
BLU = (80, 140, 220, 255)  # blue (water)
SK = (150, 200, 255, 255)  # sky blue
EY = (30, 30, 30, 255)     # eye black
PT = (190, 170, 130, 255)  # path
PT2 = (170, 150, 110, 255) # dark path
RD_COL = (220, 40, 40, 255)  # red collar
GRN_W = (60, 180, 60, 255)   # green wheel
GRN_G = (0, 200, 0, 255)     # green glow


def make(w, h):
    return Image.new("RGBA", (w, h), T)

def scale_up(img):
    return img.resize((img.width * SCALE, img.height * SCALE), Image.NEAREST)

def save(img, name):
    scaled = scale_up(img) if img.width == S else img
    scaled.save(os.path.join(OUT, name))
    print(f"  {name} ({scaled.width}x{scaled.height})")

def px(img, data):
    """Set pixels from 2D list of colors. data[0] = top row."""
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if c != T:
                img.putpixel((x, y), c)

# ============================================================
# 1. RABBIT - front facing
# ============================================================
def gen_rabbit_front():
    img = make(S, S)
    _ = T; B = BK; W = WH; P = PK; p = PK2; E = EY; N = PK
    data = [
        [_,_,_,_,B,B,_,_,_,_,B,B,_,_,_,_],
        [_,_,_,B,W,P,B,_,_,B,P,W,B,_,_,_],
        [_,_,_,B,W,P,B,_,_,B,P,W,B,_,_,_],
        [_,_,_,B,W,P,B,_,_,B,P,W,B,_,_,_],
        [_,_,_,_,B,W,B,B,B,B,W,B,_,_,_,_],
        [_,_,_,B,W,W,W,W,W,W,W,W,B,_,_,_],
        [_,_,B,W,W,E,W,W,W,W,E,W,W,B,_,_],
        [_,_,B,W,W,E,W,W,W,W,E,W,W,B,_,_],
        [_,_,B,W,W,W,W,N,N,W,W,W,W,B,_,_],
        [_,_,_,B,W,W,W,W,W,W,W,W,B,_,_,_],
        [_,_,_,B,W,W,W,W,W,W,W,W,B,_,_,_],
        [_,_,B,W,W,W,W,W,W,W,W,W,W,B,_,_],
        [_,_,B,W,p,W,W,W,W,W,W,p,W,B,_,_],
        [_,_,_,B,B,W,W,W,W,W,W,B,B,_,_,_],
        [_,_,_,_,_,B,p,B,B,p,B,_,_,_,_,_],
        [_,_,_,_,_,_,B,_,_,B,_,_,_,_,_,_],
    ]
    px(img, data)
    return img

def gen_rabbit_back():
    img = make(S, S)
    _ = T; B = BK; W = WH; P = PK
    data = [
        [_,_,_,_,B,B,_,_,_,_,B,B,_,_,_,_],
        [_,_,_,B,W,P,B,_,_,B,P,W,B,_,_,_],
        [_,_,_,B,W,P,B,_,_,B,P,W,B,_,_,_],
        [_,_,_,B,W,P,B,_,_,B,P,W,B,_,_,_],
        [_,_,_,_,B,W,B,B,B,B,W,B,_,_,_,_],
        [_,_,_,B,W,W,W,W,W,W,W,W,B,_,_,_],
        [_,_,B,W,W,W,W,W,W,W,W,W,W,B,_,_],
        [_,_,B,W,W,W,W,W,W,W,W,W,W,B,_,_],
        [_,_,B,W,W,W,W,W,W,W,W,W,W,B,_,_],
        [_,_,_,B,W,W,W,W,W,W,W,W,B,_,_,_],
        [_,_,_,B,W,W,W,W,W,W,W,W,B,_,_,_],
        [_,_,B,W,W,W,W,W,W,W,W,W,W,B,_,_],
        [_,_,B,W,W,W,W,P,P,W,W,W,W,B,_,_],
        [_,_,_,B,B,W,W,P,P,W,W,B,B,_,_,_],
        [_,_,_,_,_,B,P,B,B,P,B,_,_,_,_,_],
        [_,_,_,_,_,_,B,_,_,B,_,_,_,_,_,_],
    ]
    px(img, data)
    return img

def gen_rabbit_left():
    img = make(S, S)
    _ = T; B = BK; W = WH; P = PK; p = PK2; E = EY
    data = [
        [_,_,B,B,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,B,P,W,B,_,_,_,_,_,_,_,_,_,_,_],
        [_,B,P,W,B,_,_,_,_,_,_,_,_,_,_,_],
        [_,B,P,W,B,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,B,W,B,B,B,B,_,_,_,_,_,_,_,_],
        [_,_,B,W,W,W,W,W,B,B,_,_,_,_,_,_],
        [_,B,E,W,W,W,W,W,W,W,B,_,_,_,_,_],
        [_,B,W,W,W,W,W,W,W,W,B,_,_,_,_,_],
        [B,P,W,W,W,W,W,W,W,W,B,_,_,_,_,_],
        [_,B,W,W,W,W,W,W,W,B,_,_,_,_,_,_],
        [_,_,B,W,W,W,W,W,W,B,_,_,_,_,_,_],
        [_,_,B,W,W,W,W,W,W,W,B,_,_,_,_,_],
        [_,_,_,B,W,W,W,W,W,W,B,_,_,_,_,_],
        [_,_,_,_,B,W,W,W,W,B,_,_,_,_,_,_],
        [_,_,_,_,B,p,B,B,p,B,_,_,_,_,_,_],
        [_,_,_,_,_,B,_,_,B,_,_,_,_,_,_,_],
    ]
    px(img, data)
    return img

# ============================================================
# 2. DOG - front facing
# ============================================================
def gen_dog_front():
    img = make(S, S)
    _ = T; B = BK; D = BN; d = BN2; R = RD_COL; E = EY; N = BL; W = WH
    data = [
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,B,B,B,_,_,_,_,_,_,B,B,B,_,_],
        [_,B,D,D,D,B,_,_,_,_,B,D,D,D,B,_],
        [_,B,D,d,D,B,B,B,B,B,B,D,d,D,B,_],
        [_,_,B,D,D,D,D,d,d,D,D,D,D,B,_,_],
        [_,_,B,D,D,D,d,d,d,d,D,D,D,B,_,_],
        [_,_,B,D,E,W,d,d,d,d,W,E,D,B,_,_],
        [_,_,B,D,E,W,d,d,d,d,W,E,D,B,_,_],
        [_,_,B,D,D,d,d,N,N,d,d,D,D,B,_,_],
        [_,_,_,B,D,d,d,d,d,d,d,D,B,_,_,_],
        [_,_,_,B,R,R,R,R,R,R,R,R,B,_,_,_],
        [_,_,_,B,D,D,D,D,D,D,D,D,B,_,_,_],
        [_,_,B,D,D,D,D,D,D,D,D,D,D,B,_,_],
        [_,_,B,D,D,D,D,D,D,D,D,D,D,B,_,_],
        [_,_,_,B,B,D,D,B,B,D,D,B,B,_,_,_],
        [_,_,_,_,_,B,B,_,_,B,B,_,_,_,_,_],
    ]
    px(img, data)
    return img

def gen_dog_back():
    img = make(S, S)
    _ = T; B = BK; D = BN; d = BN2; R = RD_COL
    data = [
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,B,B,B,_,_,_,_,_,_,B,B,B,_,_],
        [_,B,D,D,D,B,_,_,_,_,B,D,D,D,B,_],
        [_,B,D,d,D,B,B,B,B,B,B,D,d,D,B,_],
        [_,_,B,D,D,D,D,D,D,D,D,D,D,B,_,_],
        [_,_,B,D,D,D,D,D,D,D,D,D,D,B,_,_],
        [_,_,B,D,D,D,D,D,D,D,D,D,D,B,_,_],
        [_,_,B,D,D,D,D,D,D,D,D,D,D,B,_,_],
        [_,_,B,D,D,D,D,D,D,D,D,D,D,B,_,_],
        [_,_,_,B,D,D,D,D,D,D,D,D,B,_,_,_],
        [_,_,_,B,R,R,R,R,R,R,R,R,B,_,_,_],
        [_,_,_,B,D,D,D,D,D,D,D,D,B,_,_,_],
        [_,_,B,D,D,D,D,D,D,D,D,D,D,B,_,_],
        [_,_,B,D,D,D,D,d,d,D,D,D,D,B,_,_],
        [_,_,_,B,B,D,D,B,B,D,D,B,B,_,_,_],
        [_,_,_,_,_,B,B,_,_,B,B,_,_,_,_,_],
    ]
    px(img, data)
    return img

def gen_dog_left():
    img = make(S, S)
    _ = T; B = BK; D = BN; d = BN2; R = RD_COL; E = EY; N = BL; W = WH
    data = [
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,B,B,B,_,_,_,_,_,_,_,_,_,_,_,_],
        [B,D,D,D,B,B,_,_,_,_,_,_,_,_,_,_],
        [B,D,d,D,D,D,B,B,B,B,_,_,_,_,_,_],
        [_,B,D,D,D,d,d,d,d,D,B,_,_,_,_,_],
        [_,B,E,W,d,d,d,d,d,D,B,_,_,_,_,_],
        [_,B,D,d,d,d,d,d,d,D,B,_,_,_,_,_],
        [B,N,D,d,d,d,d,d,d,D,B,_,_,_,_,_],
        [_,B,R,R,R,R,R,R,R,R,B,_,_,_,_,_],
        [_,_,B,D,D,D,D,D,D,D,B,_,_,_,_,_],
        [_,_,B,D,D,D,D,D,D,D,D,B,_,_,_,_],
        [_,_,_,B,D,D,D,D,D,D,D,B,_,_,_,_],
        [_,_,_,_,B,D,D,D,D,D,B,_,_,_,_,_],
        [_,_,_,_,B,D,B,B,D,D,B,_,_,_,_,_],
        [_,_,_,_,_,B,_,_,B,B,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    ]
    px(img, data)
    return img

# ============================================================
# 3. TRACTOR
# ============================================================
def gen_tractor_right():
    img = make(S, S)
    _ = T; B = BK; R = RD; r = RD2; G = GRN_W; g = GY2; Y = YL; W = GY3
    data = [
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,B,B,B,_,_,_,_,_],
        [_,_,_,_,_,_,_,B,g,g,g,B,_,_,_,_],
        [_,_,_,_,B,B,B,B,R,R,R,B,B,_,_,_],
        [_,_,_,B,R,R,R,R,R,R,R,R,R,B,_,_],
        [_,_,B,R,R,R,r,r,R,R,R,R,R,B,_,_],
        [_,_,B,R,R,r,r,r,R,R,R,R,R,B,_,_],
        [_,_,B,R,R,R,R,R,R,R,R,R,R,B,_,_],
        [_,_,B,R,R,R,R,R,R,R,R,R,R,B,_,_],
        [_,_,_,B,B,B,B,B,B,B,B,B,B,_,_,_],
        [_,_,B,G,G,B,_,_,_,B,G,G,G,B,_,_],
        [_,B,G,B,G,G,B,_,B,G,G,B,G,G,B,_],
        [_,B,G,G,G,G,B,_,B,G,G,G,G,G,B,_],
        [_,_,B,G,G,B,_,_,_,B,G,G,G,B,_,_],
        [_,_,_,B,B,_,_,_,_,_,B,B,B,_,_,_],
    ]
    px(img, data)
    return img

def gen_tractor_front():
    img = make(S, S)
    _ = T; B = BK; R = RD; r = RD2; G = GRN_W; g = GY2; Y = YL
    data = [
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,B,B,B,B,B,B,_,_,_,_,_],
        [_,_,_,_,B,g,g,g,g,g,g,B,_,_,_,_],
        [_,_,_,B,R,R,R,R,R,R,R,R,B,_,_,_],
        [_,_,B,R,R,R,R,R,R,R,R,R,R,B,_,_],
        [_,_,B,R,R,R,R,R,R,R,R,R,R,B,_,_],
        [_,_,B,R,Y,Y,R,R,R,R,Y,Y,R,B,_,_],
        [_,_,B,R,R,R,R,R,R,R,R,R,R,B,_,_],
        [_,_,B,R,R,R,R,R,R,R,R,R,R,B,_,_],
        [_,_,_,B,B,B,B,B,B,B,B,B,B,_,_,_],
        [_,B,G,G,B,_,_,_,_,_,_,B,G,G,B,_],
        [B,G,G,G,G,B,_,_,_,_,B,G,G,G,G,B],
        [B,G,B,G,G,B,_,_,_,_,B,G,G,B,G,B],
        [B,G,G,G,G,B,_,_,_,_,B,G,G,G,G,B],
        [_,B,G,G,B,_,_,_,_,_,_,B,G,G,B,_],
    ]
    px(img, data)
    return img

# ============================================================
# 4. CHICKEN
# ============================================================
def gen_chicken():
    img = make(S, S)
    _ = T; B = BK; W = WH; w = WH2; R = RD; O = OR; Y = YL
    data = [
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,B,B,B,B,_,_,_,_,_,_],
        [_,_,_,_,_,B,R,R,R,R,B,_,_,_,_,_],
        [_,_,_,_,_,_,B,R,R,B,_,_,_,_,_,_],
        [_,_,_,_,B,B,B,B,B,B,B,B,_,_,_,_],
        [_,_,_,B,W,W,W,W,W,W,W,W,B,_,_,_],
        [_,_,B,W,W,B,W,W,W,W,B,W,W,B,_,_],
        [_,_,B,W,W,B,W,W,W,W,B,W,W,B,_,_],
        [_,B,O,B,W,W,W,W,W,W,W,W,B,O,B,_],
        [_,_,B,W,W,W,W,W,W,W,W,W,W,B,_,_],
        [_,_,_,B,W,W,W,W,W,W,W,W,B,_,_,_],
        [_,_,_,_,B,W,W,W,W,W,W,B,_,_,_,_],
        [_,_,_,_,_,B,B,B,B,B,B,_,_,_,_,_],
        [_,_,_,_,_,B,Y,B,B,Y,B,_,_,_,_,_],
        [_,_,_,_,_,B,B,_,_,B,B,_,_,_,_,_],
    ]
    px(img, data)
    return img

# ============================================================
# 5. EGGS
# ============================================================
def gen_egg(col1, col2, col3):
    img = make(S, S)
    _ = T; B = BK; W = WH; c1 = col1; c2 = col2; c3 = col3
    data = [
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,B,B,B,B,_,_,_,_,_,_],
        [_,_,_,_,_,B,c1,c1,c1,c1,B,_,_,_,_,_],
        [_,_,_,_,B,c1,c1,W,W,c1,c1,B,_,_,_,_],
        [_,_,_,_,B,c1,c1,c1,c1,c1,c1,B,_,_,_,_],
        [_,_,_,B,c2,c2,c2,c2,c2,c2,c2,c2,B,_,_,_],
        [_,_,_,B,c3,c3,c3,c3,c3,c3,c3,c3,B,_,_,_],
        [_,_,_,B,c1,c1,c1,c1,c1,c1,c1,c1,B,_,_,_],
        [_,_,_,B,c2,c2,c2,c2,c2,c2,c2,c2,B,_,_,_],
        [_,_,_,_,B,c1,c1,c1,c1,c1,c1,B,_,_,_,_],
        [_,_,_,_,_,B,c1,c1,c1,c1,B,_,_,_,_,_],
        [_,_,_,_,_,_,B,B,B,B,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
        [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    ]
    px(img, data)
    return img

# ============================================================
# 6. TERRAIN TILES (top-down, full 16x16, no transparency)
# ============================================================
def gen_grass():
    img = make(S, S)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S-1, S-1], fill=GR)
    # Add variation
    random.seed(42)
    for _ in range(12):
        x, y = random.randint(0, S-1), random.randint(0, S-1)
        img.putpixel((x, y), GR2)
    for _ in range(6):
        x, y = random.randint(0, S-1), random.randint(0, S-1)
        img.putpixel((x, y), GR3)
    # Tiny flowers
    img.putpixel((3, 4), YL)
    img.putpixel((11, 9), WH)
    img.putpixel((7, 13), PK)
    return img

def gen_bush():
    img = make(S, S)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S-1, S-1], fill=DG)
    random.seed(77)
    for _ in range(20):
        x, y = random.randint(0, S-1), random.randint(0, S-1)
        img.putpixel((x, y), DG2)
    for _ in range(8):
        x, y = random.randint(0, S-1), random.randint(0, S-1)
        img.putpixel((x, y), (20, 60, 18, 255))
    # Dark border for depth
    for i in range(S):
        img.putpixel((i, 0), BK)
        img.putpixel((i, S-1), BK)
        img.putpixel((0, i), BK)
        img.putpixel((S-1, i), BK)
    return img

def gen_hay():
    img = make(S, S)
    _ = T; B = BK; H = YL2; h = (200, 180, 80, 255); H2 = YL
    data = [
        [_,_,_,_,_,B,B,B,B,B,B,_,_,_,_,_],
        [_,_,_,B,B,H,H,H,H,H,H,B,B,_,_,_],
        [_,_,B,H,H,H,h,h,H,H,H,H,H,B,_,_],
        [_,B,H,H,h,H,H,H,h,H,H,h,H,H,B,_],
        [_,B,H,h,H,H,H,H,H,H,h,H,H,H,B,_],
        [B,H,H,H,H,h,H,H,H,H,H,H,h,H,H,B],
        [B,H,h,H,H,H,H,h,H,H,H,H,H,h,H,B],
        [B,H,H,H,h,H,H,H,H,h,H,H,H,H,H,B],
        [B,H,H,H,H,H,h,H,H,H,H,h,H,H,H,B],
        [B,H,h,H,H,H,H,H,H,H,H,H,H,h,H,B],
        [B,H,H,H,H,h,H,H,h,H,H,H,H,H,H,B],
        [_,B,H,H,H,H,H,H,H,H,h,H,H,H,B,_],
        [_,B,H,h,H,H,h,H,H,H,H,H,h,H,B,_],
        [_,_,B,H,H,H,H,H,h,H,H,H,H,B,_,_],
        [_,_,_,B,B,H,H,H,H,H,H,B,B,_,_,_],
        [_,_,_,_,_,B,B,B,B,B,B,_,_,_,_,_],
    ]
    px(img, data)
    return img

def gen_fence():
    img = make(S, S)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S-1, S-1], fill=GR)
    # Horizontal rails
    d.rectangle([0, 3, S-1, 5], fill=BN)
    d.rectangle([0, 10, S-1, 12], fill=BN)
    # Vertical posts
    d.rectangle([2, 1, 4, 14], fill=BN2)
    d.rectangle([11, 1, 13, 14], fill=BN2)
    # Outlines
    d.rectangle([0, 3, S-1, 3], fill=BN3)
    d.rectangle([0, 10, S-1, 10], fill=BN3)
    return img

def gen_mud():
    img = make(S, S)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S-1, S-1], fill=MU)
    random.seed(55)
    for _ in range(15):
        x, y = random.randint(0, S-1), random.randint(0, S-1)
        img.putpixel((x, y), MU2)
    for _ in range(8):
        x, y = random.randint(0, S-1), random.randint(0, S-1)
        img.putpixel((x, y), MU3)
    # Small puddles
    d.rectangle([4, 5, 6, 7], fill=(70, 90, 120, 255))
    d.rectangle([10, 11, 12, 12], fill=(70, 90, 120, 255))
    return img

def gen_hole():
    img = make(S, S)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S-1, S-1], fill=GR)
    # Hole - concentric circles
    d.ellipse([2, 2, 13, 13], fill=BN3)
    d.ellipse([3, 3, 12, 12], fill=GY2)
    d.ellipse([5, 5, 10, 10], fill=BL)
    d.ellipse([6, 6, 9, 9], fill=(10, 10, 10, 255))
    return img

def gen_path():
    img = make(S, S)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S-1, S-1], fill=PT)
    random.seed(33)
    for _ in range(10):
        x, y = random.randint(0, S-1), random.randint(0, S-1)
        img.putpixel((x, y), PT2)
    # Subtle tire tracks
    for y in range(S):
        img.putpixel((5, y), PT2)
        img.putpixel((10, y), PT2)
    return img

def gen_exit_closed():
    img = make(S, S)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S-1, S-1], fill=GR)
    # Door frame
    d.rectangle([2, 1, 13, 14], fill=BN3)
    d.rectangle([3, 2, 12, 13], fill=RD)
    d.rectangle([3, 2, 12, 2], fill=BN)
    # Cross / X mark
    for i in range(4, 12):
        off = i - 4
        img.putpixel((3 + off, 3 + off), BK)
        img.putpixel((12 - off, 3 + off), BK)
    # Lock
    d.rectangle([7, 7, 8, 9], fill=YL)
    return img

def gen_exit_open():
    img = make(S, S)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S-1, S-1], fill=GR)
    # Door frame
    d.rectangle([2, 1, 13, 14], fill=BN3)
    d.rectangle([3, 2, 12, 13], fill=GRN_G)
    # Glow effect
    d.rectangle([5, 4, 10, 11], fill=(100, 255, 100, 255))
    d.rectangle([6, 5, 9, 10], fill=(180, 255, 180, 255))
    d.rectangle([7, 6, 8, 9], fill=(220, 255, 220, 255))
    return img

# ============================================================
# 7. BACKGROUNDS (larger images)
# ============================================================
def gen_bg_game():
    """1024x768 game background - rolling hills."""
    img = Image.new("RGBA", (1024, 768))
    d = ImageDraw.Draw(img)
    # Sky gradient
    for y in range(768):
        r = int(100 + (y / 768) * 60)
        g = int(160 + (y / 768) * 80)
        b = int(60 - (y / 768) * 30)
        d.line([(0, y), (1023, y)], fill=(r, g, b, 255))
    # Darker green base
    d.rectangle([0, 0, 1023, 767], fill=(35, 90, 30, 255))
    # Some hill shapes
    for cx, cy, rx, ry, col in [
        (200, 600, 300, 200, (45, 110, 35, 255)),
        (600, 500, 400, 250, (40, 100, 32, 255)),
        (900, 650, 250, 180, (50, 115, 40, 255)),
        (100, 400, 200, 150, (42, 105, 34, 255)),
    ]:
        d.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], fill=col)
    return img

def gen_bg_menu():
    """1024x768 menu background - Easter farm scene."""
    img = Image.new("RGBA", (1024, 768))
    d = ImageDraw.Draw(img)
    # Sky
    for y in range(400):
        r = int(130 + (1 - y / 400) * 80)
        g = int(190 + (1 - y / 400) * 50)
        b = int(240 + (1 - y / 400) * 15)
        d.line([(0, y), (1023, y)], fill=(r, g, b, 255))
    # Clouds
    for cx, cy in [(150, 80), (400, 120), (700, 60), (900, 140)]:
        d.ellipse([cx-60, cy-20, cx+60, cy+20], fill=(255, 255, 255, 200))
        d.ellipse([cx-40, cy-30, cx+40, cy+10], fill=(255, 255, 255, 200))
    # Ground
    d.rectangle([0, 350, 1023, 767], fill=(80, 170, 50, 255))
    # Hills
    d.ellipse([50, 280, 400, 450], fill=(70, 155, 45, 255))
    d.ellipse([350, 300, 750, 480], fill=(75, 160, 48, 255))
    d.ellipse([650, 290, 1050, 460], fill=(72, 158, 46, 255))
    # Fence
    for x in range(0, 1024, 48):
        d.rectangle([x+2, 430, x+6, 470], fill=(160, 110, 60, 255))
        d.rectangle([x, 440, x+48, 445], fill=(140, 95, 50, 255))
        d.rectangle([x, 460, x+48, 465], fill=(140, 95, 50, 255))
    # Eggs scattered
    random.seed(42)
    egg_colors = [(255, 150, 170), (150, 200, 255), (255, 220, 100), (180, 140, 255), (150, 255, 180)]
    for _ in range(20):
        ex = random.randint(20, 1000)
        ey = random.randint(500, 720)
        ec = egg_colors[random.randint(0, len(egg_colors)-1)]
        d.ellipse([ex-8, ey-10, ex+8, ey+10], fill=(*ec, 255))
        d.ellipse([ex-6, ey-8, ex+2, ey-2], fill=(255, 255, 255, 80))
    # Farmhouse
    d.rectangle([780, 330, 920, 430], fill=(200, 60, 60, 255))
    d.polygon([(770, 330), (850, 270), (930, 330)], fill=(180, 50, 50, 255))
    d.rectangle([830, 380, 870, 430], fill=(140, 95, 50, 255))
    d.rectangle([790, 345, 820, 370], fill=(180, 220, 255, 255))
    # Trees
    for tx in [50, 180, 550, 980]:
        d.rectangle([tx-5, 350, tx+5, 430], fill=(120, 80, 40, 255))
        d.ellipse([tx-35, 280, tx+35, 370], fill=(PK[0], PK[1], PK[2], 200))
        d.ellipse([tx-25, 290, tx+25, 350], fill=(255, 180, 200, 200))
    return img

def gen_splash():
    """600x400 splash / loading screen."""
    img = Image.new("RGBA", (600, 400))
    d = ImageDraw.Draw(img)
    # Dark background
    d.rectangle([0, 0, 599, 399], fill=(10, 26, 10, 255))
    # Stars
    random.seed(99)
    for _ in range(30):
        sx, sy = random.randint(0, 599), random.randint(0, 150)
        d.point((sx, sy), fill=(255, 255, 200, 180))
    # Ground
    d.rectangle([0, 300, 599, 399], fill=(25, 60, 20, 255))
    # Flowers on ground
    for _ in range(15):
        fx = random.randint(10, 590)
        fy = random.randint(310, 380)
        fc = random.choice([(255, 200, 100), (255, 150, 170), (200, 150, 255)])
        d.point((fx, fy), fill=fc)
    # Rabbit silhouette (centered, simplified)
    cx, cy = 300, 220
    # Ears
    d.ellipse([cx-25, cy-90, cx-10, cy-30], fill=(255, 255, 255, 255))
    d.ellipse([cx+10, cy-90, cx+25, cy-30], fill=(255, 255, 255, 255))
    d.ellipse([cx-22, cy-85, cx-13, cy-35], fill=(255, 180, 190, 255))
    d.ellipse([cx+13, cy-85, cx+22, cy-35], fill=(255, 180, 190, 255))
    # Head
    d.ellipse([cx-30, cy-40, cx+30, cy+10], fill=(255, 255, 255, 255))
    # Eyes
    d.ellipse([cx-15, cy-20, cx-8, cy-10], fill=(30, 30, 30, 255))
    d.ellipse([cx+8, cy-20, cx+15, cy-10], fill=(30, 30, 30, 255))
    d.point((cx-12, cy-17), fill=(255, 255, 255, 255))
    d.point((cx+11, cy-17), fill=(255, 255, 255, 255))
    # Nose
    d.ellipse([cx-3, cy-5, cx+3, cy+1], fill=(255, 150, 170, 255))
    # Body
    d.ellipse([cx-25, cy+5, cx+25, cy+50], fill=(255, 255, 255, 255))
    # Paws
    d.ellipse([cx-20, cy+40, cx-8, cy+55], fill=(255, 200, 210, 255))
    d.ellipse([cx+8, cy+40, cx+20, cy+55], fill=(255, 200, 210, 255))
    # Egg in paws
    d.ellipse([cx-12, cy+25, cx+12, cy+48], fill=(255, 210, 50, 255))
    d.ellipse([cx-8, cy+28, cx+2, cy+38], fill=(255, 240, 150, 255))
    # Glow around rabbit
    for r in range(80, 40, -5):
        alpha = int(15 * (80 - r) / 40)
        glow_col = (200, 255, 200, alpha)
        # Just a subtle suggestion via a larger ellipse
    return img

def gen_startup_logo():
    """500x83 startup logo banner."""
    img = Image.new("RGBA", (500, 83))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 499, 82], fill=(10, 26, 10, 255))
    # "EASTER EGG" - big blocky letters (manual pixel font)
    # Simpler: colored rectangles as stylized text blocks
    # Each letter ~30px wide
    text_col = (255, 100, 150, 255)
    sub_col = (255, 200, 50, 255)
    # Since we don't have a font loaded, draw colored blocks as placeholder
    # E A S T E R
    letters_x = 65
    for i, w in enumerate([28, 28, 26, 26, 28, 28]):
        x = letters_x + i * 32
        d.rectangle([x, 10, x + w, 38], fill=text_col)
        # Cut out middle for "letter" look
        if i in [0, 4]:  # E
            d.rectangle([x+6, 14, x+w-2, 18], fill=(10, 26, 10, 255))
            d.rectangle([x+6, 26, x+w-2, 30], fill=(10, 26, 10, 255))
        elif i == 1:  # A
            d.rectangle([x+6, 10, x+w-6, 14], fill=(10, 26, 10, 255))
            d.rectangle([x+6, 22, x+w-6, 26], fill=text_col)
        elif i == 2:  # S
            d.rectangle([x+6, 14, x+w-2, 18], fill=(10, 26, 10, 255))
            d.rectangle([x+2, 26, x+w-6, 30], fill=(10, 26, 10, 255))
        elif i == 3:  # T
            d.rectangle([x+2, 14, x+12, 38], fill=(10, 26, 10, 255))
            d.rectangle([x+18, 14, x+w-2, 38], fill=(10, 26, 10, 255))
        elif i == 5:  # R
            d.rectangle([x+6, 14, x+w-2, 18], fill=(10, 26, 10, 255))
            d.rectangle([x+6, 26, x+w-2, 38], fill=(10, 26, 10, 255))
            d.rectangle([x+12, 26, x+20, 38], fill=text_col)
    # "EGG" second word
    egg_x = letters_x + 7 * 32
    for i, w in enumerate([28, 28, 28]):
        x = egg_x + i * 32
        d.rectangle([x, 10, x + w, 38], fill=text_col)
    # "pro Kubu"
    d.rectangle([180, 50, 320, 68], fill=sub_col)
    # Small eggs decoration
    for ex, col in [(30, (255, 150, 170)), (40, (150, 200, 255)), (450, (255, 220, 100)), (465, (180, 140, 255))]:
        d.ellipse([ex-6, 25, ex+6, 45], fill=(*col, 255))
    return img


# ============================================================
# GENERATE ALL
# ============================================================
print("Generating sprites...")

# Rabbit
r = gen_rabbit_front(); save(r, "rabbit_front.png")
r = gen_rabbit_back(); save(r, "rabbit_back.png")
r = gen_rabbit_left(); save(r, "rabbit_left.png")
r = gen_rabbit_left().transpose(Image.FLIP_LEFT_RIGHT); save(r, "rabbit_right.png")

# Dog
d = gen_dog_front(); save(d, "dog_front.png")
d = gen_dog_back(); save(d, "dog_back.png")
d = gen_dog_left(); save(d, "dog_left.png")
d = gen_dog_left().transpose(Image.FLIP_LEFT_RIGHT); save(d, "dog_right.png")

# Tractor
t = gen_tractor_right(); save(t, "tractor_right.png")
t = gen_tractor_right().transpose(Image.FLIP_LEFT_RIGHT); save(t, "tractor_left.png")
t = gen_tractor_front(); save(t, "tractor_front.png")

# Chicken
save(gen_chicken(), "chicken.png")

# Eggs
save(gen_egg(PK2, BLU, PK), "egg_normal.png")
save(gen_egg(GD, GD2, GD3), "egg_golden.png")
save(gen_egg(PP, PP2, PP3), "egg_special.png")

# Tiles
save(gen_grass(), "tile_grass.png")
save(gen_bush(), "tile_bush.png")
save(gen_hay(), "tile_hay.png")
save(gen_fence(), "tile_fence.png")
save(gen_mud(), "tile_mud.png")
save(gen_hole(), "tile_hole.png")
save(gen_path(), "tile_path.png")
save(gen_exit_closed(), "tile_exit_closed.png")
save(gen_exit_open(), "tile_exit_open.png")

# Backgrounds (no scale_up, native resolution)
print("Generating backgrounds...")
bg = gen_bg_game(); bg.save(os.path.join(OUT, "bg_game.png")); print(f"  bg_game.png (1024x768)")
bg = gen_bg_menu(); bg.save(os.path.join(OUT, "bg_menu.png")); print(f"  bg_menu.png (1024x768)")
sp = gen_splash(); sp.save(os.path.join(OUT, "splash.png")); print(f"  splash.png (600x400)")
sl = gen_startup_logo(); sl.save(os.path.join(OUT, "startup-logo.png")); print(f"  startup-logo.png (500x83)")

print("\nDone! All sprites saved to assets/textures/")
