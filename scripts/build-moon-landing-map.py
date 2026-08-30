# -*- coding: utf-8 -*-
"""달 탐사 착륙지 퀴즈 — 앞면 실사 배경(주 원판) + 뒷면 인셋(작은 원, 일본 지도의
오키나와 인셋과 동일한 패턴)에 각국 착륙지를 점으로 표시.
좌표는 NASA/각국 우주기관 공식 발표 기준(공공 사실 정보, 저작권 문제 없음)."""
import math
import json
import base64

CX, CY, R = 319.5, 326.0, 280.0

def project_near(lat_deg, lon_deg):
    lat = math.radians(lat_deg)
    lon = math.radians(lon_deg)
    x = CX + R * math.cos(lat) * math.sin(lon)
    y = CY - R * math.sin(lat)
    return x, y

# 뒷면 인셋 원판 위치/반지름 (우측 하단)
FX, FY, FR = 520, 545, 90
FAR_LON0 = 180.0

def project_far(lat_deg, lon_deg):
    lat = math.radians(lat_deg)
    lon = math.radians(lon_deg - FAR_LON0)
    x = FX - FR * math.cos(lat) * math.sin(lon)  # 뒷면 시점이라 좌우 반전
    y = FY - FR * math.sin(lat)
    return x, y

# (id, 한글명, 영문명, 위도, 경도, 힌트ko, 힌트en, side) — side: 'near' or 'far'
SITES = [
    ("APOLLO11","아폴로 11호","Apollo 11", 0.6741, 23.4730,
     "1969년 인류 최초의 유인 달 착륙. 닐 암스트롱·버즈 올드린이 고요의 바다에 착륙",
     "Humanity's first crewed Moon landing in 1969; Armstrong and Aldrin landed in Mare Tranquillitatis", "near"),
    ("APOLLO12","아폴로 12호","Apollo 12", -3.0124, -23.4216,
     "1969년 11월. 폭풍의 대양에 착륙, 서베이어 3호 무인탐사선 부품을 회수",
     "November 1969; landed in Oceanus Procellarum and retrieved parts from the robotic Surveyor 3", "near"),
    ("APOLLO14","아폴로 14호","Apollo 14", -3.6453, -17.4714,
     "1970년 아폴로 13호 사고 이후 첫 성공적 유인 착륙. 프라 마우로 지역",
     "First successful crewed landing after the Apollo 13 accident (1971); Fra Mauro region", "near"),
    ("APOLLO15","아폴로 15호","Apollo 15", 26.1008, 3.6527,
     "최초로 달 탐사차(로버)를 사용한 임무. 해들리-아펜니노 지역",
     "First mission to use a lunar rover; Hadley–Apennine region", "near"),
    ("APOLLO16","아폴로 16호","Apollo 16", -8.9734, 15.5011,
     "달 고지대(하이랜드)에 착륙한 첫 임무. 데카르트 지역",
     "First mission to land in the lunar highlands; Descartes region", "near"),
    ("APOLLO17","아폴로 17호","Apollo 17", 20.1908, 30.7717,
     "1972년, 20세기 마지막 유인 달 착륙. 지질학자 슈미트가 참여한 유일한 임무",
     "1972, the last crewed Moon landing of the 20th century; the only mission with a geologist crew member", "near"),
    ("LUNA9","루나 9호","Luna 9", 7.13, -64.37,
     "1966년 소련이 세계 최초로 달 연착륙에 성공한 무인 탐사선",
     "1966; the first spacecraft in history to achieve a soft landing on the Moon (USSR)", "near"),
    ("LUNA16","루나 16호","Luna 16", -0.68, 56.30,
     "1970년, 무인 탐사선 최초로 달 샘플을 채취해 지구로 귀환",
     "1970; the first robotic mission to collect lunar samples and return them to Earth", "near"),
    ("LUNA17","루나 17호","Luna 17", 38.28, -35.0,
     "세계 최초의 달 탐사차 '루노호트 1호'를 실어나른 소련의 무인 임무",
     "Soviet mission that delivered Lunokhod 1, the world's first robotic rover on another world", "near"),
    ("LUNA24","루나 24호","Luna 24", 12.75, 62.2,
     "1976년, 20세기 소련의 마지막 달 탐사 임무",
     "1976; the final Soviet Moon mission of the 20th century", "near"),
    ("CHANGE3","창어 3호","Chang'e 3", 44.12, -19.51,
     "2013년, 중국 최초의 달 연착륙 임무. 위투 로버를 배치",
     "2013; China's first Moon soft-landing mission, deploying the Yutu rover", "near"),
    ("CHANGE5","창어 5호","Chang'e 5", 43.06, -51.92,
     "2020년, 중국 최초로 달 샘플을 채취해 지구로 귀환시킨 임무",
     "2020; China's first sample-return mission from the Moon", "near"),
    ("SLIM","SLIM(슬림)","SLIM", -13.3, 25.2,
     "2024년, 일본 최초의 달 착륙선. 정밀 핀포인트 착륙 기술을 시연",
     "2024; Japan's first Moon lander, demonstrating precision pinpoint landing technology", "near"),
    ("BERESHEET","베레시트","Beresheet", 32.59, 19.35,
     "2019년 이스라엘의 민간 달 착륙 시도. 착륙 직전 통신 두절로 충돌",
     "2019 Israeli private lunar lander attempt; lost contact and crashed just before touchdown", "near"),
    ("CHANGE4","창어 4호","Chang'e 4", -45.5, 177.6,
     "2019년, 인류 최초로 달 뒷면에 연착륙(중국). 폰 카르만 분화구(뒷면)",
     "2019; the first spacecraft to soft-land on the Moon's far side (China); Von Kármán crater (far side)", "far"),
    ("CHANGE6","창어 6호","Chang'e 6", -41.64, 153.99,
     "2024년, 인류 최초로 달 뒷면 샘플을 채취해 귀환(중국). 아폴로 분지(뒷면)",
     "2024; the first mission to return samples from the Moon's far side (China); Apollo basin (far side)", "far"),
]

