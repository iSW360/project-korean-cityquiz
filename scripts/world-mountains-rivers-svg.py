# -*- coding: utf-8 -*-
"""다른 지도들과 동일한 스타일(어두운 배경 + 실루엣 대륙 + 얇은 선)로 산맥·강 SVG 생성"""
import json
import math

with open('scripts/ne_land.geojson', encoding='utf-8') as f:
    land = json.load(f)

VB_W, VB_H = 960, 480

def geo(lat, lon):
    x = (lon + 180) / 360 * VB_W
    y = (90 - lat) / 180 * VB_H
    return x, y

def ring_to_path(ring):
    pts = [geo(lat, lon) for lon, lat in ring]  # geojson은 [lon,lat] 순서
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f} " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in pts[1:]) + " Z"
    return d

land_paths = []
for feat in land['features']:
    geom = feat['geometry']
    polys = geom['coordinates'] if geom['type'] == 'MultiPolygon' else [geom['coordinates']]
    for poly in polys:
        outer = poly[0]
        land_paths.append(ring_to_path(outer))

MOUNTAINS = [
    ("히말라야산맥", "Himalayas", [(35.8,74.5),(34.0,78.0),(29.0,83.0),(28.0,87.0),(27.7,92.0),(27.0,96.0)]),
    ("카라코람산맥", "Karakoram", [(36.5,74.0),(35.9,76.5),(35.4,77.0)]),
    ("톈산산맥", "Tian Shan", [(43.0,73.0),(42.0,77.5),(41.5,80.0),(42.2,84.0)]),
    ("안데스산맥", "Andes", [(10.5,-72.5),(0,-78),(-13.5,-72),(-24,-68),(-33,-70),(-41,-71.5),(-50,-73),(-55,-70)]),
    ("로키산맥", "Rocky Mountains", [(60,-129),(52,-119),(45,-113),(40,-106),(35,-106),(31,-106)]),
    ("시에라마드레", "Sierra Madre", [(31,-108),(25,-105),(19,-99),(15,-92)]),
    ("알프스산맥", "Alps", [(45.8,6.9),(46.0,8.3),(47.0,10.5),(46.5,12.5),(46.6,14.5)]),
    ("스칸디나비아산맥", "Scandinavian Mountains", [(68,17.5),(63,12),(61,8.5),(58,7)]),
    ("우랄산맥", "Ural Mountains", [(68,66),(60,59.5),(55,59),(51,58.5)]),
    ("코카서스산맥", "Caucasus Mountains", [(45,37.5),(43.3,42),(41.5,46.5)]),
    ("애틀러스산맥", "Atlas Mountains", [(35.5,-5.5),(33,-5),(31,-2),(33,4),(36.5,9)]),
    ("에티오피아고원", "Ethiopian Highlands", [(14,38),(11,39),(8,38),(6.5,37.5)]),
    ("드라켄즈버그산맥", "Drakensberg", [(-24.5,29.5),(-28,29),(-30.5,29),(-33,25)]),
    ("자그로스산맥", "Zagros Mountains", [(38,45.5),(33,47.5),(29,53),(27,56.5)]),
    ("그레이트디바이딩산맥", "Great Dividing Range", [(-11,143),(-17,145),(-25,151.5),(-33,150),(-37,148),(-37,143.5)]),
    ("애팔래치아산맥", "Appalachian Mountains", [(45,-70),(41,-76),(37,-81),(34,-83.5)]),
]
RIVERS = [
    ("나일강", "Nile", [(1.5,31.2),(9,32),(15.6,32.5),(19.5,32.5),(24,32.9),(30,31.2),(31.4,30.4)]),
    ("아마존강", "Amazon", [(-5.5,-77),(-4.5,-73),(-4,-63),(-3,-59.9),(-1.9,-52.6),(-0.5,-49.5)]),
    ("양쯔강", "Yangtze", [(33.4,91.2),(29,97),(28.7,104.6),(30.6,111.3),(30.6,114.3),(31.4,121.2)]),
    ("황허강", "Yellow River", [(35.0,96.5),(36.5,101.7),(37.5,106.2),(40.8,110.0),(35.6,113.8),(37.8,118.8)]),
    ("미시시피강", "Mississippi", [(47.2,-95.2),(43.5,-91.2),(38.6,-90.2),(32.3,-90.9),(29.2,-89.3)]),
    ("오브강", "Ob", [(51.2,85.6),(58,68.8),(61.2,69),(66.5,66.6)]),
    ("예니세이강", "Yenisei", [(51.5,93.5),(58,92.5),(63,87.5),(69.5,86.5)]),
    ("레나강", "Lena", [(56,107.5),(60,114),(64,123.5),(70,127.5),(72.4,126.7)]),
    ("아무르강", "Amur", [(53,122.5),(49.5,130),(50,136),(52.8,141.1)]),
    ("콩고강", "Congo", [(-11,25.9),(-4.3,15.3),(-2,16),(0,18),(-4.3,15.3),(-6,12.4)]),
    ("메콩강", "Mekong", [(33,93.9),(21.9,100.8),(17.9,104.8),(11.9,105.8),(10.3,106.5)]),
    ("볼가강", "Volga", [(57.3,32.5),(56.3,44),(51.7,46),(48.7,44.5),(45.7,47.9)]),
    ("다뉴브강", "Danube", [(48,8.2),(48.3,14.3),(47.5,19.1),(44.8,20.5),(44,25.9),(45.2,29.7)]),
    ("갠지스강", "Ganges", [(30.9,78.9),(27.6,80.9),(25.6,85.1),(24.1,88.1),(22.3,90.5)]),
    ("인더스강", "Indus", [(32.5,79.7),(35.3,74.7),(33.6,73.0),(28.4,70.3),(24.2,67.5)]),
    ("머리달링강", "Murray-Darling", [(-28.5,150.5),(-30.5,148),(-34,142),(-34.2,139.3)]),
]

