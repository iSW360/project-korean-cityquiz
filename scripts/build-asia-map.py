# -*- coding: utf-8 -*-
"""아시아 나라 퀴즈 SVG/JSON 생성. Natural Earth 1:50m 국가 경계(Public Domain) 사용.
너무 작아 폴리곤으로 그리면 점밖에 안 보이는 지역(마카오·홍콩·싱가포르·바레인 등)과
비주권/분쟁지역(북키프로스·시아첸 빙하 등)은 정사각형 마커 대신 아예 퀴즈에서 제외한다."""
import json

with open('ne_50m_countries.geojson', encoding='utf-8') as f:
    d = json.load(f)

EXCLUDE = {
    'IOA',  # 무인 해양지역
    'KAS',  # 시아첸 빙하(분쟁지역, 국가 아님)
    'CYN',  # 북키프로스(미승인국)
    'MAC', 'HKG',  # 마카오·홍콩(특별행정구, 주권국 아님)
    'SGP', 'BHR',  # 실제 국경 폴리곤이 3~4px 수준이라 표현 불가 → 제외
}

# Natural Earth 기본 한국어명 중 일부를 더 통용되는 명칭으로 교체
NAME_KO_OVERRIDE = {
    'TWN': '대만', 'PRK': '북한', 'CHN': '중국', 'TUR': '튀르키예',
}

HINTS = {
    'CHN': ("세계 최대 인구 대국 중 하나. 만리장성·자금성. 세계 2위 경제 대국", "One of the world's most populous nations; the Great Wall and Forbidden City"),
    'MNG': ("칭기즈칸의 나라. 세계에서 인구밀도가 가장 낮은 나라 중 하나. 광활한 초원", "Homeland of Genghis Khan; one of the world's least densely populated countries"),
    'KOR': ("한강의 기적. K-pop·반도체 강국. 서울이 수도", "Rapid postwar growth known as the 'Miracle on the Han River'; K-pop and semiconductors"),
    'PRK': ("한반도 북부. 평양이 수도. 세계에서 가장 폐쇄적인 나라 중 하나", "Occupies the northern Korean peninsula; capital Pyongyang"),
    'JPN': ("후지산·벚꽃·스시. 세계 3위 경제 대국. 섬나라(4개 주요 섬)", "Mount Fuji, cherry blossoms, sushi; the world's third-largest economy"),
    'TWN': ("반도체 파운드리 세계 1위(TSMC). 타이베이 101. 중국과 양안 관계", "World-leading semiconductor foundries (TSMC); Taipei 101"),
    'IND': ("세계 최대 인구국. 타지마할. IT·영화산업(발리우드) 강국", "The world's most populous country; the Taj Mahal; a major IT and film (Bollywood) hub"),
    'PAK': ("인더스 문명 발상지. 카라코람 하이웨이. 이슬라마바드가 수도", "Cradle of the Indus Valley Civilization; capital Islamabad"),
    'BGD': ("세계에서 인구밀도가 가장 높은 나라 중 하나. 벵골만 삼각주", "One of the world's most densely populated countries; delta of the Bay of Bengal"),
    'NPL': ("에베레스트가 있는 나라. 히말라야 등반의 중심지", "Home to Mount Everest; a hub for Himalayan mountaineering"),
    'BTN': ("국민총행복지수(GNH)를 국가 정책으로 삼는 나라. 히말라야 소국", "A Himalayan kingdom known for measuring 'Gross National Happiness'"),
    'LKA': ("실론티 산지. 인도양의 눈물이라 불리는 섬나라", "Famous for Ceylon tea; an island nation called the 'Teardrop of the Indian Ocean'"),
    'AFG': ("힌두쿠시 산맥. 중앙아시아와 남아시아를 잇는 교차로", "Crossroads between Central and South Asia; the Hindu Kush mountains"),
    'IRN': ("페르시아 문명의 후예. 세계 최대 천연가스 매장량 중 하나", "Heir to Persian civilization; among the world's largest natural gas reserves"),
    'IDN': ("세계 최대 도서국(1만 7천여 개 섬). 세계 최대 무슬림 인구국", "The world's largest archipelago nation (~17,000 islands); most populous Muslim-majority country"),
    'MYS': ("페트로나스 트윈타워. 말레이반도와 보르네오섬에 걸친 나라", "Home to the Petronas Twin Towers; spans the Malay Peninsula and Borneo"),
    'PHL': ("7천여 개 섬으로 이루어진 나라. 스페인·미국의 식민 지배 역사", "An archipelago of over 7,000 islands with a Spanish and American colonial past"),
    'THA': ("동남아시아에서 유일하게 식민지배를 받지 않은 나라. 방콕·사원 문화", "The only Southeast Asian nation never colonized; Bangkok and Buddhist temples"),
    'VNM': ("S자 모양의 국토. 프랑스 식민지·베트남 전쟁의 역사", "S-shaped territory; history of French colonization and the Vietnam War"),
    'MMR': ("이라와디강 유역. 파고다(불탑)의 나라", "Along the Irrawaddy River; known as the 'Land of Pagodas'"),
    'LAO': ("동남아시아 유일의 내륙국. 메콩강이 국토를 관통", "Southeast Asia's only landlocked country; the Mekong River runs through it"),
    'KHM': ("앙코르와트 유적의 나라. 크메르 제국의 후예", "Home to the Angkor Wat temple complex; heir to the Khmer Empire"),
    'BRN': ("보르네오섬 북부의 소국. 석유·천연가스로 부유한 나라", "A small, oil- and gas-rich nation on the island of Borneo"),
    'TLS': ("21세기 최초의 신생 독립국(2002년 독립). 동남아시아 최연소 국가", "The first new nation of the 21st century, independent since 2002"),
    'KAZ': ("중앙아시아 최대 영토국. 세계 최대 내륙국. 초원지대(스텝)", "Central Asia's largest and the world's largest landlocked country; vast steppe"),
    'UZB': ("실크로드의 중심 도시 사마르칸트가 있는 나라", "Home to Samarkand, a legendary Silk Road city"),
    'TKM': ("투르크메니스탄 사막의 '지옥의 문'(다르바자 가스 분화구)", "Home to the 'Door to Hell' gas crater at Darvaza"),
    'KGZ': ("톈산산맥의 나라. 유목 문화가 남아있는 중앙아시아 국가", "A Tian Shan mountain nation with strong nomadic traditions"),
    'TJK': ("파미르고원('세계의 지붕')이 있는 중앙아시아 산악국", "A mountainous Central Asian nation home to the Pamir 'Roof of the World'"),
    'TUR': ("유럽과 아시아에 걸친 나라. 이스탄불(보스포루스 해협)", "Straddles Europe and Asia; Istanbul sits on the Bosphorus Strait"),
    'SAU': ("이슬람 성지 메카·메디나가 있는 나라. 세계 최대 석유 수출국", "Home to the Islamic holy cities of Mecca and Medina; the top oil exporter"),
    'IRQ': ("메소포타미아 문명 발상지(티그리스·유프라테스강)", "Cradle of Mesopotamian civilization between the Tigris and Euphrates"),
    'SYR': ("고대 도시 다마스쿠스가 있는 나라. 오랜 내전을 겪음", "Home to ancient Damascus; a country marked by prolonged civil war"),
    'JOR': ("고대 도시 페트라가 있는 나라. 사해가 위치", "Home to the ancient city of Petra and the Dead Sea"),
    'LBN': ("지중해 동안의 작은 나라. 베이루트('중동의 파리')", "A small Mediterranean nation; Beirut once called the 'Paris of the Middle East'"),
    'ISR': ("예루살렘이 있는 나라. 사해·갈릴리 호수", "Home to Jerusalem, the Dead Sea, and the Sea of Galilee"),
    'PSX': ("가자지구·요르단강 서안으로 이루어진 지역", "Comprises the Gaza Strip and the West Bank"),
    'CYP': ("지중해의 섬나라. 아프로디테 신화의 배경", "A Mediterranean island nation linked to the myth of Aphrodite"),
    'ARM': ("코카서스산맥 남쪽의 기독교 최초 국교화 국가", "South of the Caucasus; the first nation to adopt Christianity as a state religion"),
    'AZE': ("카스피해 연안의 석유 산업국. 불의 나라라는 별칭", "An oil-rich nation on the Caspian Sea, nicknamed the 'Land of Fire'"),
    'GEO': ("코카서스산맥의 나라. 와인 발상지 중 하나로 꼽힘", "A Caucasus nation often cited as one of the birthplaces of wine"),
    'ARE': ("두바이·아부다비가 있는 연방국가. 부르즈 할리파", "A federation including Dubai and Abu Dhabi; home to the Burj Khalifa"),
    'QAT': ("천연가스 부국. 2022 FIFA 월드컵 개최국", "A gas-rich nation; hosted the 2022 FIFA World Cup"),
    'KWT': ("페르시아만 연안의 석유 부국", "An oil-rich nation on the Persian Gulf"),
    'OMN': ("아라비아반도 동남단의 술탄국", "A sultanate on the southeastern tip of the Arabian Peninsula"),
    'YEM': ("아라비아반도 남단의 나라. 오랜 내전을 겪는 중", "At the southern tip of the Arabian Peninsula; enduring prolonged conflict"),
}

