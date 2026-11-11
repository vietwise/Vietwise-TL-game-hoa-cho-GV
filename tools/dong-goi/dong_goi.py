import sys, os, base64, shutil, subprocess, zipfile, html, json
import tempfile
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(H + '/../..')
SK = REPO + '/skill/game-hoc-vietwise'
SP = tempfile.mkdtemp()
OUT = SP + '/pkg/Tro-ly-Game-hoc-Vietwise'
os.makedirs(OUT + '/3-Game-mau', exist_ok=True)
os.makedirs(OUT + '/4-Cai-Skill', exist_ok=True)

def b64(p, mime):
    return 'data:%s;base64,%s' % (mime, base64.b64encode(open(p, 'rb').read()).decode())

# Phiên bản Skill: một nguồn là tools/dong-goi/phien-ban.json; các chỗ ghi số phải khớp
PB = json.load(open(H + '/phien-ban.json', encoding='utf-8'))
for p, mau in [(SK + '/SKILL.md', '**Phiên bản Skill: %s (%s).**'), (SK + '/README.md', '**Phiên bản Skill: %s (%s).**'),
               (SK + '/assets/trinh-choi.html', "var SKV='%s';"), (H + '/mau/doc-truoc.html', "var PB='%s'"),
               (H + '/mau/doc-truoc.html', 'bản <b id="pb-nay">%s</b> (%s)')]:
    can = mau % ((PB['so'], PB['ngay']) if mau.count('%s') == 2 else (PB['so'],))
    if can not in open(p, encoding='utf-8').read():
        sys.exit('dong_goi: %s chưa ghi đúng phiên bản (%s). Sửa cho khớp phien-ban.json.' % (os.path.relpath(p, REPO), can))
shutil.copy(H + '/phien-ban.json', REPO + '/phien-ban.json')

# 4: skill zip (để tải lên Claude)
inner = OUT + '/4-Cai-Skill/game-hoc-vietwise.zip'
subprocess.check_call(['zip', '-qr', inner, 'game-hoc-vietwise'], cwd=os.path.dirname(SK))

# 3: game mẫu
games = [
    ('1-Khoa-hoc-tu-nhien-8-On-bai.html', 'on-bai-khtn8-mol-nong-do.json'),
    ('2-Tieng-Anh-7-Doc-ngoai-ngu.html', 'on-bai-tienganh7-nhan-hop-sua.json'),
    ('3-Ngu-van-6-Sach-la-Thay.html', 'sach-la-thay-van6-de-men.json'),
    ('4-Khoa-hoc-tu-nhien-9-Bon-level.html', 'on-bai-khtn9-lipid-carbohydrate-protein-4-level.json'),
]
for out, js in games:
    co_giong = H + '/giong/' + js
    nguon = co_giong if os.path.exists(co_giong) else SK + '/references/vi-du/' + js
    subprocess.check_call(['python3', SK + '/scripts/dung_trang.py', nguon, OUT + '/3-Game-mau/' + out])

# 2: giao diện giao việc
subprocess.check_call(['python3', H + '/dung_giao_viec.py', SP + '/giaoviec.html'])
shutil.copy(SP + '/giaoviec.html', OUT + '/2-Giao-viec-mo-trong-Claude.html')

# 1: README
# 1: Đọc trước + phiếu giao việc (trang tĩnh trong mau/)
shutil.copy(H + '/mau/doc-truoc.html', OUT + '/1-DOC-TRUOC-README-VA-PHIEU-GIAO-VIEC.html')

# Trang đầu trên web (GitHub Pages): index.html, choi-thu/, tai-ve/ ở gốc repo
subprocess.check_call(['python3', H + '/dung_trang_dau.py', OUT])

# zip theo thứ tự
final = sys.argv[1] if len(sys.argv) > 1 else REPO + '/dist/Tro-ly-Game-hoc-Vietwise.zip'
os.makedirs(os.path.dirname(final), exist_ok=True)
if os.path.exists(final): os.remove(final)
names = []
for root, ds, fs in os.walk(OUT):
    for f in fs: names.append(os.path.relpath(os.path.join(root, f), os.path.dirname(OUT)))
names.sort()
with zipfile.ZipFile(final, 'w', zipfile.ZIP_DEFLATED) as z:
    for n in names: z.write(os.path.join(os.path.dirname(OUT), n), n)
print('\n'.join(names)); print(os.path.getsize(final))
