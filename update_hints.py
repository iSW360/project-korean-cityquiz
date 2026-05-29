"""Update Seoul and US state hints with rich content."""
import json

# ── Seoul district hints ──────────────────────────────────────────────────────
SEOUL_HINTS = {
    '종로구': ('경복궁·창덕궁·광화문. 조선왕조 500년 정치의 중심. 인사동·북촌 한옥마을',
               "Gyeongbokgung Palace, Gwanghwamun Gate; center of Joseon Dynasty politics; Insadong and Bukchon Hanok Village"),
    '중구': ('명동(한국 최대 쇼핑 거리). 남대문시장(600년 역사). 덕수궁·서울역',
             "Myeongdong (Korea's largest shopping district); Namdaemun Market (600-year history); Deoksugung Palace"),
    '용산구': ('국립중앙박물관. 용산공원(미군기지 반환). 이태원 국제문화거리',
              "National Museum of Korea; Yongsan Park (former US military base); Itaewon international culture district"),
    '성동구': ('성수동 서울 숲 카페거리(젊음의 성지). 서울숲. 한양대학교',
              "Seongsu-dong cafe street (Seoul's trendiest neighborhood); Seoul Forest; Hanyang University"),
    '광진구': ('건국대학교. 어린이대공원. 광나루 한강공원',
              "Konkuk University; Children's Grand Park; Gwangnaru Han River Park"),
    '동대문구': ('동대문디자인플라자(DDP, 자하 하디드 설계). 경희대·한국외대. 청량리 약령시',
               "DDP (Dongdaemun Design Plaza, designed by Zaha Hadid); major university district"),
    '중랑구': ('중랑 장미원(서울 최대 장미 공원). 망우리 공원(독립운동가 묘역)',
              "Jungnang Rose Garden (Seoul's largest); Manguri Cemetery (graves of independence movement heroes)"),
    '성북구': ('북한산국립공원 접경. 간송미술관(한국 최초 사립 미술관). 성균관대',
              "Adjacent to Bukhansan National Park; Gansong Art Museum (Korea's first private museum); Sungkyunkwan University"),
    '강북구': ('우이동 계곡. 수유리 4·19혁명 기념관. 북한산 둘레길',
              "Ui-dong valley; April 19th Revolution Memorial; Bukhansan둘레길 trail"),
    '도봉구': ('도봉산 등산 명소. 연산군 묘역. 창동 문화예술 클러스터',
              "Dobongsan mountain hiking; tomb of King Yeonsangun; Changdong cultural arts cluster"),
    '노원구': ('서울 과학기술대·육군사관학교. 화랑대 철도공원. 도봉산·수락산',
              "Seoul National University of Science and Technology; Korea Military Academy; Hwangrangdae Railroad Park"),
    '은평구': ('은평 뉴타운. 진관사(한국전쟁 위문 불화 발견). 봉산 탈춤 발원지',
              "Eunpyeong New Town development; Jingwansa Temple (WWII comfort women Buddhist paintings discovered); Bongsan mask dance"),
    '서대문구': ('서대문형무소(일제 독립운동 탄압 역사). 연세대·이화여대',
               "Seodaemun Prison (colonial-era independence movement suppression); Yonsei University and Ewha Womans University"),
    '마포구': ('홍대 대학 문화 거리. 디지털미디어시티. 공덕 출판 단지',
              "Hongdae university culture and nightlife; Digital Media City; major publishing and media hub"),
    '양천구': ('목동 학원가(사교육 중심). 서울 방송 클러스터(MBC·KBS)',
              "Mokdong private education hub; major broadcasting cluster with MBC and KBS headquarters"),
    '강서구': ('김포국제공항. 허준 박물관(동의보감 저자). 마곡 LG사이언스파크',
              "Gimpo International Airport; Heo Jun Museum (author of Dongibogam medical encyclopedia); LG Science Park in Magok"),
    '구로구': ('구로공단(한국 산업화 상징). 가리봉동 중국 동포 차이나타운',
              "Guro Industrial Complex (symbol of Korea's industrialization era); Garibong-dong Korean-Chinese community"),
    '금천구': ('서울 디지털 산업단지(옛 구로공단). 호암산 도립공원',
              "Seoul Digital Industrial Complex (redeveloped from Guro Industrial Complex); Hoamsan Provincial Park"),
    '영등포구': ('여의도 금융 중심지(증권거래소·KB·신한은행). 타임스퀘어 쇼핑몰',
               "Yeouido financial hub (Korea Stock Exchange, major banks); Times Square mall; LG and Hyundai Twin Towers"),
    '동작구': ('국립서울현충원(현충사·국가유공자 묘역). 사당동·노량진 학원가',
              "Seoul National Cemetery (national war memorial); Noryangjin major exam prep district"),
    '관악구': ('서울대학교. 관악산 등산로. 신림동 순대타운',
              "Seoul National University; Gwanaksan mountain trails; Sillim-dong sundae soup village"),
    '서초구': ('삼성전자 서초사옥. 예술의 전당. 국립중앙도서관. 강남 법조타운',
              "Samsung Electronics Seocho HQ; Seoul Arts Center; National Library; major legal and judicial district"),
    '강남구': ('코엑스(전시 컨벤션). 강남역(서울 최대 유동인구). 압구정·청담 패션·명품거리. 한류 문화',
              "COEX exhibition center; Gangnam Station (highest foot traffic in Seoul); Apgujeong and Cheongdam luxury fashion streets; K-pop hub"),
    '송파구': ('롯데월드(세계 최대 실내 테마파크). 몽촌토성·석촌호수(백제 문화). 올림픽 주경기장(1988)',
              "Lotte World (world's largest indoor theme park); Mongchontoseong fortress; 1988 Summer Olympics Stadium"),
    '강동구': ('암사동 선사유적지(신석기 마을 유적). 고덕강일 공공주택지구',
              "Amsa-dong Prehistoric Settlement Site (Neolithic village ruins); major new housing development area"),
}

