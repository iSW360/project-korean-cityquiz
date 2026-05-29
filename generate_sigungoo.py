"""
Generates quiz-korea-sigungoo.json + maps/korea/sigungoo.svg
with merged city polygons (uses shapely for gu → city union),
province boundary overlay, and rich per-region hints.
"""
import json, math, urllib.request, os, sys
from collections import defaultdict
from shapely.geometry import shape
from shapely.ops import unary_union

sys.setrecursionlimit(20000)

# ── Download ──────────────────────────────────────────────────────────────────
MUNI_URL = 'https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2013/json/skorea_municipalities_geo_simple.json'
PROV_URL = 'https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2013/json/skorea_provinces_geo_simple.json'
print('Downloading GeoJSON data...')
with urllib.request.urlopen(MUNI_URL) as r: muni_data = json.loads(r.read().decode('utf-8'))
with urllib.request.urlopen(PROV_URL) as r: prov_data = json.loads(r.read().decode('utf-8'))
print(f'  municipalities: {len(muni_data["features"])}, provinces: {len(prov_data["features"])}')

# ── Province labels ───────────────────────────────────────────────────────────
PROV_KO = {'21':'부산','22':'대구','23':'인천','26':'울산','29':'세종',
            '31':'경기도','32':'강원도','33':'충청북도','34':'충청남도',
            '35':'전라북도','36':'전라남도','37':'경상북도','38':'경상남도','39':'제주'}
PROV_EN = {'21':'Busan','22':'Daegu','23':'Incheon','26':'Ulsan','29':'Sejong',
            '31':'Gyeonggi-do','32':'Gangwon-do','33':'Chungbuk','34':'Chungnam',
            '35':'Jeonbuk','36':'Jeonnam','37':'Gyeongbuk','38':'Gyeongnam','39':'Jeju'}

# ── Cities with gu that must be merged (code_prefix → {ko, en}) ──────────────
MERGE = {
    '3101': ('수원시','Suwon-si'),
    '3102': ('성남시','Seongnam-si'),
    '3104': ('안양시','Anyang-si'),
    '3105': ('부천시','Bucheon-si'),
    '3109': ('안산시','Ansan-si'),
    '3110': ('고양시','Goyang-si'),
    '3119': ('용인시','Yongin-si'),
    '3301': ('청주시','Cheongju-si'),
    '3401': ('천안시','Cheonan-si'),
    '3501': ('전주시','Jeonju-si'),
    '3701': ('포항시','Pohang-si'),
    '3811': ('창원시','Changwon-si'),
}

