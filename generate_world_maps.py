"""
Generate Africa and Europe country quiz maps from Natural Earth 50m data.
Usage: py generate_world_maps.py
"""
import json, math, urllib.request, os, sys

NE_URL   = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson'
NE_CACHE = 'ne_50m_countries.geojson'

# ── Natural Earth NAME → (iso_a3_override) for tricky cases ─────────────────
NAME_FIX = {
    'Czech Republic': 'CZE', 'Czechia': 'CZE',
    'Bosnia and Herz.': 'BIH',
    'Macedonia': 'MKD', 'North Macedonia': 'MKD',
    'Dem. Rep. Congo': 'COD', 'Congo, Dem. Rep.': 'COD',
    'Republic of the Congo': 'COG', 'Congo': 'COG',
    'Sao Tome and Principe': 'STP',
    'eSwatini': 'SWZ', 'Swaziland': 'SWZ',
    'Western Sahara': None,  # exclude
    'Somaliland': None,
    'Kosovo': 'XKX',
    # NE 50m has ISO_A3=-99 for these; match by NAME instead
    'France': 'FRA',
    'Norway': 'NOR',
}

# ── Explicit country sets (ISO A3) ───────────────────────────────────────────
AFRICA_ISO = {
    'DZA','AGO','BEN','BWA','BFA','BDI','CMR','CPV','CAF','TCD',
    'COM','COD','COG','DJI','EGY','GNQ','ERI','SWZ','ETH','GAB',
    'GMB','GHA','GIN','GNB','CIV','KEN','LSO','LBR','LBY','MDG',
    'MWI','MLI','MRT','MUS','MAR','MOZ','NAM','NER','NGA','RWA',
    'STP','SEN','SLE','SOM','ZAF','SSD','SDN','TZA','TGO','TUN',
    'UGA','ZMB','ZWE','SYC',
}
EUROPE_ISO = {
    'ALB','AND','AUT','BLR','BEL','BIH','BGR','HRV','CYP','CZE',
    'DNK','EST','FIN','FRA','DEU','GRC','HUN','ISL','IRL','ITA',
    'XKX','LVA','LIE','LTU','LUX','MLT','MDA','MCO','MNE','NLD',
    'MKD','NOR','POL','PRT','ROU','RUS','SMR','SRB','SVK','SVN',
    'ESP','SWE','CHE','TUR','UKR','GBR','VAT',
}