MOUNTAIN_OFFSET = {
    "그레이트디바이딩산맥": (-140, -14), "우랄산맥": (-55, -26), "코카서스산맥": (8, 20),
    "카라코람산맥": (-70, -10), "톈산산맥": (6, -22), "시에라마드레": (-90, 0),
    "스칸디나비아산맥": (-6, -30), "에티오피아고원": (8, 16), "드라켄즈버그산맥": (-10, 16),
}
RIVER_OFFSET = {
    "오브강": (8, -20), "예니세이강": (-70, -10), "레나강": (8, -10), "아무르강": (8, 8),
    "황허강": (8, -22), "인더스강": (-90, -6), "머리달링강": (-100, 10),
}

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VB_W} {VB_H}">']
svg.append(f'<rect width="{VB_W}" height="{VB_H}" fill="#0C1220"/>')
svg.append('<g fill="rgba(255,255,255,.08)" stroke="rgba(255,255,255,.15)" stroke-width="0.6">')
for d in land_paths:
    svg.append(f'<path d="{d}"/>')
svg.append('</g>')

def catmull_rom(pts, samples=10):
    """점 목록을 부드러운 곡선으로 촘촘히 보간"""
    if len(pts) < 3:
        return pts
    p = [pts[0]] + pts + [pts[-1]]
    out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i-1], p[i], p[i+1], p[i+2]
        for s in range(samples):
            t = s / samples
            t2, t3 = t*t, t*t*t
            x = 0.5*((2*p1[0]) + (-p0[0]+p2[0])*t + (2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2 + (-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
            y = 0.5*((2*p1[1]) + (-p0[1]+p2[1])*t + (2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2 + (-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
            out.append((x, y))
    out.append(pts[-1])
    return out

def tangents(pts):
    n = len(pts)
    tg = []
    for i in range(n):
        a = pts[max(0, i-1)]
        b = pts[min(n-1, i+1)]
        dx, dy = b[0]-a[0], b[1]-a[1]
        l = math.hypot(dx, dy) or 1
        tg.append((dx/l, dy/l))
    return tg

# ── 산맥: 불규칙한 높낮이의 봉우리가 자연스럽게 이어지는 능선 실루엣 ──
class LCG:
    """이름 기반 시드로 항상 같은 결과를 재현하는 간단한 난수 생성기"""
    def __init__(self, seed):
        self.s = seed & 0xffffffff or 1
    def rand(self):
        self.s = (1103515245 * self.s + 12345) & 0x7fffffff
        return self.s / 0x7fffffff
    def uniform(self, a, b):
        return a + self.rand() * (b - a)
    def randint(self, a, b):
        return a + int(self.rand() * (b - a + 1))

def ridge_heights(n, seed):
    """불규칙 간격의 제어점(봉우리·골짜기)을 두고 선형보간 + 잔물결 잡음을 더해
    자연스러운 산 능선 실루엣 높이 배열을 만든다. 시작/끝은 0(대지)으로 수렴."""
    rnd = LCG(seed)
    ctrl_x, ctrl_h = [0], [0]
    x = 0
    while x < n - 1:
        x += rnd.randint(3, 7)
        x = min(x, n - 1)
        is_valley = rnd.rand() < 0.32
        h = rnd.uniform(2.5, 5.5)/3 if is_valley else rnd.uniform(7, 13)/3
        ctrl_x.append(x); ctrl_h.append(h)
    if ctrl_x[-1] != n - 1:
        ctrl_x.append(n - 1); ctrl_h.append(0)
    else:
        ctrl_h[-1] = 0
    heights = []
    ci = 0
    for i in range(n):
        while ci < len(ctrl_x) - 2 and i > ctrl_x[ci+1]:
            ci += 1
        x0, x1 = ctrl_x[ci], ctrl_x[ci+1]
        h0, h1 = ctrl_h[ci], ctrl_h[ci+1]
        t = (i - x0) / (x1 - x0) if x1 > x0 else 0
        h = h0 + (h1 - h0) * t
        jitter = math.sin(i * 2.3 + seed) * 0.5 + math.sin(i * 5.1 + seed*0.7) * 0.3
        heights.append(max(0, h + jitter))
    return heights

svg.append('<g>')
for ko, en, path in MOUNTAINS:
    raw = [geo(la, lo) for la, lo in path]
    pts = catmull_rom(raw, samples=16)
    tg = tangents(pts)
    n = len(pts)
    seed = sum(ord(c) for c in ko) * 977
    hs = ridge_heights(n, seed)
    # 경로 전체에 대해 '봉우리가 솟는 쪽'을 한 번만 결정(점마다 다시 판단하면 능선이
    # 크게 휘는 구간에서 방향이 뒤집혀 톱니가 반대쪽으로 튀는 문제가 생김)
    avg_ny = sum(-tyn for txn, tyn in tg) / n
    flip = avg_ny > 0
    top = []
    for i, (x, y) in enumerate(pts):
        txn, tyn = tg[i]
        nx, ny = -tyn, txn
        if flip:
            nx, ny = -nx, -ny
        top.append((x + nx*hs[i], y + ny*hs[i]))
    d = ('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in top) +
         ' L' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in reversed(pts)) + ' Z')
    svg.append(f'<path d="{d}" fill="#E8B84B" fill-opacity="0.8" stroke="#F5DFA8" stroke-width="0.6" '
                f'stroke-linejoin="round" stroke-linecap="round"/>')
svg.append('</g>')

# ── 강: 발원지→하구로 갈수록 폭이 넓어지는 유선형 리본 + 중심선 ──
svg.append('<g>')
for ko, en, path in RIVERS:
    raw = [geo(la, lo) for la, lo in path]
    pts = catmull_rom(raw, samples=14)
    tg = tangents(pts)
    n = len(pts)
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        t = i / (n - 1)
        w = (0.5 + t * 2.6) / 3  # 발원지 0.5px → 하구 3.1px 반폭
        txn, tyn = tg[i]
        nx, ny = -tyn, txn
        left.append((x + nx*w, y + ny*w))
        right.append((x - nx*w, y - ny*w))
    d = ('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in left) +
         ' L' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in reversed(right)) + ' Z')
    svg.append(f'<path d="{d}" fill="#3ECFB2" fill-opacity="0.55" stroke="#3ECFB2" stroke-width="0.8" stroke-linejoin="round" opacity="0.95"/>')
    # 하구 쪽에 작은 삼각주 느낌의 점(도착지 강조)
    mx, my = pts[-1]
    svg.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="2.4" fill="#9EE6D6"/>')
svg.append('</g>')

svg.append('<g font-family="sans-serif" font-weight="700">')
for ko, en, path in MOUNTAINS:
    pts = [geo(la, lo) for la, lo in path]
    mx, my = pts[len(pts)//2]
    ox, oy = MOUNTAIN_OFFSET.get(ko, (5, -10))
    mx, my = mx+ox, my+oy
    svg.append(f'<text x="{mx:.1f}" y="{my:.1f}" font-size="10.5" fill="#F5DFA8">{ko}</text>')
    svg.append(f'<text x="{mx:.1f}" y="{my+11:.1f}" font-size="8" fill="#C9AE7A" font-weight="400">({en})</text>')
for ko, en, path in RIVERS:
    pts = [geo(la, lo) for la, lo in path]
    mx, my = pts[len(pts)//2]
    ox, oy = RIVER_OFFSET.get(ko, (5, 4))
    mx, my = mx+ox, my+oy
    svg.append(f'<text x="{mx:.1f}" y="{my:.1f}" font-size="10.5" fill="#9EE6D6">{ko}</text>')
    svg.append(f'<text x="{mx:.1f}" y="{my+11:.1f}" font-size="8" fill="#6FB8AC" font-weight="400">({en})</text>')
svg.append('</g>')
svg.append('</svg>')

with open('scripts/world-mountains-rivers-styled.svg', 'w', encoding='utf-8') as f:
    f.write(''.join(svg))
print('저장 완료')
