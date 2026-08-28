# -*- coding: utf-8 -*-
import json

gj_path = 'node_modules/japan-choropleth/data/geojson/prefectures.geojson'
with open(gj_path, encoding='utf-8') as f:
    data = json.load(f)

# Prefecture code -> (romaji id, ko name, en name)
PREF_INFO = {
    '01': ('HOK', '홋카이도', 'Hokkaido'),
    '02': ('AOM', '아오모리현', 'Aomori'),
    '03': ('IWT', '이와테현', 'Iwate'),
    '04': ('MYG', '미야기현', 'Miyagi'),
    '05': ('AKT', '아키타현', 'Akita'),
    '06': ('YMG', '야마가타현', 'Yamagata'),
    '07': ('FKS', '후쿠시마현', 'Fukushima'),
    '08': ('IBR', '이바라키현', 'Ibaraki'),
    '09': ('TCG', '도치기현', 'Tochigi'),
    '10': ('GNM', '군마현', 'Gunma'),
    '11': ('SIT', '사이타마현', 'Saitama'),
    '12': ('CHB', '지바현', 'Chiba'),
    '13': ('TKY', '도쿄도', 'Tokyo'),
    '14': ('KNG', '가나가와현', 'Kanagawa'),
    '15': ('NGT', '니가타현', 'Niigata'),
    '16': ('TYM', '도야마현', 'Toyama'),
    '17': ('ISK', '이시카와현', 'Ishikawa'),
    '18': ('FKI', '후쿠이현', 'Fukui'),
    '19': ('YNS', '야마나시현', 'Yamanashi'),
    '20': ('NGN', '나가노현', 'Nagano'),
    '21': ('GIF', '기후현', 'Gifu'),
    '22': ('SZO', '시즈오카현', 'Shizuoka'),
    '23': ('AIC', '아이치현', 'Aichi'),
    '24': ('MIE', '미에현', 'Mie'),
    '25': ('SIG', '시가현', 'Shiga'),
    '26': ('KYT', '교토부', 'Kyoto'),
    '27': ('OSK', '오사카부', 'Osaka'),
    '28': ('HYG', '효고현', 'Hyogo'),
    '29': ('NAR', '나라현', 'Nara'),
    '30': ('WKY', '와카야마현', 'Wakayama'),
    '31': ('TTR', '돗토리현', 'Tottori'),
    '32': ('SMN', '시마네현', 'Shimane'),
    '33': ('OKY', '오카야마현', 'Okayama'),
    '34': ('HRS', '히로시마현', 'Hiroshima'),
    '35': ('YGC', '야마구치현', 'Yamaguchi'),
    '36': ('TKS', '도쿠시마현', 'Tokushima'),
    '37': ('KGW', '가가와현', 'Kagawa'),
    '38': ('EHM', '에히메현', 'Ehime'),
    '39': ('KCH', '고치현', 'Kochi'),
    '40': ('FKO', '후쿠오카현', 'Fukuoka'),
    '41': ('SAG', '사가현', 'Saga'),
    '42': ('NGS', '나가사키현', 'Nagasaki'),
    '43': ('KMM', '구마모토현', 'Kumamoto'),
    '44': ('OIT', '오이타현', 'Oita'),
    '45': ('MYZ', '미야자키현', 'Miyazaki'),
    '46': ('KGS', '가고시마현', 'Kagoshima'),
    '47': ('OKN', '오키나와현', 'Okinawa'),
}