# ── Rich hints ────────────────────────────────────────────────────────────────
HINTS = {
'수원시': ('유네스코 세계유산 화성(수원성) 소재. 삼성전자 본사가 있는 한국 전자·IT 도시',
           "Home to UNESCO Hwaseong Fortress and Samsung Electronics HQ; Korea's electronics hub"),
'성남시': ('판교 테크노밸리(한국의 실리콘밸리). 카카오·네이버 등 IT 기업 밀집',
           "Pangyo Techno Valley hosts Kakao, Naver, and major tech firms—Korea's Silicon Valley"),
'안양시': ('안양예술공원 소재. 영화감독 봉준호(기생충 아카데미 수상)가 성장한 도시',
           "Anyang Art Park; director Bong Joon-ho (Oscar-winning Parasite) grew up here"),
'부천시': ('부천국제판타스틱영화제 개최지. 한국 만화(웹툰) 산업의 중심',
           "Hosts Bucheon International Fantastic Film Festival; center of Korean webtoon/comics industry"),
'안산시': ('시화호 생태 복원 성공 사례. 국내 최대 외국인 근로자 다문화 특구',
           "Sihwa Lake ecological restoration success; Korea's largest multicultural district for foreign workers"),
'고양시': ('KINTEX(국내 최대 전시 컨벤션센터) 소재. 고양 국제꽃박람회 개최',
           "Hosts KINTEX (Korea's largest exhibition center) and the Goyang International Flower Festival"),
'용인시': ('에버랜드(삼성 테마파크·국내 최대) 소재. 기흥 반도체 클러스터. 한국민속촌',
           "Home to Everland (largest theme park) and Samsung semiconductor cluster; Korean Folk Village"),
'의정부시': ('부대찌개의 발상지(미군 부대 음식 문화). 경기 북부 교통 중심지',
             "Birthplace of budae-jjigae (army stew born from US military food culture)"),
'광명시': ('폐광을 재활용한 광명동굴 와인동굴. KTX 광명역 소재',
           "Gwangmyeong Cave (repurposed coal mine) hosts wine tasting; KTX high-speed rail station"),
'평택시': ('캠프 험프리스(아시아 최대 미군 기지) 소재. 반도체 허브 성장',
           "Home to Camp Humphreys (largest US military base in Asia); emerging semiconductor hub"),
'동두천시': ('소요산 관광지. 미군 기지 영향으로 형성된 외국 문화 거리',
             "Soyosan mountain resort; historic town shaped by US military base culture"),
'과천시': ('국립현대미술관·서울대공원 소재. 서울 인접 소도시',
           "National Museum of Modern and Contemporary Art; Seoul Grand Park (zoo & theme park)"),
'구리시': ('동구릉(조선 왕릉군) 유네스코 세계유산. 한강 코스모스 축제',
           "Donggureung Royal Tombs (UNESCO World Heritage); Han River cosmos flower festival"),
'남양주시': ('다산 정약용 생가 및 실학박물관. 팔당 유기농 수자원보호구역',
             "Birthplace of scholar Jeong Yak-yong (Dasan); Paldang reservoir organic farming zone"),
'오산시': ('궐리사(공자 후손 사당) 소재. 화성 세계유산과 인접',
           "Gwollisa Shrine dedicated to Confucius' descendants; adjacent to UNESCO Hwaseong Fortress"),
'시흥시': ('시흥 갯골 생태공원. 옛 소래염전 소금 역사',
           "Siheung Gaetgol Ecological Park (tidal flat); historic Sorae salt field heritage"),
'군포시': ('수리산 도립공원. 영화 건축학개론 촬영지',
           "Surisan Provincial Park; filming location for iconic Korean romance film 'Architecture 101'"),
'의왕시': ('한국 철도박물관 소재. 백운호수 관광지',
           "Home to Korea Railroad Museum; Baekun Lake popular leisure destination"),
'하남시': ('스타필드 하남 대형 복합몰. 미사리 조정경기장. 위례신도시',
           "Starfield Hanam mega mall; Misari Regatta course; Wirye New Town development"),
'파주시': ('아시아 최대 출판문화단지. 헤이리 예술마을. DMZ 인접',
           "Asia's largest book publishing cluster; Heyri Art Village; gateway to the Demilitarized Zone"),
'이천시': ('도예의 고장(고려·조선 도자기 전통). 이천 쌀·복숭아 특산',
           "Korea's pottery capital since Goryeo Dynasty; Icheon Ceramic Festival; premium rice and peaches"),
'안성시': ('안성맞춤 관용어 유래지. 안성 유기(놋그릇)와 배 특산',
           "Origin of Korean proverb 'Anseong-matchum' (a perfect fit); famed for brass crafts and pears"),
'김포시': ('장릉(조선 원종 왕릉). 아라뱃길 수도권 운하 기점',
           "Jangneung Royal Tomb of Wonjong; Ara Waterway canal linking Han River to the Yellow Sea"),
'화성시': ('정조대왕 융건릉 세계유산. 현대·기아차 공장. 제부도 조석간만 도로',
           "Yunggeolleung Royal Tombs of King Jeongjo (UNESCO); Hyundai-Kia plants; Jebu Island tidal road"),
'광주시': ('남한산성 유네스코 세계유산. 조선 백자·분청사기 산지',
           "Namhansanseong Fortress (UNESCO); historic center of Joseon white and buncheong porcelain"),
'양주시': ('회암사지(고려 최대 사찰 터). 나리농원 꽃 관광지',
           "Hoeamsa Temple Site (largest Goryeo-era temple complex); Nari Farm seasonal flower garden"),
'포천시': ('이동갈비 발상지. 광릉수목원(국립수목원). 산정호수',
           "Birthplace of Idong galbi grilled ribs; Gwangneung National Arboretum; Sanjeong Lake resort"),
'여주시': ('세종대왕릉(영릉) 소재. 여주 도자기·고구마·쌀 특산',
           "Sejong the Great's royal tomb Yeongneung; famous for pottery, sweet potatoes, and premium rice"),
'연천군': ('한탄강 유네스코 세계지질공원. 전곡리 구석기 유적. 두루미 철새 도래지',
           "UNESCO Hantan River Global Geopark; Jeongok-ri Paleolithic site; winter habitat for endangered cranes"),
'가평군': ('자라섬 국제재즈페스티벌. 쁘띠프랑스(프랑스 문화마을). 아침고요수목원',
           "Jarasum International Jazz Festival; Petite France cultural village; Garden of Morning Calm"),
'양평군': ('두물머리(양수리) 일출 명소. 유기농 특산. 여운형 독립운동가 생가',
           "Dumulmeori sunrise spot (where two rivers meet); leading organic farming district; birthplace of independence activist Yeo Un-hyeong"),
'춘천시': ('닭갈비·막국수의 고장. 소양강댐·스카이워크. 강원도청 소재',
           "Birthplace of dakgalbi and makguksu noodles; Soyang Dam & Skybridge; Gangwon Province capital"),
'원주시': ('뮤지엄 산(안도 타다오 설계). 한지 공예. 치악산국립공원',
           "Museum SAN (designed by Tadao Ando); Korean hanji paper crafts; Chiaksan National Park"),
'강릉시': ('2018 동계올림픽 빙상 경기 개최. 오죽헌(율곡 이이 생가). 한국의 커피 도시',
           "2018 Winter Olympics ice venue; Ojukheon birthplace of Yi I (5,000-won note); Korea's 'coffee city'"),
'동해시': ('무릉계곡 명승. 묵호항 오징어·대게 특산',
           "Mureung Valley scenic gorge; Mukho Port known for squid and snow crab"),
'태백시': ('옛 국내 최대 탄광 도시. 태백산 눈꽃 축제. 낙동강·한강 발원지',
           "Former coal mining capital; Taebaek Mountain Snow Festival; source of Han and Nakdong rivers"),
'속초시': ('설악산국립공원 관문. 아바이마을 실향민 문화. 속초 닭강정 유명',
           "Gateway to Seoraksan National Park; Abai Village preserving North Korean refugee food culture"),
'삼척시': ('환선굴(국내 최대 동굴). 죽서루 명승. 해양 레포츠',
           "Hwanseon Cave (Korea's largest natural cave); Jugseoruek historic pavilion; coastal water sports"),
'홍천군': ('강원도 면적 최대 군. 홍천강 래프팅. 수박 특산',
           "Largest county by area in Gangwon; Hongcheongang River rafting; famous sweet watermelons"),
'횡성군': ('횡성 한우(명품 쇠고기) 특산. 태기산 풍력발전단지',
           "Premium Hoengseong Hanwoo beef; Taegisan wind power farm; Hoengseong Alpine ski resort"),
'영월군': ('단종 유배지 청령포. 동강 래프팅. 별마로 천문대',
           "Cheongnyeongpo where King Danjong was exiled; Donggang River rafting; Byeollmaro Observatory"),
'평창군': ('2018 평창 동계올림픽 설상 경기 개최. 이효석 메밀꽃 필 무렵 배경. 고랭지 채소',
           "Host of 2018 Winter Olympics alpine events; backdrop of Yi Hyo-seok's 'When Buckwheat Flowers Bloom'"),
'정선군': ('강원랜드 카지노(유일한 내국인 카지노). 정선 아리랑. 레일바이크',
           "Gangwon Land Casino (Korea's only casino open to residents); birthplace of Jeongseon Arirang folk song"),
'철원군': ('한탄강 지질공원. 철원 오대쌀(명품 쌀). 두루미 천연기념물 서식지',
           "Hantan River lava plateau; premium Cheolwon rice; winter habitat for endangered Siberian cranes"),
'화천군': ('산천어 축제(세계 4대 겨울 축제). 평화의 댐',
           "Hwacheon Sancheoneo Ice Festival (CNN's top winter festivals worldwide); Peace Dam"),
'양구군': ('펀치볼(해안분지) 특이 지형. 박수근 미술관',
           "Punchbowl basin (unique bowl-shaped valley); Park Soo-keun Art Museum dedicated to Korea's beloved painter"),
'인제군': ('내린천 래프팅. 설악산 일부. 만해 한용운 생가',
           "Naerin River rafting; part of Seoraksan National Park; birthplace of independence poet Han Yong-un"),
'고성군': ('금강산 육로 관광 출발 거점. 왕곡마을 전통 가옥 보존',
           "Former gateway for land tours to Mt. Kumgang (North Korea); Wanggok traditional thatched-roof village"),
'양양군': ('서핑 성지 죽도해변. 낙산사(관동팔경). 송이버섯 최대 산지',
           "Korea's top surfing beach at Jukdo; Naksan Temple (one of Eight Scenic Views); largest matsutake mushroom producer"),
'청주시': ('유네스코 기록유산 직지(세계 최초 금속활자 인쇄 1377). 청주 국제공항',
           "Jikji—world's oldest metal movable type print (1377, UNESCO Memory of the World); Cheongju International Airport"),
'충주시': ('우륵 가야금 창제 설화지. 충주호 레저. 탄금대 유적',
           "Legendary home of Ureuk who created the gayageum zither; Chungju Lake; Tangeumdae historic terrace"),
'제천시': ('한방 약초의 도시. 청풍문화재 단지. 의림지(삼한시대 수리시설)',
           "Hub of traditional herbal medicine; Cheongpung Heritage Complex; Uirimji reservoir (2,000-year-old irrigation)"),
'청원군': ('2014년 청주시와 통합. 청남대(역대 대통령 별장) 소재',
           "Merged with Cheongju in 2014; Cheongnamdae Presidential Villa (former retreat of Korean presidents)"),
'보은군': ('속리산국립공원. 정이품송(600년 수령 천연기념물 소나무)',
           "Songnisan National Park; Jeong II-pum Song pine tree (600-year-old natural monument)"),
'옥천군': ('시인 정지용(향수) 생가지. 포도·육쪽마늘 특산',
           "Birthplace of poet Jeong Ji-yong who wrote the beloved 'Nostalgia'; famous for grapes and six-clove garlic"),
'영동군': ('과일의 고장(포도·감·배). 박연(국악 창제) 유적지. 와인 명소',
           "Fruit capital (grapes, persimmons, pears); heritage of Goryeo court music master Park Yeon; wine culture"),
'증평군': ('2003년 신설된 국내 최신 군. 인삼 특산지',
           "Korea's newest county (established 2003); notable ginseng growing area"),
'진천군': ('생거진천(살기 좋은 고장) 관용어 유래. 농다리(고려시대 돌다리)',
           "Origin of proverb 'paradise of the living'; Nongdari Bridge—900-year-old Goryeo-era stone bridge"),
'괴산군': ('산막이 옛길 호반 산책. 유기농 채소 산지',
           "Sanmagi Old Trail lakeside walk; major organic vegetable farming area"),
'음성군': ('홍삼 특산. 음성 품바 축제(각설이 타령 발원지)',
           "Major red ginseng producer; home of Pumbba Festival celebrating traditional peddler folk songs"),
'단양군': ('도담삼봉·고수동굴 석회암 절경. 단양 마늘. 퇴계 이황 학문지',
           "Dodamsambong rocks and Gosu Cave; premium garlic; Yi Hwang's Dosan Seowon scholarship site"),
'천안시': ('독립기념관. 유관순 열사 생가지. 호두과자 발상지',
           "Independence Hall of Korea; birthplace of independence activist Yu Gwan-sun; origin of walnut pastry"),
'공주시': ('백제 무령왕릉·공산성 유네스코 세계유산. 공주 밤(율) 특산',
           "Baekje's Muryeong Royal Tomb and Gongsan Fortress (UNESCO); famous for sweet chestnuts"),
'보령시': ('대천해수욕장. 보령 머드 축제(세계 4대 여름 축제)',
           "Daecheon Beach; Boryeong Mud Festival—one of the world's largest mud festivals"),
'아산시': ('현충사(이순신 장군 사당). 온양온천(600년 역사). 현대자동차 공장',
           "Hyeonchungsa Shrine to Admiral Yi Sun-sin; Onyang Hot Springs (600-year history); Hyundai Motor plant"),
'서산시': ('백제 마애여래삼존상(백제의 미소). 서산 마늘. 간월도 굴',
           "Baekje rock Buddha carvings known as the 'Baekje Smile'; premium garlic; Ganyeoldo oysters"),
'논산시': ('국내 최대 딸기 산지. 관촉사 은진미륵. 논산훈련소',
           "Korea's largest strawberry producing city; Gwanchoksa's giant Eunjin Mireuk statue; Nonsan Army Training Center"),
'계룡시': ('육군·해군·공군 본부 모두 위치한 군사 도시',
           "Houses headquarters of Army, Navy, and Air Force—Korea's unified military command city"),
'당진시': ('현대제철 일관제철소. 삽교호 방조제. 당진 쌀',
           "Hyundai Steel integrated steelworks; Sapgyo Lake tidal dike; premium Dangjin rice"),
'금산군': ('국내 인삼 최대 산지. 금산 인삼 축제. 칠백의총(임진왜란 격전지)',
           "Korea's largest ginseng region; Geumsan Ginseng Festival; Chilbaek shrine to 700 Imjin War martyrs"),
'부여군': ('백제 사비 왕도. 부소산성·궁남지 유네스코 세계유산. 연꽃 축제',
           "Baekje Kingdom's last capital; Busosan Fortress and Gungnamji Pond (UNESCO); Lotus Festival"),
'서천군': ('국립생태원 소재. 한산모시(유네스코 무형문화유산) 생산지',
           "National Ecological Institute; Hansan ramie weaving (UNESCO Intangible Heritage)"),
'청양군': ('구기자·고추 특산. 칠갑산 도립공원. 천장호 출렁다리',
           "Famous for goji berries and hot peppers; Chilgapsan Provincial Park; Cheongyang Swinging Bridge"),
'홍성군': ('김좌진 장군(청산리 대첩 영웅) 생가지. 홍성 한우 특산',
           "Birthplace of General Kim Jwa-jin, hero of the 1920 Battle of Cheongsan-ri; premium Hanwoo beef"),
'예산군': ('추사 김정희(추사체 서예가) 생가지. 예당저수지(국내 최대 저수지)',
           "Birthplace of calligrapher Kim Jeong-hui (Chusa script); Yedan Reservoir (Korea's largest reservoir)"),
'태안군': ('태안해안국립공원. 꽃지 할미할아비바위. 서해 낙조 절경',
           "Taean Coast National Park; Kkotji Beach Granny and Grandpa Rocks; spectacular Yellow Sea sunsets"),
'전주시': ('유네스코 창의도시(음식). 전주한옥마을. 비빔밥·판소리 발상지',
           "UNESCO Creative City of Gastronomy; Jeonju Hanok Village; birthplace of bibimbap and pansori music"),
'군산시': ('일제강점기 쌀 수탈항. 근대문화유산거리. 군산 꽃게·젓갈',
           "Colonial-era port used for rice extraction; Modern Heritage Street with 1930s architecture; famous for blue crab"),
'익산시': ('백제 미륵사지(국내 최대 석탑) 유네스코 세계유산. 보석·귀금속 집산지',
           "Mireuksa Temple Site with Korea's largest stone pagoda (UNESCO); major gem and jewelry trading hub"),
'정읍시': ('동학농민혁명(1894) 발원지. 내장산 단풍. 내장사',
           "Birthplace of the 1894 Donghak Peasant Revolution; Naejangsan autumn foliage; Naejangsa Temple"),
'남원시': ('춘향전 배경지. 광한루원. 남원 목기·추어탕',
           "Setting of 'Chunhyangjeon' love story; Gwanghallu Pavilion Garden; woodcraft and loach soup specialty"),
'김제시': ('국내 유일 지평선 축제. 벽골제(삼한시대 최대 저수지). 쌀 생산량 전국 1위',
           "Korea's only flat-horizon landscape festival; Byeokgolje ancient reservoir; top rice-producing city"),
'완주군': ('삼례문화예술촌(곡물 창고 재활용). 대아저수지. 딸기 특산',
           "Samrye Culture Arts Village (repurposed granary); Daea Reservoir; major strawberry producing area"),
'진안군': ('마이산(역고드름 현상). 홍삼 특산',
           "Maisan (Horse Ear Mountain) with unique reverse icicle phenomenon; premium red ginseng"),
'무주군': ('무주 태권도원(태권도 국기원). 반딧불이 서식지. 덕유산 리조트',
           "Korea Taekwondo Park (world headquarters); protected firefly habitat; Deoggyusan ski resort"),
'장수군': ('장수 사과·한우 특산. 금강 발원지',
           "Premium apples and Hanwoo cattle; source of the Geum River which flows to the Yellow Sea"),
'임실군': ('벨기에 신부 지정환이 전파한 임실 치즈 발상지. 오수의 개 설화',
           "Birthplace of Korean cheese culture (introduced by Belgian priest Father Didier in 1967); legend of the loyal dog"),
'순창군': ('순창 고추장(조선 왕실 진상품). 강천산 단풍',
           "Home of Korea's most famous gochujang chili paste (once offered to Joseon royalty); Gangcheonsan Valley scenery"),
'고창군': ('고인돌 유네스코 세계유산(약 2,000기). 복분자·수박 특산. 선운사',
           "UNESCO Gochang Dolmen Sites (2,000 megalith tombs); famous for bokbunja wild raspberry; Seonunsa Temple"),
'부안군': ('변산반도 국립공원. 채석강(책을 쌓은 듯한 절벽 해안). 서해 낙조',
           "Byeonsanbando National Park; Chaesokgang shale cliff (resembling stacked books); Yellow Sea sunsets"),
'목포시': ('유달산·삼학도. 목포 홍어(삭힌 홍어)·세발낙지 특산. 근대역사문화공간',
           "Yudalsan and Samhakdo islands; famous for fermented skate (hongeo) and small octopus; colonial heritage district"),
'여수시': ('2012 여수 세계박람회 개최. 이순신 한산도·거북선 역사. 돌산 갓김치',
           "Hosted Expo 2012; Admiral Yi Sun-sin's naval base; Dolsan leaf mustard kimchi; Hallyeo Maritime National Park"),
'순천시': ('순천만 국가정원·람사르 습지. 드라마 촬영지. 선암사·송광사',
           "Suncheonman National Garden; Ramsar-listed Suncheon Bay tidal flat; major drama filming location"),
'나주시': ('나주 배(국내 최대 배 산지). 나주 곰탕. 한국전력(KEPCO) 본사(혁신도시)',
           "Korea's largest pear producing city; Naju Gom-tang beef bone soup; KEPCO headquarters in innovation city"),
'광양시': ('포스코 광양제철소(세계 최대급). 광양 매화 축제. 광양 불고기',
           "POSCO Gwangyang Steelworks (one of world's largest steel plants); plum blossom festival; Gwangyang bulgogi"),
'담양군': ('대나무·죽세공예의 고장. 메타세쿼이아 가로수길. 담양 떡갈비·죽순',
           "Capital of bamboo craft; iconic Metasequoia tree-lined road; Damyang tteok-galbi and bamboo shoots"),
'곡성군': ('섬진강 기차마을(증기기관차 관광). 장미 축제. 참외·토마토 특산',
           "Seomjingang Train Village with steam locomotive rides; Rose Festival; premium chamoe melons"),
'구례군': ('지리산국립공원 관문. 섬진강 벚꽃길. 산수유 마을',
           "Gateway to Jirisan National Park; Seomjingang cherry blossom road; Sansuyu (cornelian cherry) village"),
'고흥군': ('나로도 우주센터(한국 최초 우주발사체 발사지). 유자·석류 특산',
           "Naro Space Center (first Korean space rocket launch site); famous for yuzu citrus and pomegranates"),
'보성군': ('국내 최대 녹차밭. 보성 녹차·벌교 꼬막 특산',
           "Korea's largest green tea fields; Boseong green tea; Beolgyo cockle clams (a Korean culinary treasure)"),
'화순군': ('고인돌 유네스코 세계유산. 운주사 천불천탑. 화순 복숭아',
           "UNESCO Hwasun Dolmen Sites; Unjusa Temple's 1,000 stone Buddhas and pagodas; peach orchards"),
'장흥군': ('표고버섯·키조개 특산. 천관산 억새. 장흥 한우',
           "Premium shiitake mushrooms and surf clams; Cheongwansan autumn pampas grass; free-range Hanwoo cattle"),
'강진군': ('다산 정약용 유배지(대표 저작 집필지). 고려청자 도요지',
           "Exile site of Jeong Yak-yong (wrote masterworks here); historic Goryeo celadon kiln sites"),
'해남군': ('한반도 최남단 땅끝마을. 두륜산 대흥사. 고구마 최대 산지',
           "Southernmost tip of Korean peninsula (Ttangkkeut Village); Daeheungsa Temple; largest sweet potato producer"),
'영암군': ('왕인박사 일본 파견(백제 학자). 월출산국립공원. 무화과 특산',
           "Scholar Wang In brought Chinese classics to Japan from here; Wolchulsan National Park; fig specialty"),
'무안군': ('무안 국제공항(광주공항 이전). 낙지·양파 특산',
           "Muan International Airport; famous for octopus; major onion growing area"),
'함평군': ('함평 나비 축제(국내 최초 나비 생태 축제). 함평 천지 쌀',
           "Hampyeong Butterfly Festival (Korea's first butterfly ecology festival); premium Hamwon rice"),
'영광군': ('법성포 굴비의 고장(전국 굴비 80% 생산). 백제 불교 최초 도래지',
           "Beopsungpo port produces 80% of Korea's dried yellow corvina (gulbi); first landing of Buddhism in Baekje"),
'장성군': ('홍길동 생가지(소설 홍길동전 배경). 백양사 황금 단풍',
           "Birthplace of fictional hero Hong Gil-dong; Baegyang Temple renowned for stunning golden maple leaves"),
'완도군': ('전복 최대 산지(전국 80%). 청산도 슬로시티. 장보고 청해진 역사',
           "Produces 80% of Korea's abalone; Cheongsando (Asia's first Slow City); maritime base of hero Jang Bogo"),
'진도군': ('진도 신비의 바닷길(연 2회 갈라짐). 진도개·진도 아리랑·홍주',
           "Jindo Sea Parting (sea divides twice yearly); home of Jindo dog (natural monument) and Jindo Arirang folk song"),
'신안군': ('섬이 가장 많은 군(1,004개 섬). 퍼플섬(반월·박지도). 천일염·낙지 특산',
           "Korea's island-richest county (1,004 islands); Purple Island (Banwol & Bakji); premium sun-dried salt and octopus"),
'포항시': ('포스코(POSCO) 소재 철강 도시. 구룡포 과메기(청어·꽁치 건조). 죽도시장',
           "Home to POSCO (global steel giant); Guryongpo port famous for gwamaegi (dried saury); Jukdo Market"),
'경주시': ('신라 천년 고도. 불국사·석굴암 유네스코 세계유산. 첨성대. 황남빵',
           "Millennium capital of Silla Kingdom; Bulguksa Temple and Seokguram Grotto (UNESCO); Cheomseongdae Observatory"),
'김천시': ('직지사(신라 고찰). 포도·자두 특산. KTX 김천구미역',
           "Jikjisa Buddhist Temple (Silla era); premium grapes and plums; KTX Gimcheon-Gumi high-speed rail station"),
'안동시': ('조선 유교 문화의 수도. 하회마을 유네스코 세계유산. 안동 간고등어·찜닭·헛제사밥',
           "Center of Korean Confucian culture; Hahoe Folk Village (UNESCO); famous for salted mackerel and jjimdak chicken stew"),
'구미시': ('LG전자·삼성전자 공장. 한국 전자산업 발상지. 박정희 전 대통령 생가',
           "Major LG and Samsung factory hub; birthplace of Korea's electronics industry; hometown of President Park Chung-hee"),
'영주시': ('최초 사액서원 소수서원(유네스코). 부석사(유네스코). 풍기 인삼·사과',
           "Sosuseowon (first royal-chartered Confucian academy, UNESCO); Buseoksa Temple (UNESCO); Punggi ginseng"),
'영천시': ('국내 최대 포도 산지. 보현산 천문대. 임고서원(정몽주 생가)',
           "Korea's largest grape production area; Bohyeonsan Astronomical Observatory; Imgoseowon shrine to Jeong Mong-ju"),
'상주시': ('사과·곶감의 고장. 낙동강 자전거길 기점. 자전거 박물관',
           "Famous for apples and dried persimmons; start of Nakdong River Bicycle Trail; Korea's Bicycle Museum"),
'문경시': ('문경 새재(조선 과거 응시 길). 사과 특산. 도예 마을',
           "Mungyeongsaejae Pass (historic Joseon civil exam trail); premium apples; traditional ceramics village"),
'경산시': ('대학 도시(영남대·경일대 등). 대추 최대 산지',
           "University city with major campuses; Korea's largest jujube (red date) producing area"),
'군위군': ('삼국유사 저자 일연 스님 인각사. 코스모스 축제. 사과 특산',
           "Ingaksa Temple where monk Ilyeon compiled Samguk Yusa; Cosmos Festival; premium apples"),
'의성군': ('의성 마늘(국내 생산 1위). 빙계계곡 자연 얼음 동굴',
           "Korea's top garlic producing county; Bingye Valley natural ice cave; hub of independence movement"),
'청송군': ('주왕산국립공원. 청송 사과·달기약수 닭백숙',
           "Juwangsan National Park; Cheongsong premium apples; Dalgi mineral spring chicken stew specialty"),
'영양군': ('고추 최대 산지. 아시아 최초 국제밤하늘보호공원. 소설가 이문열 출생지',
           "Korea's top red pepper county; first International Dark Sky Park in Asia; birthplace of novelist Yi Mun-yol"),
'영덕군': ('영덕 대게의 원산지. 해파랑길 시작점. 창포말 등대',
           "Original home of Yeongdeok snow crab; start of Haeparang coastal trail; Changpoma Lighthouse"),
'청도군': ('청도 소싸움(국가무형문화재). 복숭아·감 특산. 와인터널(폐철도 재활용)',
           "Cheongdo bullfighting (intangible cultural heritage); premium peaches and persimmons; Wine Tunnel in old railway"),
'고령군': ('대가야 왕도. 지산동 고분군 유네스코 세계유산. 딸기 특산',
           "Capital of the Daegaya kingdom; Jisandong Tumuli (UNESCO World Heritage); premium strawberry production"),
'성주군': ('참외 최대 산지(국내 생산 80%). 세종대왕 관련 역사 유적',
           "Produces 80% of Korea's chamoe (oriental melon); historic sites linked to Sejong the Great's family"),
'칠곡군': ('낙동강 방어 전투(한국전쟁 최후 방어선) 역사. 왜관 포도',
           "Site of decisive Nakdong River Perimeter battles in Korean War; Waegwan township famous for grapes"),
'예천군': ('회룡포(육지 안의 섬 마을). 삼강주막(마지막 전통 주막)',
           "Hoeryongpo river island village (river wraps 270° around farmland); Samgang tavern—Korea's last traditional inn"),
'봉화군': ('송이버섯 산지. 청량산(이황 학문지). 분천역 산타마을',
           "Premium matsutake mushroom area; Cheongnyangsan where Yi Hwang studied; Buncheon Station Christmas Village"),
'울진군': ('왕피천 생태경관보전지역. 금강송(황장목) 군락. 대게·파래 특산',
           "Wangpicheon River Ecological Conservation Area; primeval Geumgangso pine forest; snow crab and seaweed"),
'울릉군': ('울릉도·독도 관할. 오징어·호박엿 특산. 나리분지(화산 칼데라). 독도는 한국 고유 영토',
           "Administers Ulleung and Dokdo islands; volcanic Nari Basin caldera; famous for squid and pumpkin taffy"),
'창원시': ('경남도청 소재. 마산·창원·진해 통합(2010). 진해 군항제(전국 최대 벚꽃 축제)',
           "Gyeongnam Province capital; formed by merger of Masan, Changwon, Jinhae (2010); Jinhae Cherry Blossom Festival"),
'진주시': ('진주성 임진왜란 3대첩. 논개 의거. 남강유등축제. 진주비빔밥·진주실크',
           "Site of great Imjin War victory; patriot Nongae's sacrifice; Nam River Lantern Festival; Jinju bibimbap and silk"),
'통영시': ('동양의 나폴리. 한산도 대첩(이순신). 통영 굴·충무김밥. 박경리·윤이상 예술가 도시',
           "Called 'Naples of the East'; Battle of Hansando (Admiral Yi); home of novelist Park Kyung-ni and composer Yun I-sang"),
'사천시': ('한국항공우주산업(KAI) 본사. 삼천포 아귀찜',
           "Korea Aerospace Industries (KAI) headquarters; Samcheonpo monkfish stew specialty"),
'김해시': ('금관가야 도읍지. 수로왕릉. 인도 허황옥 공주 도래 설화',
           "Capital of Geumgwan Gaya kingdom; King Suro's Tomb; legend of Princess Heo Hwang-ok from ancient India"),
'밀양시': ('밀양 아리랑 민요. 표충사. 밀양 얼음골(여름에도 결빙되는 천연기념물)',
           "Miryang Arirang folk song; Pyochungsa Temple; Miryang ice valley (natural monument—freezes in summer)"),
'거제시': ('한국전쟁 포로수용소 역사. 삼성·대우 조선소. 외도 보태니아 가든',
           "Korean War POW camp heritage; Samsung and Daewoo shipyards; Oedo-Botania Garden island"),
'양산시': ('통도사(불보사찰, 한국 3보 사찰 중 하나). 부산 근교 위성도시. 양산 딸기',
           "Tongdosa Temple (one of Korea's Three Jewel Temples); fast-growing Busan satellite city; premium strawberries"),
'의령군': ('홍의장군 곽재우(임진왜란 의병장) 생가지. 의령 망개떡 특산',
           "Birthplace of 'Red-robed General' Gwak Jae-u (Imjin War guerrilla leader); Mangae tteok specialty"),
'함안군': ('아라가야의 고도. 말이산 고분군. 함안 수박·연꽃 테마파크',
           "Former Aragaya kingdom capital; Marisan ancient tumuli; famous watermelons; Lotus Land theme park"),
'창녕군': ('우포늪(국내 최대 자연 내륙 습지, 람사르 등록). 창녕 마늘·양파',
           "Upo Wetlands (Korea's largest natural inland wetland, Ramsar site); famous for garlic and onions"),
'고성군': ('공룡 발자국 화석 세계 최대 밀집지. 고성 공룡엑스포',
           "World's highest concentration of dinosaur footprint fossils; Goseong Dinosaur Expo"),
'남해군': ('독일마을(독일 파견 광부·간호사 귀환 정착). 멸치·마늘 특산',
           "'German Village' settled by Korean workers returning from Germany (1960s-70s); famous for anchovies and garlic"),
'하동군': ('화개장터(경남·전남 경계 시장). 하동 녹차(국내 최초 차 시배지). 박경리 토지 배경',
           "Hwagae Market (boundary market of two provinces); first tea cultivation site in Korea; setting of Park Kyung-ni's 'Land'"),
'산청군': ('지리산국립공원. 한방약초 특산. 동의보감촌(한방의료 관광)',
           "Jirisan National Park; center of traditional medicinal herbs; Dongibogam Village for Korean medicine tourism"),
'함양군': ('상림숲(1,100년 전 최치원이 조성한 숲). 지리산 천왕봉',
           "Sangnim Forest (planted by scholar Choe Chiwon 1,100 years ago); Mt. Jirisan's highest peak Cheonwangbong"),
'거창군': ('수승대 계곡. 사과 특산. 거창 국제연극제',
           "Suseungdae Valley; premium apples; Geochang International Theater Festival"),
'합천군': ('해인사(팔만대장경 유네스코 세계유산 보관). 황매산 철쭉. 합천 영상테마파크',
           "Haeinsa Temple housing the Tripitaka Koreana (UNESCO); Hwangmaesan azalea festival; Hapcheon Film Theme Park"),
'제주시': ('한라산국립공원. 성산일출봉 세계자연유산. 감귤·흑돼지·말. 해녀 문화',
           "Hallasan National Park; Seongsan Ilchulbong (UNESCO Natural Heritage); haenyeo (women divers) intangible heritage; tangerines"),
'서귀포시': ('정방폭포(동양 유일 바다 직폭). 효돈 감귤. 제주 올레길. 섶섬·문섬 다이빙',
             "Jeongbang Waterfall (Asia's only falls plunging directly into the sea); Jeju Olle hiking trail; diving at Seopseom"),
'기장군': ('부산 기장 대게·미역 특산. 롯데월드 어드벤처 부산(아시아 최대 실내 테마파크)',
           "Gijang snow crab and seaweed specialties; Lotte World Adventure Busan (Asia's largest indoor theme park)"),
'달성군': ('도동서원 유네스코 세계유산. 삼성 라이온즈 야구 연고지. 비슬산 참꽃 축제',
           "Dodongseowon Academy (UNESCO); home of Samsung Lions KBO team; Bisulsan royal azalea festival"),
'강화군': ('고인돌 유네스코 세계유산. 마니산 참성단(단군 제천 유적). 강화 화문석·인삼·새우젓',
           "UNESCO Ganghwa Dolmen Sites; Manisan mountain Chamseongdan Altar (Dangun mythology); ginseng, woven mats, fermented shrimp"),
'옹진군': ('백령도 두무진(화강암 해안 천연기념물). 대청도 모래사막. 서해 최북단 섬 관할',
           "Baengnyeongdo's Dumujin granite coast (natural monument); Daecheongdo sand dunes; northernmost Yellow Sea islands"),
'울주군': ('반구대 암각화(세계 최고 고래 사냥 기록, 약 8000년 전). 언양 불고기 특산',
           "Bangudae Petroglyphs (world's earliest known whaling record, c. 6000 BCE); Eonyang bulgogi specialty"),
'세종특별자치시': ('2012년 출범 행정중심복합도시. 국무총리·주요 부처 이전. 한국 최초 계획 행정수도',
                  "Established 2012 as Korea's planned administrative capital; houses Prime Minister's office and most government ministries"),
'세종시': ('2012년 출범 행정중심복합도시. 국무총리·주요 부처 이전. 한국 최초 계획 행정수도',
           "Established 2012 as Korea's planned administrative capital; houses Prime Minister's office and most government ministries"),
}

