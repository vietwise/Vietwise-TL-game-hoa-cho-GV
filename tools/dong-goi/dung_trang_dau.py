"""Dựng trang đầu trên web (index.html ở gốc repo, chạy bằng GitHub Pages) từ mau/doc-truoc.html.

Trang đầu lưu được ra màn hình chính điện thoại như một app (theo cách của repo thuan-gene-truong-tho):
manifest.webmanifest + icon-192/512 + apple-touch-icon + hướng dẫn iPhone/Android ngay trên trang.

Chạy qua dong_goi.py (tự gọi). Chạy riêng:
    python3 tools/dong-goi/dung_trang_dau.py <thư mục gói đã dựng>
Thư mục gói phải có 3-Game-mau/*.html và 4-Cai-Skill/game-hoc-vietwise.zip.
Ra: index.html, choi-thu/*.html, tai-ve/game-hoc-vietwise.zip ở gốc repo.
"""
import os
import shutil
import sys

H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(H + '/../..')
URL = 'https://vietwise.github.io/Vietwise-TL-game-hoa-cho-GV/'


def thay(s, cu, moi, so=1):
    n = s.count(cu)
    if n != so:
        sys.exit('dung_trang_dau: mong %d chỗ "%s", thấy %d. Mẫu doc-truoc.html đã đổi, sửa script này.' % (so, cu[:60], n))
    return s.replace(cu, moi)


HEAD = '''<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Trợ lý Game-hóa cho Thầy Cô: điền phiếu giao việc, gửi cho Claude kèm ảnh trang sách, nhận về trò chơi chiếu lên lớp. Không thu phí.">
<meta name="theme-color" content="#8a459a">
<meta property="og:title" content="Trợ lý Game-hóa cho Thầy Cô">
<meta property="og:description" content="Skill Game-học của Viện Giáo dục và Quản trị Nhân lực và Vườn Game-học Vietwise. Không thu phí, không thi đua, không chấm điểm.">
<meta property="og:image" content="''' + URL + '''icon-512.png">
<link rel="icon" type="image/png" sizes="64x64" href="favicon-64.png">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="manifest.webmanifest">
<meta name="apple-mobile-web-app-title" content="Game-học">
<meta name="application-name" content="Game-học">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">'''

CSS = '''
/* Trang đầu trên web: lưu ra màn hình chính */
:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
[hidden]{display:none!important}
.mhc-bar{display:none;align-items:center;justify-content:space-between;gap:10px;background:#fbeef9;border-bottom:1px solid #e9c9e4;padding:10px 16px;font-weight:700;color:var(--tim);font-size:14.5px}
.mhc-bar img{width:34px;height:34px;border-radius:9px;flex:0 0 auto}
.mhc-bar span{flex:1;min-width:0}
.mhc-bar .btn{padding:8px 16px;font-size:14px;white-space:nowrap}
@media(max-width:820px){.mhc-bar{display:flex}}
@media(display-mode:standalone){.mhc-bar{display:none!important}}
.mhc{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-top:12px}
.mhc .card{margin:0;padding:16px}
.mhc ol{margin:0;padding-left:20px}
.mhc .k{font-weight:800;color:var(--hong)}
.mhc-head{display:flex;gap:14px;align-items:center}
.mhc-head img{width:72px;height:72px;border-radius:18px;box-shadow:0 0 0 3px #ecc459,0 6px 16px rgba(0,0,0,.18);flex:0 0 auto}
.mhc-ok{display:none}
@media(display-mode:standalone){.mhc-ok{display:block}.mhc-huongdan{display:none}}
'''

BAR = '''<div class="mhc-bar" id="mhc-bar"><img src="icon-192.png" alt="" width="34" height="34"><span>Lưu trang này thành app trên màn hình điện thoại</span><button class="btn" type="button" id="mhc-xem">Cách lưu</button></div>
'''

