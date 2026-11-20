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


def anh_rong():
    import base64
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mau', 'anh', 'trong-chua-co-game.webp')
    if not os.path.exists(p):
        return ''
    return ('<img src="data:image/webp;base64,%s" alt="" style="display:block;width:160px;height:auto;margin:0 0 8px">'
            % base64.b64encode(open(p, 'rb').read()).decode())

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
<meta name="apple-mobile-web-app-title" content="Trợ lý Game-học">
<meta name="application-name" content="Trợ lý Game-học">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">'''

CSS = '''
body:not([data-tab=readme]) #man-hinh-chinh{display:none}
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
.luu-cach{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin:12px 0 4px}
.luu-cach div{background:#FEF6D9;border:1.5px solid #F7C52A;border-radius:14px;padding:12px;font-size:14.5px;line-height:1.45}
.luu-cach strong{display:block;color:var(--blue);font-size:15px;margin-bottom:2px}
.tep-chon{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:10px}
.tep-chon input[type=file]{position:absolute;width:1px;height:1px;opacity:0}
.kq-list .loai{display:inline-block;font-size:12px;font-weight:700;border-radius:999px;padding:1px 8px;margin-right:6px;background:#EAF5E2;color:#2F6B12}
.kq-list .loai.lk{background:#E8ECFF;color:var(--blue)}
#xem-game{position:fixed;inset:0;z-index:9999;background:#000;display:flex;flex-direction:column}
#xem-game[hidden]{display:none!important}
#xem-game .thanh{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:8px 12px;padding-top:calc(8px + env(safe-area-inset-top,0px));background:#1530D0;color:#fff;font-weight:700}
#xem-game .thanh span{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#xem-game iframe{flex:1;width:100%;border:0;background:#fff}
'''

FLOW = '''<ol class="flow" aria-label="Các bước dùng app Game-học">
  <li class="gv"><span class="n">1</span><b>Lưu app</b>Mở trang này, chạm Chia sẻ (iPhone) hoặc ⋮ (Android), chọn Thêm vào màn hình chính.</li>
  <li class="gv"><span class="n">2</span><b>Phiếu giao việc</b>Chạm biểu tượng Game-học, điền phiếu ở thẻ Giao việc, bấm sao chép.</li>
  <li class="gv"><span class="n">3</span><b>Gửi cho Claude</b>Dán phiếu vào Claude (đã bật Skill), đính kèm ảnh trang sách.</li>
  <li class="cl"><span class="n">4</span><b>Claude trả kết quả</b>Trợ lý soạn game, trả về link trang chơi. Thầy Cô xem lại, nhờ sửa nếu cần.</li>
  <li class="gv"><span class="n">5</span><b>Lưu game</b>Tải tệp game .html từ Claude (hoặc lấy link), đưa vào thẻ Game của tôi để giữ trên máy.</li>
  <li class="lop"><span class="n">6</span><b>Chơi trên lớp</b>Chạm Mở game, chiếu lên màn hình. Phím mũi tên sang bước, phím G cho Thầy Cô.</li>
</ol>
<p class="flow-chu"><span class="gv">Việc của Thầy Cô</span><span class="cl">Việc của Claude</span><span class="lop">Cả lớp</span></p>'''

BAR = '''<div class="mhc-bar" id="mhc-bar"><img src="icon-192.png" alt="" width="34" height="34"><span>Lưu trang này thành app trên màn hình điện thoại</span><button class="btn" type="button" id="mhc-xem">Cách lưu</button></div>
'''