# ── Projection ────────────────────────────────────────────────────────────────
LON0, LON1 = 124.5, 131.1
LAT0, LAT1 = 33.0, 38.75
W, H, PAD = 680, 800, 15
lat_c = (LAT0+LAT1)/2
cos_lat = math.cos(math.radians(lat_c))
lon_range = (LON1-LON0)*cos_lat; lat_range = LAT1-LAT0
scale = min((W-2*PAD)/lon_range, (H-2*PAD)/lat_range)
map_w = lon_range*scale; map_h = lat_range*scale
ox = PAD+(W-2*PAD-map_w)/2; oy = PAD+(H-2*PAD-map_h)/2

def proj(lon, lat):
    return round(ox+(lon-LON0)*cos_lat*scale,1), round(oy+(LAT1-lat)*scale,1)

def _dp(pts, eps):
    if len(pts)<3: return list(pts)
    dx=pts[-1][0]-pts[0][0]; dy=pts[-1][1]-pts[0][1]
    L=math.hypot(dx,dy)
    if L<1e-10: return [pts[0],pts[-1]]
    mi,md=1,0
    for i in range(1,len(pts)-1):
        d=abs(dy*pts[i][0]-dx*pts[i][1]+pts[-1][0]*pts[0][1]-pts[-1][1]*pts[0][0])/L
        if d>md: mi,md=i,d
    if md>eps: return _dp(pts[:mi+1],eps)[:-1]+_dp(pts[mi:],eps)
    return [pts[0],pts[-1]]

