"""미국·유럽·아프리카 지도 아이콘 SVG 생성 (NE 50m 데이터 활용)"""
import json, math
from shapely.ops import unary_union
from shapely.geometry import shape

with open('ne_50m_countries.geojson', encoding='utf-8') as f:
    features = json.load(f)['features']

def get_feat(iso=None, name=None):
    for f in features:
        p = f['properties']
        if iso and p.get('ISO_A3') == iso: return f
        if name and p.get('NAME') == name: return f
    return None

AFRICA_ISO = {'DZA','AGO','BEN','BWA','BFA','BDI','CMR','CPV','CAF','TCD',
    'COM','COD','COG','DJI','EGY','GNQ','ERI','SWZ','ETH','GAB','GMB',
    'GHA','GIN','GNB','CIV','KEN','LSO','LBR','LBY','MDG','MWI','MLI',
    'MRT','MUS','MAR','MOZ','NAM','NER','NGA','RWA','STP','SEN','SLE',
    'SOM','ZAF','SSD','SDN','TZA','TGO','TUN','UGA','ZMB','ZWE','SYC'}
EUROPE_ISO = {'ALB','AND','AUT','BLR','BEL','BIH','BGR','HRV','CYP','CZE',
    'DNK','EST','FIN','DEU','GRC','HUN','ISL','IRL','ITA','LVA','LIE',
    'LTU','LUX','MLT','MDA','MCO','MNE','NLD','MKD','NOR','POL','PRT',
    'ROU','RUS','SMR','SRB','SVK','SVN','ESP','SWE','CHE','TUR','UKR','GBR','VAT'}

# ── Douglas-Peucker ──────────────────────────────────────────────────────────
def _d(px,py,ax,ay,bx,by):
    dx,dy=bx-ax,by-ay
    if dx==0 and dy==0: return math.hypot(px-ax,py-ay)
    t=max(0,min(1,((px-ax)*dx+(py-ay)*dy)/(dx*dx+dy*dy)))
    return math.hypot(px-(ax+t*dx),py-(ay+t*dy))
def dp(pts,eps):
    if len(pts)<3: return pts
    dm,idx=0,0
    a,b=pts[0],pts[-1]
    for i in range(1,len(pts)-1):
        d=_d(pts[i][0],pts[i][1],a[0],a[1],b[0],b[1])
        if d>dm: dm,idx=d,i
    if dm>=eps: return dp(pts[:idx+1],eps)[:-1]+dp(pts[idx:],eps)
    return [pts[0],pts[-1]]

# ── SVG 아이콘 생성 ──────────────────────────────────────────────────────────
def make_icon(geom, path, color='#3ECFB2', W=100, H=100, pad=5, eps=1.2,
              lon_clip=None, lat_clip=None):
    """geom: shapely geometry → SVG 파일 저장"""
    # 경계 클리핑
    minx,miny,maxx,maxy = geom.bounds
    if lon_clip: minx=max(minx,lon_clip[0]); maxx=min(maxx,lon_clip[1])
    if lat_clip: miny=max(miny,lat_clip[0]); maxy=min(maxy,lat_clip[1])

    gw=maxx-minx; gh=maxy-miny
    scale=min((W-2*pad)/gw, (H-2*pad)/gh)
    ox=(W-gw*scale)/2 - minx*scale
    oy=(H-gh*scale)/2 + maxy*scale

    def proj(lon,lat):
        if lon_clip and not (lon_clip[0]<=lon<=lon_clip[1]): return None
        if lat_clip and not (lat_clip[0]<=lat<=lat_clip[1]): return None
        return round(ox+lon*scale,1), round(oy-lat*scale,1)

    def ring_to_d(coords):
        pts=[]
        for lon,lat,*_ in coords:
            p=proj(lon,lat)
            if p: pts.append(p)
        if len(pts)<3: return ''
        simp=dp(pts,eps)
        if len(simp)<3: return ''
        return 'M'+' '.join(f'{x},{y}' for x,y in simp)+'Z'

    parts=[]
    def process(g):
        if g.geom_type=='Polygon':
            d=ring_to_d(list(g.exterior.coords))
            if d: parts.append(d)
        elif g.geom_type=='MultiPolygon':
            for poly in g.geoms:
                d=ring_to_d(list(poly.exterior.coords))
                if d: parts.append(d)

    process(geom)

    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">'
         f'<g fill="{color}" fill-opacity="0.85" stroke="#0C1220" stroke-width="0.7">'
         +''.join(f'<path d="{d}"/>' for d in parts)
         +'</g></svg>')
    with open(path,'w',encoding='utf-8') as f:
        f.write(svg)
    print(f'  {path} ({len(parts)} paths)')

print('지도 아이콘 생성 중...')

# ── 미국 (알래스카·하와이 제외, 본토만) ─────────────────────────────────────
usa_f = get_feat('USA') or get_feat(name='United States of America')
if usa_f:
    usa_geom = shape(usa_f['geometry'])
    # 본토만 (Polygon or biggest polygon in MultiPolygon)
    if usa_geom.geom_type == 'MultiPolygon':
        mainland = max(usa_geom.geoms, key=lambda p: p.area)
    else:
        mainland = usa_geom
    make_icon(mainland, 'img/icon-us.svg',
              color='#60B4FF',
              lon_clip=(-128, -65), lat_clip=(24, 50),
              eps=0.8, W=120, H=70)

# ── 유럽 (러시아 제외) ────────────────────────────────────────────────────────
eu_isos = EUROPE_ISO - {'RUS'}
eu_feats = [f for f in features
            if f['properties'].get('ISO_A3') in eu_isos
            or f['properties'].get('NAME') in {'France','Norway'}]
if eu_feats:
    eu_geom = unary_union([shape(f['geometry']) for f in eu_feats if f.get('geometry')])
    make_icon(eu_geom, 'img/icon-europe.svg',
              color='#9B7FD4',
              lon_clip=(-27, 46), lat_clip=(34, 72),
              eps=0.8, W=100, H=90)

# ── 아프리카 ─────────────────────────────────────────────────────────────────
af_feats = [f for f in features
            if f['properties'].get('ISO_A3') in AFRICA_ISO]
if af_feats:
    af_geom = unary_union([shape(f['geometry']) for f in af_feats if f.get('geometry')])
    make_icon(af_geom, 'img/icon-africa.svg',
              color='#E8914B',
              lon_clip=(-20, 55), lat_clip=(-36, 38),
              eps=0.8, W=90, H=100)

print('완료!')
