# -*- coding: utf-8 -*-
"""세계 산맥·강 퀴즈 — scripts/world-mountains-rivers-svg.py의 실루엣 스타일을 그대로 쓰되,
이름 라벨은 빼고 각 도형에 data-id/data-ko/data-en/data-grp를 달아 클릭 가능한 퀴즈 지역으로 만든다."""
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
    pts = [geo(lat, lon) for lon, lat in ring]
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f} " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in pts[1:]) + " Z"
    return d

land_paths = []
for feat in land['features']:
    geom = feat['geometry']
    polys = geom['coordinates'] if geom['type'] == 'MultiPolygon' else [geom['coordinates']]
    for poly in polys:
        land_paths.append(ring_to_path(poly[0]))

# (id, ko, en, [(lat,lon),...], hint_ko, hint_en)
MOUNTAINS = [
    ("HIMALAYAS", "히말라야산맥", "Himalayas", [(35.8,74.5),(34.0,78.0),(29.0,83.0),(28.0,87.0),(27.7,92.0),(27.0,96.0)],
     "세계에서 가장 높은 산맥. 에베레스트를 포함한 8000m급 봉우리가 여럿 있음", "The world's highest range, home to Everest and several 8,000m peaks"),
    ("KARAKORAM", "카라코람산맥", "Karakoram", [(36.5,74.0),(35.9,76.5),(35.4,77.0)],
     "세계 2위 고봉 K2가 있는 산맥. 파키스탄·중국·인도 접경지대", "Home to K2, the world's second-highest peak, on the Pakistan-China-India border"),
    ("TIANSHAN", "톈산산맥", "Tian Shan", [(43.0,73.0),(42.0,77.5),(41.5,80.0),(42.2,84.0)],
     "'하늘의 산'이라는 뜻. 중앙아시아를 가로지르는 산맥", "Name means 'Mountains of Heaven'; crosses Central Asia"),
    ("ANDES", "안데스산맥", "Andes", [(10.5,-72.5),(0,-78),(-13.5,-72),(-24,-68),(-33,-70),(-41,-71.5),(-50,-73),(-55,-70)],
     "세계에서 가장 긴 산맥(약 7,000km). 남미 서부를 따라 뻗음", "The world's longest range (~7,000km), running along South America's west coast"),
    ("ROCKY", "로키산맥", "Rocky Mountains", [(60,-129),(52,-119),(45,-113),(40,-106),(35,-106),(31,-106)],
     "북미 서부를 남북으로 가로지르는 대산맥", "A major range running north-south through western North America"),
    ("SIERRAMADRE", "시에라마드레", "Sierra Madre", [(31,-108),(25,-105),(19,-99),(15,-92)],
     "멕시코를 남북으로 가로지르는 산맥", "A mountain system running through Mexico"),
    ("ALPS", "알프스산맥", "Alps", [(45.8,6.9),(46.0,8.3),(47.0,10.5),(46.5,12.5),(46.6,14.5)],
     "유럽에서 가장 높은 산맥. 몽블랑이 최고봉", "Europe's highest range; Mont Blanc is its tallest peak"),
    ("SCANDINAVIAN", "스칸디나비아산맥", "Scandinavian Mountains", [(68,17.5),(63,12),(61,8.5),(58,7)],
     "노르웨이와 스웨덴 사이를 가르는 산맥", "Range dividing Norway and Sweden"),
    ("URAL", "우랄산맥", "Ural Mountains", [(68,66),(60,59.5),(55,59),(51,58.5)],
     "전통적으로 유럽과 아시아의 경계로 여겨지는 산맥", "Traditionally regarded as the boundary between Europe and Asia"),
    ("CAUCASUS", "코카서스산맥", "Caucasus Mountains", [(45,37.5),(43.3,42),(41.5,46.5)],
     "흑해와 카스피해 사이. 유럽 최고봉 엘브루스산이 있음", "Between the Black and Caspian Seas; home to Europe's highest peak, Mount Elbrus"),
    ("ATLAS", "애틀러스산맥", "Atlas Mountains", [(35.5,-5.5),(33,-5),(31,-2),(33,4),(36.5,9)],
     "북아프리카를 가로지르는 산맥", "A mountain range crossing North Africa"),
    ("ETHIOPIAN", "에티오피아고원", "Ethiopian Highlands", [(14,38),(11,39),(8,38),(6.5,37.5)],
     "'아프리카의 지붕'이라 불리는 고원지대", "A highland region often called 'the Roof of Africa'"),
    ("DRAKENSBERG", "드라켄즈버그산맥", "Drakensberg", [(-24.5,29.5),(-28,29),(-30.5,29),(-33,25)],
     "남아프리카공화국 동부의 대규모 절벽 산맥", "A dramatic escarpment range in eastern South Africa"),
    ("ZAGROS", "자그로스산맥", "Zagros Mountains", [(38,45.5),(33,47.5),(29,53),(27,56.5)],
     "이란과 이라크에 걸친 산맥", "A mountain range spanning Iran and Iraq"),
    ("GREATDIVIDING", "그레이트디바이딩산맥", "Great Dividing Range", [(-11,143),(-17,145),(-25,151.5),(-33,150),(-37,148),(-37,143.5)],
     "호주 동부 해안을 따라 남북으로 뻗은 산맥", "Range running along Australia's eastern coast"),
    ("APPALACHIAN", "애팔래치아산맥", "Appalachian Mountains", [(45,-70),(41,-76),(37,-81),(34,-83.5)],
     "북미 동부의 오래된 산맥", "An ancient mountain range in eastern North America"),
]