def ring_to_d(raw_coords, eps):
    ring = list(raw_coords)
    if ring and ring[0]==ring[-1]: ring=ring[:-1]
    if len(ring)<3: return ''
    coords = [proj(lon,lat) for lon,lat in ring]
    simp = _dp(coords, eps)
    if len(simp)<3: return ''
    return 'M'+' '.join(f'{x},{y}' for x,y in simp)+'Z'

EPS_M = 0.8   # si/gun paths
EPS_P = 0.5   # province borders

def geom_to_d(geom_dict, eps):
    t = geom_dict['type']; cs = geom_dict['coordinates']
    d = ''
    if t=='Polygon':
        for ring in cs: d += ring_to_d(ring, eps)
    elif t=='MultiPolygon':
        for poly in cs:
            for ring in poly: d += ring_to_d(ring, eps)
    return d

def shapely_to_d(geom, eps):
    d = ''
    gtype = geom.geom_type
    if gtype == 'Polygon':
        d += ring_to_d(list(geom.exterior.coords), eps)
        for interior in geom.interiors:
            d += ring_to_d(list(interior.coords), eps)
    elif gtype == 'MultiPolygon':
        for poly in geom.geoms:
            d += ring_to_d(list(poly.exterior.coords), eps)
            for interior in poly.interiors:
                d += ring_to_d(list(interior.coords), eps)
    return d

