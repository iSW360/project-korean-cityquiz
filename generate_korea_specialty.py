"""한국 지역 특성 퀴즈 생성 (기존 sigungoo 지도 재사용)"""
import json

# ── 특산물·산업·문화 데이터 ─────────────────────────────────────────────────
# (지역 한국어명, 특성 ko, 특성 en, ko_hint, en_hint)
SPECIALTY = [

# ── 농업 특산물 ──────────────────────────────────────────────────────────────
('이천시','이천 쌀','Icheon Rice',
 '조선 임금님 진상미. 해안분지 일교차가 커 찰지고 윤기나는 최고급 쌀 생산. 경기도 이천시',
 "Royal tribute rice since Joseon; large temperature gap in basin creates premium sticky quality"),
('철원군','철원 쌀','Cheorwon Rice',
 '비무장지대(DMZ) 인접 청정 오대쌀 산지. 용암대지의 비옥한 토양과 맑은 물. 강원도 철원군',
 "Premium Odae rice grown near DMZ; fertile volcanic plateau soil and clean water"),
('논산시','논산 딸기','Nonsan Strawberry',
 '전국 딸기 생산량 1위. 논산딸기축제 개최. 비닐하우스 딸기 재배의 메카. 충청남도 논산시',
 "Korea's #1 strawberry producer; Nonsan Strawberry Festival; greenhouse cultivation hub"),
('담양군','담양 대나무','Damyang Bamboo',
 '전국 대나무 생산 1위. 죽녹원(대나무 숲 공원). 메타세쿼이아 가로수길. 전라남도 담양군',
 "Korea's top bamboo producer; Juknokwon bamboo forest park; famous Metasequoia road"),
('나주시','나주 배','Naju Pear',
 '500년 역사의 배 재배. 황금배 품종으로 유명. 고려·조선 시대 행정 중심지. 전라남도 나주시',
 "500-year pear cultivation history; Hwanggeumbae golden pear; historic Goryeo administrative center"),
('의성군','의성 마늘','Uiseong Garlic',
 '전국 마늘 생산량 1위. 의성마늘 한지형 최고 품종. 고려홍삼보다 알리신 풍부. 경상북도 의성군',
 "Korea's #1 garlic producer; Uiseong hardneck garlic; highest allicin content variety"),
('남해군','남해 마늘·멸치','Namhae Garlic·Anchovy',
 '마늘·멸치 주산지. 독일마을(독일 교포 정착촌). 다랭이논 유명. 경상남도 남해군',
 "Major garlic and anchovy producer; German Village (Korean diaspora settlement); Daraengi terraced fields"),
('보성군','보성 녹차','Boseong Green Tea',
 '국내 녹차 생산량 1위(전체 40%). 녹차밭 경관 드라마·CF 촬영지. 전라남도 보성군',
 "Korea's top green tea producer (40% of total); scenic tea fields famous for drama filming"),
('서귀포시','서귀포 감귤','Seogwipo Citrus',
 '한국 감귤 생산의 중심. 한라봉·천혜향 등 고급 감귤 품종. 제주특별자치도 서귀포시',
 "Korea's citrus capital; Hallabong and Cheonhyehyang premium varieties; subtropical climate"),
('금산군','금산 인삼','Geumsan Ginseng',
 '전국 인삼 거래량 80% 집산. 세계 인삼 교역의 중심. 금산인삼축제. 충청남도 금산군',
 "80% of Korea's ginseng trade; world ginseng trading center; Geumsan Ginseng Festival"),
('영양군','영양 고추','Yeongyang Pepper',
 '고추 재배 최적지(일교차·일조량). 국내 고추 산지 중 최상급 품질. 경상북도 영양군',
 "Optimal pepper growing conditions (temperature gap, sunlight); Korea's premium pepper region"),
('청송군','청송 사과','Cheongsong Apple',
 '경북 내륙 분지 지형에서 자란 최상급 사과. 청송사과는 밀도·당도·색상 3박자. 경상북도 청송군',
 "Premium apples grown in North Gyeongsang inland basin; best density, sweetness and color"),
('영천시','영천 포도','Yeongcheon Grape',
 '국내 최대 포도 주산지. 캠벨얼리·거봉 등 다양한 품종. 와인 생산도 활발. 경상북도 영천시',
 "Korea's largest grape producing region; Campbell Early and Kyoho varieties; growing wine industry"),
('횡성군','횡성 한우','Hoengseong Hanwoo',
 '1++ 등급 한우 브랜드의 대명사. 강원도 청정 환경에서 자란 프리미엄 한우. 강원도 횡성군',
 "Synonymous with 1++ grade Korean beef; premium hanwoo raised in clean Gangwon environment"),
('완도군','완도 전복','Wando Abalone',
 '전국 전복 생산량 80% 담당. 청정 남해 해역. 전복·미역·다시마 양식 메카. 전라남도 완도군',
 "Produces 80% of Korea's abalone; pristine South Sea waters; abalone and seaweed farming hub"),
('고흥군','고흥 유자','Goheung Citrus yuzu',
 '전국 유자 생산량 70% 담당. 유자차·유자청 원료 산지. 나로우주센터 소재지. 전라남도 고흥군',
 "Produces 70% of Korea's yuzu; yuza tea and syrup source; location of Naro Space Center"),
('순창군','순창 고추장','Sunchang Gochujang',
 '조선왕조실록에 기록된 500년 고추장 전통. 순창고추장마을 민속촌. 전라북도 순창군',
 "500-year gochujang tradition recorded in Joseon Dynasty annals; Sunchang Gochujang Folk Village"),
('무안군','무안 양파','Muan Onion',
 '전국 양파 생산량 1위. 황토 토양이 만든 단맛 강한 양파. 무안국제공항 소재지. 전라남도 무안군',
 "Korea's #1 onion producer; red clay soil creates notably sweet onions; home of Muan Airport"),

# ── 공업·산업 지역 ────────────────────────────────────────────────────────────
('포항시','포항 철강','Pohang Steel',
 'POSCO(포스코) 본사·제철소. 한국 철강 산업의 심장. 영일만 입지. 경상북도 포항시',
 "POSCO headquarters and steelworks; heart of Korea's steel industry; Yeongil Bay location"),
('거제시','거제 조선','Geoje Shipbuilding',
 '현대중공업·삼성중공업 조선소. 세계 최대 규모 조선 단지. 경상남도 거제시',
 "Hyundai Heavy Industries and Samsung Heavy Industries shipyards; world-class shipbuilding complex"),
('여수시','여수 석유화학','Yeosu Petrochemical',
 '국내 최대 석유화학 단지(여수국가산업단지). GS칼텍스·LG화학 등 집적. 전라남도 여수시',
 "Korea's largest petrochemical complex; GS Caltex, LG Chem; Yeosu National Industrial Complex"),
('광양시','광양 철강','Gwangyang Steel',
 '포스코 광양제철소(세계 단일 최대 생산 철강소). 광양항 컨테이너 물동량 전국 3위. 전라남도 광양시',
 "POSCO Gwangyang Steelworks (world's largest single-site steel plant); major container port"),
('구미시','구미 전자','Gumi Electronics',
 '삼성전자·LG전자 공장. 한국 전자산업 발상지. 구미국가산업단지. 경상북도 구미시',
 "Samsung and LG Electronics factories; birthplace of Korea's electronics industry; Gumi National Industrial Complex"),
('창원시','창원 기계','Changwon Machinery',
 '두산·한화 방위산업 및 기계 클러스터. 경남 최대 도시. 국가산업단지 1호. 경상남도 창원시',
 "Doosan, Hanwha defense and machinery cluster; Gyeongnam's largest city; Korea's first national industrial complex"),
('파주시','파주 반도체·LCD','Paju Semiconductor·LCD',
 'LG디스플레이 파주공장(세계 최대 LCD 생산). 반도체·디스플레이 클러스터. 경기도 파주시',
 "LG Display Paju plant (world's largest LCD production); semiconductor and display cluster"),
('화성시','화성 반도체','Hwaseong Semiconductor',
 '삼성전자 반도체 최대 생산기지(기흥·화성캠퍼스). D램·낸드플래시 세계 1위 생산. 경기도 화성시',
 "Samsung Electronics largest semiconductor campus; world #1 DRAM and NAND flash production"),

# ── 문화·관광 지역 ────────────────────────────────────────────────────────────
('경주시','경주 역사문화','Gyeongju History',
 '신라 천년 수도. 불국사·석굴암(유네스코). 황리단길. 도시 전체가 노천 박물관. 경상북도 경주시',
 "Silla Kingdom's 1,000-year capital; Bulguksa and Seokguram UNESCO sites; open-air museum city"),
('안동시','안동 유교문화','Andong Confucian Culture',
 '하회마을(유네스코 세계유산). 한국 정신문화의 수도. 안동 소주·간고등어. 경상북도 안동시',
 "Hahoe Village UNESCO World Heritage; Korea's spiritual culture capital; Andong soju and mackerel"),
('전주시','전주 한옥마을·비빔밥','Jeonju Hanok·Bibimbap',
 '전주한옥마을(800채 한옥). 전주비빔밥 발원지. 전주국제영화제. 전라북도 전주시',
 "Jeonju Hanok Village (800 traditional houses); birthplace of bibimbap; Jeonju Int\'l Film Festival"),
('강릉시','강릉 커피·해변','Gangneung Coffee·Beach',
 '커피거리(안목해변) 한국 커피 성지. 정동진·경포해변. 2018 동계올림픽 개최지. 강원도 강릉시',
 "Korea's coffee culture hub (Anmok Beach); Jeongdongjin beach; hosted 2018 Winter Olympics"),
('통영시','통영 굴·예술','Tongyeong Oyster·Arts',
 '동양의 나폴리. 굴 생산 1위 항구도시. 박경리·윤이상 예술가 고향. 경상남도 통영시',
 "Naples of the East; Korea's top oyster port; birthplace of novelist Park Kyong-ni and composer Yun Isang"),
]