with open('scripts/moon-bg-b64.txt', encoding='ascii') as f:
    near_b64 = f.read().strip()
with open('scripts/moon-farside-bg.jpg', 'rb') as f:
    far_b64 = base64.b64encode(f.read()).decode('ascii')

paths = []
for rid, ko, en, lat, lon, hko, hen, side in SITES:
    if side == 'near':
        cx, cy = project_near(lat, lon)
    else:
        cx, cy = project_far(lat, lon)
    r = 8 if side == 'near' else 5
    d = f"M{cx-r:.1f},{cy:.1f} A{r},{r} 0 1,0 {cx+r:.1f},{cy:.1f} A{r},{r} 0 1,0 {cx-r:.1f},{cy:.1f} Z"
    paths.append(f'<path id="r{rid}" data-id="{rid}" data-ko="{ko}" data-en="{en}" data-grp="SITE" d="{d}"/>')

far_inset_deco = (
    f'<circle cx="{FX}" cy="{FY}" r="{FR}" fill="none" stroke="rgba(255,255,255,.35)" stroke-width="1.5" stroke-dasharray="3,2"/>'
    f'<text x="{FX-FR}" y="{FY-FR-8}" font-size="11" fill="rgba(255,255,255,.55)">달 뒷면</text>'
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 640">
<defs>
<clipPath id="moondisk"><circle cx="{CX}" cy="{CY}" r="{R-1}"/></clipPath>
<clipPath id="fardisk"><circle cx="{FX}" cy="{FY}" r="{FR-1}"/></clipPath>
</defs>
<image href="data:image/jpeg;base64,{near_b64}" x="0" y="0" width="640" height="640" preserveAspectRatio="xMidYMid slice"/>
<image href="data:image/jpeg;base64,{far_b64}" x="{FX-FR}" y="{FY-FR}" width="{FR*2}" height="{FR*2}" preserveAspectRatio="xMidYMid slice" clip-path="url(#fardisk)"/>
<g id="deco" pointer-events="none">{far_inset_deco}</g>
<g id="regions" clip-path="url(#moondisk)">
{chr(10).join(p for p, s in zip(paths, [s[-1] for s in SITES]) if s == 'near')}
</g>
<g id="regions-far" clip-path="url(#fardisk)">
{chr(10).join(p for p, s in zip(paths, [s[-1] for s in SITES]) if s == 'far')}
</g>
</svg>
'''
with open('maps/world/moon-landing.svg', 'w', encoding='utf-8') as f:
    f.write(svg)
print(f'Wrote maps/world/moon-landing.svg: {len(SITES)} sites (near+far inset)')

regions = []
for rid, ko, en, lat, lon, hko, hen, side in SITES:
    regions.append({"id": rid, "svgPathId": f"r{rid}", "names": {"ko": ko, "en": en}, "hints": {"ko": hko, "en": hen}})

out = {
    "meta": {"id": "moon-landing", "mapSvg": "/maps/world/moon-landing.svg", "defaultLang": "ko", "totalRegions": len(regions), "noZoom": True},
    "regions": regions
}
with open('data/quiz-moon-landing.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f'Wrote data/quiz-moon-landing.json with {len(regions)} regions')