# ── Country data: iso → (ko_name, en_name, ko_hint, en_hint) ────────────────
DATA = {
# ── Africa ──────────────────────────────────────────────────────────────────
'DZA':('알제리','Algeria',
    '아프리카 최대 면적 국가. 사하라 사막이 국토의 85%. 카스바(알제) 유네스코 세계유산. 지중해·사막 문화 공존',
    "Africa's largest country; 85% Sahara Desert; Kasbah of Algiers UNESCO; Mediterranean meets Saharan culture"),
'AGO':('앙골라','Angola',
    '아프리카 대표 석유 수출국. 커피·다이아몬드 산지. 1975년 포르투갈에서 독립 후 27년 내전',
    "Major African oil exporter; coffee and diamond production; 27-year civil war after independence from Portugal in 1975"),
'BEN':('베냉','Benin',
    '부두교(Voodoo) 발상지. 아프리카 첫 민주주의 전환국(1990). 오요 왕국 역사 유적. 코토누 최대 도시',
    "Birthplace of Voodoo religion; Africa's pioneer of democratic transition (1990); ancient Oyo Kingdom heritage"),
'BWA':('보츠와나','Botswana',
    '세계 최대 다이아몬드 생산국. 오카방고 삼각주 유네스코 세계유산. 아프리카에서 가장 꾸준한 경제 성장률',
    "World's top diamond producer; Okavango Delta UNESCO World Heritage; Africa's longest sustained economic growth"),
'BFA':('부르키나파소','Burkina Faso',
    "'정직한 사람들의 땅' 뜻. 서아프리카 사헬 지역 위기 중심. 세계 최대 면화·가죽 수출국 중 하나",
    "Name means 'Land of Upright People'; Sahel region crisis zone; major cotton and livestock exporter"),
'BDI':('부룬디','Burundi',
    '아프리카 최빈국 중 하나. 탕가니카 호수 접경. 커피 수출 경제. 1994년 대학살 여파로 수십만 명 사망',
    "One of Africa's poorest nations; Lake Tanganyika shores; coffee economy; hundreds of thousands killed in 1990s ethnic conflict"),
'CMR':('카메룬','Cameroon',
    "'아프리카의 축소판' — 열대우림·사바나·산악·해안 공존. 사무엘 에토'o 축구 스타 출신. 영어·프랑스어 공용",
    "'Africa in miniature' — rainforest, savanna, mountains and coast; Samuel Eto'o's birthplace; bilingual (English/French)"),
'CPV':('카보베르데','Cabo Verde',
    '대서양 화산 군도(15개 섬). 모르나 음악(세자리아 에보라)의 나라. 아프리카 최고 민주주의 안정 국가 중 하나',
    "Atlantic volcanic archipelago (15 islands); birthplace of morna music (Cesária Évora); one of Africa's most stable democracies"),
'CAF':('중앙아프리카공화국','Central African Republic',
    '아프리카 대륙 지리적 중심부. 다이아몬드·금·우라늄 매장. 만성적 내전과 인도주의 위기',
    "Geographic heart of Africa; diamond, gold and uranium reserves; chronic civil war and humanitarian crisis"),
'TCD':('차드','Chad',
    '아프리카 5번째 큰 나라. 차드 호수가 수십 년간 90% 감소(기후 위기). 사하라·사헬·수단 사바나 3개 기후대',
    "Africa's 5th largest country; Lake Chad shrank 90% due to climate change; three climate zones: Sahara, Sahel, savanna"),
'COM':('코모로','Comoros',
    '아프리카 연합 소속 섬나라(인도양). 세계 최대 바닐라·정향 수출국. 세계에서 쿠데타가 가장 잦은 나라',
    "Indian Ocean island nation; world's top vanilla and clove exporter; most coup attempts per capita in the world"),
'COD':('콩고민주공화국','DR Congo',
    '아프리카 2번째 큰 나라. 콩고 분지 열대우림(세계 2위). 콜탄(스마트폰 필수 광물) 세계 최대 매장국',
    "Africa's 2nd largest country; Congo Basin rainforest (world's 2nd largest); world's largest coltan reserves for smartphones"),
'COG':('콩고공화국','Republic of Congo',
    '콩고강 서쪽 연안. 석유 수출 경제. 수도 브라자빌은 강 하나 사이로 킨샤사(DRC)와 마주보는 세계에서 가장 가까운 두 수도',
    "West bank of Congo River; oil economy; Brazzaville and Kinshasa face each other across the river — world's closest capital pair"),
'DJI':('지부티','Djibouti',
    '아프리카의 뿔 전략 요충지. 미국·프랑스·중국 군사기지 공존. 아살 호수(세계에서 가장 짠 호수 중 하나)',
    "Strategic Horn of Africa; hosts US, French and Chinese military bases simultaneously; Lake Assal among world's saltiest lakes"),
'EGY':('이집트','Egypt',
    '피라미드·스핑크스(고대 7대 불가사의). 수에즈 운하(세계 해상 무역 12% 담당). 나일강 문명 발상지',
    "Pyramids and Sphinx (ancient world wonder); Suez Canal (12% of global maritime trade); cradle of Nile civilization"),
'GNQ':('적도기니','Equatorial Guinea',
    '아프리카에서 유일한 스페인어 공용국. 석유 발견 후 1인당 GDP 아프리카 최고. 비오코 섬·본토로 구성',
    "Only Spanish-speaking country in Africa; highest GDP per capita in Africa after oil discovery; Bioko Island plus mainland"),
'ERI':('에리트레아','Eritrea',
    '1993년 에티오피아에서 독립. 홍해 연안 전략적 위치. 극도로 폐쇄적인 독재 체제로 아프리카의 북한으로 불림',
    "Independent from Ethiopia in 1993; strategic Red Sea coastline; called 'Africa's North Korea' for authoritarian isolation"),
'SWZ':('에스와티니','Eswatini',
    '아프리카 최소 내륙국 중 하나. 세계 마지막 절대 군주제(음스와티 3세). 세계 최고 HIV/AIDS 감염률',
    "One of Africa's smallest landlocked nations; world's last absolute monarchy; world's highest HIV/AIDS prevalence rate"),
'ETH':('에티오피아','Ethiopia',
    '아프리카 2위 인구 대국(1억 2천만+). 커피 발상지. 아프리카 연합(AU) 본부. 유럽 열강의 식민 지배를 막아낸 아프리카 유일 독립국(아도와 전투)',
    "Africa's 2nd most populous (120M+); birthplace of coffee; African Union HQ; only African nation to defeat European colonizers at Battle of Adwa"),
'GAB':('가봉','Gabon',
    '국토의 88%가 열대우림(아프리카 최고). 석유 수출국. 알베르트 슈바이처 박사 람바레네 병원',
    "88% tropical forest cover (highest in Africa); oil exporter; Albert Schweitzer's famous hospital in Lambaréné"),
'GMB':('감비아','Gambia',
    '아프리카 본토 최소 국가. 감비아 강을 따라 세네갈에 둘러싸인 지형. 서아프리카 최초 관광 명소 중 하나',
    "Africa's smallest mainland country; enclave within Senegal along the Gambia River; one of West Africa's earliest tourism destinations"),
'GHA':('가나','Ghana',
    '아프리카 최초 독립국(1957, 과메 은크루마). 세계 코코아 2위 생산국. 황금해안(Gold Coast) 역사',
    "First sub-Saharan African nation to gain independence (1957, Kwame Nkrumah); world's 2nd largest cocoa producer; historic Gold Coast"),
'GIN':('기니','Guinea',
    '세계 최대 보크사이트(알루미늄 원료) 매장국. 서아프리카 음악·문화의 중심지. 포르투갈 최초 아프리카 거점',
    "World's largest bauxite reserves (key for aluminum); West African musical and cultural hub; first Portuguese African foothold"),
'GNB':('기니비사우','Guinea-Bissau',
    '세계 최대 캐슈넛 수출국 중 하나. 아프리카 최빈국. 비자구 군도(유네스코 생물권 보전지역)',
    "Among world's top cashew nut exporters; one of Africa's least developed nations; Bijagós Archipelago UNESCO biosphere reserve"),
'CIV':('코트디부아르','Ivory Coast',
    '세계 최대 코코아 생산국(전 세계 40%). 야무수크루 대성당(세계 최대 규모 중 하나). 서아프리카 경제 중심지',
    "World's largest cocoa producer (40% of global supply); Yamoussoukro Basilica; West Africa's economic powerhouse"),
'KEN':('케냐','Kenya',
    '마라톤·장거리 육상 강국. 마사이마라 국립보호구(연간 100만 마리 동물 대이동). 나이로비 실리콘 사바나(IT 허브)',
    "Marathon and long-distance running powerhouse; Maasai Mara wildebeest migration; Nairobi 'Silicon Savannah' tech hub"),
'LSO':('레소토','Lesotho',
    '남아공에 완전히 둘러싸인 내륙국. 세계에서 가장 높은 저점(해발 1,400m). 세계 최대 다이아몬드 중 하나 발견지',
    "Entirely enclosed within South Africa; world's highest lowest point (1,400m elevation); major diamond discoveries"),
'LBR':('라이베리아','Liberia',
    '미국 해방 노예들이 세운 나라(1847). 아프리카 최초 공화국. 세계 최대 선박 등록국(편의치적)',
    "Founded by freed American slaves (1847); Africa's first republic; world's largest ship registry (flag of convenience)"),
'LBY':('리비아','Libya',
    '세계 9위 원유 매장량. 국토의 90%가 사하라 사막. 2011년 카다피 정권 붕괴 후 내전 지속',
    "9th largest oil reserves globally; 90% Sahara Desert; ongoing civil war since Gaddafi's fall in 2011"),
'MDG':('마다가스카르','Madagascar',
    '세계 4번째 큰 섬. 동식물 90%가 지구 어디에도 없는 고유종. 바오밥 나무 가로수길',
    "World's 4th largest island; 90% of wildlife found nowhere else on Earth; iconic Avenue of the Baobabs"),
'MWI':('말라위','Malawi',
    "'아프리카의 따뜻한 심장'. 말라위 호수(세계 3번째 큰 아프리카 담수호). 최빈국이지만 평화로운 국가",
    "'The Warm Heart of Africa'; Lake Malawi (3rd largest in Africa); one of poorest but most peaceful African nations"),
'MLI':('말리','Mali',
    '말리 제국(아프리카 최대 중세 왕국). 팀북투(이슬람 학문 중심지). 금 생산 아프리카 3위. 사하라 교역로',
    "Ancient Mali Empire (Africa's largest medieval kingdom); Timbuktu Islamic scholarship; 3rd largest gold producer in Africa"),
'MRT':('모리타니','Mauritania',
    '국토 절반 이상이 사하라 사막. 세계 최대 철광석 매장지 중 하나. 2007년까지 노예제 공식 유지',
    "Over half Sahara Desert; massive iron ore deposits; slavery officially criminalized only in 2007; ancient Chinguetti city"),
'MUS':('모리셔스','Mauritius',
    '인도양 화산섬. 멸종된 도도새의 고향. 아프리카에서 가장 높은 인간개발지수(HDI). 다문화·다언어 사회',
    "Indian Ocean volcanic island; former home of the extinct dodo bird; Africa's highest human development index; multicultural society"),
'MAR':('모로코','Morocco',
    '아프리카에서 유럽과 가장 가까운 나라(지브롤터 해협 14km). 마라케시·페스 고대 도시(유네스코). 세계 최대 인산염 수출국',
    "14km from Europe at Strait of Gibraltar; Marrakesh and Fes UNESCO medinas; world's largest phosphate exporter"),
'MOZ':('모잠비크','Mozambique',
    '인도양 동부 해안. 1975년 포르투갈에서 독립. 세계 최대 루비 광산(근래 발견). 마푸토 항구 수도',
    "Indian Ocean coast; Portuguese colony until 1975; world's largest ruby mines recently discovered; Maputo coastal capital"),
'NAM':('나미비아','Namibia',
    '세계에서 가장 오래된 사막(나미브 사막, 5500만년). 소수스블레이 붉은 사구. 야생동물 공동체 보전 선진국',
    "World's oldest desert (Namib, 55M years old); Sossusvlei red dunes; global leader in community-based wildlife conservation"),
'NER':('니제르','Niger',
    '아프리카에서 가장 큰 나라(면적). 세계 최대 우라늄 생산국 중 하나. 니제르강 유역. 만성적 식량 위기',
    "Africa's largest country by area; one of world's top uranium producers; Niger River basin; recurring severe food crises"),
'NGA':('나이지리아','Nigeria',
    '아프리카 최다 인구(2억 2천만+). 아프리카 최대 경제 대국. 놀리우드(세계 2위 영화 산업). 석유 수출국',
    "Africa's most populous (220M+) and largest economy; 'Nollywood' film industry (world's 2nd largest); major oil exporter"),
'RWA':('르완다','Rwanda',
    '1994년 르완다 대학살(100일간 80만 명). 키갈리(아프리카에서 가장 청결한 도시). 마운틴 고릴라 서식지. 아프리카 싱가포르',
    "1994 genocide (800,000 killed in 100 days); Kigali named Africa's cleanest city; mountain gorillas; 'Singapore of Africa' rapid rise"),
'STP':('상투메 프린시페','São Tomé and Príncipe',
    '아프리카 두 번째로 작은 나라. 대서양 화산 군도. 코코아 생산. 포르투갈어 사용 도서 국가',
    "Africa's 2nd smallest country; Atlantic volcanic islands; historic cocoa production; Lusophone island nation"),
'SEN':('세네갈','Senegal',
    '다카르(아프리카 최서단 도시). 전통 레슬링(람브) 국민 스포츠. 테랑가(환대) 문화. 다카르 랠리 출발지',
    "Dakar (Africa's westernmost city); Laamb traditional wrestling as national sport; Teranga hospitality culture; former Dakar Rally start"),
'SLE':('시에라리온','Sierra Leone',
    '세계 최대 다이아몬드 매장지 중 하나. 블러드 다이아몬드 내전 역사. 프리타운(아프리카 최초 영국 정착지)',
    "Major diamond deposits; Blood Diamond civil war history; Freetown (first British settlement in Africa)"),
'SOM':('소말리아','Somalia',
    '아프리카의 뿔 최동단. 2000년대 세계 해적 활동 중심지. 세계 최고 취약 국가 지수. 고대 유향 교역의 중심',
    "Horn of Africa's easternmost point; global piracy hub in 2000s; consistently top fragile state index; ancient frankincense trade"),
'ZAF':('남아프리카공화국','South Africa',
    '넬슨 만델라와 아파르트헤이트 종식(1994). 세계 최대 금·백금 생산국. 희망봉. 2010 FIFA 월드컵 개최',
    "Nelson Mandela and end of apartheid (1994); world's top gold and platinum producer; Cape of Good Hope; hosted 2010 FIFA World Cup"),
'SSD':('남수단','South Sudan',
    '2011년 세계 최신 독립국. 석유 부국이나 내전·기근. 나일강 지류 인근. 세계 최대 난민 발생국 중 하나',
    "World's newest country (independence 2011); oil-rich but devastated by civil war and famine; one of world's largest refugee crises"),
'SDN':('수단','Sudan',
    '세계 최다 피라미드 보유국(200개 이상, 이집트보다 많음). 하르툼(청·백 나일강 합류점). 2011년 남수단 분리',
    "More pyramids than Egypt (200+); Khartoum at confluence of Blue and White Nile; South Sudan separated in 2011"),
'TZA':('탄자니아','Tanzania',
    '킬리만자로(아프리카 최고봉 5,895m). 세렝게티 동물 대이동. 잔지바르 향신료 섬. 세계 최대 다이아몬드 광산',
    "Kilimanjaro (Africa's highest peak, 5,895m); Serengeti migration; Zanzibar spice island; world's largest diamond mines"),
'TGO':('토고','Togo',
    '베냉만 연안의 가늘고 긴 나라. 로메 부두교 시장. 아프리카 최대 인산염 수출국 중 하나',
    "Long thin Gulf of Benin country; Lomé's famous voodoo market; one of Africa's top phosphate exporters"),
'TUN':('튀니지','Tunisia',
    '아프리카 최북단 국가. 카르타고 고대 문명 유적(유네스코). 2010년 아랍의 봄 발원지. 지중해 올리브·날짜 생산',
    "Africa's northernmost country; ancient Carthage ruins UNESCO; birthplace of the 2010 Arab Spring; Mediterranean olive and date production"),
'UGA':('우간다','Uganda',
    '비룽가 마운틴 고릴라. 빅토리아 호수(세계 최대 열대 담수호). 진자(나일강 발원지). 처칠이 아프리카의 진주라 부름',
    "Mountain gorillas in Bwindi; Lake Victoria (world's largest tropical lake); Jinja: Source of the Nile; Churchill called it 'Pearl of Africa'"),
'ZMB':('잠비아','Zambia',
    '빅토리아 폭포(세계 최대 폭포 면적). 카퍼벨트(구리 광산 지대). 잠베지강. 1964년 독립',
    "Victoria Falls (world's largest waterfall by area); Copperbelt copper mines; Zambezi River; independence in 1964"),
'ZWE':('짐바브웨','Zimbabwe',
    '빅토리아 폭포(잠비아 공유). 그레이트 짐바브웨 유네스코 유적. 2008년 초인플레이션(100조 달러 지폐). 풍부한 야생동물',
    "Victoria Falls (shared with Zambia); Great Zimbabwe ruins UNESCO; 2008 hyperinflation (100-trillion dollar note); rich wildlife"),
'SYC':('세이셸','Seychelles',
    '인도양 115개 섬으로 이루어진 군도. 세계 최소 아프리카 국가(면적 455㎢). 코코드메르(세계 최대 씨앗) 유일 산지',
    "115-island Indian Ocean archipelago; Africa's smallest country by area; only habitat of the coco de mer (world's largest seed)"),

# ── Europe ───────────────────────────────────────────────────────────────────
'ALB':('알바니아','Albania',
    "독수리의 땅(알바니아어: Shqipëri). 아드리아해·이오니아해 연안. 1991년 공산주의 붕괴 후 급격한 변화. 스칸데르베그 민족 영웅",
    "'Land of Eagles'; Adriatic and Ionian coast; rapid transformation after 1991 communist collapse; national hero Skanderbeg"),
'AND':('안도라','Andorra',
    '피레네 산맥 소국(468㎢). 세계 최저 세율 중 하나(면세 쇼핑). 100% 수력 전기. 스키 리조트 천국',
    "Pyrenean microstate (468 km²); one of Europe's lowest tax rates (duty-free); 100% hydroelectric power; ski resort paradise"),
'AUT':('오스트리아','Austria',
    '모차르트·슈베르트·베토벤의 나라. 빈 오페라·왈츠. 알프스 스키. 합스부르크 제국 600년 중심지',
    "Birthplace of Mozart, Schubert; Vienna opera and waltz; Alpine skiing; 600-year center of the Habsburg Empire"),
'BLR':('벨라루스','Belarus',
    "유럽의 마지막 독재자(루카셴코). 2020년 대규모 민주화 시위. 체르노빌 원전 최대 피해국. 소련 감성 보존",
    "'Europe's last dictator' (Lukashenko); massive democracy protests 2020; worst Chernobyl fallout zone; Soviet-era culture preserved"),
'BEL':('벨기에','Belgium',
    '세계 최고 초콜릿·맥주·와플. NATO·EU 본부 소재지(브뤼셀). 플라망어·왈롱어 언어 갈등의 나라',
    "World-class chocolate, beer and waffles; NATO and EU headquarters in Brussels; Flemish-Walloon linguistic divide"),
'BIH':('보스니아 헤르체고비나','Bosnia and Herzegovina',
    '사라예보(1914 프란츠 페르디난트 암살, 1차 세계대전 도화선). 1992~95 보스니아 전쟁. 모스타르 스타리 모스트 다리(유네스코)',
    "Sarajevo: Franz Ferdinand assassination sparked WWI; Bosnian War 1992-95; Mostar's Stari Most bridge UNESCO"),
'BGR':('불가리아','Bulgaria',
    '장미 오일 세계 최대 생산지(장미 계곡). 키릴 문자 발상지. 흑해 연안 리조트. 트라키아 황금 유물',
    "World's largest rose oil producer (Valley of Roses); birthplace of Cyrillic alphabet; Black Sea resorts; Thracian gold treasures"),
'HRV':('크로아티아','Croatia',
    '지중해 섬 1,200개(최다). 플리트비체 호수 국립공원(유네스코). 2018 FIFA 월드컵 준우승. 달마티아 해안',
    "1,200 islands (most in Mediterranean); Plitvice Lakes UNESCO; 2018 FIFA World Cup runners-up; Dalmatian coast"),
'CYP':('키프로스','Cyprus',
    '지중해 3번째 큰 섬. 1974년 터키 침공으로 분단. 아프로디테 신화 발상지. EU 최동단 회원국',
    "3rd largest Mediterranean island; divided since 1974 Turkish invasion; mythical birthplace of Aphrodite; easternmost EU member"),
'CZE':('체코','Czech Republic',
    '프라하(유럽 가장 아름다운 구시가지 중 하나). 맥주 소비량 세계 1위(1인당). 보헤미아 크리스탈. 1989년 벨벳 혁명',
    "Prague's fairy-tale old town; world's #1 beer consumption per capita; Bohemian crystal; 1989 Velvet Revolution"),
'DNK':('덴마크','Denmark',
    '레고의 나라. 세계 최고 행복 지수 상위권. 뉴 노르딕 요리(노마 레스토랑). 안데르센 동화 고향',
    "Birthplace of LEGO; consistently top global happiness rankings; New Nordic cuisine (Noma); Hans Christian Andersen's homeland"),
'EST':('에스토니아','Estonia',
    "e-에스토니아(세계 최선진 디지털 정부). 탈린 구시가지(유네스코). 스카이프 탄생지. '노래하는 혁명'으로 소련 독립",
    "'e-Estonia' digital governance pioneer; Tallinn medieval old town UNESCO; Skype invented here; 'Singing Revolution' from USSR"),
'FIN':('핀란드','Finland',
    '산타클로스 공식 고향(로바니에미). 사우나 발상지(300만 개 이상). 세계 최고 교육 시스템. 북극광 관측 명소',
    "Official home of Santa Claus (Rovaniemi); birthplace of sauna (3M+ saunas); world's best education system; Northern Lights"),
'FRA':('프랑스','France',
    '에펠탑·루브르. 세계 최다 관광객(연 9천만). 와인·치즈·패션. 프랑스혁명과 인권선언(1789)',
    "Eiffel Tower and Louvre; world's most visited country (90M tourists/year); wine, cheese, fashion; French Revolution 1789"),
'DEU':('독일','Germany',
    'BMW·벤츠·폭스바겐 자동차 강국. 옥토버페스트. 베를린 장벽 붕괴(1989). EU 최대 경제 대국',
    "BMW, Mercedes, Volkswagen automotive hub; Oktoberfest; Berlin Wall fall (1989); EU's largest economy"),
'GRC':('그리스','Greece',
    '서양 문명·민주주의 발상지. 올림픽 발상지. 아크로폴리스·파르테논(유네스코). 지중해 섬 6,000개 이상',
    "Cradle of Western civilization and democracy; birthplace of Olympics; Acropolis and Parthenon UNESCO; 6,000+ Mediterranean islands"),
'HUN':('헝가리','Hungary',
    "부다페스트('다뉴브의 진주'). 루빅스 큐브 발명국. 오스트리아-헝가리 제국. 인구 대비 노벨상 수상자 세계 3위",
    "Budapest 'Pearl of the Danube'; invented Rubik's Cube; Austro-Hungarian Empire; 3rd highest Nobel laureates per capita"),
'ISL':('아이슬란드','Iceland',
    '세계 최대 지열 에너지 사용 비율. 간헐천·빙하·오로라. 세계 가장 평화로운 나라 1위. 북대서양 화산섬',
    "World's greenest geothermal energy; geysers, glaciers and Northern Lights; #1 most peaceful country; North Atlantic volcanic island"),
'IRL':('아일랜드','Ireland',
    '켈트 문화·아이리시 위스키. 1845~52년 대기근(인구 25% 감소). 조이스·베케트·예이츠 문학 강국. 성 패트릭의 날',
    "Celtic culture; Irish whiskey; Great Famine (1845-52); literary giants Joyce, Beckett, Yeats; St. Patrick's Day"),
'ITA':('이탈리아','Italy',
    '피자·파스타·에스프레소 발상지. 르네상스(레오나르도·미켈란젤로). 유네스코 세계유산 최다 보유국. 바티칸 포함',
    "Pizza, pasta and espresso birthplace; Renaissance (Leonardo, Michelangelo); most UNESCO World Heritage sites; hosts Vatican City"),
'XKX':('코소보','Kosovo',
    '2008년 독립 선언(세계 최신 나라 중 하나). 1999년 코소보 전쟁(NATO 개입). 세르비아가 주권 불인정. 유럽 최연소 인구',
    "Declared independence 2008; Kosovo War 1999 (NATO intervention); disputed by Serbia; youngest population in Europe"),
'LVA':('라트비아','Latvia',
    '발트 3국. 리가(유럽 최대 아르누보 건축물 밀집지). 노래 축제(노래하는 혁명). 호박(발트 황금) 주요 산지',
    "Baltic state; Riga has Europe's largest Art Nouveau architecture; Singing Revolution; amber ('Baltic gold') production"),
'LIE':('리히텐슈타인','Liechtenstein',
    '세계 6번째 작은 나라. 라인강 연안. 1인당 GDP 세계 최고 수준. 성 전체가 계곡 하나에 들어가는 소국',
    "6th smallest country; Rhine River border; one of world's highest GDP per capita; entire country fits in one mountain valley"),
'LTU':('리투아니아','Lithuania',
    '발트 3국 중 가장 큰 나라. 1990년 소련 최초 독립 선언. 빌뉴스 구시가(유네스코). 농구 강국',
    "Largest Baltic state; first Soviet republic to declare independence (1990); Vilnius old town UNESCO; basketball powerhouse"),
'LUX':('룩셈부르크','Luxembourg',
    '세계 최고 1인당 GDP 국가 중 하나. EU 핵심 창설 멤버(1957). 은행·금융 허브. 3개 공용어(룩셈부르크·프랑스·독일어)',
    "One of world's highest GDP per capita; EU founding member (1957); banking and finance hub; trilingual nation"),
'MLT':('몰타','Malta',
    '지중해 중심부 군도. 몰타 기사단 역사. EU 최소 회원국(316㎢). 왕좌의 게임 촬영지',
    "Central Mediterranean islands; Knights of Malta history; smallest EU member state (316 km²); Game of Thrones filming location"),
'MDA':('몰도바','Moldova',
    '유럽 최빈국. 세계 최대 와인 지하 동굴(밀레스티 미치, 200km). 트란스니스트리아 분리 지역',
    "Europe's poorest country; world's largest wine cellar Mileștii Mici (200km tunnels); unrecognized breakaway Transnistria region"),
'MCO':('모나코','Monaco',
    '세계 2번째 작은 나라(바티칸 다음). F1 모나코 그랑프리. 세계 최고 인구 밀도(1만 9천명/㎢). 카지노·부호의 나라',
    "2nd smallest country (after Vatican); Monaco F1 Grand Prix; world's highest population density; Monte Carlo casino"),
'MNE':('몬테네그로','Montenegro',
    "'검은 산'의 나라. 아드리아해 마지막 비밀 명소. 코토르 만(유네스코). 2017년 NATO 가입",
    "'Black Mountain' meaning; Adriatic hidden gem; Kotor Bay UNESCO World Heritage; joined NATO in 2017"),
'NLD':('네덜란드','Netherlands',
    '풍차·튤립·고다 치즈. 세계 최고 자전거 이용 국가. 렘브란트·페르메이르 황금 시대 예술. 로테르담(유럽 최대 항구)',
    "Windmills, tulips and Gouda cheese; world's top cycling nation; Dutch Golden Age art (Rembrandt, Vermeer); Europe's largest port"),
'MKD':('북마케도니아','North Macedonia',
    '알렉산더 대왕 탄생지(스코페 근처). 그리스와 국명 분쟁(2019년 해결). 오흐리드 호수(유네스코). 마더 테레사 고향',
    "Near birthplace of Alexander the Great; name dispute with Greece resolved 2019; Lake Ohrid UNESCO; Mother Teresa's birthplace"),
'NOR':('노르웨이','Norway',
    '피요르드(유네스코 세계유산). 세계 최대 국부 펀드(석유 기금). 노벨 평화상 수여국. 북극권 오로라·백야',
    "UNESCO fjords; world's largest sovereign wealth fund (oil fund); Nobel Peace Prize ceremony; Northern Lights and midnight sun"),
'POL':('폴란드','Poland',
    '바르샤바(2차 세계대전 90% 파괴 후 재건). 코페르니쿠스·퀴리 부인 고향. 아우슈비츠(유네스코). 쇼팽 고향',
    "Warsaw rebuilt after 90% WWII destruction; birthplace of Copernicus and Marie Curie; Auschwitz memorial UNESCO; Chopin's homeland"),
'PRT':('포르투갈','Portugal',
    '세계 최초 대항해 시대 주도(바스코 다 가마). 파두 음악(유네스코 무형유산). 세계 최대 코르크 수출국. 리스본 전차',
    "Pioneer of Age of Discovery (Vasco da Gama); Fado music UNESCO; world's largest cork exporter; Lisbon's iconic trams"),
'ROU':('루마니아','Romania',
    '드라큘라 전설(트란실바니아). 나디아 코마네치 체조(올림픽 최초 10점 만점). 카르파티아 불곰 최대 서식지. 부쿠레슈티',
    "Dracula legend in Transylvania; Nadia Comaneci gymnastics (first perfect 10); largest Carpathian brown bear population; Bucharest"),
'RUS':('러시아','Russia',
    '세계 최대 영토(지구 육지 11%). 모스크바 크렘린·붉은 광장. 발레·우주 개발·체스 강국. 바이칼 호수(세계 최심 담수호)',
    "World's largest country (11% of land); Kremlin and Red Square; ballet, space race, chess; Lake Baikal world's deepest lake"),
'SMR':('산마리노','San Marino',
    '세계에서 가장 오래된 공화국(서기 301년 건국). 이탈리아에 완전히 둘러싸인 내륙국. 티타노산 세 탑',
    "World's oldest republic (founded 301 AD); entirely enclave within Italy; three towers on Mount Titano; no national debt"),
'SRB':('세르비아','Serbia',
    '베오그라드 요새 도시. 니콜라 테슬라 고향. 유고슬라비아 해체의 중심. 라키야(자두 브랜디) 문화',
    "Belgrade fortress capital; birthplace of Nikola Tesla; center of Yugoslavia's dissolution; rakija plum brandy culture"),
'SVK':('슬로바키아','Slovakia',
    '타트라 산맥 스키. 체코슬로바키아에서 평화 분리(1993, 벨벳 이혼). 1인당 성(城) 보유량 세계 최다. 브라티슬라바',
    "Tatra Mountains skiing; peaceful split from Czech Republic 1993 ('Velvet Divorce'); most castles per capita; Bratislava on Danube"),
'SVN':('슬로베니아','Slovenia',
    '알프스·지중해·판노니아 평원 모두 보유. 블레드 호수(동화 속 섬). 1991년 유고슬라비아 최초 독립. EU·NATO 회원',
    "Alps, Mediterranean coast and Pannonian Plain combined; Lake Bled fairy-tale island; first Yugoslav republic independent 1991"),
'ESP':('스페인','Spain',
    '가우디·피카소·살바도르 달리. 바르셀로나·마드리드. 플라멩코·투우. 세계 2위 와인·올리브유 생산국',
    "Gaudí, Picasso, Dalí; Barcelona and Madrid; flamenco and bullfighting; world's 2nd largest wine and olive oil producer"),
'SWE':('스웨덴','Sweden',
    '이케아·볼보·에릭슨·스포티파이 모두 이곳 탄생. 노벨상 제정국. 북유럽 복지 모델. 스칸디나비아 디자인',
    "IKEA, Volvo, Ericsson, Spotify all founded here; Nobel Prize established here; Nordic welfare model; Scandinavian design"),
'CHE':('스위스','Switzerland',
    '알프스·시계·초콜릿·에멘탈 치즈. 1815년부터 영구 중립국. 유엔 유럽 본부·국제적십자 본부. 세계 최고 삶의 질',
    "Alps, watches, chocolate and Emmental cheese; permanent neutrality since 1815; UN European HQ and Red Cross HQ; highest quality of life"),
'TUR':('튀르키예','Turkey',
    '유럽·아시아 교차점(보스포루스 해협). 이스탄불(1,200년간 세계 최대 도시). 카파도키아 열기구. 케밥·바클라바',
    "Straddles Europe and Asia (Bosphorus Strait); Istanbul world's largest city for 1,200 years; Cappadocia balloons; kebab and baklava"),
'UKR':('우크라이나','Ukraine',
    '유럽 최대 영토국(러시아 제외). 체르노빌 원전 사고(1986). 유럽의 빵바구니(밀·해바라기). 2022년 러시아 침공',
    "Europe's largest country (excl. Russia); Chernobyl disaster (1986); 'Breadbasket of Europe'; Russian invasion 2022"),
'GBR':('영국','United Kingdom',
    '셰익스피어·뉴턴·다윈의 나라. 산업혁명 발상지. 비틀즈·해리포터. 대영제국(역사상 최대 제국)',
    "Shakespeare, Newton, Darwin; Industrial Revolution birthplace; Beatles and Harry Potter; largest empire in history"),
'VAT':('바티칸','Vatican',
    '세계 최소 국가(0.44㎢). 교황청. 성 베드로 대성당·시스티나 예배당. 전 세계 13억 가톨릭 신자의 중심',
    "World's smallest country (0.44 km²); Holy See; St. Peter's Basilica and Sistine Chapel; center for 1.3 billion Catholics"),
}