THE = '''
<!-- ===== ĐẶT RA MÀN HÌNH CHÍNH ===== -->
<section class="card" id="man-hinh-chinh" aria-labelledby="h-mhc">
  <div class="mhc-head">
    <img src="icon-512.png" alt="Biểu tượng Trợ lý Game-học: cuốn sách mở có mầm xanh" width="72" height="72">
    <div>
      <h2 id="h-mhc">Đặt ra màn hình chính điện thoại</h2>
      <p class="lead" style="margin:0">Lưu trang này một lần, từ đó chạm biểu tượng <b>Trợ lý Game-học</b> là mở ngay, như một app.</p>
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
          <li>Chọn <span class="k">Thêm vào MH chính</span>. Kiểm tra tên là <b>Trợ lý Game-học</b>, hình là cuốn sách mở có mầm xanh, rồi chạm <b>Thêm</b>.</li>
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
    <a class="btn ghost" href="https://drive.google.com/file/d/1lxmNKys-VrcU8QX3Ql1B2KfUMWMr5y1c/view?usp=sharing" target="_blank" rel="noopener">Tải cả gói về máy tính (.zip, Google Drive)</a>
  </div>
</section>
'''

TAB = '''
<!-- ===== GAME CỦA TÔI ===== -->
<section class="panel" id="p-tra-ket-qua" role="tabpanel" aria-labelledby="t-tra-ket-qua">
  <div class="card">
    <h2>Game của tôi</h2>
    <p class="lead">Claude soạn xong sẽ trả về trang game. Thầy Cô lưu game theo một trong hai cách dưới đây (làm cả hai càng chắc). Lúc lên lớp, mở app, vào thẻ này, chạm <b>Mở game</b>.</p>
    <div class="luu-cach">
      <div><strong>📥 Cách 1: Lưu tệp game (nên dùng)</strong>Trong Claude, chạm vào game, bấm nút <b>Tải xuống</b> (biểu tượng ⤓ hoặc ⋯ rồi Download). Máy lưu một tệp <b>.html</b>. Quay lại đây, bấm <b>Chọn tệp game</b>. Game nằm luôn trong app, mở được cả khi không có mạng.</div>
      <div><strong>🔗 Cách 2: Lưu link game</strong>Trong Claude, bấm <b>Chia sẻ</b> (Publish/Share) để có link công khai, bấm sao chép, rồi dán link vào ô bên dưới. Mở bằng link thì cần có mạng.</div>
    </div>

    <h3 style="margin-top:16px">📥 Lưu tệp game</h3>
    <div class="tep-chon">
      <label class="btn" for="tep-game" style="cursor:pointer">Chọn tệp game (.html)</label>
      <input type="file" id="tep-game" accept=".html,.htm,text/html" multiple>
      <small style="color:var(--mut)">Tệp thường nằm trong thư mục Tải về (Downloads) hoặc app Tệp trên iPhone.</small>
    </div>
    <div class="err" id="tep-err" aria-live="polite"></div>

    <h3 style="margin-top:16px">🔗 Lưu link game</h3>
    <form id="kq-form" novalidate>
      <label for="kq-link">Link game Claude trả về</label>
      <input type="text" id="kq-link" inputmode="url" autocomplete="off" placeholder="https://claude.ai/…">
      <label for="kq-ten">Tên game <small>(không bắt buộc, ví dụ: KHTN 8, bài Nồng độ dung dịch)</small></label>
      <input type="text" id="kq-ten" autocomplete="off">
      <div class="err" id="kq-err" aria-live="polite"></div>
      <div class="btns"><button class="btn" type="submit">Lưu link</button></div>
    </form>

    <h3 style="margin-top:18px">🎮 Danh sách game đã lưu</h3>
    <ul class="kq-list" id="kq-list"></ul>
    <p class="kq-rong" id="kq-rong">''' + anh_rong() + '''Chưa có game nào. Giao việc cho Claude ở thẻ Giao việc, rồi lưu game Claude trả về vào đây.</p>
    <p class="lead" style="font-size:14px;margin:14px 0 0">Game và link chỉ lưu trên máy này, không gửi đi đâu. Đổi máy hoặc xoá dữ liệu trình duyệt thì danh sách mất, nên Thầy Cô giữ thêm tệp .html trong thư mục Tải về hoặc Google Drive của mình.</p>
    <details class="them" style="margin-top:10px"><summary>Lỡ quên lưu? Tìm lại game trong Claude</summary>
      <ul>
        <li>Mở Claude, xem danh sách <b>cuộc trò chuyện</b> (biểu tượng ☰). Mở lại cuộc trò chuyện đã giao việc, game vẫn nằm ở đó.</li>
        <li>Trên máy tính, mục <b>Artifacts</b> ở thanh bên trái của claude.ai liệt kê mọi trang Claude đã tạo.</li>
        <li>Mở được game rồi thì tải tệp hoặc lấy link như hai cách bên trên.</li>
      </ul>
    </details>
  </div>
</section>
<div id="xem-game" hidden role="dialog" aria-modal="true" aria-label="Đang chơi game"><div class="thanh"><span id="xem-ten"></span><button class="btn" type="button" id="xem-dong" style="padding:6px 14px;font-size:14px">✕ Đóng</button></div><iframe id="xem-khung" title="Game" allow="autoplay; fullscreen"></iframe></div>
'''