# ── Group features ────────────────────────────────────────────────────────────
all_features = muni_data['features']

# Skip Seoul (11xxx) and metro city gu (21-26 that are simple 5-digit codes, not ending in 1/2/3)
def is_metro_gu(f):
    code = f['properties']['code']
    name = f['properties']['name']
    # Metro city gu (부산, 대구, 인천, 광주, 대전, 울산): code like 21010, 21020...
    # These have prefix 21-26 and their 5th digit is 0
    if not name.endswith('구'): return False
    prefix2 = code[:2]
    if prefix2 in ('21','22','23','24','25','26') and len(code)==5 and code[4]=='0':
        return True
    return False

def is_seoul_gu(f):
    return f['properties']['code'].startswith('11')

# Identify provincial cities with gu (to merge)
merge_groups = defaultdict(list)
for f in all_features:
    name = f['properties']['name']
    code = f['properties']['code']
    if name.endswith('구') and not is_seoul_gu(f) and not is_metro_gu(f):
        prefix4 = code[:4]
        merge_groups[prefix4].append(f)

print(f'City groups to merge: {len(merge_groups)}')
for p,flist in sorted(merge_groups.items()):
    print(f'  {p}: {len(flist)} gu → {MERGE.get(p, ("?","?"))[0]}')

# Build merged city features
merged_city_features = []
for prefix4, gu_list in merge_groups.items():
    if prefix4 not in MERGE:
        print(f'  WARNING: no MERGE entry for prefix {prefix4}')
        continue
    ko_name, en_name = MERGE[prefix4]
    city_code = prefix4 + '0'  # e.g. 31010 for 수원시
    prov_prefix = prefix4[:2]

    shapes_list = [shape(f['geometry']) for f in gu_list]
    merged_geom = unary_union(shapes_list)

    merged_city_features.append({
        'code': city_code,
        'ko': ko_name,
        'en': en_name,
        'grp': prov_prefix,
        'geometry': merged_geom,
    })

