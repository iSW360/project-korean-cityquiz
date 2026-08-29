# -*- coding: utf-8 -*-
"""달 앞면 실사 배경 + USGS 공식 데이터(위경도/지름/bbox) + 실사진 대조 보정으로 배치"""
import math
import json

CX, CY, R = 319.5, 326.0, 280.0

def project(lat_deg, lon_deg):
    lat = math.radians(lat_deg)
    lon = math.radians(lon_deg)
    x = CX + R * math.cos(lat) * math.sin(lon)
    y = CY - R * math.sin(lat)
    return x, y

with open('scripts/moon-usgs-clean.json', encoding='utf-8') as f:
    USGS = json.load(f)

MOON_R_KM = 1737.4

def crater_radius_px(diam_km):
    ang_rad = math.asin(min(1.0, (diam_km / 2) / MOON_R_KM))
    return R * ang_rad

def mare_ellipse_px(d):
    cx, cy = project(d['lat'], d['lon'])
    corners = [
        (d['min_lat'], d['min_lon']), (d['min_lat'], d['max_lon']),
        (d['max_lat'], d['min_lon']), (d['max_lat'], d['max_lon']),
    ]
    xs, ys = [], []
    for la, lo in corners:
        px, py = project(la, lo)
        xs.append(px); ys.append(py)
    rx = (max(xs) - min(xs)) / 2
    ry = (max(ys) - min(ys)) / 2
    return cx, cy, max(rx, 8), max(ry, 8)

HINTS = {
    "IMBRIUM": ("비의 바다","Mare Imbrium","달에서 가장 큰 바다(지름 약 1,145km). 약 39억 년 전 거대 충돌로 형성된 분지","Moon's largest mare (~1,145km across); formed by a giant impact ~3.9 billion years ago"),
    "SERENITATIS": ("청명의 바다","Mare Serenitatis","아폴로 17호가 착륙한 곳 인근. 현무암 용암으로 채워진 원형 분지","Near the Apollo 17 landing site; a circular basin filled with basalt lava"),
    "TRANQUILLITATIS": ("고요의 바다","Mare Tranquillitatis","1969년 아폴로 11호가 인류 최초로 착륙한 곳","Site of humanity's first Moon landing, Apollo 11 (1969)"),
    "CRISIUM": ("위난의 바다","Mare Crisium","달 동쪽 끝의 독립된 원형 바다. 지구에서 맨눈으로도 뚜렷이 보임","An isolated round mare near the Moon's eastern limb; clearly visible to the naked eye from Earth"),
    "FECUNDITATIS": ("풍요의 바다","Mare Fecunditatis","소련 루나 16호가 최초로 무인 샘플 채취에 성공한 곳","Where the Soviet Luna 16 mission achieved the first robotic sample return"),
    "NECTARIS": ("감로의 바다","Mare Nectaris","아폴로 16호 착륙지 인근의 비교적 작은 원형 바다","A relatively small circular mare near the Apollo 16 landing site"),
    "FRIGORIS": ("냉담의 바다","Mare Frigoris","달 북쪽을 가로지르는 좁고 긴 띠 모양의 바다","A long, narrow mare stretching across the Moon's northern region"),
    "PROCELLARUM": ("폭풍의 대양","Oceanus Procellarum","달에서 가장 넓은 용암 평원(대양). 아폴로 12호가 착륙한 곳","The Moon's largest lava plain (ocean); site of the Apollo 12 landing"),
    "HUMORUM": ("습기의 바다","Mare Humorum","가상디 분화구와 인접한 원형 바다","A circular mare adjacent to the Gassendi crater"),
    "NUBIUM": ("구름의 바다","Mare Nubium","서베이어 5호가 착륙했던 비교적 평탄한 용암 바다","A relatively flat lava mare where Surveyor 5 landed"),
    "VAPORUM": ("증기의 바다","Mare Vaporum","달 중앙부에 위치한 작은 바다. 아폴로 착륙지들 사이에 위치","A small mare near the Moon's center, situated among several Apollo landing sites"),
    "IRIDUM": ("무지개의 만","Sinus Iridum","비의 바다 북서쪽 가장자리에 있는 반원형 만. '무지개의 만'이라는 뜻","A semicircular bay on Mare Imbrium's northwest rim, meaning 'Bay of Rainbows'"),
    "TYCHO": ("티코","Tycho","약 1억 년 전 형성된 젊은 충돌구. 사방으로 뻗은 광조(光條)가 보름달에 뚜렷함","A young ~100-million-year-old impact crater; its bright ray system is striking at full moon"),
    "COPERNICUS": ("코페르니쿠스","Copernicus","지름 93km의 뚜렷한 광조 분화구. '달의 제왕'이라는 별명","A prominent 93km-wide ray crater nicknamed 'the Monarch of the Moon'"),
    "KEPLER": ("케플러","Kepler","폭풍의 대양에 위치한 밝은 광조 분화구","A bright ray crater located within Oceanus Procellarum"),
    "ARISTARCHUS": ("아리스타르코스","Aristarchus","달 표면에서 가장 밝은 분화구. 지구에서도 쉽게 식별 가능","The brightest crater on the Moon's surface; easily identified from Earth"),
    "PLATO": ("플라토","Plato","비의 바다 북쪽 가장자리의 어두운 용암으로 채워진 분화구","A dark lava-filled crater on the northern edge of Mare Imbrium"),
    "CLAVIUS": ("클라비우스","Clavius","달에서 가장 큰 분화구 중 하나(지름 231km). 남쪽 고지대에 위치","One of the Moon's largest craters (231km diameter), located in the southern highlands"),
    "GRIMALDI": ("그리말디","Grimaldi","달의 서쪽 가장자리 부근의 매우 어두운 용암 바닥 분화구","A very dark lava-floored crater near the Moon's western limb"),
    "GASSENDI": ("가상디","Gassendi","습기의 바다 북쪽 가장자리, 균열이 많은 분화구 바닥으로 유명","On the northern rim of Mare Humorum, famous for its heavily fractured floor"),
}

