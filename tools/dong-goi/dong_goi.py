import sys, os, base64, shutil, subprocess, zipfile, html
import tempfile
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(H + '/../..')
SK = REPO + '/skill/game-hoc-vietwise'
SP = tempfile.mkdtemp()
OUT = SP + '/pkg/Tro-ly-Game-hoa-Vietwise'
os.makedirs(OUT + '/3-Game-mau', exist_ok=True)
os.makedirs(OUT + '/4-Cai-Skill', exist_ok=True)

def b64(p, mime):
    return 'data:%s;base64,%s' % (mime, base64.b64encode(open(p, 'rb').read()).decode())

# 4: skill zip (để tải lên Claude)
inner = OUT + '/4-Cai-Skill/game-hoc-vietwise.zip'
subprocess.check_call(['zip', '-qr', inner, 'game-hoc-vietwise'], cwd=os.path.dirname(SK))

# 3: game mẫu
games = [
    ('1-Khoa-hoc-tu-nhien-8-On-bai.html', 'on-bai-khtn8-mol-nong-do.json'),
    ('2-Tieng-Anh-7-Doc-ngoai-ngu.html', 'on-bai-tienganh7-nhan-hop-sua.json'),
    ('3-Ngu-van-6-Sach-la-Thay.html', 'sach-la-thay-van6-de-men.json'),
]
for out, js in games:
    subprocess.check_call(['python3', SK + '/scripts/dung_trang.py', SK + '/references/vi-du/' + js, OUT + '/3-Game-mau/' + out])

# 2: giao diện giao việc
subprocess.check_call(['python3', H + '/dung_giao_viec.py', SP + '/giaoviec.html'])
shutil.copy(SP + '/giaoviec.html', OUT + '/2-Giao-viec-mo-trong-Claude.html')

# 1: README
# 1: Đọc trước + phiếu giao việc (trang tĩnh trong mau/)
shutil.copy(H + '/mau/doc-truoc.html', OUT + '/1-DOC-TRUOC-README-VA-PHIEU-GIAO-VIEC.html')

# zip theo thứ tự
final = sys.argv[1] if len(sys.argv) > 1 else REPO + '/dist/Tro-ly-Game-hoa-Vietwise.zip'
os.makedirs(os.path.dirname(final), exist_ok=True)
if os.path.exists(final): os.remove(final)
names = []
for root, ds, fs in os.walk(OUT):
    for f in fs: names.append(os.path.relpath(os.path.join(root, f), os.path.dirname(OUT)))
names.sort()
with zipfile.ZipFile(final, 'w', zipfile.ZIP_DEFLATED) as z:
    for n in names: z.write(os.path.join(os.path.dirname(OUT), n), n)
print('\n'.join(names)); print(os.path.getsize(final))
