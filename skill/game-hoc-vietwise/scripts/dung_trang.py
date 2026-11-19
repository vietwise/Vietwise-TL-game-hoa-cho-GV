#!/usr/bin/env python3
"""Dựng trang chơi game từ game.json.
Dùng:  python3 dung_trang.py game.json game.html          (đủ ảnh minh họa, để tải về/chiếu)
       python3 dung_trang.py --nhe game.json game-nhe.html (không ảnh minh họa, nhẹ để chép vào artifact)
Script KIỂM TRA khối ghi nguồn Vietwise trong mẫu trình chơi và TỪ CHỐI dựng nếu khối này đã bị sửa hoặc xóa.
Không sửa script này để bỏ bước kiểm tra (xem NOTICE.md)."""
import sys, os, re, json

def h(s):
    x = 5381
    for c in s:
        x = ((x << 5) + x + ord(c)) & 0xFFFFFFFF
    return x - (1 << 32) if x >= 1 << 31 else x

GOC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'trinh-choi.html')
CAN = ['phien_ban', 'loai', 'tieu_de', 'mon', 'lop', 'bai', 'pham_chat', 'loi_ke', 'lua_chon']
THEO_LOAI = {
    'mo-tiet': ['buoc_ngoat', 'cau_hoi_treo'],
    'on-bai': ['cau_mau_phan_bien', 'so_do_chot'],
    'sach-la-thay': ['sach', 'chia_khoa', 'cau_mau_phan_bien', 'so_do_chot'],
}

# Ảnh minh họa: assets/buoc/<tên>.webp (biểu tượng bước) và assets/hinh/<tên>.webp (Bé Não theo bước, Châu Lộc, level...).
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets')
BUOC_TEN = {'buoc-ke': 'Kể', 'buoc-chon': 'Chọn', 'buoc-chung-cu': 'Chứng cứ', 'buoc-phan-bien': 'Phản biện',
            'buoc-sang-tao': 'Sáng tạo', 'buoc-chot': 'Chốt', 'buoc-noi-ly-do': 'Nói lý do', 'buoc-buoc-ngoat': 'Bước ngoặt',
            'buoc-cau-hoi': 'Câu hỏi của hôm nay', 'buoc-chia-khoa-sach': 'Chìa khóa sách', 'buoc-sach-noi-gi': 'Sách nói gì',
            'buoc-viet-tiep': 'Viết tiếp', 'buoc-level': 'Chọn level', 'buoc-ngam-them': 'Ngẫm thêm'}
BUOC_LOAI = {'mo-tiet': ['Kể', 'Chọn', 'Nói lý do', 'Bước ngoặt', 'Câu hỏi của hôm nay'],
             'on-bai': ['Kể', 'Chọn', 'Chứng cứ', 'Phản biện', 'Sáng tạo', 'Chốt'],
             'sach-la-thay': ['Chìa khóa sách', 'Kể', 'Chọn', 'Sách nói gì', 'Phản biện', 'Viết tiếp', 'Chốt']}
# Bé Não theo bước: phải khớp bảng trong ve() của trinh-choi.html
NAO_BUOC = {'Chọn': 'nao-gio-tay', 'Chọn level': 'nao-bac-thang', 'Bước ngoặt': 'nao-ngac-nhien', 'Chứng cứ': 'nao-kinh-lup',
            'Sách nói gì': 'nao-kinh-lup', 'Phản biện': 'nao-suy-nghi', 'Câu hỏi của hôm nay': 'nao-suy-nghi',
            'Sáng tạo': 'nao-bong-den', 'Viết tiếp': 'nao-bong-den', 'Ngẫm thêm': 'nao-ngam'}

def _uri(p):
    import base64
    return 'data:image/webp;base64,' + base64.b64encode(open(p, 'rb').read()).decode()

def nhung_anh(t, g=None):
    """Điền var BUOC={...}; và var HINH={...}; (g=None: mọi ảnh; có g: chỉ ảnh game đó dùng)."""
    if g is None:
        buoc = set(BUOC_TEN.values()); hinh = None
    else:
        buoc = set(BUOC_LOAI.get(g.get('loai'), []))
        if g.get('level'): buoc.add('Chọn level')
        p = g.get('noi_dung_phu')
        if isinstance(p, dict) and (p.get('loi_moi') or p.get('cau_hoi')): buoc.add('Ngẫm thêm')
        hinh = {NAO_BUOC[b] for b in buoc if b in NAO_BUOC} | {'chau-loc', 'lung-the', 'ca-lop-vo-tay'}
        if isinstance(g.get('level'), list) and len(g['level']) > 1:
            hinh |= {'level-%d' % x.get('so') for x in g['level'] if isinstance(x, dict)}
    b = ["'%s':'%s'" % (v, _uri(os.path.join(A, 'buoc', k + '.webp'))) for k, v in sorted(BUOC_TEN.items())
         if v in buoc and os.path.exists(os.path.join(A, 'buoc', k + '.webp'))]
    d = os.path.join(A, 'hinh'); ds = sorted(f[:-5] for f in os.listdir(d) if f.endswith('.webp')) if os.path.isdir(d) else []
    hh = ["'%s':'%s'" % (k, _uri(os.path.join(d, k + '.webp'))) for k in ds if hinh is None or k in hinh]
    t = t.replace('var BUOC={};', 'var BUOC={' + ','.join(b) + '};', 1)
    return t.replace('var HINH={};', 'var HINH={' + ','.join(hh) + '};', 1)