JS = r'''
<script>
(function(){
  var bar=document.getElementById('mhc-bar'),the=document.getElementById('man-hinh-chinh');
  document.getElementById('mhc-xem').addEventListener('click',function(){var r=document.getElementById('t-readme');if(r)r.click();setTimeout(function(){the.scrollIntoView({behavior:'smooth',block:'start'})},60)});
  var standalone=(window.matchMedia&&matchMedia('(display-mode: standalone)').matches)||navigator.standalone===true;
  if(standalone&&bar)bar.hidden=true;
  // Android Chrome: nút cài app khi trình duyệt cho phép
  var hoan=null,wrap=document.getElementById('mhc-cai-wrap');
  window.addEventListener('beforeinstallprompt',function(e){e.preventDefault();hoan=e;wrap.hidden=false});
  document.getElementById('mhc-cai').addEventListener('click',function(){
    if(!hoan)return;hoan.prompt();hoan.userChoice.then(function(){hoan=null;wrap.hidden=true});
  });
  window.addEventListener('appinstalled',function(){wrap.hidden=true;if(bar)bar.hidden=true});
  // Game của tôi: link (localStorage) và tệp game (IndexedDB) lưu trên máy
  var KEY='gamehoc-ket-qua',ds=[];
  try{ds=JSON.parse(localStorage.getItem(KEY)||'[]')||[]}catch(e){ds=[]}
  function luu(){try{localStorage.setItem(KEY,JSON.stringify(ds))}catch(e){}}
  var tep=[],db=null;
  function moDb(cb){
    if(db)return cb(db);
    try{var rq=indexedDB.open('gamehoc-tep',1);
      rq.onupgradeneeded=function(){rq.result.createObjectStore('game',{keyPath:'id'})};
      rq.onsuccess=function(){db=rq.result;cb(db)};rq.onerror=function(){cb(null)};
    }catch(e){cb(null)}
  }
  function giaoDich(kieu,lam,xong){moDb(function(d){if(!d){xong&&xong(null);return}
    try{var tx=d.transaction('game',kieu),st=tx.objectStore('game'),kq=lam(st);
      tx.oncomplete=function(){xong&&xong(kq&&kq.result!==undefined?kq.result:true)};tx.onerror=function(){xong&&xong(null)};
    }catch(e){xong&&xong(null)}})}
  function napTep(cb){giaoDich('readonly',function(st){return st.getAll()},function(r){tep=(r||[]).map(function(g){return{id:g.id,ten:g.ten,ngay:g.ngay,co:g.co}});tep.sort(function(x,y){return y.id-x.id});cb&&cb()})}
  function homNay(){var d=new Date();return('0'+d.getDate()).slice(-2)+'/'+('0'+(d.getMonth()+1)).slice(-2)+'/'+d.getFullYear()}
  var list=document.getElementById('kq-list'),rong=document.getElementById('kq-rong');
  var hop=document.getElementById('xem-game'),khung=document.getElementById('xem-khung'),urlXem=null;
  function dongXem(){hop.hidden=true;khung.removeAttribute('src');if(urlXem){URL.revokeObjectURL(urlXem);urlXem=null}document.body.style.overflow=''}
  document.getElementById('xem-dong').addEventListener('click',dongXem);
  function moTep(g){giaoDich('readonly',function(st){return st.get(g.id)},function(r){
    if(!r||!r.html){alert('Không mở được tệp này. Thầy Cô chọn lại tệp game nhé.');return}
    urlXem=URL.createObjectURL(new Blob([r.html],{type:'text/html'}));
    document.getElementById('xem-ten').textContent=r.ten;khung.src=urlXem;hop.hidden=false;document.body.style.overflow='hidden';
    setTimeout(function(){try{khung.focus()}catch(e){}},300);
  })}
  function taiTep(g){giaoDich('readonly',function(st){return st.get(g.id)},function(r){if(!r)return;
    var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([r.html],{type:'text/html'}));a.download=(r.ten||'game').replace(/[\\/:*?"<>|]+/g,' ').trim()+'.html';document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove()},1500)})}
  function nut(chu,ghost,fn){var x=document.createElement('button');x.type='button';x.className='btn'+(ghost?' ghost':'');x.textContent=chu;x.addEventListener('click',fn);return x}
  function dong(ten,loai,phu){var li=document.createElement('li');var t=document.createElement('span');t.className='ten';
    var l=document.createElement('span');l.className='loai'+(loai==='Link'?' lk':'');l.textContent=loai;t.appendChild(l);t.appendChild(document.createTextNode(ten));
    var sm=document.createElement('small');sm.textContent=phu;t.appendChild(sm);li.appendChild(t);return li}
  function ve(){
    list.innerHTML='';rong.hidden=(ds.length+tep.length)>0;
    tep.forEach(function(g){
      var li=dong(g.ten,'Tệp',g.ngay+' · mở được khi không có mạng');
      li.appendChild(nut('Mở game',false,function(){moTep(g)}));
      li.appendChild(nut('Tải về',true,function(){taiTep(g)}));
      li.appendChild(nut('Xoá',true,function(){if(confirm('Xoá "'+g.ten+'" khỏi app?')){giaoDich('readwrite',function(st){return st.delete(g.id)},function(){napTep(ve)})}}));
      list.appendChild(li);
    });
    ds.forEach(function(g,i){
      var li=dong(g.ten||'Game '+(i+1),'Link',g.ngay+' · '+g.url.replace(/^https?:\/\//,''));
      var a=document.createElement('a');a.className='btn';a.href=g.url;a.target='_blank';a.rel='noopener';a.textContent='Mở game';li.appendChild(a);
      li.appendChild(nut('Xoá',true,function(){if(confirm('Xoá "'+(g.ten||'game này')+'" khỏi danh sách?')){ds.splice(i,1);luu();ve()}}));
      list.appendChild(li);
    });
  }
  function tenTuHtml(h,tenTep){var j=h.match(/"tieu_de"\s*:\s*"((?:[^"\\]|\\.){1,200})"/);if(j){try{return JSON.parse('"'+j[1]+'"')}catch(e){}}
    var m=h.match(/<title[^>]*>([^<]{1,160})<\/title>/i);var t=m?m[1].replace(/\s+/g,' ').trim():'';if(/^Game-học Vietwise$/i.test(t))t='';
    t=t.replace(/&amp;/g,'&').replace(/&#39;|&apos;/g,"'").replace(/&quot;/g,'"');return t||tenTep.replace(/\.html?$/i,'')}
  document.getElementById('tep-game').addEventListener('change',function(e){
    var fs=[].slice.call(e.target.files||[]),err=document.getElementById('tep-err');err.textContent='';
    if(!fs.length)return;
    var con=fs.length;
    fs.forEach(function(f,k){
      if(!/\.html?$/i.test(f.name)&&f.type!=='text/html'){err.textContent='Tệp "'+f.name+'" không phải trang game (.html).';if(--con===0)napTep(ve);return}
      var rd=new FileReader();
      rd.onload=function(){var h=String(rd.result||'');
        var g={id:Date.now()+k,ten:tenTuHtml(h,f.name),ngay:homNay(),html:h};
        giaoDich('readwrite',function(st){return st.put(g)},function(ok){if(!ok)err.textContent='Máy chưa cho lưu tệp trong app (có thể đang ở chế độ ẩn danh). Thầy Cô giữ tệp trong thư mục Tải về nhé.';if(--con===0){napTep(ve);document.getElementById('tep-game').value=''}})};
      rd.onerror=function(){err.textContent='Không đọc được tệp "'+f.name+'".';if(--con===0)napTep(ve)};
      rd.readAsText(f);
    });
  });
  document.getElementById('kq-form').addEventListener('submit',function(e){
    e.preventDefault();
    var v=document.getElementById('kq-link').value.trim(),err=document.getElementById('kq-err');
    var m=v.match(/https:\/\/[^\s"'<>]+/);
    if(!m){err.textContent='Link chưa đúng. Link game bắt đầu bằng https:// (thường là https://claude.ai/…).';return}
    err.textContent='';
    ds.unshift({url:m[0],ten:document.getElementById('kq-ten').value.trim(),ngay:homNay()});luu();ve();
    document.getElementById('kq-link').value='';document.getElementById('kq-ten').value='';
  });
  ve();napTep(ve);
})();
</script>
'''