# 8 traditional regions (地方) for color grouping
REGION_GRP = {
    '01':'HOKKAIDO',
    '02':'TOHOKU','03':'TOHOKU','04':'TOHOKU','05':'TOHOKU','06':'TOHOKU','07':'TOHOKU',
    '08':'KANTO','09':'KANTO','10':'KANTO','11':'KANTO','12':'KANTO','13':'KANTO','14':'KANTO',
    '15':'CHUBU','16':'CHUBU','17':'CHUBU','18':'CHUBU','19':'CHUBU','20':'CHUBU','21':'CHUBU','22':'CHUBU','23':'CHUBU',
    '24':'KINKI','25':'KINKI','26':'KINKI','27':'KINKI','28':'KINKI','29':'KINKI','30':'KINKI',
    '31':'CHUGOKU','32':'CHUGOKU','33':'CHUGOKU','34':'CHUGOKU','35':'CHUGOKU',
    '36':'SHIKOKU','37':'SHIKOKU','38':'SHIKOKU','39':'SHIKOKU',
    '40':'KYUSHU','41':'KYUSHU','42':'KYUSHU','43':'KYUSHU','44':'KYUSHU','45':'KYUSHU','46':'KYUSHU','47':'KYUSHU',
}

OKINAWA_CODE = '47'

def iter_coords(geom):
    t = geom['type']
    if t == 'Polygon':
        for ring in geom['coordinates']:
            for pt in ring:
                yield pt
    elif t == 'MultiPolygon':
        for poly in geom['coordinates']:
            for ring in poly:
                for pt in ring:
                    yield pt

# ── 1) 본토(혼슈·홋카이도·규슈·시코쿠) 영역만으로 bbox 계산 → 확대 ──
main_minx = main_miny = float('inf')
main_maxx = main_maxy = float('-inf')
oki_minx = oki_miny = float('inf')
oki_maxx = oki_maxy = float('-inf')

MAIN_LAT_MIN = 29.5  # 규슈 본토(야쿠시마 포함) 아래 아마미 등 원격 도서 제외

for feat in data['features']:
    code = feat['id']
    if code not in PREF_INFO:
        continue
    if code == OKINAWA_CODE:
        for x, y in iter_coords(feat['geometry']):
            oki_minx = min(oki_minx, x); oki_maxx = max(oki_maxx, x)
            oki_miny = min(oki_miny, y); oki_maxy = max(oki_maxy, y)
    else:
        for x, y in iter_coords(feat['geometry']):
            if y < MAIN_LAT_MIN:
                continue  # 가고시마현 원격 도서(아마미 등) bbox 계산에서 제외
            main_minx = min(main_minx, x); main_maxx = max(main_maxx, x)
            main_miny = min(main_miny, y); main_maxy = max(main_maxy, y)

print(f'main lon: {main_minx:.2f} - {main_maxx:.2f}, lat: {main_miny:.2f} - {main_maxy:.2f}')
print(f'okinawa lon: {oki_minx:.2f} - {oki_maxx:.2f}, lat: {oki_miny:.2f} - {oki_maxy:.2f}')

VB_W = 620
PAD = 18

lon_span = main_maxx - main_minx
lat_span = main_maxy - main_miny
scale = (VB_W - 2*PAD) / lon_span

def project(x, y):
    px = (x - main_minx) * scale + PAD
    py = (main_maxy - y) * scale + PAD
    return px, py

MAIN_CONTENT_H = lat_span * scale
INSET_H = 96
VB_H = int(PAD + MAIN_CONTENT_H + 16 + INSET_H + PAD)

# ── Okinawa 인셋 박스 (본토 지도 바로 아래, 좌측 정렬) ──
INSET_X, INSET_Y = 18, int(PAD + MAIN_CONTENT_H + 16)
INSET_W = 150
oki_lon_span = oki_maxx - oki_minx
oki_lat_span = oki_maxy - oki_miny
oki_scale = min((INSET_W - 8) / oki_lon_span, (INSET_H - 8) / oki_lat_span)

def project_okinawa(x, y):
    px = (x - oki_minx) * oki_scale + INSET_X + 4
    py = (oki_maxy - y) * oki_scale + INSET_Y + 4
    return px, py