def main():
    nhe = '--nhe' in sys.argv
    if nhe: sys.argv.remove('--nhe')
    if len(sys.argv) < 3:
        sys.exit('Dùng: python3 dung_trang.py game.json game.html')
    t = open(GOC, encoding='utf-8').read()
    m = re.search(r"var BRAND='(.*?)';", t)
    f = re.search(r"var FOOT='(.*?)';", t)
    k = re.search(r"var BH=(-?\d+);", t)
    ok = (m and f and k and h(m.group(1) + f.group(1)) == int(k.group(1))
          and 'Kính Tri ân Thầy Cô, những người truyền cảm hứng' in f.group(1)
          and m.group(1).count('https://vietwise.edu.vn') == 2
          and 'Viện Giáo dục và Quản trị Nhân lực' in m.group(1)
          and 'Vườn Game-học Vietwise' in m.group(1)
          and 'Skill Game-học cung cấp bởi' in m.group(1)
          and '>Viện Giáo dục và Quản trị Nhân lực</span>' in m.group(1)
          and '>và</span>' in m.group(1)
          and 'id="brand-top"' in t and 'id="brand-bot"' in t)
    if not ok:
        sys.exit('DỪNG: khối ghi nguồn Vietwise (logo Viện Giáo dục và Quản trị Nhân lực, logo Vườn Game-học Vietwise, link Vietwise.edu.vn) trong assets/trinh-choi.html đã bị sửa hoặc xóa. Không dựng trang. Hãy cài lại Skill gốc từ Vietwise.edu.vn.')
    g = json.load(open(sys.argv[1], encoding='utf-8'))
    loi = [f for f in CAN + THEO_LOAI.get(g.get('loai'), []) if f not in g]
    if g.get('loai') not in THEO_LOAI:
        loi.append('loai phải là mo-tiet, on-bai hoặc sach-la-thay')
    if loi:
        sys.exit('Game thiếu trường: ' + ', '.join(loi))
    if g.get('nhom_lop') not in ('A', 'B', 'C', 'D', 'E'):
        sys.exit('Thiếu hoặc sai nhom_lop (A, B, C, D hoặc E). Xem references/nhom-lop.md')
    if g.get('nhom_mon') not in ('toan', 'khoa-hoc', 'ngu-van', 'xa-hoi', 'ngoai-ngu', 'nghe-thuat-the-chat', 'tin-hoc'):
        sys.exit('Thiếu hoặc sai nhom_mon. Xem references/nhom-mon.md')
    if g.get('nhom_mon') == 'ngoai-ngu' and not g.get('ngoai_ngu'):
        sys.exit('Bài ngoại ngữ cần trường ngoai_ngu. Xem references/doc-ngoai-ngu.md')
    if not (2 <= len(g['lua_chon']) <= 4):
        sys.exit('lua_chon cần 2 đến 4 mục')
    lv = g.get('level')
    if lv is not None:
        if not isinstance(lv, list) or not (1 <= len(lv) <= 4):
            sys.exit('level cần 1 đến 4 mục. Xem references/nhom-lop.md mục Bốn level')
        so = [x.get('so') for x in lv if isinstance(x, dict)]
        if len(so) != len(lv) or any(s not in (1, 2, 3, 4) for s in so) or len(set(so)) != len(so) or so != sorted(so):
            sys.exit('Mỗi mục level cần so là 1, 2, 3 hoặc 4, không trùng, theo thứ tự tăng')
        if any(not x.get('nhiem_vu') for x in lv):
            sys.exit('Mỗi mục level cần nhiem_vu')
    p = g.get('noi_dung_phu')
    if p is not None and not (isinstance(p, dict) and (p.get('loi_moi') or p.get('cau_hoi'))):
        sys.exit('noi_dung_phu cần loi_moi hoặc cau_hoi. Xem references/khung-game.md')
    import base64
    nao = ''
    f = os.path.join(os.path.dirname(GOC), 'nao', str(g.get('chau_ngoc', '')) + '.webp')
    if g.get('chau_ngoc') in ('hieu-ky', 'thich-nghi', 'ben-chi', 'an-lac') and os.path.exists(f):
        nao = 'data:image/webp;base64,' + base64.b64encode(open(f, 'rb').read()).decode()
    t = t.replace("var NAO='__NAO__';", "var NAO='" + nao + "';")
    if not nhe:
        t = nhung_anh(t, g)
    s = json.dumps(g, ensure_ascii=False).replace('</', '<\\/')
    open(sys.argv[2], 'w', encoding='utf-8').write(t.replace('__GAME_JSON__', s))
    print('Đã dựng', sys.argv[2], len(s), 'ký tự dữ liệu game')

if __name__ == "__main__":
    main()