# ===== ĐĂNG KÝ THẦY CÔ + SỐ LIỆU SỬ DỤNG (gửi về Sổ Thầy Cô, app "Quản lý Game-học" ở quan-ly/) =====
# Địa chỉ Apps Script lấy từ trường "so_thay_co" trong phien-ban.json. Chưa có trường đó thì
# app không hiện phiếu và không gửi gì.
DK_CSS = """
body:not([data-tab=readme]) #dang-ky{display:none}
body:not([data-tab=phieu]) #dk-moi{display:none}
#dk-moi{display:flex;align-items:center;gap:10px;justify-content:space-between;background:#EAF6E3;border:1px solid #BFE0AC;border-radius:12px;padding:10px 14px;margin:0 0 14px;font-size:14.5px}
#dk-moi span{flex:1}#dk-moi .x{border:0;background:none;font-size:20px;color:var(--mut);cursor:pointer;padding:0 4px}
#dang-ky .dk-o{margin-top:12px}#dang-ky label{display:block;font-weight:700;margin-bottom:4px}
#dang-ky input[type=email],#dang-ky input[type=tel]{width:100%;font:inherit;padding:10px 12px;border:1.5px solid var(--line);border-radius:10px;background:#fff;color:var(--ink)}
#dang-ky .dk-dy{display:flex;gap:8px;align-items:flex-start;font-weight:400;margin-top:14px}
#dang-ky .dk-dy input{margin-top:5px;width:18px;height:18px;flex:0 0 auto}
"""

