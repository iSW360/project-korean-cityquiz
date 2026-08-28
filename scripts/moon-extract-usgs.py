# -*- coding: utf-8 -*-
import shapefile
import json

sf = shapefile.Reader('scripts/moon_nom/MOON_nomenclature_center_pts.shp')
fields = [f[0] for f in sf.fields[1:]]

# 정확히 일치하는 이름만 (Satellite Feature 등 하위 지형 제외)
PRIMARY = {
    "Mare Imbrium":"IMBRIUM", "Mare Serenitatis":"SERENITATIS", "Mare Tranquillitatis":"TRANQUILLITATIS",
    "Mare Crisium":"CRISIUM", "Mare Fecunditatis":"FECUNDITATIS", "Mare Nectaris":"NECTARIS",
    "Mare Frigoris":"FRIGORIS", "Oceanus Procellarum":"PROCELLARUM", "Mare Humorum":"HUMORUM",
    "Mare Nubium":"NUBIUM", "Mare Vaporum":"VAPORUM", "Sinus Iridum":"IRIDUM",
    "Tycho":"TYCHO", "Copernicus":"COPERNICUS", "Kepler":"KEPLER", "Aristarchus":"ARISTARCHUS",
    "Plato":"PLATO", "Clavius":"CLAVIUS", "Grimaldi":"GRIMALDI", "Gassendi":"GASSENDI",
}

out = {}
for i in range(len(sf)):
    rec = sf.record(i)
    d = dict(zip(fields, rec))
    name = d.get('clean_name') or d.get('name') or ''
    if name in PRIMARY:
        rid = PRIMARY[name]
        lon = float(d['center_lon'])
        if lon > 180:
            lon -= 360
        min_lon = float(d['min_lon']); max_lon = float(d['max_lon'])
        if min_lon > 180: min_lon -= 360
        if max_lon > 180: max_lon -= 360
        out[rid] = {
            "name": name,
            "lat": float(d['center_lat']),
            "lon": lon,
            "diam_km": float(d['diameter']),
            "min_lon": min_lon, "max_lon": max_lon,
            "min_lat": float(d['min_lat']), "max_lat": float(d['max_lat']),
        }

with open('scripts/moon-usgs-clean.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f'Extracted {len(out)}/{len(PRIMARY)} target features')
missing = set(PRIMARY.values()) - set(out.keys())
if missing:
    print('MISSING:', missing)
