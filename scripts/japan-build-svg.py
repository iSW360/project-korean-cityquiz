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

# Compute bounding box across all coordinates
minx = miny = float('inf')
maxx = maxy = float('-inf')

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

for feat in data['features']:
    for x, y in iter_coords(feat['geometry']):
        minx = min(minx, x); maxx = max(maxx, x)
        miny = min(miny, y); maxy = max(maxy, y)

print(f'lon range: {minx} - {maxx}')
print(f'lat range: {miny} - {maxy}')

# viewBox target size
VB_W = 620
VB_H = 760
PAD = 20

lon_span = maxx - minx
lat_span = maxy - miny
scale = min((VB_W - 2*PAD) / lon_span, (VB_H - 2*PAD) / lat_span)

def project(x, y):
    # lon -> x (increases eastward), lat -> y (flip, north is up = smaller y)
    px = (x - minx) * scale + PAD
    py = (maxy - y) * scale + PAD
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

def ring_to_path(ring, epsilon=0.02):
    pts = douglas_peucker(ring, epsilon)
    if len(pts) < 4:
        pts = ring[::max(1,len(ring)//8)]
    if pts[0] != pts[-1]:
        pts = pts + [pts[0]]
    parts = []
    for i, (x, y) in enumerate(pts):
        px, py = project(x, y)
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

def geom_to_path(geom, epsilon=0.02, min_area_ratio=0.01):
    t = geom['type']
    d_parts = []
    if t == 'Polygon':
        for ring in geom['coordinates']:
            d_parts.append(ring_to_path(ring, epsilon))
    elif t == 'MultiPolygon':
        polys = geom['coordinates']
        areas = [ring_area(p[0]) for p in polys]
        max_area = max(areas) if areas else 0
        for poly, area in zip(polys, areas):
            if area < max_area * min_area_ratio:
                continue
            outer = poly[0]
            d_parts.append(ring_to_path(outer, epsilon))
    return ' '.join(d_parts)

svg_paths = []
for feat in data['features']:
    code = feat['id']
    if code not in PREF_INFO:
        continue
    rid, ko, en = PREF_INFO[code]
    d = geom_to_path(feat['geometry'], epsilon=0.03, min_area_ratio=0.02)
    svg_paths.append(f'<path id="r{rid}" data-id="{rid}" data-ko="{ko}" data-en="{en}" d="{d}"/>')

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VB_W} {VB_H}">
<g id="regions">
{chr(10).join(svg_paths)}
</g>
</svg>
'''

with open('maps/world/japan.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

print(f'Wrote maps/world/japan.svg ({len(svg_content)} bytes, {len(svg_paths)} prefectures)')