LON0, LON1 = 25, 148
LAT0, LAT1 = -11, 56
VB_W, VB_H = 1160, 670

def geo(lon, lat):
    x = (lon - LON0) / (LON1 - LON0) * VB_W
    y = (LAT1 - lat) / (LAT1 - LAT0) * VB_H
    return x, y

def ring_to_d(ring):
    pts = [geo(lon, lat) for lon, lat in ring]
    return f"M{pts[0][0]:.1f},{pts[0][1]:.1f} " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in pts[1:]) + "Z"

asia = [f for f in d['features'] if f['properties']['CONTINENT'] == 'Asia'
        and f['properties']['ADM0_A3'] not in EXCLUDE]

regions = []
svg_paths = []
for f in asia:
    p = f['properties']
    a3 = p['ADM0_A3']
    ko = NAME_KO_OVERRIDE.get(a3, p.get('NAME_KO') or p['NAME'])
    en = p['NAME']
    geom = f['geometry']
    polys = geom['coordinates'] if geom['type'] == 'MultiPolygon' else [geom['coordinates']]
    d_parts = [ring_to_d(poly[0]) for poly in polys]
    d_attr = ' '.join(d_parts)
    svg_paths.append(f'<path id="r{a3}" data-id="{a3}" data-ko="{ko}" data-en="{en}" d="{d_attr}"/>')
    hko, hen = HINTS.get(a3, (f"{p['SUBREGION']} 소재국", f"A country in {p['SUBREGION']}"))
    regions.append({
        "id": a3, "svgPathId": f"r{a3}",
        "names": {"ko": ko, "en": en},
        "hints": {"ko": hko, "en": hen}
    })

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VB_W} {VB_H}">',
       '<g id="regions">'] + svg_paths + ['</g></svg>']

with open('maps/world/asia.svg', 'w', encoding='utf-8') as f:
    f.write('\n'.join(svg))

out = {
    "meta": {"id": "asia", "mapSvg": "/maps/world/asia.svg", "defaultLang": "ko", "totalRegions": len(regions)},
    "regions": regions
}
with open('data/quiz-asia.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f'저장 완료: {len(regions)}개국 (제외 {len(EXCLUDE)}곳)')