# Build non-gu features (keep)
si_gun_features = []
for f in all_features:
    name = f['properties']['name']
    code = f['properties']['code']
    if is_seoul_gu(f): continue
    if is_metro_gu(f): continue
    if name.endswith('구'): continue  # provincial city gu (handled via merge)
    en = f['properties']['name_eng']
    # Clean en name
    el = en.lower()
    if el.endswith('si') and not el.endswith('-si'): en = en[:-2]+'-si'
    elif el.endswith('gun') and not el.endswith('-gun'): en = en[:-3]+'-gun'
    prov_prefix = code[:2]
    si_gun_features.append({
        'code': code,
        'ko': name,
        'en': en,
        'grp': prov_prefix,
        'geometry': f['geometry'],  # raw GeoJSON dict
        'is_shapely': False,
    })

# Combine
all_regions = []
# Merged cities first
for m in merged_city_features:
    all_regions.append({
        'code': m['code'], 'ko': m['ko'], 'en': m['en'], 'grp': m['grp'],
        'geometry': m['geometry'], 'is_shapely': True
    })
for f in si_gun_features:
    all_regions.append(f)

print(f'Total regions: {len(all_regions)} (merged cities: {len(merged_city_features)}, si/gun: {len(si_gun_features)})')

# ── Build quiz JSON ───────────────────────────────────────────────────────────
regions_json = []
muni_paths = []

