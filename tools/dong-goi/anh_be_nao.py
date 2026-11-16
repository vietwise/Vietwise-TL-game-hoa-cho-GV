"""Điền ảnh Bé Não (assets/sprites/be-nao/*.webp) vào chỗ __ANH_<tên>__ của một trang HTML, dạng data URI."""
import os, re, base64
H = os.path.dirname(os.path.abspath(__file__))
TM = os.path.abspath(H + '/../../assets/sprites/be-nao')

def uri(ten):
    with open(os.path.join(TM, ten + '.webp'), 'rb') as f:
        return 'data:image/webp;base64,' + base64.b64encode(f.read()).decode()

def dien(t):
    return re.sub(r'__ANH_([a-z0-9-]+)__', lambda m: uri(m.group(1)), t)