def douglas_peucker(points, epsilon):
    if len(points) < 3:
        return points
    def perp_dist(pt, a, b):
        (x, y), (ax, ay), (bx, by) = pt, a, b
        dx, dy = bx - ax, by - ay
        if dx == 0 and dy == 0:
            return ((x-ax)**2 + (y-ay)**2) ** 0.5
        t = ((x-ax)*dx + (y-ay)*dy) / (dx*dx + dy*dy)
        t = max(0, min(1, t))
        px, py = ax + t*dx, ay + t*dy
        return ((x-px)**2 + (y-py)**2) ** 0.5
    dmax, idx = 0, 0
    for i in range(1, len(points)-1):
        d = perp_dist(points[i], points[0], points[-1])
        if d > dmax:
            dmax, idx = d, i
    if dmax > epsilon:
        left = douglas_peucker(points[:idx+1], epsilon)
        right = douglas_peucker(points[idx:], epsilon)
        return left[:-1] + right
    else:
        return [points[0], points[-1]]

def ring_to_path(ring, proj_fn, epsilon=0.02):
    pts = douglas_peucker(ring, epsilon)
    if len(pts) < 4:
        pts = ring[::max(1,len(ring)//8)]
    if pts[0] != pts[-1]:
        pts = pts + [pts[0]]
    parts = []
    for i, (x, y) in enumerate(pts):
        px, py = proj_fn(x, y)
        cmd = 'M' if i == 0 else 'L'
        parts.append(f'{cmd}{px:.1f},{py:.1f}')
    parts.append('Z')
    return ' '.join(parts)

def ring_area(ring):
    a = 0
    for i in range(len(ring)-1):
        x1,y1 = ring[i]; x2,y2 = ring[i+1]
        a += x1*y2 - x2*y1
    return abs(a) / 2

def geom_to_path(geom, proj_fn, epsilon=0.02, min_area_ratio=0.02):
    t = geom['type']
    d_parts = []
    if t == 'Polygon':
        for ring in geom['coordinates']:
            d_parts.append(ring_to_path(ring, proj_fn, epsilon))
    elif t == 'MultiPolygon':
        polys = geom['coordinates']
        areas = [ring_area(p[0]) for p in polys]
        max_area = max(areas) if areas else 0
        for poly, area in zip(polys, areas):
            if area < max_area * min_area_ratio:
                continue
            outer = poly[0]
            d_parts.append(ring_to_path(outer, proj_fn, epsilon))
    return ' '.join(d_parts)

svg_paths = []
for feat in data['features']:
    code = feat['id']
    if code not in PREF_INFO:
        continue
    rid, ko, en = PREF_INFO[code]
    grp = REGION_GRP[code]
    if code == OKINAWA_CODE:
        d = geom_to_path(feat['geometry'], project_okinawa, epsilon=0.01, min_area_ratio=0.05)
    else:
        d = geom_to_path(feat['geometry'], project, epsilon=0.03, min_area_ratio=0.06)
    svg_paths.append(f'<path id="r{rid}" data-id="{rid}" data-ko="{ko}" data-en="{en}" data-grp="{grp}" d="{d}"/>')

# Okinawa 인셋 박스 테두리 + 라벨
inset_box = (
    f'<rect x="{INSET_X}" y="{INSET_Y}" width="{INSET_W}" height="{INSET_H}" '
    f'fill="none" stroke="rgba(255,255,255,.25)" stroke-width="1" stroke-dasharray="3,2" rx="6"/>'
    f'<text x="{INSET_X+6}" y="{INSET_Y-6}" font-size="11" fill="rgba(255,255,255,.5)">오키나와</text>'
)

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VB_W} {VB_H}">
<g id="regions">
{chr(10).join(svg_paths)}
</g>
<g id="inset-deco" pointer-events="none">
{inset_box}
</g>
</svg>
'''

with open('maps/world/japan.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

print(f'Wrote maps/world/japan.svg ({len(svg_content)} bytes, {len(svg_paths)} prefectures)')