DK = """
<!-- ===== ĐĂNG KÝ THẦY CÔ ===== -->
<section class="card" id="dang-ky" aria-labelledby="h-dk" hidden>
  <h2 id="h-dk">Thầy Cô đăng ký dùng Trợ lý Game-học</h2>
  <p class="lead" style="margin:0">Đăng ký để Vườn Game-học biết Thầy Cô đang dùng, báo khi có bản mới và hỗ trợ khi cần. Vẫn <b>miễn phí vĩnh viễn</b>, không đăng ký vẫn dùng được.</p>
  <p class="ok" id="dk-xong" hidden></p>
  <form id="dk-form" novalidate>
    <div class="row">
      <div class="dk-o"><label for="dk-ten">Họ tên <span class="err" id="dk-e-ten" hidden>Thầy Cô cho em biết tên nhé</span></label><input type="text" id="dk-ten" maxlength="80" autocomplete="name"></div>
      <div class="dk-o"><label for="dk-truong">Trường</label><input type="text" id="dk-truong" maxlength="120"></div>
    </div>
    <div class="row">
      <div class="dk-o"><label for="dk-tinh">Tỉnh, thành</label><input type="text" id="dk-tinh" maxlength="40"></div>
      <div class="dk-o"><label for="dk-cap">Cấp dạy</label><select id="dk-cap"><option value="">Chọn cấp</option><option>Tiểu học</option><option>THCS</option><option>THPT</option><option>Khác</option></select></div>
    </div>
    <div class="dk-o"><label for="dk-mon">Môn dạy <small>(nhiều môn thì cách nhau dấu phẩy)</small></label><input type="text" id="dk-mon" maxlength="60"></div>
    <div class="dk-o"><label for="dk-lh">Zalo hoặc email <small>(không bắt buộc, để Vườn Game-học hỗ trợ)</small></label><input type="text" id="dk-lh" maxlength="80" inputmode="email"></div>
    <label class="dk-dy"><input type="checkbox" id="dk-dy"><span>Tôi đồng ý cho Vietwise lưu các thông tin trên để hỗ trợ và báo tin về Trợ lý Game-học. Vietwise không chia sẻ cho ai khác. <span class="err" id="dk-e-dy" hidden>Thầy Cô đánh dấu ô này để gửi nhé</span></span></label>
    <div class="btns"><button class="btn" type="submit" id="dk-gui">Gửi đăng ký</button></div>
    <p class="err" id="dk-loi" hidden></p>
  </form>
  <p class="nho" style="margin-top:12px">App cũng gửi về Vườn Game-học vài con số để biết app có giúp được Thầy Cô không: số lần mở app, số game đã lưu, phiên bản app, loại máy. Không gửi nội dung game, ảnh sách hay tên học sinh. <label style="display:inline;font-weight:400"><input type="checkbox" id="dk-sd" checked> Cho phép gửi các con số này</label></p>
</section>
"""