RIVERS = [
    ("NILE", "나일강", "Nile", [(1.5,31.2),(9,32),(15.6,32.5),(19.5,32.5),(24,32.9),(30,31.2),(31.4,30.4)],
     "세계에서 손꼽히는 최장 하천(약 6,650km). 아프리카 동북부를 흘러 지중해로", "One of the world's longest rivers (~6,650km), flowing through northeast Africa to the Mediterranean"),
    ("AMAZON", "아마존강", "Amazon", [(-5.5,-77),(-4.5,-73),(-4,-63),(-3,-59.9),(-1.9,-52.6),(-0.5,-49.5)],
     "유량 기준 세계 최대의 강. 남미를 가로질러 대서양으로", "The world's largest river by discharge, crossing South America to the Atlantic"),
    ("YANGTZE", "양쯔강", "Yangtze", [(33.4,91.2),(29,97),(28.7,104.6),(30.6,111.3),(30.6,114.3),(31.4,121.2)],
     "아시아에서 가장 긴 강. 중국을 가로질러 동중국해로", "Asia's longest river, flowing across China to the East China Sea"),
    ("YELLOWRIVER", "황허강", "Yellow River", [(35.0,96.5),(36.5,101.7),(37.5,106.2),(40.8,110.0),(35.6,113.8),(37.8,118.8)],
     "'중국 문명의 발상지'로 불리는 강", "Often called the cradle of Chinese civilization"),
    ("MISSISSIPPI", "미시시피강", "Mississippi", [(47.2,-95.2),(43.5,-91.2),(38.6,-90.2),(32.3,-90.9),(29.2,-89.3)],
     "북미에서 손꼽히는 긴 강. 멕시코만으로 흘러듦", "One of North America's longest rivers, emptying into the Gulf of Mexico"),
    ("OB", "오브강", "Ob", [(51.2,85.6),(58,68.8),(61.2,69),(66.5,66.6)],
     "시베리아 서부를 흘러 북극해로 향하는 강", "Flows through western Siberia to the Arctic Ocean"),
    ("YENISEI", "예니세이강", "Yenisei", [(51.5,93.5),(58,92.5),(63,87.5),(69.5,86.5)],
     "시베리아 중부를 남북으로 가로지르는 강", "Flows north to south through central Siberia"),
    ("LENA", "레나강", "Lena", [(56,107.5),(60,114),(64,123.5),(70,127.5),(72.4,126.7)],
     "시베리아 동부의 대하천. 북극해로 흘러듦", "A major river in eastern Siberia, flowing to the Arctic Ocean"),
    ("AMUR", "아무르강", "Amur", [(53,122.5),(49.5,130),(50,136),(52.8,141.1)],
     "러시아와 중국의 국경 일부를 이루는 강", "Forms part of the border between Russia and China"),
    ("CONGO", "콩고강", "Congo", [(-11,25.9),(-4.3,15.3),(-2,16),(0,18),(-4.3,15.3),(-6,12.4)],
     "아프리카에서 가장 깊은 강. 유량 기준 세계 2위", "Africa's deepest river; second in the world by discharge"),
    ("MEKONG", "메콩강", "Mekong", [(33,93.9),(21.9,100.8),(17.9,104.8),(11.9,105.8),(10.3,106.5)],
     "동남아시아 여러 나라를 흐르는 강", "Flows through multiple Southeast Asian countries"),
    ("VOLGA", "볼가강", "Volga", [(57.3,32.5),(56.3,44),(51.7,46),(48.7,44.5),(45.7,47.9)],
     "유럽에서 가장 긴 강. 러시아를 흐름", "Europe's longest river, flowing through Russia"),
    ("DANUBE", "다뉴브강", "Danube", [(48,8.2),(48.3,14.3),(47.5,19.1),(44.8,20.5),(44,25.9),(45.2,29.7)],
     "여러 유럽 국가를 거쳐 흑해로 흘러드는 강", "Flows through many European countries to the Black Sea"),
    ("GANGES", "갠지스강", "Ganges", [(30.9,78.9),(27.6,80.9),(25.6,85.1),(24.1,88.1),(22.3,90.5)],
     "인도에서 신성시되는 강", "A river considered sacred in India"),
    ("INDUS", "인더스강", "Indus", [(32.5,79.7),(35.3,74.7),(33.6,73.0),(28.4,70.3),(24.2,67.5)],
     "인더스 문명이 발원한 강", "The river that gave rise to the Indus Valley Civilization"),
    ("MURRAYDARLING", "머리달링강", "Murray-Darling", [(-28.5,150.5),(-30.5,148),(-34,142),(-34.2,139.3)],
     "호주 최대의 강 유역계", "Australia's largest river system"),
]

