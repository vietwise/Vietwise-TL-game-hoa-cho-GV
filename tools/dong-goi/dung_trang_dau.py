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
<meta name="description" content="Trợ lý Game-học cho Thầy Cô: điền phiếu giao việc, gửi cho Claude kèm ảnh trang sách, nhận về trò chơi chiếu lên lớp. Không thu phí.">
<meta name="theme-color" content="#1530D0">
<meta property="og:title" content="Trợ lý Game-học cho Thầy Cô">
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
.mhc-bar{display:none;align-items:center;justify-content:space-between;gap:10px;background:#FFEFE5;border-bottom:1px solid #F8C4A6;padding:10px 16px;font-weight:700;color:var(--blue);font-size:14.5px}
.mhc-bar img{width:34px;height:34px;border-radius:9px;flex:0 0 auto}
.mhc-bar span{flex:1;min-width:0}
.mhc-bar .btn{padding:8px 16px;font-size:14px;white-space:nowrap}
@media(max-width:820px){.mhc-bar{display:flex}}
@media(display-mode:standalone){.mhc-bar{display:none!important}}
.mhc{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-top:12px}
.mhc .card{margin:0;padding:16px}
.mhc ol{margin:0;padding-left:20px}
.mhc .k{font-weight:800;color:var(--cam)}
.mhc-head{display:flex;gap:14px;align-items:center}
.mhc-head img{width:72px;height:72px;border-radius:18px;box-shadow:0 0 0 3px #F7C52A,0 6px 16px rgba(0,0,0,.18);flex:0 0 auto}
.mhc-ok{display:none}
@media(display-mode:standalone){.mhc-ok{display:block}.mhc-huongdan{display:none}}
/* Flow hướng dẫn */
.flow{list-style:none;margin:14px 0 4px;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:22px 26px}
.flow li{position:relative;border-radius:14px;padding:12px 12px 12px 12px;font-size:14.5px;line-height:1.45;border:1.5px solid;min-width:0}
.flow li b{display:block;font-size:15px;margin-bottom:2px}
.flow li .n{display:inline-grid;place-items:center;width:26px;height:26px;border-radius:50%;font-weight:800;font-size:14px;margin-bottom:6px;color:#fff}
.flow .gv{background:#FEF6D9;border-color:#F7C52A}.flow .gv .n{background:#B8860B}
.flow .cl{background:#EAF5E2;border-color:#A9D68C}.flow .cl .n{background:var(--xanh)}
.flow .lop{background:#FFEFE5;border-color:#F8C4A6}.flow .lop .n{background:var(--cam)}
.flow li:not(:last-child)::after{content:"→";position:absolute;right:-22px;top:50%;transform:translateY(-50%);font-weight:800;color:var(--blue);font-size:18px}
.flow li:nth-child(3n)::after{content:none}
@media(max-width:620px){.flow{grid-template-columns:1fr;gap:26px}.flow li:not(:last-child)::after,.flow li:nth-child(3n):not(:last-child)::after{content:"↓";right:auto;left:50%;top:auto;bottom:-25px;transform:translateX(-50%)}}
.flow-chu{display:flex;gap:14px;flex-wrap:wrap;font-size:13.5px;color:var(--mut);margin:8px 0 0}
.flow-chu span::before{content:"";display:inline-block;width:12px;height:12px;border-radius:4px;margin-right:6px;vertical-align:-1px;border:1.5px solid}
.flow-chu .gv::before{background:#FEF6D9;border-color:#F7C52A}.flow-chu .cl::before{background:#EAF5E2;border-color:#A9D68C}.flow-chu .lop::before{background:#FFEFE5;border-color:#F8C4A6}
/* Trả kết quả */
.kq-list{list-style:none;padding:0;margin:14px 0 0;display:grid;gap:10px}
.kq-list li{display:flex;gap:10px;align-items:center;flex-wrap:wrap;background:#fff;border:1px solid var(--line);border-radius:14px;padding:10px 12px}
.kq-list .ten{flex:1 1 180px;min-width:0;font-weight:700;color:var(--blue);overflow-wrap:anywhere}
.kq-list .ten small{display:block;font-weight:400;color:var(--mut);font-size:12.5px}
.kq-list .btn{padding:8px 16px;font-size:14px;text-decoration:none}
.kq-rong{color:var(--mut);font-style:italic;margin:12px 0 0}
'''

FLOW = '''<ol class="flow" aria-label="Các bước dùng app Game-học">
  <li class="gv"><span class="n">1</span><b>Lưu app</b>Mở trang này, chạm Chia sẻ (iPhone) hoặc ⋮ (Android), chọn Thêm vào màn hình chính.</li>
  <li class="gv"><span class="n">2</span><b>Phiếu giao việc</b>Chạm biểu tượng Game-học, điền phiếu ở thẻ 1, bấm sao chép.</li>
  <li class="gv"><span class="n">3</span><b>Gửi cho Claude</b>Dán phiếu vào Claude (đã bật Skill), đính kèm ảnh trang sách.</li>
  <li class="cl"><span class="n">4</span><b>Claude trả kết quả</b>Trợ lý soạn game, trả về link trang chơi. Thầy Cô xem lại, nhờ sửa nếu cần.</li>
  <li class="gv"><span class="n">5</span><b>Lưu link game</b>Dán link vào thẻ 4. Trả kết quả để giữ trên máy.</li>
  <li class="lop"><span class="n">6</span><b>Chơi trên lớp</b>Chạm Mở game, chiếu lên màn hình. Phím mũi tên sang bước, phím G cho Thầy Cô.</li>
</ol>
<p class="flow-chu"><span class="gv">Việc của Thầy Cô</span><span class="cl">Việc của Claude</span><span class="lop">Cả lớp</span></p>'''

BAR = '''<div class="mhc-bar" id="mhc-bar"><img src="icon-192.png" alt="" width="34" height="34"><span>Lưu trang này thành app trên màn hình điện thoại</span><button class="btn" type="button" id="mhc-xem">Cách lưu</button></div>
'''

THE = '''
<!-- ===== ĐẶT RA MÀN HÌNH CHÍNH ===== -->
<section class="card" id="man-hinh-chinh" aria-labelledby="h-mhc">
  <div class="mhc-head">
    <img src="icon-512.png" alt="Biểu tượng Game-học: chú Não đeo huy chương Bền chí" width="72" height="72">
    <div>
      <h2 id="h-mhc">Đặt ra màn hình chính điện thoại</h2>
      <p class="lead" style="margin:0">Lưu trang này một lần, từ đó chạm biểu tượng <b>Game-học</b> là mở ngay, như một app.</p>
    </div>
  </div>
  <h3 style="margin-top:16px">Flow hướng dẫn: từ màn hình chính đến lớp học</h3>
''' + FLOW + '''
  <p class="mhc-ok ok" style="margin-top:12px">Thầy Cô đang mở trang từ màn hình chính. Đã lưu xong.</p>
  <div class="mhc-huongdan">
    <div class="btns" id="mhc-cai-wrap" hidden><button class="btn" type="button" id="mhc-cai">Cài app Game-học</button></div>
    <div class="mhc">
      <div class="card">
        <h3>iPhone, iPad (Safari)</h3>
        <ol>
          <li>Mở trang này bằng <b>Safari</b> (không mở trong Zalo, Messenger hay app Claude).</li>
          <li>Chạm nút <span class="k">Chia sẻ</span> (ô vuông có mũi tên lên).</li>
          <li>Chọn <span class="k">Thêm vào MH chính</span>. Kiểm tra tên là <b>Game-học</b>, hình là chú Não đeo huy chương Bền chí, rồi chạm <b>Thêm</b>.</li>
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
    <a class="btn ghost" href="dist/Tro-ly-Game-hoc-Vietwise.zip" download>Tải cả gói về máy tính (.zip)</a>
  </div>
</section>
'''

TAB = '''
<!-- ===== TRẢ KẾT QUẢ ===== -->
<section class="panel" id="p-tra-ket-qua" role="tabpanel" aria-labelledby="t-tra-ket-qua">
  <div class="card">
    <h2>Trả kết quả: game của Thầy Cô</h2>
    <p class="lead">Claude soạn xong sẽ trả về link trang chơi (dạng <b>claude.ai/…</b>). Dán link vào đây để lưu trên máy này. Lúc lên lớp, mở app Game-học, vào thẻ này, chạm <b>Mở game</b>.</p>
    <form id="kq-form" novalidate>
      <label for="kq-link">Link game Claude trả về</label>
      <input type="text" id="kq-link" inputmode="url" autocomplete="off" placeholder="https://claude.ai/…">
      <label for="kq-ten">Tên game <small>(không bắt buộc, ví dụ: KHTN 8, bài Nồng độ dung dịch)</small></label>
      <input type="text" id="kq-ten" autocomplete="off">
      <div class="err" id="kq-err" aria-live="polite"></div>
      <div class="btns"><button class="btn" type="submit">Lưu game</button></div>
    </form>
    <ul class="kq-list" id="kq-list"></ul>
    <p class="kq-rong" id="kq-rong">Chưa có game nào. Giao việc cho Claude ở thẻ 1, rồi dán link Claude trả về vào đây.</p>
    <p class="lead" style="font-size:14px;margin:14px 0 0">Link chỉ lưu trên máy này, không gửi đi đâu. Lần đầu mở, Claude có thể hỏi đăng nhập một lần trong Safari hoặc Chrome.</p>
  </div>
  <div class="card">
    <h3>Flow hướng dẫn</h3>
    ''' + FLOW + '''
  </div>
</section>
'''

JS = r'''
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
  // Trả kết quả: danh sách link game lưu trên máy
  var KEY='gamehoc-ket-qua',ds=[];
  try{ds=JSON.parse(localStorage.getItem(KEY)||'[]')||[]}catch(e){ds=[]}
  function luu(){try{localStorage.setItem(KEY,JSON.stringify(ds))}catch(e){}}
  var list=document.getElementById('kq-list'),rong=document.getElementById('kq-rong');
  function ve(){
    list.innerHTML='';rong.hidden=ds.length>0;
    ds.forEach(function(g,i){
      var li=document.createElement('li');
      var t=document.createElement('span');t.className='ten';t.textContent=g.ten||'Game '+(i+1);
      var sm=document.createElement('small');sm.textContent=g.ngay+' · '+g.url.replace(/^https?:\/\//,'');t.appendChild(sm);
      var a=document.createElement('a');a.className='btn';a.href=g.url;a.target='_blank';a.rel='noopener';a.textContent='Mở game';
      var x=document.createElement('button');x.type='button';x.className='btn ghost';x.textContent='Xoá';
      x.addEventListener('click',function(){if(confirm('Xoá "'+(g.ten||'game này')+'" khỏi danh sách?')){ds.splice(i,1);luu();ve()}});
      li.appendChild(t);li.appendChild(a);li.appendChild(x);list.appendChild(li);
    });
  }
  document.getElementById('kq-form').addEventListener('submit',function(e){
    e.preventDefault();
    var v=document.getElementById('kq-link').value.trim(),err=document.getElementById('kq-err');
    var m=v.match(/https:\/\/[^\s"'<>]+/);
    if(!m){err.textContent='Link chưa đúng. Link game bắt đầu bằng https:// (thường là https://claude.ai/…).';return}
    err.textContent='';
    var d=new Date(),ngay=('0'+d.getDate()).slice(-2)+'/'+('0'+(d.getMonth()+1)).slice(-2)+'/'+d.getFullYear();
    ds.unshift({url:m[0],ten:document.getElementById('kq-ten').value.trim(),ngay:ngay});luu();ve();
    document.getElementById('kq-link').value='';document.getElementById('kq-ten').value='';
  });
  ve();
})();
</script>
'''


def dung(goi):
    s = open(H + '/mau/doc-truoc.html', encoding='utf-8').read()
    s = thay(s, '<meta name="viewport" content="width=device-width, initial-scale=1">', HEAD)
    s = thay(s, '<title>Trợ lý Game-học: Phiếu giao việc cho Thầy Cô</title>', '<title>Trợ lý Game-học cho Thầy Cô</title>')
    s = thay(s, '</style>\n</head>', CSS + '</style>\n</head>')
    s = thay(s, '\n<header>', '\n' + BAR + '<header>')
    s = thay(s, '<span class="nobreak"><b>4-Cai-Skill/game-hoc-vietwise.zip</b></span> trong gói này.',
             '<a class="nobreak" href="tai-ve/game-hoc-vietwise.zip" download><b>game-hoc-vietwise.zip</b></a> (bấm để tải về máy).')
    s = thay(s, 'Mỗi loại một game, nằm trong thư mục <b>3-Game-mau</b> của gói này. Bấm để mở trong tab mới (mở bằng trình duyệt, không cần mạng), rồi',
             'Mỗi loại một game. Bấm để mở trong tab mới, rồi')
    s = thay(s, 'href="3-Game-mau/', 'href="choi-thu/', 3)
    s = thay(s, '<button role="tab" id="t-tham-khao" data-tab="tham-khao" aria-selected="false">3. Tham khảo</button>',
             '<button role="tab" id="t-tham-khao" data-tab="tham-khao" aria-selected="false">3. Tham khảo</button>\n      <button role="tab" id="t-tra-ket-qua" data-tab="tra-ket-qua" aria-selected="false">4. Trả kết quả</button>')
    s = thay(s, "var tabs=['phieu','readme','tham-khao'];", "var tabs=['phieu','readme','tham-khao','tra-ket-qua'];")
    s = thay(s, 'Thầy Cô xem lại, nói muốn sửa gì thì trợ lý sửa nội dung.</li>',
             'Thầy Cô xem lại, nói muốn sửa gì thì trợ lý sửa nội dung. Dán link game vào thẻ <a href="#tra-ket-qua">4. Trả kết quả</a> để lưu lại.</li>')
    s = thay(s, '\n</main>', TAB + THE + '\n</main>')
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