DK_MOI = """<div id="dk-moi" hidden><span>🌱 Thầy Cô đăng ký để nhận tin bản mới và được hỗ trợ.</span><a class="btn" href="#dang-ky" id="dk-moi-di">Đăng ký</a><button class="x" type="button" id="dk-moi-x" aria-label="Ẩn">×</button></div>
"""

DK_JS = r"""
<script>
/* Đăng ký Thầy Cô và số liệu sử dụng: gửi về Sổ Thầy Cô (Google Apps Script của Vietwise) */
(function(){
  var K={may:'gamehoc-ma-may',dk:'gamehoc-da-dang-ky',an:'gamehoc-an-moi-dk',sd:'gamehoc-gui-so-lieu',luc:'gamehoc-gui-luc'};
  function doc(k){try{return localStorage.getItem(k)}catch(e){return null}}
  function ghi(k,v){try{localStorage.setItem(k,v)}catch(e){}}
  function $(id){return document.getElementById(id)}
  function maMay(){var m=doc(K.may);if(m&&/^[A-Za-z0-9_-]{8,40}$/.test(m))return m;var a=new Uint8Array(12);(window.crypto||{getRandomValues:function(x){for(var i=0;i<x.length;i++)x[i]=Math.random()*256|0;return x}}).getRandomValues(a);
    m=btoa(String.fromCharCode.apply(null,a)).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');ghi(K.may,m);return m}
  function thietBi(){var u=navigator.userAgent||'';return /iPhone|iPod/.test(u)?'iPhone':/iPad/.test(u)||(/Macintosh/.test(u)&&navigator.maxTouchPoints>1)?'iPad':/Android/.test(u)?'Android':/Windows/.test(u)?'Windows':/Macintosh/.test(u)?'Mac':'Khác'}
  function phienBan(){return doc('gamehoc-skill-da-tai')||''}
  function gui(url,o){return fetch(url,{method:'POST',headers:{'Content-Type':'text/plain;charset=utf-8'},body:JSON.stringify(o)}).then(function(r){return r.json()})
    .catch(function(){return fetch(url,{method:'POST',mode:'no-cors',headers:{'Content-Type':'text/plain;charset=utf-8'},body:JSON.stringify(o)}).then(function(){return{ok:true,mu:true}})})}
  function soGame(cb){var n=0;try{n=(JSON.parse(doc('gamehoc-ket-qua')||'[]')||[]).length}catch(e){}
    try{var rq=indexedDB.open('gamehoc-tep',1);rq.onupgradeneeded=function(){try{rq.result.createObjectStore('tep',{keyPath:'id'})}catch(e){}};
      rq.onsuccess=function(){try{var d=rq.result,c=d.transaction('tep','readonly').objectStore('tep').count();c.onsuccess=function(){cb(n+c.result);d.close()};c.onerror=function(){cb(n)}}catch(e){cb(n)}};rq.onerror=function(){cb(n)}}catch(e){cb(n)}}
  function daXong(){var t=doc(K.dk);if(!t)return;$('dk-xong').textContent='Thầy Cô đã đăng ký ngày '+t+'. Cảm ơn Thầy Cô! Muốn sửa thông tin thì điền lại và gửi.';$('dk-xong').hidden=false;$('dk-moi').hidden=true}
  function bat(url){
    $('dang-ky').hidden=false;$('dk-sd').checked=doc(K.sd)!=='0';daXong();
    if(!doc(K.dk)&&!doc(K.an))$('dk-moi').hidden=false;
    $('dk-moi-x').addEventListener('click',function(){ghi(K.an,'1');$('dk-moi').hidden=true});
    $('dk-moi-di').addEventListener('click',function(e){e.preventDefault();var b=document.querySelector('[data-tab=readme]');if(b)b.click();setTimeout(function(){$('dang-ky').scrollIntoView({behavior:'smooth'})},60)});
    $('dk-ten').addEventListener('input',function(){$('dk-e-ten').hidden=true});$('dk-dy').addEventListener('change',function(){$('dk-e-dy').hidden=true});
    $('dk-sd').addEventListener('change',function(){ghi(K.sd,this.checked?'1':'0')});
    $('dk-form').addEventListener('submit',function(e){e.preventDefault();
      var ten=$('dk-ten').value.trim(),dy=$('dk-dy').checked;$('dk-e-ten').hidden=!!ten;$('dk-e-dy').hidden=dy;$('dk-loi').hidden=true;if(!ten||!dy)return;
      var b=$('dk-gui');b.disabled=true;b.textContent='Đang gửi…';
      gui(url,{viec:'dang_ky',ma_may:maMay(),ho_ten:ten,truong:$('dk-truong').value.trim(),tinh:$('dk-tinh').value.trim(),mon:$('dk-mon').value.trim(),cap:$('dk-cap').value,lien_he:$('dk-lh').value.trim(),dong_y:true})
        .then(function(j){b.disabled=false;b.textContent='Gửi đăng ký';
          if(j&&j.ok){var d=new Date();ghi(K.dk,('0'+d.getDate()).slice(-2)+'/'+('0'+(d.getMonth()+1)).slice(-2)+'/'+d.getFullYear());daXong();$('dk-xong').scrollIntoView({behavior:'smooth',block:'center'})}
          else{$('dk-loi').textContent='Chưa gửi được. Thầy Cô kiểm tra lại họ tên và ô đồng ý rồi thử lại nhé.';$('dk-loi').hidden=false}})
        .catch(function(){b.disabled=false;b.textContent='Gửi đăng ký';$('dk-loi').textContent='Chưa gửi được vì mất mạng. Thầy Cô thử lại khi có mạng nhé.';$('dk-loi').hidden=false});
    });
    baoDung(url);
  }
  function baoDung(url){if(doc(K.sd)==='0')return;var t=+doc(K.luc)||0;if(Date.now()-t<30*60*1000)return;
    soGame(function(n){gui(url,{viec:'su_dung',ma_may:maMay(),so_game_luu:n,phien_ban:phienBan(),thiet_bi:thietBi()}).then(function(j){if(j&&j.ok)ghi(K.luc,String(Date.now()))},function(){})})}
  try{fetch('https://vietwise.github.io/Vietwise-TL-game-hoa-cho-GV/phien-ban.json',{cache:'no-store'}).then(function(r){return r.ok?r.json():null})
    .then(function(j){var u=j&&j.so_thay_co;if(u&&/^https:\/\/script\.google\.com\/macros\/s\/[A-Za-z0-9_-]+\/exec$/.test(u))bat(u)}).catch(function(){})}catch(e){}
})();
</script>
"""