# ── US State hints ──────────────────────────────────────────────────────────
US_HINTS = {
    'Alabama': ('나사(NASA) 마샬 우주비행센터 소재. 시민권 운동 역사(몽고메리 버스 보이콧). 철강 산업',
                "Marshall Space Flight Center (NASA); birthplace of the Civil Rights Movement (Montgomery Bus Boycott); steel industry"),
    'Alaska': ('미국 최대 주(면적). 데날리(북미 최고봉). 북극광 관측 명소. 러시아에서 매입(1867)',
               "Largest US state by area; Denali (highest peak in North America); northern lights; purchased from Russia in 1867"),
    'Arizona': ('그랜드 캐니언. 선인장 국립공원. 피닉스(대도시). 미국 남서부 사막 문화',
                "Grand Canyon; Saguaro National Park; Phoenix metro area; Navajo Nation lands; southwestern desert culture"),
    'Arkansas': ('캐딜락 마운틴. 세계 최대 다이아몬드 광산(크레이터 오브 다이아몬즈). 월마트 본사',
                 "Crater of Diamonds State Park (world's only public diamond mine); Walmart headquarters in Bentonville"),
    'California': ('미국에서 가장 인구 많은 주. 할리우드·실리콘밸리. 나파밸리 와인. 국내총생산(GDP) 세계 5위권',
                   "Most populous US state; Hollywood, Silicon Valley, Napa Valley wine; economy rivaling world's top 5 nations"),
    'Colorado': ('로키산맥. 스키 리조트(아스펜, 베일). 덴버 마일하이시티. 대마초 합법화 선도',
                 "Rocky Mountain ski resorts (Aspen, Vail); Denver 'Mile High City'; first state to legalize recreational marijuana"),
    'Connecticut': ('미국 최초 헌법 비준 주. 이비성(보험 산업 수도). 예일 대학교',
                    "Yale University; first state to ratify the Constitution; Hartford known as 'Insurance Capital of the World'"),
    'Delaware': ('미국 최초로 헌법 비준한 주(원조 주). 기업 등록지로 유명(포춘 500 기업 60% 등록)',
                 "First state to ratify the US Constitution; nearly 60% of Fortune 500 companies incorporated here for tax benefits"),
    'Florida': ('디즈니월드(세계 최대 테마파크). 케네디 우주센터. 마이애미 라틴 문화. 은퇴자 천국',
                "Walt Disney World (world's largest theme park); Kennedy Space Center; Miami's Latin culture; retirement destination"),
    'Georgia': ('마틴 루터 킹 주니어 생가(애틀랜타). 코카콜라 본사. 복숭아 주(피치 스테이트)',
                "Atlanta: birthplace of MLK Jr.; Coca-Cola headquarters; known as the 'Peach State'; CNN headquarters"),
    'Hawaii': ('50번째 주(1959년 편입). 진주만 공격 역사(1941). 화산 국립공원. 서핑 발상지',
               "50th and most recent state (1959); Pearl Harbor attack (1941); Hawaii Volcanoes National Park; birthplace of surfing"),
    'Idaho': ('미국 최대 감자 생산지(아이다호 감자). 썬밸리 스키 리조트. 크레이터 오브 더 문 국립기념물',
              "America's potato capital (Idaho potatoes); Sun Valley ski resort; Craters of the Moon National Monument"),
    'Illinois': ('시카고(미국 2위 도시). 미국 대통령 다수 배출(링컨·오바마). 딥디쉬 피자 발상지',
                 "Chicago (America's 'Second City'); birthplace of Abraham Lincoln; Deep Dish pizza; Barack Obama's political base"),
    'Indiana': ('인디애나폴리스 500 마일 레이스. 노터데임 대학교. 자동차 부품 산업의 중심',
                "Indianapolis 500 Mile Race; University of Notre Dame; major auto parts manufacturing hub"),
    'Iowa': ('미국 최대 옥수수·대두 생산지. 대선 코커스 선두주자. 아이오와 대학',
             "America's largest corn and soybean producer; Iowa Caucuses kick off presidential primaries; University of Iowa"),
    'Kansas': ('미국 지리적 중심부. 밀 생산량 전국 1위. 도로시와 오즈의 마법사 배경',
               "Geographic center of the contiguous US; top wheat producing state; setting of 'The Wizard of Oz' (Dorothy's Kansas)"),
    'Kentucky': ('켄터키 더비(세계 최대 경마 대회). 버번 위스키 생산의 중심(전 세계 95% 생산). 루이빌 슬러거 야구 배트',
                 "Kentucky Derby (world's oldest major horse race); produces 95% of world's bourbon whiskey; Louisville Slugger baseball bats"),
    'Louisiana': ('뉴올리언스 재즈·크레올 문화. 마디그라 축제. 미시시피강 삼각주. 케이준 음식 문화',
                  "New Orleans jazz and Creole culture; Mardi Gras festival; Mississippi River delta; Cajun cuisine heritage"),
    'Maine': ('동북쪽 최동단 주. 바닷가재(메인 랍스터) 최대 산지. 아카디아 국립공원. 스티븐 킹 출신지',
              "Easternmost US state; Maine lobster capital; Acadia National Park; birthplace of author Stephen King"),
    'Maryland': ('볼티모어 항구 도시. 국립해양박물관. 체사피크만 블루크랩. 국립항공우주박물관',
                 "Baltimore Inner Harbor; Chesapeake Bay blue crab specialty; Johns Hopkins University; adjacent to DC"),
    'Massachusetts': ('미국 독립 발상지(보스턴 티 파티). 하버드·MIT. 메이플라워 청교도 역사',
                      "Birthplace of American Revolution (Boston Tea Party); Harvard, MIT; Mayflower Pilgrims; Boston Red Sox and Celtics"),
    'Michigan': ('디트로이트(미국 자동차 산업의 수도). GM·포드·크라이슬러 본사. 오대호 접경 주',
                 "Detroit 'Motor City' (GM, Ford, Chrysler headquarters); Great Lakes shoreline; Motown music birthplace"),
    'Minnesota': ('미국 최대 스칸디나비아계 이민자. 미니애폴리스 아트신. 미시시피강 발원지. 3M 본사',
                  "Mississippi River headwaters; Minneapolis arts scene; 3M and Target headquarters; large Scandinavian heritage"),
    'Mississippi': ('미국 가장 가난한 주. 블루스 음악의 고향. 미시시피강 접경. 목화 역사',
                    "Birthplace of blues music; Mississippi Delta cotton farming history; William Faulkner's literary home"),
    'Missouri': ('미시시피강·미주리강 합류지. 세인트루이스 아치(서부 개척 기념). 캔자스시티 바비큐',
                 "Gateway Arch in St. Louis (symbol of westward expansion); Kansas City BBQ; birthplace of Mark Twain"),
    'Montana': ('옐로스톤 국립공원 북쪽. 빙하 국립공원. 광활한 목장 지대. 구리 광업 역사',
                "Glacier National Park; northern Yellowstone; vast ranch lands; historic copper mining; 'Big Sky Country'"),
    'Nebraska': ('미국 최대 옥수수 생산지. 플래트강. 오마하(워런 버핏 거주지). 소 생산량 전국 2위',
                 "Major corn producer; Omaha (Warren Buffett's hometown); Platte River flyway for migrating cranes"),
    'Nevada': ('라스베이거스(세계 최대 카지노·엔터테인먼트). 후버 댐. 미국 가장 건조한 주',
               "Las Vegas (world's entertainment and casino capital); Hoover Dam; driest US state; Area 51 conspiracy lore"),
    'New Hampshire': ('미국 대선 첫 프라이머리 주. 뉴잉글랜드 단풍. 화이트마운틴 국립숲. 세금 없는 주',
                      "First state to hold presidential primary elections; White Mountains; no state income or sales tax"),
    'New Jersey': ('뉴욕 근교 위성주. 애틀랜틱시티(카지노). 에디슨(전구 발명)과 아인슈타인 거주지',
                   "Adjacent to NYC; Atlantic City casino resort; Thomas Edison's laboratory; Princeton University; dense population"),
    'New Mexico': ('치리카와·앨버커키. 로스웰 UFO 사건(1947). 멕시코 문화 영향. 핵폭탄 로스앨러모스 연구소',
                   "Roswell UFO incident (1947); Los Alamos National Laboratory (birthplace of atomic bomb); Georgia O'Keeffe arts heritage"),
    'New York': ('뉴욕시(세계 금융·문화 수도). 자유의 여신상. 브로드웨이. 월스트리트',
                 "New York City (world's finance and culture capital); Statue of Liberty; Broadway theater; Wall Street"),
    'North Carolina': ('리서치 트라이앵글(듀크·UNC·NC주립대). 최초 동력 비행(키티호크). 스모키마운틴',
                       "Research Triangle (Duke, UNC, NC State); first powered flight at Kitty Hawk (Wright Brothers); Smoky Mountains"),
    'North Dakota': ('미국 최대 해바라기·밀 산지. 퍼거스폴스 형성. 시팅불 인디언 부족의 땅',
                     "America's top sunflower and wheat producer; Theodore Roosevelt National Park; Sitting Bull's homeland"),
    'Ohio': ('미국 대통령 최다 배출 주(8명). 에어로스페이스 허브(닐 암스트롱·존 글렌 출신). 클리블랜드 록음악명예의전당',
             "Birthplace of 8 US presidents; Neil Armstrong and John Glenn born here; Rock and Roll Hall of Fame in Cleveland"),
    'Oklahoma': ('체로키·크리크 등 아메리카 원주민 영토 역사. 오클라호마 시티 폭탄 테러(1995). 오클라호마 뮤지컬',
                 "Native American territory history (Five Civilized Tribes); Oklahoma City bombing memorial (1995); oil industry"),
    'Oregon': ('포틀랜드 마이크로브루어리 수도. 오리건 트레일(개척자 이주 역사). 크레이터호 국립공원',
               "Portland craft beer capital; Oregon Trail historic route; Crater Lake National Park; Silicon Forest tech hub"),
    'Pennsylvania': ('미국 독립선언서 서명지(필라델피아). 게티즈버그 남북전쟁. 아미시 공동체. 필리 치즈스테이크',
                     "Philadelphia: birthplace of US independence (Liberty Bell, Declaration of Independence); Gettysburg; Amish communities"),
    'Rhode Island': ('미국 최소 주(면적). 로드아일랜드 레드(닭 품종 유래). 뉴포트 브레이커스(도금시대 대저택)',
                     "Smallest US state; Newport's Gilded Age mansions; first US colony to declare independence from Britain"),
    'South Carolina': ('포트섬터(남북전쟁 시작지). 찰스턴 역사 도심. 마스터스 골프 토너먼트 근처. 복숭아 생산',
                       "Fort Sumter (start of Civil War); historic Charleston; Masters Golf Tournament nearby (Augusta); peach production"),
    'South Dakota': ('마운트 러시모어(미국 4대 대통령 조각). 배드랜즈 국립공원. 블랙힐스 금광',
                     "Mount Rushmore (carved faces of 4 presidents); Badlands National Park; Black Hills gold rush history"),
    'Tennessee': ('멤피스 블루스·소울 음악. 내슈빌 컨트리 뮤직 수도. 엘비스 프레슬리 그레이슬랜드',
                  "Nashville: country music capital; Memphis: birthplace of blues and rock 'n' roll; Elvis Presley's Graceland"),
    'Texas': ('미국 대륙 최대 주. 석유 산업. 텍스 멕스 음식. 미항공우주국(NASA) 존슨 우주센터. 미국에서 두 번째로 큰 경제',
              "Largest US state in lower 48; oil industry capital; NASA Johnson Space Center; second largest economy in the US"),
    'Utah': ('모르몬교(LDS 교회) 본거지. 아치스·자이온·브라이스 캐니언 국립공원. 솔트레이크 도시',
             "LDS Church (Mormon) headquarters in Salt Lake City; five national parks (Arches, Zion, Bryce, Canyonlands, Capitol Reef)"),
    'Vermont': ('단풍 시럽 생산 1위(미국 전체의 35%). 스키 리조트. 벤앤제리스 아이스크림 본사',
                "America's top maple syrup producer (35% of US total); ski resorts; Ben & Jerry's ice cream birthplace"),
    'Virginia': ('식민지 시대 최초 영구 영국 정착지(제임스타운). 조지 워싱턴·토머스 제퍼슨 생가. 펜타곤',
                 "First permanent English settlement (Jamestown 1607); birthplace of Washington and Jefferson; Pentagon; Civil War history"),
    'Washington': ('마이크로소프트·아마존·보잉 본사. 스타벅스 발상지. 레이니어 산. 시애틀',
                   "Microsoft, Amazon, Boeing headquarters; Starbucks birthplace (Seattle); Mount Rainier; Columbia River gorge"),
    'West Virginia': ('석탄 광업의 역사. 새넌도어 국립공원. 찰스턴(주도). 미국 남북전쟁 분리 배경',
                      "Coal mining heritage; Shenandoah National Park; split from Virginia during Civil War; New River Gorge"),
    'Wisconsin': ('치즈 생산량 미국 최대(치즈스테이트). 밀워키 할리데이비슨 본사. 그린베이 패커스 NFL',
                  "America's top cheese producer ('Cheese State'); Harley-Davidson Museum in Milwaukee; Green Bay Packers NFL team"),
    'Wyoming': ('옐로스톤 국립공원(미국 최초 국립공원). 그랜드 티턴. 미국 인구 최소 주. 카우보이 문화',
                "Yellowstone (first US national park); Grand Teton National Park; least populous US state; cowboy and ranching culture"),
}

