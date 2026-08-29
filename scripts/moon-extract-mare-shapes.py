# -*- coding: utf-8 -*-
"""USGS 통합 지질도(Mercator)에서 실제 바다(mare) 경계를 색상 플러드필로 추출,
정투영(orthographic) 뷰 좌표로 재투영해 SVG path 생성"""
import json
import math
import cv2
import numpy as np

# ── Mercator 이미지 좌표 보정 (Copernicus/Gassendi 실측 2점 보정) ──
# 패널 크롭 상단을 166px 늘렸으므로(북쪽 여백 확보, 범례와 겹치지 않는 최대치) Y0도 그만큼 보정
X0, SCALE_X = 4424.7, 23.89   # x = X0 + SCALE_X * lon(deg, East+)
Y0, K = 1493.9 + 166, 1437.9  # y = Y0 - K * ln(tan(pi/4 + lat_rad/2))

def merc_xy(lat_deg, lon_deg):
    lat = math.radians(lat_deg)
    x = X0 + SCALE_X * lon_deg
    y = Y0 - K * math.log(math.tan(math.pi/4 + lat/2))
    return x, y

def merc_inv(x, y):
    lon = (x - X0) / SCALE_X
    lat = 2 * (math.atan(math.exp((Y0 - y) / K)) - math.pi/4)
    return math.degrees(lat), lon

with open('scripts/moon-usgs-clean.json', encoding='utf-8') as f:
    USGS = json.load(f)

MARIA_IDS = ["IMBRIUM","SERENITATIS","TRANQUILLITATIS","CRISIUM","FECUNDITATIS","NECTARIS",
             "FRIGORIS","PROCELLARUM","HUMORUM","NUBIUM","VAPORUM","IRIDUM"]

img_bgr = cv2.imread('scripts/moon_geo/mercator_panel_full.jpg')
H, W = img_bgr.shape[:2]
img_lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)  # 색상 유사도 판단에 유리

results = {}
for rid in MARIA_IDS:
    d = USGS[rid]
    cx, cy = merc_xy(d['lat'], d['lon'])
    # bbox 절반 크기를 참고해 crop 반경 결정(넉넉하게 2배)
    half_lon = max((d['max_lon']-d['min_lon'])/2, 3) * SCALE_X * 1.8
    half_lat_deg = max((d['max_lat']-d['min_lat'])/2, 3)
    # 위도 반경을 대략 픽셀로 환산(로컬 근사)
    lat1, lat2 = d['lat']-half_lat_deg, d['lat']+half_lat_deg
    _, y1 = merc_xy(lat1, d['lon']); _, y2 = merc_xy(lat2, d['lon'])
    half_lat_px = abs(y2-y1)/2 * 1.8

    x0c, x1c = int(cx-half_lon), int(cx+half_lon)
    y0c, y1c = int(cy-half_lat_px), int(cy+half_lat_px)
    x0c, y0c = max(0,x0c), max(0,y0c)
    x1c, y1c = min(W,x1c), min(H,y1c)

    # ROI 타원(실제 bbox의 1.35배) — 크롭보다 훨씬 좁게 잡아 같은 색상의 이웃 바다(예: 폭풍의 대양↔비의 바다)로
    # 플러드필이 새는 것을 원천 차단. 크롭은 넉넉히, ROI는 타이트하게.
    roi_rx = half_lon / 1.8 * 1.35
    roi_ry = half_lat_px / 1.8 * 1.35

    crop_lab_raw = img_lab[y0c:y1c, x0c:x1c]
    if crop_lab_raw.size == 0:
        print(f'{rid}: empty crop, skip (likely off top/bottom of panel)')
        continue
    crop_lab = crop_lab_raw
    seed_local = (int(cx-x0c), int(cy-y0c))
    if not (0 <= seed_local[0] < crop_lab.shape[1] and 0 <= seed_local[1] < crop_lab.shape[0]):
        print(f'{rid}: seed out of crop bounds, skip')
        continue

    # 시드가 접촉선 등 경계 픽셀에 걸렸을 경우를 대비해 주변 오프셋도 시도.
    # "가장 넓은 것"이 아니라 "합리적 범위(크롭의 3~65%)에 드는 첫 성공"을 채택 — 최대값은 누출(leak) 위험.
    crop_area = crop_lab.shape[0]*crop_lab.shape[1]
    offsets = [(0,0),(5,0),(-5,0),(0,5),(0,-5),(8,8),(-8,-8),(8,-8),(-8,8)]
    chosen_mask = None
    fallback_mask, fallback_area = None, 0
    for dx,dy in offsets:
        sx, sy = seed_local[0]+dx, seed_local[1]+dy
        if not (0 <= sx < crop_lab.shape[1] and 0 <= sy < crop_lab.shape[0]):
            continue
        mask = np.zeros((crop_lab.shape[0]+2, crop_lab.shape[1]+2), np.uint8)
        cv2.floodFill(crop_lab.copy(), mask, (sx,sy), (255,255,255),
                      loDiff=(20,20,20), upDiff=(20,20,20), flags=cv2.FLOODFILL_MASK_ONLY|8)
        area = int(mask.sum()) / 255  # floodFill mask 값은 255
        ratio = area / crop_area
        if 0.005 <= ratio <= 0.65:
            chosen_mask = mask
            break
        if area > fallback_area:
            fallback_area, fallback_mask = area, mask
    best_mask = chosen_mask if chosen_mask is not None else fallback_mask
    best_area = (chosen_mask.sum()/255) if chosen_mask is not None else fallback_area
    if best_mask is None or best_area < 500:
        print(f'{rid}: flood fill failed (best_area={best_area})')
        continue
    region_mask = (best_mask[1:-1,1:-1] > 0).astype(np.uint8) * 255

    # 노이즈 제거(모폴로지) 후 최대 컨투어
    region_mask = cv2.morphologyEx(region_mask, cv2.MORPH_CLOSE, np.ones((9,9),np.uint8))
    region_mask = cv2.morphologyEx(region_mask, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))
    cnts,_ = cv2.findContours(region_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        print(f'{rid}: no contour found')
        continue
    cnt = max(cnts, key=cv2.contourArea)
    area_px = cv2.contourArea(cnt)
    total_px = region_mask.shape[0]*region_mask.shape[1]
    epsilon = 0.0025 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True).reshape(-1,2)

    # local crop 좌표 -> 전역 Mercator 좌표 -> lat/lon
    latlon_pts = []
    for lx, ly in approx:
        gx, gy = lx+x0c, ly+y0c
        lat, lon = merc_inv(gx, gy)
        latlon_pts.append((lat, lon))

    results[rid] = {"points": latlon_pts, "area_ratio": round(area_px/total_px,3), "n": len(latlon_pts)}
    print(f'{rid}: {len(latlon_pts)} pts, area_ratio={area_px/total_px:.2f}, crop=({x0c},{y0c})-({x1c},{y1c})')

with open('scripts/moon-mare-shapes.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f'\nExtracted {len(results)}/{len(MARIA_IDS)} maria shapes')