def catmull_rom(pts, samples=10):
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

class LCG:
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
    rnd = LCG(seed)
    ctrl_x, ctrl_h = [0], [0]
    x = 0
    while x < n - 1:
        x += rnd.randint(3, 7)
        x = min(x, n - 1)
        is_valley = rnd.rand() < 0.32
        h = rnd.uniform(2.5, 5.5) if is_valley else rnd.uniform(7, 13)
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

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VB_W} {VB_H}">']
svg.append(f'<rect width="{VB_W}" height="{VB_H}" fill="#0C1220"/>')
svg.append('<g fill="rgba(255,255,255,.08)" stroke="rgba(255,255,255,.15)" stroke-width="0.6">')
for d in land_paths:
    svg.append(f'<path d="{d}"/>')
svg.append('</g>')

regions = []

svg.append('<g>')
for rid, ko, en, path, hko, hen in MOUNTAINS:
    raw = [geo(la, lo) for la, lo in path]
    pts = catmull_rom(raw, samples=16)
    tg = tangents(pts)
    n = len(pts)
    seed = sum(ord(c) for c in ko) * 977
    hs = ridge_heights(n, seed)
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
    svg.append(f'<path id="r{rid}" data-id="{rid}" data-ko="{ko}" data-en="{en}" data-grp="MOUNTAIN" d="{d}" '
                f'stroke-width="0.6" stroke-linejoin="round" stroke-linecap="round"/>')
    regions.append({"id": rid, "svgPathId": f"r{rid}", "names": {"ko": ko, "en": en}, "hints": {"ko": hko, "en": hen}})
svg.append('</g>')

svg.append('<g>')
for rid, ko, en, path, hko, hen in RIVERS:
    raw = [geo(la, lo) for la, lo in path]
    pts = catmull_rom(raw, samples=14)
    tg = tangents(pts)
    n = len(pts)
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        t = i / (n - 1)
        w = 2.2 + t * 4.2  # 클릭 가능하도록 참고용 이미지보다 다소 두껍게(발원지→하구)
        txn, tyn = tg[i]
        nx, ny = -tyn, txn
        left.append((x + nx*w, y + ny*w))
        right.append((x - nx*w, y - ny*w))
    d = ('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in left) +
         ' L' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in reversed(right)) + ' Z')
    svg.append(f'<path id="r{rid}" data-id="{rid}" data-ko="{ko}" data-en="{en}" data-grp="RIVER" d="{d}" '
                f'stroke-width="0.8" stroke-linejoin="round"/>')
    regions.append({"id": rid, "svgPathId": f"r{rid}", "names": {"ko": ko, "en": en}, "hints": {"ko": hko, "en": hen}})
svg.append('</g>')
svg.append('</svg>')

with open('maps/world/world-mountains-rivers.svg', 'w', encoding='utf-8') as f:
    f.write(''.join(svg))

out = {
    "meta": {
        "id": "world-mountains-rivers",
        "mapSvg": "/maps/world/world-mountains-rivers.svg",
        "defaultLang": "ko",
        "totalRegions": len(regions),
        "mildZoom": True
    },
    "regions": regions
}
with open('data/quiz-world-mountains-rivers.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f'저장 완료: maps/world/world-mountains-rivers.svg, data/quiz-world-mountains-rivers.json ({len(regions)}개 지역)')