# ── Update Seoul quiz ──────────────────────────────────────────────────────────
with open('data/quiz-korea-seoul.json', encoding='utf-8') as f:
    seoul = json.load(f)

updated = 0
for r in seoul['regions']:
    ko = r['names']['ko']
    if ko in SEOUL_HINTS:
        r['hints'] = {'ko': SEOUL_HINTS[ko][0], 'en': SEOUL_HINTS[ko][1]}
        updated += 1

with open('data/quiz-korea-seoul.json', 'w', encoding='utf-8') as f:
    json.dump(seoul, f, ensure_ascii=False, indent=2)

print(f'Seoul: updated {updated}/{len(seoul["regions"])} hints')
missing = [r['names']['ko'] for r in seoul['regions'] if not r['hints'].get('ko')]
if missing: print(f'  Missing: {missing}')

# ── Update US states quiz ──────────────────────────────────────────────────────
with open('data/quiz-us-states.json', encoding='utf-8') as f:
    us = json.load(f)

updated = 0
for r in us['regions']:
    en = r['names'].get('en', '')
    if en in US_HINTS:
        r['hints'] = {'ko': US_HINTS[en][0], 'en': US_HINTS[en][1]}
        updated += 1

with open('data/quiz-us-states.json', 'w', encoding='utf-8') as f:
    json.dump(us, f, ensure_ascii=False, indent=2)

print(f'US: updated {updated}/{len(us["regions"])} hints')
missing = [r['names'].get('en') for r in us['regions'] if not r['hints'].get('ko')]
if missing: print(f'  Missing: {missing}')

print('Done.')