# ── Map configurations ────────────────────────────────────────────────────────
MAPS = {
    'africa': {
        'iso_set': AFRICA_ISO,
        'json_out': 'data/quiz-africa.json',
        'svg_out':  'maps/world/africa.svg',
        'svg_ref':  '/maps/world/africa.svg',
        'W':720,'H':760,'PAD':12,
        'LON0':-20,'LON1':55,'LAT0':-36,'LAT1':38,
        'proj':'equirect','EPS':1.2,
        'label_ko':'아프리카 나라','label_en':'African Countries',
    },
    'europe': {
        'iso_set': EUROPE_ISO,
        'json_out': 'data/quiz-europe.json',
        'svg_out':  'maps/world/europe.svg',
        'svg_ref':  '/maps/world/europe.svg',
        'W':760,'H':580,'PAD':12,
        'LON0':-27,'LON1':50,'LAT0':33,'LAT1':73,
        'proj':'mercator','EPS':0.8,
        'label_ko':'유럽 나라','label_en':'European Countries',
    },
}

# ── Douglas-Peucker ───────────────────────────────────────────────────────────
def _dp_dist(px,py,ax,ay,bx,by):
    dx,dy=bx-ax,by-ay
    if dx==0 and dy==0: return math.hypot(px-ax,py-ay)
    t=max(0,min(1,((px-ax)*dx+(py-ay)*dy)/(dx*dx+dy*dy)))
    return math.hypot(px-(ax+t*dx),py-(ay+t*dy))

