"""Dựng biểu tượng màn hình chính từ logo "Trợ lý Game-học cho Thầy Cô" (Hong chốt 19/11/2026).
Nguồn: tools/dong-goi/mau/logo-app.png (vuông, nền kem).
Ra ở gốc repo: icon-512, icon-192, apple-touch-icon (cả logo), icon-maskable-512 (logo thu nhỏ trong vùng an toàn),
favicon-64 (chỉ hình cuốn sách và mầm, vì chữ quá nhỏ sẽ không đọc được).
Chạy: python3 tools/dong-goi/dung_bieu_tuong.py"""
import os
from PIL import Image

H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(H + '/../..')
KEM = (249, 250, 247)
logo = Image.open(H + '/mau/logo-app.png').convert('RGB')
w, h = logo.size
s = min(w, h); logo = logo.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))
for ten, kt in [('icon-512.png', 512), ('icon-192.png', 192), ('apple-touch-icon.png', 180)]:
    logo.resize((kt, kt), Image.LANCZOS).save(os.path.join(REPO, ten), optimize=True); print('ra', ten)
m = Image.new('RGB', (512, 512), KEM); k = int(512 * 0.78)
m.paste(logo.resize((k, k), Image.LANCZOS), ((512 - k) // 2, (512 - k) // 2)); m.save(REPO + '/icon-maskable-512.png', optimize=True); print('ra icon-maskable-512.png')
# favicon: phần hình (sách + mầm) ở nửa trên logo
b = logo.crop((int(s * 0.17), int(s * 0.02), int(s * 0.83), int(s * 0.50)))
f = Image.new('RGB', (b.width, b.width), KEM); f.paste(b, (0, (b.width - b.height) // 2))
f.resize((64, 64), Image.LANCZOS).save(REPO + '/favicon-64.png', optimize=True); print('ra favicon-64.png')
