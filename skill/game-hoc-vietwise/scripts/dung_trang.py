#!/usr/bin/env python3
"""Dựng trang chơi game từ game.json.
Dùng:  python3 dung_trang.py game.json game.html
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

def main():
    if len(sys.argv) < 3:
        sys.exit('Dùng: python3 dung_trang.py game.json game.html')
    t = open(GOC, encoding='utf-8').read()
    m = re.search(r"var BRAND='(.*?)';", t)
    k = re.search(r"var BH=(-?\d+);", t)
    ok = (m and k and h(m.group(1)) == int(k.group(1))
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
    if not (2 <= len(g['lua_chon']) <= 4):
        sys.exit('lua_chon cần 2 đến 4 mục')
    s = json.dumps(g, ensure_ascii=False).replace('</', '<\\/')
    open(sys.argv[2], 'w', encoding='utf-8').write(t.replace('__GAME_JSON__', s))
    print('Đã dựng', sys.argv[2], len(s), 'ký tự dữ liệu game')

main()