def dp_simplify(pts,eps):
    if len(pts)<3: return pts
    dmax,idx=0,0
    a,b=pts[0],pts[-1]
    for i in range(1,len(pts)-1):
        d=_dp_dist(pts[i][0],pts[i][1],a[0],a[1],b[0],b[1])
        if d>dmax: dmax,idx=d,i
    if dmax>=eps:
        l=dp_simplify(pts[:idx+1],eps)
        r=dp_simplify(pts[idx:],eps)
        return l[:-1]+r
    return [pts[0],pts[-1]]

# ── Projection ───────────────────────────────────────────────────────────────
def _merc(d):
    return math.log(math.tan(math.pi/4+math.radians(max(-85,min(85,d)))/2))

def project_ring(ring, cfg):
    W,H,PAD=cfg['W'],cfg['H'],cfg['PAD']
    LON0,LON1,LAT0,LAT1=cfg['LON0'],cfg['LON1'],cfg['LAT0'],cfg['LAT1']
    EPS=cfg['EPS']
    raw=[]
    if cfg['proj']=='mercator':
        m0,m1=_merc(LAT0),_merc(LAT1)
    for lon,lat,*_ in ring:
        x=PAD+(lon-LON0)/(LON1-LON0)*(W-2*PAD)
        if cfg['proj']=='mercator':
            y=H-PAD-(_merc(lat)-m0)/(m1-m0)*(H-2*PAD)
        else:
            y=H-PAD-(lat-LAT0)/(LAT1-LAT0)*(H-2*PAD)
        raw.append((round(x,1),round(y,1)))
    return dp_simplify(raw,EPS)