# ── 기존 sigungoo JSON에서 svgPathId 조회 ──────────────────────────────────
with open('data/quiz-korea-sigungoo.json', encoding='utf-8') as f:
    sigungoo = json.load(f)

name_to_region = {r['names']['ko']: r for r in sigungoo['regions']}

# ── 퀴즈 JSON 생성 ─────────────────────────────────────────────────────────
regions = []
missing = []

for ko_region, ko_name, en_name, ko_hint, en_hint in SPECIALTY:
    r = name_to_region.get(ko_region)
    if not r:
        missing.append(ko_region)
        continue
    regions.append({
        'id':        r['id'],
        'svgPathId': r['svgPathId'],
        'names':     {'ko': ko_name, 'en': en_name},
        'hints':     {'ko': f'{ko_region} — {ko_hint}', 'en': en_hint},
    })

quiz = {
    'meta': {
        'id': 'korea-specialty',
        'mapSvg': '/maps/korea/sigungoo.svg',
        'defaultLang': 'ko',
        'totalRegions': len(regions),
        'questionText': {
            'ko': '<strong style="color:var(--gold)">강조된 지역</strong>의 대표 특성은?',
            'en': 'What is this region <strong style="color:var(--gold)">best known for</strong>?',
        },
    },
    'regions': regions,
}

with open('data/quiz-korea-specialty.json', 'w', encoding='utf-8') as f:
    json.dump(quiz, f, ensure_ascii=False, indent=2)

print(f'생성 완료: {len(regions)}개 지역')
if missing:
    print(f'누락 (지명 불일치): {missing}')