def dung(goi):
    s = open(H + '/mau/doc-truoc.html', encoding='utf-8').read()
    def anh_tab(ten):
        import base64
        p = H + '/mau/anh/' + ten + '.webp'
        return ('<img class="ti" src="data:image/webp;base64,%s" alt="">' % base64.b64encode(open(p, 'rb').read()).decode()) if os.path.exists(p) else ''
    s = thay(s, '<meta name="viewport" content="width=device-width, initial-scale=1">', HEAD)
    s = thay(s, '<title>Trợ lý Game-học: Phiếu giao việc cho Thầy Cô</title>', '<title>Trợ lý Game-học cho Thầy Cô</title>')
    s = thay(s, '</style>\n</head>', CSS + DK_CSS + '</style>\n</head>')
    s = thay(s, '\n<header>', '\n' + BAR + '<header>')
    s = thay(s, '<span class="nobreak"><b>4-Cai-Skill/game-hoc-vietwise.zip</b></span> trong gói này.',
             '<a class="nobreak" href="tai-ve/game-hoc-vietwise.zip" download><b>game-hoc-vietwise.zip</b></a> (bấm để tải về máy).')
    s = thay(s, 'Mỗi loại một game, nằm trong thư mục <b>3-Game-mau</b> của gói này. Bấm để mở trong tab mới (mở bằng trình duyệt, không cần mạng), rồi',
             'Mỗi loại một game. Bấm để mở trong tab mới, rồi')
    s = thay(s, 'href="3-Game-mau/', 'href="choi-thu/', 4)
    s = thay(s, '<span class="tl">Game mẫu</span></button>',
             '<span class="tl">Game mẫu</span></button>\n      <button role="tab" id="t-tra-ket-qua" data-tab="tra-ket-qua" aria-selected="false">' + anh_tab('the-tra-ket-qua') + '<span class="tl">Game của tôi</span></button>')
    s = thay(s, "var tabs=['phieu','readme','tham-khao'];", "var tabs=['phieu','readme','tham-khao','tra-ket-qua'];")
    s = thay(s, '<span>Lưu link game để lần sau mở lại.</span></li>',
             '<span>Lưu game: trong Claude bấm <b>Tải xuống</b> để có tệp .html (hoặc bấm Chia sẻ để lấy link), rồi đưa vào thẻ <a href="#tra-ket-qua" data-go="tra-ket-qua"><b>Game của tôi</b></a>. Lần sau mở lại ngay, không cần mạng.</span></li>')
    s = thay(s, '          <li><span class="ic" aria-hidden="true">📽️</span>', '          <li><span class="ic" aria-hidden="true">📽️</span>')
    s = thay(s, '<section class="panel on" id="p-phieu" role="tabpanel" aria-labelledby="t-phieu">\n', '<section class="panel on" id="p-phieu" role="tabpanel" aria-labelledby="t-phieu">\n' + DK_MOI)
    s = thay(s, '\n</main>', TAB + DK + THE + '\n</main>')
    s = thay(s, '</body>', JS + DK_JS + '</body>')
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
