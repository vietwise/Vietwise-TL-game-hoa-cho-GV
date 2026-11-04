import re,json,base64
import os,sys
H=os.path.dirname(os.path.abspath(__file__))
REPO=os.path.abspath(H+'/../..')
P=open(REPO+'/skill/game-hoc-vietwise/assets/trinh-choi.html').read()
css=re.search(r"\.brand\{.*?\n\.brand\.bot\{[^\n]*\n\.brand a\{[^\n]*\n\.brand \.t\{[^\n]*\n",P,re.S).group(0)+re.search(r"#lock\{[^\n]*\n",P).group(0)
lockdiv=re.search(r'<div id="lock">.*?</div></div>\n',P,re.S).group(0)
blk=re.search(r"// ===== KHỐI GHI NGUỒN.*?// ===== HẾT KHỐI KHÓA =====\n",P,re.S).group(0)
t=open(H+'/mau/giao-viec.tpl.html').read()
t=t.replace('__CSSBRAND__',css).replace('__LOCKDIV__',lockdiv).replace('__BLK__',blk)
t=t.replace('__PLAYER__',P.replace('</script>','<\\/script>'))
for n in ['vay-tay','hieu-ky','thich-nghi','ben-chi','an-lac','guong-than','toan-do']:
    t=t.replace(f'__SPR_{n}__','data:image/webp;base64,'+base64.b64encode(open(H+f'/sprite/{n}.webp','rb').read()).decode())
R=REPO+'/skill/game-hoc-vietwise/references/vi-du/'
ex=json.load(open(R+'on-bai-khtn8-mol-nong-do.json'));fs=json.load(open(R+'on-bai-khoahoc4-nuoc.json'))
t=t.replace('__EXAMPLE__',json.dumps(ex,ensure_ascii=False).replace('</','<\\/')).replace('__FEWSHOT__',json.dumps(fs,ensure_ascii=False))
open(sys.argv[1] if len(sys.argv)>1 else REPO+'/web/giao-viec.html','w').write(t);print(len(t))