MARIA_IDS = ["IMBRIUM","SERENITATIS","TRANQUILLITATIS","CRISIUM","FECUNDITATIS","NECTARIS",
             "FRIGORIS","PROCELLARUM","HUMORUM","NUBIUM","VAPORUM","IRIDUM"]

# 실사진 대조 검증 결과: 공식 위경도 정투영이 남반구·주변부에서 최대 40px 어긋나
# Hough 원 검출 + 수동 그리드 판독으로 보정한 값(px, 원본 640x640 기준).
# None인 항목은 정투영 공식값을 그대로 사용(교차검증에서 실사와 일치 확인됨).
CRATER_OVERRIDE = {
    "TYCHO":       (250, 486, 15),   # Hough 검출 + 실사 확인
    "COPERNICUS":  (263, 230, 22),   # 실사 격자 판독으로 확인된 광조 분화구 중심
    "KEPLER":      None,             # 공식값 유지, 클릭 영역만 넉넉히
    "ARISTARCHUS": None,
    "PLATO":       None,             # 실사와 정확히 일치 확인
    "CLAVIUS":     (271, 564, 28),   # Hough 검출
    "GRIMALDI":    None,             # 실사와 정확히 일치 확인
    "GASSENDI":    (152, 411, 14),   # Hough 검출
}
# 위치 불확실성이 남은 항목은 클릭 반경을 넉넉히 키워 실사 위치와의 오차를 흡수
CRATER_MIN_RADIUS = {
    "TYCHO":15, "COPERNICUS":22, "KEPLER":18, "ARISTARCHUS":16,
    "PLATO":16, "CLAVIUS":28, "GRIMALDI":19, "GASSENDI":14,
}

