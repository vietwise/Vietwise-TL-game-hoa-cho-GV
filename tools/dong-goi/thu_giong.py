#!/usr/bin/env python3
"""Thu sẵn giọng đọc (Microsoft Edge TTS) cho các game mẫu và nhúng vào JSON (trường `giong`).

Cần: pip install edge-tts ; ffmpeg ; mạng tới speech.platform.bing.com.
Dùng:  python3 tools/dong-goi/thu_giong.py            # thu thật, ra tools/dong-goi/giong/*.json
       python3 tools/dong-goi/thu_giong.py --gia      # tạo âm thử bằng ffmpeg (kiểm tra đường ống, không phải giọng thật)
Cách chia đoạn PHẢI giống trình chơi (hàm rng/chia/tach trong assets/trinh-choi.html) và khóa băm giống hàm hk."""
import sys, os, re, json, base64, subprocess, asyncio, hashlib

H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(H + '/../..')
VIDU = REPO + '/skill/game-hoc-vietwise/references/vi-du/'
RA = H + '/giong'
GAME_MAU = ['on-bai-khtn8-mol-nong-do', 'on-bai-tienganh7-nhan-hop-sua', 'sach-la-thay-van6-de-men']
VOICE = {'vi-VN': 'vi-VN-HoaiMyNeural', 'en-US': 'en-US-AriaNeural', 'zh-CN': 'zh-CN-XiaoxiaoNeural', 'ja-JP': 'ja-JP-NanamiNeural',
         'ko-KR': 'ko-KR-SunHiNeural', 'ru-RU': 'ru-RU-SvetlanaNeural', 'fr-FR': 'fr-FR-DeniseNeural', 'de-DE': 'de-DE-KatjaNeural',
         'es-ES': 'es-ES-ElviraNeural', 'it-IT': 'it-IT-ElsaNeural'}
RATE = {'vi-VN': '-20%'}  # ngoại ngữ: -15%
MAL = {'en': 'en-US', 'zh': 'zh-CN', 'ja': 'ja-JP', 'ko': 'ko-KR', 'fr': 'fr-FR', 'de': 'de-DE', 'ru': 'ru-RU', 'es': 'es-ES', 'it': 'it-IT'}
RUN = '[぀-ヿ㐀-鿿가-힯Ѐ-ӿ]'
RE = re.compile(RUN + '[぀-ヿ㐀-鿿가-힯Ѐ-ӿ　-〿＀-￯\\s]*')

def hk(l, t):
    s = (l + '|' + t).encode('utf-16-le')
    x = 5381
    for i in range(0, len(s), 2):
        x = ((x << 5) + x + (s[i] | s[i + 1] << 8)) & 0xFFFFFFFF
    return str(x)

def rng(x, ma):
    o = []
    for m in RE.finditer(x or ''):
        s = m.group(0).rstrip()
        if re.search('[가-힯]', s): l = 'ko-KR'
        elif re.search('[぀-ヿ]', s): l = 'ja-JP'
        elif re.search('[Ѐ-ӿ]', s): l = 'ru-RU'
        else: l = 'ja-JP' if ma == 'ja' else 'zh-CN'
        o.append((m.start(), m.start() + len(s), s, l))
    if ma in ('en', 'fr', 'de', 'es', 'it'):
        for m in re.finditer('"([^"]{2,90})"', x or ''):
            o.append((m.start(), m.end(), m.group(1), MAL[ma]))
    o.sort(key=lambda r: r[0])
    return o

def tach(x, ma):
    seen, o = set(), []
    for s, e, t, l in rng(x, ma):
        if t not in seen:
            seen.add(t); o.append((t, l))
    return o[:6]

def chia(x, ma):
    o, p, x = [], 0, x or ''
    ok = lambda v: re.search('[A-Za-zÀ-ỹ0-9]', v)
    for s, e, t, l in rng(x, ma):
        if s < p: continue
        v = x[p:s]
        if ok(v): o.append((v.replace('"', ' '), 'vi-VN'))
        o.append((t, l)); p = e
    v = x[p:]
    if ok(v): o.append((v.replace('"', ' '), 'vi-VN'))
    return o

def doan_can_thu(g):
    ma = (g.get('ngoai_ngu') or {}).get('ma', '')
    out = {}
    for t, l in chia(g.get('loi_ke'), ma) + tach(g.get('loi_ke'), ma) + tach(g.get('buoc_ngoat'), ma) + tach(g.get('cau_hoi_treo'), ma):
        out[hk(l, t)] = (t, l)
    return out

async def thu(t, l, ra):
    import edge_tts, ssl
    import edge_tts.communicate as ec
    ca = os.environ.get('SSL_CERT_FILE') or os.environ.get('REQUESTS_CA_BUNDLE')
    if ca: ec._SSL_CTX = ssl.create_default_context(cafile=ca)  # máy sau proxy có CA riêng
    proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
    rate = RATE.get(l, '-15%')
    await edge_tts.Communicate(t, VOICE[l], rate=rate, proxy=proxy).save(ra)

def nen(src, dst):
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-ac', '1', '-ar', '24000', '-b:a', '24k', dst])

def gia(t, dst):
    d = max(0.5, min(20, len(t) * 0.06))
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'sine=frequency=440:duration=%.2f' % d, '-ac', '1', '-ar', '24000', '-b:a', '24k', dst])

def main():
    che_do_gia = '--gia' in sys.argv
    os.makedirs(RA + '/cache', exist_ok=True)
    for ten in GAME_MAU:
        g = json.load(open(VIDU + ten + '.json', encoding='utf-8'))
        g.pop('giong', None)
        giong = {}
        for k, (t, l) in doan_can_thu(g).items():
            cache = '%s/cache/%s%s.mp3' % (RA, 'gia-' if che_do_gia else '', k)
            if not os.path.exists(cache):
                tmp = cache + '.tmp.mp3'
                if che_do_gia: gia(t, cache)
                else:
                    asyncio.run(thu(t, l, tmp)); nen(tmp, cache); os.remove(tmp)
            giong[k] = 'data:audio/mpeg;base64,' + base64.b64encode(open(cache, 'rb').read()).decode()
        g['giong'] = giong
        json.dump(g, open('%s/%s.json' % (RA, ten), 'w', encoding='utf-8'), ensure_ascii=False)
        print(ten, len(giong), 'đoạn,', sum(len(v) for v in giong.values()) // 1024, 'KB')

if __name__ == '__main__':
    main()
