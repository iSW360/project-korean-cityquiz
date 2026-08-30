# -*- coding: utf-8 -*-
"""달 뒷면 퀴즈 — NASA LRO 정투영 사진(180°E, 0° 중심, public domain) 위에
뒷면 착륙지(창어 4·6호) + 주요 지형을 배치"""
import math
import json

CX, CY, R = 319.5, 319.5, 318.0
LON0 = 180.0  # 이 사진의 투영 중심 경도(파일 설명에 명시)

MOON_R_KM = 1737.4
def radius_px(diam_km):
    ang = math.asin(min(1.0, (diam_km/2)/MOON_R_KM))
    return R * ang

def project(lat_deg, lon_deg):
    lat = math.radians(lat_deg)
    lon = math.radians(lon_deg - LON0)
    # 뒷면(180도 반대편)에서 바라보는 시점이라 동경 방향이 좌우 반전됨
    x = CX - R * math.cos(lat) * math.sin(lon)
    y = CY - R * math.sin(lat)
    return x, y

# (id, 한글명, 영문명, 위도, 경도, 지름km, 힌트ko, 힌트en, grp)
# ※ 착륙지(창어 4·6호)는 "달 탐사 착륙지" 퀴즈로 통합됨 — 여기는 순수 지형만
ITEMS = [
    ("SPA","사우스폴-에이트켄 분지","South Pole–Aitken Basin", -53.0, 191.0, 2500,
     "태양계에서 가장 크고 오래된 충돌구 중 하나(지름 약 2,500km). 달 남극 부근에 위치",
     "One of the largest and oldest known impact basins in the Solar System (~2,500km across), near the Moon's south pole", "MARE"),
    ("MOSCOVIENSE","모스크바의 바다","Mare Moscoviense", 27.3, 147.9, 277,
     "뒷면에 드물게 존재하는 용암 바다 중 하나. 1959년 소련 루나 3호가 처음 촬영해 명명",
     "One of the few lava maria on the far side; first photographed and named by the Soviet Luna 3 in 1959", "MARE"),
    ("TSIOLKOVSKIY","치올코프스키 분화구","Tsiolkovskiy", -20.4, 128.9, 180,
     "뒷면에서 가장 눈에 띄는 분화구 중 하나. 어두운 용암 바닥과 중앙 봉우리가 특징",
     "One of the most conspicuous far-side craters, notable for its dark lava floor and central peak", "CRATER"),
    ("KOROLEV","코롤료프 분화구","Korolev", 4.4, -164.5, 437,
     "소련 로켓공학자 세르게이 코롤료프의 이름을 딴 대형 분화구(지름 437km)",
     "A large crater (437km diameter) named after Soviet rocket engineer Sergei Korolev", "CRATER"),
    ("APOLLOBASIN","아폴로 분지","Apollo Basin", -36.1, 208.3, 505,
     "사우스폴-에이트켄 분지 안에 있는 대형 충돌구. 창어 6호가 이 안에서 샘플을 채취함",
     "A large impact basin within the South Pole–Aitken Basin; Chang'e 6 collected samples from within it", "CRATER"),
    ("HERTZSPRUNG","헤르츠스프룽 분화구","Hertzsprung", 1.4, -128.9, 570,
     "뒷면에서 가장 큰 분화구 중 하나(지름 570km). 다중 고리 구조를 가진 충돌 분지",
     "One of the largest craters on the far side (570km diameter); a multi-ring impact basin", "CRATER"),
]

paths = []
for rid, ko, en, lat, lon, diam, hko, hen, grp in ITEMS:
    rad = min(radius_px(diam), 100)  # 너무 크게 화면을 덮지 않도록 상한
    cx, cy = project(lat, lon)
    d = f"M{cx-rad:.1f},{cy:.1f} A{rad},{rad} 0 1,0 {cx+rad:.1f},{cy:.1f} A{rad},{rad} 0 1,0 {cx-rad:.1f},{cy:.1f} Z"
    paths.append(f'<path id="r{rid}" data-id="{rid}" data-ko="{ko}" data-en="{en}" data-grp="{grp}" d="{d}"/>')

with open('scripts/moon-farside-bg-b64.txt', 'w', encoding='ascii') as fout:
    import base64
    with open('scripts/moon-farside-bg.jpg', 'rb') as fin:
        fout.write(base64.b64encode(fin.read()).decode('ascii'))
with open('scripts/moon-farside-bg-b64.txt', encoding='ascii') as f:
    b64 = f.read().strip()

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640">
<defs><clipPath id="moondisk"><circle cx="{CX}" cy="{CY}" r="{R-1}"/></clipPath></defs>
<image href="data:image/jpeg;base64,{b64}" x="0" y="0" width="640" height="640" preserveAspectRatio="xMidYMid slice"/>
<g id="regions" clip-path="url(#moondisk)">
{chr(10).join(paths)}
</g>
</svg>
'''
with open('maps/world/moon-farside.svg', 'w', encoding='utf-8') as f:
    f.write(svg)
print(f'Wrote maps/world/moon-farside.svg: {len(ITEMS)} items')

regions = []
for rid, ko, en, lat, lon, diam, hko, hen, grp in ITEMS:
    regions.append({"id": rid, "svgPathId": f"r{rid}", "names": {"ko": ko, "en": en}, "hints": {"ko": hko, "en": hen}})

out = {
    "meta": {"id": "moon-farside", "mapSvg": "/maps/world/moon-farside.svg", "defaultLang": "ko", "totalRegions": len(regions)},
    "regions": regions
}
with open('data/quiz-moon-farside.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f'Wrote data/quiz-moon-farside.json with {len(regions)} regions')
