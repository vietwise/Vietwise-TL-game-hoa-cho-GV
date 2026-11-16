"""Đưa ảnh minh họa (Hong tạo) vào app trang đầu mau/doc-truoc.html.
Ảnh gốc PNG nền trắng -> tách nền, WebP -> tools/dong-goi/mau/anh/<ten>.webp
rồi điền src của mọi <img data-anh="<ten>" src="..."> và ảnh nền đầu trang (giữa /*NEN*/ và /*HET-NEN*/).
Dùng:  python3 tools/dong-goi/nhung_anh_app.py [ten=anh-goc.png ...]   (không tham số: nhúng lại ảnh đã có)"""
import sys, os, re, base64
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__))
D = H + '/mau/anh'

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

CO = {'loai-mo-tiet': 160, 'loai-on-bai': 160, 'loai-sach-la-thay': 160,
      'the-phieu': 64, 'the-readme': 64, 'the-tra-ket-qua': 64, 'nen-dau-trang': 1400}
for arg in sys.argv[1:]:
    ten, f = arg.split('=', 1)
    assert ten in CO, ten
    im = Image.open(f)
    os.makedirs(D, exist_ok=True)
    if ten == 'nen-dau-trang':
        im = im.convert('RGB'); im.thumbnail((CO[ten], CO[ten]), Image.LANCZOS)
        im.save(D + '/' + ten + '.webp', 'WEBP', quality=70, method=6)
    else:
        im.thumbnail((CO[ten] * 2.5, CO[ten] * 2.5)); im = tach_nen(im); im = im.crop(im.getbbox())
        im.thumbnail((CO[ten], CO[ten]), Image.LANCZOS); im.save(D + '/' + ten + '.webp', 'WEBP', quality=82, method=6)
    print(ten, im.size, os.path.getsize(D + '/' + ten + '.webp'), 'byte')
P = H + '/mau/doc-truoc.html'
t = open(P, encoding='utf-8').read()
def uri(ten):
    p = D + '/' + ten + '.webp'
    return 'data:image/webp;base64,' + base64.b64encode(open(p, 'rb').read()).decode() if os.path.exists(p) else ''
t = re.sub(r'(<img[^>]*data-anh="([a-z-]+)"[^>]*src=")[^"]*(")', lambda m: m.group(1) + uri(m.group(2)) + m.group(3), t)
n = uri('nen-dau-trang')
nen = ('header{background:url("%s") center/cover no-repeat,linear-gradient(180deg,var(--kem) 0%%,#E6EAFB 100%%)}' % n) if n else ''
t, k = re.subn(r'/\*NEN\*/.*?/\*HET-NEN\*/', lambda m: '/*NEN*/' + nen + '/*HET-NEN*/', t, count=1, flags=re.S)
assert k == 1, 'doc-truoc.html thiếu /*NEN*/.../*HET-NEN*/'
open(P, 'w', encoding='utf-8').write(t)
print('Đã nhúng ảnh app vào doc-truoc.html')