def ellipse_path(cx, cy, rx, ry, n=24):
    pts = []
    for i in range(n):
        ang = 2 * math.pi * i / n
        pts.append((cx + rx * math.cos(ang), cy + ry * math.sin(ang)))
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f} " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in pts[1:]) + " Z"
    return d

def points_path(pts):
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f} " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in pts[1:]) + " Z"
    return d

# 우선순위: USGS 지질도(Unified Geologic Map of the Moon, 공공저작물) 색상 플러드필 트레이싱 > 타원 근사
# ※ 나무위키 소스(namu.wiki)는 사이트 기본 라이선스가 CC BY-NC-SA(비영리)이고 개별 파일의
#   CC0 여부를 확인할 수 없어(캡차로 출처 확인 불가) 상업 서비스 안전을 위해 사용하지 않음.
try:
    with open('scripts/moon-mare-shapes.json', encoding='utf-8') as f:
        TRACED = json.load(f)
except FileNotFoundError:
    TRACED = {}

paths = []
markers = []
for rid in MARIA_IDS:
    ko, en, hko, hen = HINTS[rid]
    if rid in TRACED:
        latlon_pts = TRACED[rid]['points']
        pts = [project(la, lo) for la, lo in latlon_pts]
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        d = points_path(pts)
        print(f'{rid}: using TRACED shape ({len(pts)} pts)')
    else:
        d_usgs = USGS[rid]
        cx, cy, rx, ry = mare_ellipse_px(d_usgs)
        d = ellipse_path(cx, cy, rx, ry)
        print(f'{rid}: using ellipse fallback')
    paths.append(f'<path id="r{rid}" data-id="{rid}" data-ko="{ko}" data-en="{en}" data-grp="MARE" d="{d}"/>')
    markers.append((rid, "MARE", cx, cy))

for rid in CRATER_OVERRIDE:
    override = CRATER_OVERRIDE[rid]
    if override:
        cx, cy, radius = override
    else:
        d_usgs = USGS[rid]
        cx, cy = project(d_usgs['lat'], d_usgs['lon'])
        radius = max(crater_radius_px(d_usgs['diam_km']), CRATER_MIN_RADIUS[rid])
    radius = max(radius, CRATER_MIN_RADIUS[rid])
    ko, en, hko, hen = HINTS[rid]
    d = ellipse_path(cx, cy, radius, radius, n=20)
    paths.append(f'<path id="r{rid}" data-id="{rid}" data-ko="{ko}" data-en="{en}" data-grp="CRATER" d="{d}"/>')
    markers.append((rid, "CRATER", cx, cy))

with open('scripts/moon-bg-b64.txt', encoding='ascii') as f:
    b64 = f.read().strip()

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640">
<defs><clipPath id="moondisk"><circle cx="{CX}" cy="{CY}" r="{R-1}"/></clipPath></defs>
<image href="data:image/jpeg;base64,{b64}" x="0" y="0" width="640" height="640" preserveAspectRatio="xMidYMid slice"/>
<g id="regions" clip-path="url(#moondisk)">
{chr(10).join(paths)}
</g>
</svg>
'''

with open('maps/world/moon.svg', 'w', encoding='utf-8') as f:
    f.write(svg)

print(f'Wrote maps/world/moon.svg: {len(MARIA_IDS)} maria + {len(CRATER_OVERRIDE)} craters = {len(paths)} regions, {len(svg)} bytes')

regions = []
for rid in MARIA_IDS + list(CRATER_OVERRIDE.keys()):
    ko, en, hko, hen = HINTS[rid]
    regions.append({"id": rid, "svgPathId": f"r{rid}", "names": {"ko": ko, "en": en}, "hints": {"ko": hko, "en": hen}})

out = {
    "meta": {"id": "moon", "mapSvg": "/maps/world/moon.svg", "defaultLang": "ko", "totalRegions": len(regions)},
    "regions": regions
}
with open('data/quiz-moon.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f'Wrote data/quiz-moon.json with {len(regions)} regions')
