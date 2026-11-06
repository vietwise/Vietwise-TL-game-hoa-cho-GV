"""Dựng biểu tượng màn hình chính (icon-192/512, apple-touch-icon, favicon-64) từ ảnh Não vẫy tay.
Chạy: python3 tools/dong-goi/dung_bieu_tuong.py   (ra ở thư mục gốc repo)"""
import os
from PIL import Image, ImageDraw

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SPRITE = os.path.join(REPO, 'assets/sprites/nao/nao-vay-tay.webp')
TIM, HONG, KEM, VANG = (138, 69, 154), (202, 65, 188), (245, 241, 232), (236, 196, 89)
N = 1024  # vẽ to rồi thu nhỏ cho mịn


def nen():
    im = Image.new('RGB', (N, N))
    px = im.load()
    for y in range(N):
        for x in range(N):
            t = (x + y) / (2 * N - 2)  # chéo 160°, như trang Trường Thọ
            px[x, y] = tuple(round(a + (b - a) * t) for a, b in zip(TIM, HONG))
    d = ImageDraw.Draw(im)
    r = int(N * 0.40)
    c = N // 2
    d.ellipse((c - r - 14, c - r - 14, c + r + 14, c + r + 14), fill=VANG)
    d.ellipse((c - r, c - r, c + r, c + r), fill=KEM)
    s = Image.open(SPRITE).convert('RGBA')
    w = int(N * 0.66)
    h = round(s.height * w / s.width)
    s = s.resize((w, h), Image.LANCZOS)
    im.paste(s, ((N - w) // 2, (N - h) // 2 + int(N * 0.02)), s)
    return im


big = nen()
for ten, kt in [('icon-512.png', 512), ('icon-192.png', 192), ('apple-touch-icon.png', 180), ('favicon-64.png', 64)]:
    big.resize((kt, kt), Image.LANCZOS).save(os.path.join(REPO, ten), optimize=True)
    print('ra', ten)