for r in all_regions:
    code = r['code']
    ko = r['ko']
    en = r['en']
    grp = r['grp']
    pid = f'r{code}'

    # Hint
    hint_ko, hint_en = HINTS.get(ko, ('', ''))

    regions_json.append({
        'id': code,
        'svgPathId': pid,
        'names': {'ko': ko, 'en': en},
        'hints': {'ko': hint_ko, 'en': hint_en},
    })

    # SVG path
    if r['is_shapely']:
        d = shapely_to_d(r['geometry'], EPS_M)
    else:
        d = geom_to_d(r['geometry'], EPS_M)

    if d:
        ko_safe = ko.replace('"', '&quot;')
        en_safe = en.replace('"', '&quot;')
        muni_paths.append(
            f'  <path id="{pid}" data-id="{code}" data-grp="{grp}" '
            f'data-ko="{ko_safe}" data-en="{en_safe}" d="{d}"/>')

# Province boundary paths
prov_paths = []
for f in prov_data['features']:
    d = geom_to_d(f['geometry'], EPS_P)
    if d:
        pc = f['properties']['code']
        prov_paths.append(f'  <path data-pc="{pc}" d="{d}"/>')

# ── Save JSON ─────────────────────────────────────────────────────────────────
quiz_json = {
    'meta': {
        'id': 'korea-sigungoo',
        'mapSvg': '/maps/korea/sigungoo.svg',
        'defaultLang': 'ko',
        'totalRegions': len(regions_json)
    },
    'regions': regions_json
}
with open('data/quiz-korea-sigungoo.json', 'w', encoding='utf-8') as f:
    json.dump(quiz_json, f, ensure_ascii=False, indent=2)
print(f'Saved JSON: {len(regions_json)} regions')

# ── Save SVG ──────────────────────────────────────────────────────────────────
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">\n'
       '<g id="regions">\n' + '\n'.join(muni_paths) +
       '\n</g>\n<g id="prov-borders" pointer-events="none">\n' + '\n'.join(prov_paths) +
       '\n</g>\n</svg>\n')

os.makedirs('maps/korea', exist_ok=True)
with open('maps/korea/sigungoo.svg', 'w', encoding='utf-8') as f:
    f.write(svg)

sz = os.path.getsize('maps/korea/sigungoo.svg')
print(f'Saved SVG: {sz//1024}KB, {len(muni_paths)} region paths + {len(prov_paths)} province border paths')

# Check hint coverage
missing = [r['names']['ko'] for r in regions_json if not r['hints']['ko']]
if missing:
    print(f'Missing hints for {len(missing)}: {missing[:10]}')
else:
    print(f'All {len(regions_json)} regions have hints!')
print('Done.')