MIN_SVG=7  # minimum visible size in SVG units

def expand_to_min(pts):
    """If pts < 3 or bbox < MIN_SVG, replace with a small square centered on centroid."""
    if not pts: return pts
    if len(pts)<3:
        cx=sum(p[0] for p in pts)/len(pts); cy=sum(p[1] for p in pts)/len(pts)
        r=MIN_SVG/2
        return [(cx-r,cy-r),(cx+r,cy-r),(cx+r,cy+r),(cx-r,cy+r),(cx-r,cy-r)]
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    if max(xs)-min(xs)>=MIN_SVG and max(ys)-min(ys)>=MIN_SVG:
        return pts
    cx=sum(xs)/len(xs); cy=sum(ys)/len(ys)
    r=MIN_SVG/2
    return [(cx-r,cy-r),(cx+r,cy-r),(cx+r,cy+r),(cx-r,cy+r),(cx-r,cy-r)]

def ring_to_path(pts):
    if len(pts)<3: return ''
    d='M'+' '.join(f'{x},{y}' for x,y in pts)+'Z'
    return d

def feature_to_path(geom,cfg):
    parts=[]
    if geom['type']=='Polygon':
        polys=[geom['coordinates']]
    elif geom['type']=='MultiPolygon':
        polys=geom['coordinates']
    else:
        return ''
    for poly in polys:
        outer=project_ring(poly[0],cfg)
        outer=expand_to_min(outer)
        p=ring_to_path(outer)
        if p: parts.append(p)
    return ' '.join(parts)

