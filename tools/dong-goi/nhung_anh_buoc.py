"""Đưa ảnh biểu tượng bước vào trình chơi.
Ảnh gốc (PNG nền trắng, Hong tạo) -> tách nền trắng, thu về 128 px, WebP -> skill/game-hoc-vietwise/assets/buoc/<ten>.webp
(scripts/dung_trang.py nhúng ảnh vào từng game khi dựng; trinh-choi.html giữ var BUOC={}; var HINH={}; rỗng cho nhẹ).
Dùng:  python3 tools/dong-goi/nhung_anh_buoc.py [ten=anh-goc.png ...]
Ảnh Bé Não theo bước và viên Châu Lộc (tên trong HINH_TEN) vào assets/hinh/."""
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
HINH_TEN = {'nao-gio-tay': 160, 'nao-bac-thang': 160, 'nao-ngac-nhien': 160, 'nao-kinh-lup': 160, 'nao-suy-nghi': 160,
            'nao-bong-den': 160, 'nao-ngam': 160, 'chau-loc': 72, 'level-1': 64, 'level-2': 64, 'level-3': 64, 'level-4': 64,
            'lung-the': 360, 'ca-lop-vo-tay': 420}
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
    os.makedirs(thu, exist_ok=True); im.save(thu + '/' + ten + '.webp', 'WEBP', quality={'lung-the': 60, 'ca-lop-vo-tay': 55}.get(ten, 82), method=6)
    print(ten, im.size, os.path.getsize(thu + '/' + ten + '.webp'), 'byte')

print('Ảnh nằm trong assets/buoc và assets/hinh; scripts/dung_trang.py nhúng khi dựng game.')
