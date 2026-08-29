# -*- coding: utf-8 -*-
"""트레이싱된 바다 폴리곤끼리 겹치는 부분을 shapely로 제거.
우선순위: 면적이 큰(공식 지름이 큰) 바다가 먼저 영역을 차지하고, 나중 바다는 겹치는 부분을 양보."""
import json
from shapely.geometry import Polygon
from shapely.validation import make_valid

with open('scripts/moon-mare-shapes.json', encoding='utf-8') as f:
    shapes = json.load(f)
with open('scripts/moon-usgs-clean.json', encoding='utf-8') as f:
    USGS = json.load(f)

# 작은(구체적인) 바다부터 처리(공식 지름 오름차순) — 폭풍의 대양처럼 거대한 배경격 바다가
# 특정 이름의 작은 바다를 잠식하지 않도록, 작은 바다가 먼저 자기 영역을 확정하고
# 큰 바다는 나중에 이미 확정된 영역을 피해서 남은 부분만 차지
order = sorted(shapes.keys(), key=lambda rid: USGS[rid]['diam_km'])
print('처리 순서:', order)

polys = {}
for rid in order:
    pts = shapes[rid]['points']
    # (lat, lon) -> (lon, lat) 순서로 shapely에 투입(단순 평면 근사, 이 목적엔 충분)
    coords = [(lon, lat) for lat, lon in pts]
    poly = Polygon(coords)
    if not poly.is_valid:
        poly = make_valid(poly)
        if poly.geom_type == 'MultiPolygon':
            poly = max(poly.geoms, key=lambda g: g.area)
    polys[rid] = poly

claimed = None
result = {}
for rid in order:
    poly = polys[rid]
    if claimed is not None:
        poly = poly.difference(claimed)
    if poly.is_empty:
        print(f'{rid}: 겹침 제거 후 영역 없음 - 원본 유지')
        poly = polys[rid]
    if poly.geom_type == 'MultiPolygon':
        poly = max(poly.geoms, key=lambda g: g.area)
    result[rid] = poly
    claimed = poly if claimed is None else claimed.union(poly)

# 결과를 다시 (lat, lon) 포인트 리스트로 저장
out = {}
for rid, poly in result.items():
    coords = list(poly.exterior.coords)
    pts = [(lat, lon) for lon, lat in coords]
    out[rid] = {"points": pts, "n": len(pts)}
    print(f'{rid}: {len(pts)} pts (deoverlapped)')

with open('scripts/moon-mare-shapes.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print('저장 완료')