# ── Load NE data ──────────────────────────────────────────────────────────────
def load_ne():
    if not os.path.exists(NE_CACHE):
        print('Downloading Natural Earth 50m countries...',flush=True)
        urllib.request.urlretrieve(NE_URL,NE_CACHE)
        print(f'  Saved {NE_CACHE}')
    with open(NE_CACHE,encoding='utf-8') as f:
        return json.load(f)

# ── Generate one map ──────────────────────────────────────────────────────────
def generate(cfg_key,features):
    cfg=MAPS[cfg_key]
    iso_set=cfg['iso_set']
    W,H=cfg['W'],cfg['H']
    regions=[]
    paths_html=[]

    for feat in features:
        props=feat['properties']
        iso=props.get('ISO_A3','').strip()
        name=props.get('NAME','').strip()

        # fix/override ISO for known tricky names
        if name in NAME_FIX:
            fixed=NAME_FIX[name]
            if fixed is None: continue   # exclude
            iso=fixed

        if iso not in iso_set: continue
        if iso not in DATA:
            print(f'  WARNING: no data for {iso} ({name})')
            continue

        ko,en,ko_hint,en_hint=DATA[iso]
        geom=feat.get('geometry')
        if not geom: continue
        d=feature_to_path(geom,cfg)
        if not d: continue

        path_id=f'r{iso}'
        paths_html.append(
            f'<path id="{path_id}" data-id="{iso}" data-ko="{ko}" data-en="{en}" d="{d}"/>'
        )
        regions.append({
            'id':iso,'svgPathId':path_id,
            'names':{'ko':ko,'en':en},
            'hints':{'ko':ko_hint,'en':en_hint},
        })

    # SVG
    os.makedirs(os.path.dirname(cfg['svg_out']),exist_ok=True)
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">\n'
    svg+='<g id="regions">\n'
    svg+='\n'.join(paths_html)+'\n'
    svg+='</g>\n</svg>'
    with open(cfg['svg_out'],'w',encoding='utf-8') as f:
        f.write(svg)

    # JSON
    quiz={
        'meta':{'id':cfg_key,'mapSvg':cfg['svg_ref'],'defaultLang':'ko','totalRegions':len(regions)},
        'regions':regions,
    }
    with open(cfg['json_out'],'w',encoding='utf-8') as f:
        json.dump(quiz,f,ensure_ascii=False,indent=2)

    print(f'{cfg_key}: {len(regions)} countries → {cfg["svg_out"]}, {cfg["json_out"]}')
    missing=iso_set-{r["id"] for r in regions}
    if missing: print(f'  Missing ISO: {sorted(missing)}')

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__=='__main__':
    data=load_ne()
    features=data['features']
    generate('africa',features)
    generate('europe',features)
    print('Done.')
