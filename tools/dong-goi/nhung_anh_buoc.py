"""Đưa ảnh biểu tượng bước vào trình chơi.
Ảnh gốc (PNG nền trắng, Hong tạo) -> tách nền trắng, thu về 128 px, WebP -> skill/game-hoc-vietwise/assets/buoc/<ten>.webp
rồi viết dòng `var BUOC={...};` trong assets/trinh-choi.html (ngoài khối khóa).
Dùng:  python3 tools/dong-goi/nhung_anh_buoc.py [ten=anh-goc.png ...]
Không có tham số thì chỉ nhúng lại các .webp đã có.
Ảnh Bé Não theo bước và viên Châu Lộc (tên trong HINH_TEN) vào assets/hinh/, nhúng vào `var HINH={...};`."""
import sys, os, re, io, base64
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
SK = os.path.abspath(H + '/../../skill/game-hoc-vietwise')
D = SK + '/assets/buoc'
# tên tệp -> tên bước hiện trong trình chơi
TEN = {'buoc-ke': 'Kể', 'buoc-chon': 'Chọn', 'buoc-chung-cu': 'Chứng cứ', 'buoc-phan-bien': 'Phản biện',
       'buoc-sang-tao': 'Sáng tạo', 'buoc-chot': 'Chốt', 'buoc-noi-ly-do': 'Nói lý do', 'buoc-buoc-ngoat': 'Bước ngoặt',
       'buoc-cau-hoi': 'Câu hỏi của hôm nay', 'buoc-chia-khoa-sach': 'Chìa khóa sách', 'buoc-sach-noi-gi': 'Sách nói gì',
       'buoc-viet-tiep': 'Viết tiếp', 'buoc-level': 'Chọn level', 'buoc-ngam-them': 'Ngẫm thêm'}

# ảnh khác trong trình chơi: tên -> cỡ tối đa (px)
HINH_TEN = {'nao-gio-tay': 160, 'nao-bac-thang': 160, 'nao-ngac-nhien': 160, 'chau-loc': 72}
DH = SK + '/assets/hinh'

def tach_nen(im):
    im = im.convert('RGBA')
    px = im.load(); w, h = im.size
    # loang từ viền: điểm gần trắng nối với viền thì thành trong suốt
    seen = set(); st = [(x, y) for x in range(w) for y in (0, h - 1)] + [(x, y) for y in range(h) for x in (0, w - 1)]
    while st:
        x, y = st.pop()
        if (x, y) in seen or not (0 <= x < w and 0 <= y < h): continue
        r, g, b, a = px[x, y]
        if min(r, g, b) < 235: continue
        seen.add((x, y)); px[x, y] = (255, 255, 255, 0)
        st += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return im

for arg in sys.argv[1:]:
    ten, f = arg.split('=', 1)
    assert ten in TEN or ten in HINH_TEN, ten
    co = HINH_TEN.get(ten, 128); thu = DH if ten in HINH_TEN else D
    im = Image.open(f); im.thumbnail((co * 2.5, co * 2.5))
    im = tach_nen(im); im = im.crop(im.getbbox()); im.thumbnail((co, co), Image.LANCZOS)
    os.makedirs(thu, exist_ok=True); im.save(thu + '/' + ten + '.webp', 'WEBP', quality=82, method=6)
    print(ten, im.size, os.path.getsize(thu + '/' + ten + '.webp'), 'byte')

o = []
for ten in sorted(TEN):
    p = D + '/' + ten + '.webp'
    if os.path.exists(p):
        o.append("'%s':'data:image/webp;base64,%s'" % (TEN[ten], base64.b64encode(open(p, 'rb').read()).decode()))
P = SK + '/assets/trinh-choi.html'
t = open(P, encoding='utf-8').read()
moi = 'var BUOC={' + ','.join(o) + '};'
t, n = re.subn(r'var BUOC=\{.*?\};', lambda m: moi, t, count=1)
assert n == 1, 'trinh-choi.html thiếu dòng var BUOC={...};'
o = ["'%s':'data:image/webp;base64,%s'" % (ten, base64.b64encode(open(DH + '/' + ten + '.webp', 'rb').read()).decode())
     for ten in sorted(HINH_TEN) if os.path.exists(DH + '/' + ten + '.webp')]
moi = 'var HINH={' + ','.join(o) + '};'
t, n = re.subn(r'var HINH=\{.*?\};', lambda m: moi, t, count=1)
assert n == 1, 'trinh-choi.html thiếu dòng var HINH={...};'
open(P, 'w', encoding='utf-8').write(t)
print('Đã nhúng ảnh bước và', len(o), 'ảnh HINH vào trinh-choi.html')