THE = '''
<!-- ===== ĐẶT RA MÀN HÌNH CHÍNH ===== -->
<section class="card" id="man-hinh-chinh" aria-labelledby="h-mhc">
  <div class="mhc-head">
    <img src="icon-512.png" alt="Biểu tượng Game-học: chú Não vẫy tay" width="72" height="72">
    <div>
      <h2 id="h-mhc">Đặt ra màn hình chính điện thoại</h2>
      <p class="lead" style="margin:0">Lưu trang này một lần, từ đó chạm biểu tượng <b>Game-học</b> là mở ngay, như một app.</p>
    </div>
  </div>
  <p class="mhc-ok ok" style="margin-top:12px">Thầy Cô đang mở trang từ màn hình chính. Đã lưu xong.</p>
  <div class="mhc-huongdan">
    <div class="btns" id="mhc-cai-wrap" hidden><button class="btn" type="button" id="mhc-cai">Cài app Game-học</button></div>
    <div class="mhc">
      <div class="card">
        <h3>iPhone, iPad (Safari)</h3>
        <ol>
          <li>Mở trang này bằng <b>Safari</b> (không mở trong Zalo, Messenger hay app Claude).</li>
          <li>Chạm nút <span class="k">Chia sẻ</span> (ô vuông có mũi tên lên).</li>
          <li>Chọn <span class="k">Thêm vào MH chính</span>. Kiểm tra tên là <b>Game-học</b>, hình là chú Não, rồi chạm <b>Thêm</b>.</li>
        </ol>
      </div>
      <div class="card">
        <h3>Android (Chrome)</h3>
        <ol>
          <li>Mở trang này bằng <b>Chrome</b>.</li>
          <li>Chạm <span class="k">⋮</span> ở góc trên bên phải.</li>
          <li>Chọn <span class="k">Thêm vào màn hình chính</span> (hoặc <b>Cài đặt ứng dụng</b>), chạm <b>Thêm</b>.</li>
        </ol>
      </div>
    </div>
    <p class="lead" style="margin:12px 0 0;font-size:14.5px">Địa chỉ trang: <a href="''' + URL + '''">''' + URL.replace('https://', '') + '''</a>. Gửi địa chỉ này cho đồng nghiệp để cùng dùng.</p>
  </div>
  <div class="btns">
    <a class="btn ghost" href="dist/Tro-ly-Game-hoa-Vietwise.zip" download>Tải cả gói về máy tính (.zip)</a>
  </div>
</section>
'''

JS = '''
<script>
(function(){
  var bar=document.getElementById('mhc-bar'),the=document.getElementById('man-hinh-chinh');
  document.getElementById('mhc-xem').addEventListener('click',function(){the.scrollIntoView({behavior:'smooth',block:'start'})});
  var standalone=(window.matchMedia&&matchMedia('(display-mode: standalone)').matches)||navigator.standalone===true;
  if(standalone&&bar)bar.hidden=true;
  // Android Chrome: nút cài app khi trình duyệt cho phép
  var hoan=null,wrap=document.getElementById('mhc-cai-wrap');
  window.addEventListener('beforeinstallprompt',function(e){e.preventDefault();hoan=e;wrap.hidden=false});
  document.getElementById('mhc-cai').addEventListener('click',function(){
    if(!hoan)return;hoan.prompt();hoan.userChoice.then(function(){hoan=null;wrap.hidden=true});
  });
  window.addEventListener('appinstalled',function(){wrap.hidden=true;if(bar)bar.hidden=true});
})();
</script>
'''


def dung(goi):
    s = open(H + '/mau/doc-truoc.html', encoding='utf-8').read()
    s = thay(s, '<meta name="viewport" content="width=device-width, initial-scale=1">', HEAD)
    s = thay(s, '<title>Trợ lý Game-hoá: Phiếu giao việc cho Thầy Cô</title>', '<title>Trợ lý Game-hóa cho Thầy Cô</title>')
    s = thay(s, '</style>\n</head>', CSS + '</style>\n</head>')
    s = thay(s, '\n<header>', '\n' + BAR + '<header>')
    s = thay(s, '<span class="nobreak"><b>4-Cai-Skill/game-hoc-vietwise.zip</b></span> trong gói này.',
             '<a class="nobreak" href="tai-ve/game-hoc-vietwise.zip" download><b>game-hoc-vietwise.zip</b></a> (bấm để tải về máy).')
    s = thay(s, 'Mỗi loại một game, nằm trong thư mục <b>3-Game-mau</b> của gói này. Bấm để mở trong tab mới (mở bằng trình duyệt, không cần mạng), rồi',
             'Mỗi loại một game. Bấm để mở trong tab mới, rồi')
    s = thay(s, 'href="3-Game-mau/', 'href="choi-thu/', 3)
    s = thay(s, '\n</main>', THE + '\n</main>')
    s = thay(s, '</body>', JS + '</body>')
    open(REPO + '/index.html', 'w', encoding='utf-8').write(s)

    if os.path.isdir(REPO + '/choi-thu'):
        shutil.rmtree(REPO + '/choi-thu')
    shutil.copytree(goi + '/3-Game-mau', REPO + '/choi-thu')
    os.makedirs(REPO + '/tai-ve', exist_ok=True)
    shutil.copy(goi + '/4-Cai-Skill/game-hoc-vietwise.zip', REPO + '/tai-ve/game-hoc-vietwise.zip')
    print('dung_trang_dau: index.html, choi-thu/, tai-ve/')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    dung(sys.argv[1])
