"""Generate 2026 FIFA World Cup quiz map (48 nations on world map)."""
import json, math, urllib.request, os

NE_COUNTRIES_CACHE = 'ne_50m_countries.geojson'
NE_MAP_UNITS_URL   = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_map_units.geojson'
NE_MAP_UNITS_CACHE = 'ne_50m_map_units.geojson'

# ── 48개 출전국 데이터 ────────────────────────────────────────────────────────
# key = ISO_A3 (잉글랜드·스코틀랜드는 GU_A3)
# (ko_name, en_name, confederation, ko_hint, en_hint)
WC_TEAMS = {
# ── UEFA 유럽 (16) ───────────────────────────────────────────────────────────
'ENG':('잉글랜드','England','UEFA',
    '1966 자국 월드컵 유일 우승. 해리 케인·벨링엄. 프리미어리그 종주국. 1872년 세계 최초 국제경기',
    "Only World Cup win in 1966 on home soil; Harry Kane, Bellingham; home of the Premier League"),
'SCO':('스코틀랜드','Scotland','UEFA',
    '1872년 잉글랜드와 세계 최초 국제경기 상대. 셀틱·레인저스 올드펌 라이벌. 맥토미니·로버트슨',
    "Played in world's first international (1872 vs England); Old Firm Celtic-Rangers rivalry; McTominay"),
'FRA':('프랑스','France','UEFA',
    '2018 챔피언. 음바페·그리즈만. 레 블뢰. 1998 자국 개최 첫 우승. 2회 월드컵 우승',
    "2018 champions; Mbappé, Griezmann; Les Bleus; two-time World Cup winners (1998, 2018)"),
'HRV':('크로아티아','Croatia','UEFA',
    '2018 준우승·2022 3위. 모드리치(발롱도르). 발칸 축구의 자존심. 체크무늬 유니폼',
    "2018 runners-up, 2022 third place; Luka Modrić (Ballon d'Or); iconic checkered jersey"),
'NOR':('노르웨이','Norway','UEFA',
    '얼링 홀란드(역대 EPL 최다 득점). 홀란드 세대 덕분에 처음으로 월드컵 본선 진출',
    "Home of Erling Haaland (Premier League all-time top scorer); first World Cup in modern era"),
'PRT':('포르투갈','Portugal','UEFA',
    '호날두 시대에서 주앙 펠릭스 세대로. 2016 유로 챔피언. 황금세대·2022 8강',
    "Transition from Ronaldo era to new generation; 2016 European champions; 2022 quarter-finals"),
'DEU':('독일','Germany','UEFA',
    '4회 월드컵 우승(1954·74·90·2014). 전차군단(Die Mannschaft). 무시알라·키미히',
    "Four-time World Cup winners (1954, 74, 90, 2014); Die Mannschaft; Musiala and Kimmich era"),
'NLD':('네덜란드','Netherlands','UEFA',
    '토탈 풋볼의 나라(요한 크루이프). 반다이크·뎁시·가크포. 3회 준우승. 오렌지 군단',
    "Birthplace of Total Football (Johan Cruyff); Van Dijk; three-time runners-up; Oranje"),
'CHE':('스위스','Switzerland','UEFA',
    '자카·샤카 형제 배출. 유럽의 복병. 8회 연속 월드컵 진출. 16강 단골손님',
    "Produced Xhaka and Shaqiri; consistent European dark horse; eight consecutive World Cups"),
'ESP':('스페인','Spain','UEFA',
    '2010 챔피언. 티키타카 창시자. 라민 야말(역대 최연소 유로 득점). 바르셀로나·레알 왕국',
    "2010 champions; tiki-taka creators; Lamine Yamal (youngest Euro scorer ever); LaLiga powers"),
'AUT':('오스트리아','Austria','UEFA',
    '마르코 아르나우토비치. 그렉시·라이너 세대. 2024 유로 8강. 중유럽 다크호스',
    "Marko Arnautović; Gregoritsch-Laimer generation; Euro 2024 quarter-finalists; dark horse"),
'BEL':('벨기에','Belgium','UEFA',
    '황금세대(루카쿠·데브라위너·아자르) 마무리. 2018 3위. 피파 랭킹 오랫동안 1위',
    "Golden Generation (Lukaku, De Bruyne, Hazard); 3rd place 2018; long-time FIFA #1 ranked"),
'BIH':('보스니아 헤르체고비나','Bosnia and Herzegovina','UEFA',
    '유럽 플레이오프 결승서 이탈리아 꺾고 진출. 코디치·콜라시나츠. 사라예보의 축구 열정',
    "Beat Italy in European playoff final; Kodić, Kolasinac; passionate football culture in Sarajevo"),
'SWE':('스웨덴','Sweden','UEFA',
    '이브라히모비치의 나라(은퇴). 1994 3위. 이사크·포르스베리. 스칸디나비아 대표',
    "Ibrahimović era over; 1994 third place; Isak and Forsberg era; Scandinavian football"),
'TUR':('튀르키예','Turkey','UEFA',
    '2002 월드컵 3위. 아르다 귈레르(레알 마드리드). 튀르키예 르네상스 시대',
    "3rd place 2002 World Cup; Arda Güler (Real Madrid); Turkish football renaissance"),
'CZE':('체코','Czech Republic','UEFA',
    '체코슬로바키아 시절 1934·62 준우승. 파티크 슈칙·콜라르. 중유럽 전통 강호',
    "As Czechoslovakia, runners-up 1934 and 1962; Patrik Schick; Central European stalwart"),

# ── CONMEBOL 남아메리카 (6) ──────────────────────────────────────────────────
'ARG':('아르헨티나','Argentina','CONMEBOL',
    '2022 챔피언(3회 우승). 메시 시대 이후 재건. 알바레스·파레데스·마르티네스. 라 알비셀레스테',
    "2022 champions (3 titles); post-Messi era rebuild; Álvarez, Martínez; La Albiceleste"),
'BRA':('브라질','Brazil','CONMEBOL',
    '5회 우승(역대 최다). 비니시우스 주니오르·엔드릭크. 셀레상. 삼바 축구. 역대 WC 최다 출전',
    "Five-time winners (most ever); Vinícius Júnior, Endrick; Seleção; samba football"),
'COL':('콜롬비아','Colombia','CONMEBOL',
    '2024 코파아메리카 결승 진출. 루이스 디아스(리버풀)·하메스 로드리게스 이후 황금세대',
    "2024 Copa América finalists; Luis Díaz (Liverpool); new golden generation post-James Rodríguez"),
'ECU':('에콰도르','Ecuador','CONMEBOL',
    '에네르 발렌시아·이스라 플로레스. 안데스 산맥 홈 어드밴티지(고지대 훈련). 3회 연속 WC',
    "Enner Valencia; Andes altitude home advantage; three consecutive World Cups"),
'PRY':('파라과이','Paraguay','CONMEBOL',
    '남미의 수문장. 수비 전술 강호. 2010 8강. 과라니 문화. 라틴아메리카 축구 복병',
    "South America's defensive powerhouse; 2010 quarter-finalists; Guaraní football culture"),
'URY':('우루과이','Uruguay','CONMEBOL',
    '최초 월드컵 챔피언(1930·50 2회 우승). 누녜스(리버풀)·발베르데. 셀레스테. 작은 나라 큰 축구',
    "First and two-time World Cup champions (1930, 1950); Núñez and Valverde; Celeste"),

# ── CONCACAF 북중미카리브 (6) ────────────────────────────────────────────────
'USA':('미국','USA','CONCACAF',
    '공동 개최국. MLS 성장. 풀리식·웨아·아라우호. 1930·94 WC 개최. 축구 성장 진행 중',
    "Co-host; MLS growing; Pulisic, Weah, Araújo; hosted 1994; US soccer on the rise"),
'CAN':('캐나다','Canada','CONCACAF',
    '공동 개최국. 역대 2번째 WC(1986 이후 40년). 알폰소 데이비스(바이에른)·조나단 데이비드',
    "Co-host; second World Cup ever (40 years after 1986); Alphonso Davies (Bayern), Jonathan David"),
'MEX':('멕시코','Mexico','CONCACAF',
    '공동 개최국. 7회 연속 16강(1994-2018) 이후 부진. 엘 트리. 아스테카 스타디움의 전설',
    "Co-host; 7 straight round of 16 (1994-2018); El Tri; legendary Azteca Stadium history"),
'PAN':('파나마','Panama','CONCACAF',
    '2018 첫 월드컵 이후 2회 연속 진출. 에릭 데이비스·아데마르 가리도. 중미 신흥 강호',
    "Two consecutive World Cups after debut in 2018; Éric Davis; rising Central American force"),
'HTI':('아이티','Haiti','CONCACAF',
    '카리브해 축구 강호. 48팀 체제 확대 수혜. 나이젤 아바·귈라노 형제. 1974 WC 이후 52년 만',
    "Caribbean powerhouse; beneficiary of 48-team expansion; first World Cup since 1974"),
'CUW':('퀴라소','Curaçao','CONCACAF',
    '첫 월드컵 진출! 네덜란드령 카리브 섬(인구 15만). 역대 최소국 WC 데뷔 중 하나',
    "First ever World Cup! Dutch Caribbean island (population 150,000); historic debut"),

# ── CAF 아프리카 (10) ────────────────────────────────────────────────────────
'MAR':('모로코','Morocco','CAF',
    '2022 4강(아프리카 역대 최고). 아틀라스 라이언스. 지야슈·엔 네시리. 북아프리카 대표',
    "2022 semi-finalists (Africa's best ever); Atlas Lions; Ziyech, En-Nesyri; North African kings"),
'TUN':('튀니지','Tunisia','CAF',
    '카르타고 독수리. 7회 WC 진출. 북아프리카 전통 강호. 마네스·브룸·드라게르',
    "Carthage Eagles; seven World Cups; North African stalwart; Msakni and Bronn generation"),
'EGY':('이집트','Egypt','CAF',
    '모하메드 살라의 나라. 파라오. 아프리카 챔피언십 7회 우승(최다). 피라미드 FC 문화',
    "Mohamed Salah's country; The Pharaohs; seven Africa Cup of Nations titles (most ever)"),
'DZA':('알제리','Algeria','CAF',
    '2019 아프리카 챔피언. 여우들. 마나 베나우아·이스마일 베나세르(AC밀란). 북아프리카 강호',
    "2019 Africa Cup winners; Les Fennecs (The Foxes); Bennacer (AC Milan); North African force"),
'GHA':('가나','Ghana','CAF',
    '블랙스타스. 2010 8강(아프리카 역대 최고 공동). 파르티(아스널)·쿠두스. 서아프리카 대표',
    "Black Stars; 2010 quarter-finalists (Africa record); Thomas Partey (Arsenal); West Africa"),
'CPV':('카보베르데','Cape Verde','CAF',
    '상어들. 소국의 기적(인구 56만). 아프리카 랭킹 상승 중. 주앙 필리페·조나스 군도',
    "The Sharks; miracle of a 560,000-population island nation; rising African ranking"),
'ZAF':('남아프리카공화국','South Africa','CAF',
    '바파나 바파나. 2010 WC 개최국. 아프리카 최초 WC 개최. 스피코 음부아·파르코',
    "Bafana Bafana; hosted 2010 World Cup (Africa's first); Sphiko Mbua; rainbow nation football"),
'CIV':('코트디부아르','Ivory Coast','CAF',
    '코끼리. 드로그바 이후 재건. 세바스티앙 알레르·시모 피나우·포파나. 서아프리카 강호',
    "Les Éléphants; post-Drogba rebuilding; Sébastien Haller, Fofana; West African powerhouse"),
'SEN':('세네갈','Senegal','CAF',
    '2021·2022 아프리카 챔피언. 사디오 마네·이드리사 게이에·파티 디아. 테랑가 라이온즈',
    "2021 and 2022 Africa Cup champions; Sadio Mané, Idrissa Gueye; Lions of Teranga"),
'COD':('콩고민주공화국','DR Congo','CAF',
    '아프리카 거인의 귀환. 대륙간 플레이오프 극복. 치아니·바카마부. 아프리카 2번째 큰 나라',
    "Africa's giant returns; won intercontinental playoff; Cuypers, Bakambu; 2nd largest African country"),

# ── AFC 아시아 (9) ───────────────────────────────────────────────────────────
'KOR':('한국','South Korea','AFC',
    '태극전사. 2002 4강 신화(아시아 역대 최고). 손흥민(토트넘)·이강인(PSG). 아시아 최다 WC 출전(공동)',
    "Taeguk Warriors; 2002 semi-finals (Asia's best ever); Son Heung-min (Spurs), Lee Kang-in (PSG)"),
'JPN':('일본','Japan','AFC',
    '사무라이 블루. 아시아 최다 WC 출전(8회). 도안 리츠·미토마 카오루. 2022 스페인·독일 격파',
    "Samurai Blue; most World Cups in Asia (8 times); Doan, Mitoma; shocked Spain and Germany 2022"),
'IRN':('이란','Iran','AFC',
    '팀 멜리. 아시아 최다 WC 출전 공동. 메흐디 타레미(인터밀란). 중동 최강 전통 축구 강국',
    "Team Melli; joint most World Cups in Asia; Mehdi Taremi (Inter Milan); Middle East powerhouse"),
'UZB':('우즈베키스탄','Uzbekistan','AFC',
    '첫 월드컵 진출! 중앙아시아 신흥 축구 강국. 쇼무로도프(로마)·호자마토프. 역사적 데뷔',
    "First ever World Cup! Central Asian rising power; Shomurodov (Roma); historic debut"),
'JOR':('요르단','Jordan','AFC',
    '첫 월드컵 진출! 플레이오프 극복. 야잔 알 나이마트. 아랍 세계의 새 축구 강호',
    "First ever World Cup! Won via playoff; Yazan Al Naimat; new force in Arab football"),
'AUS':('호주','Australia','AFC',
    '사커루스. 2006 16강. 해리 사우터·마티 라이언. AFC 편입 후 아시아 강호 자리매김',
    "Socceroos; 2006 round of 16; Harry Souttar, Mat Ryan; dominant in AFC since joining"),
'QAT':('카타르','Qatar','AFC',
    '2022 개최국 조별리그 탈락. 재도전. 알모에즈 알리. 소국 축구 투자 모델. 아스파이어 아카데미',
    "2022 host eliminated in group stage; redemption quest; Al-Moez Ali; Aspire Academy model"),
'SAU':('사우디아라비아','Saudi Arabia','AFC',
    '2022 아르헨티나 격파 대이변. 살레크·알다우사리. 사우디 프로리그 세계적 선수 영입 붐',
    "Shocked Argentina in 2022; Salem Al-Dawsari; Saudi Pro League global signing spree"),
'IRQ':('이라크','Iraq','AFC',
    '대륙간 플레이오프 극복 진출. 아이멘 후세인. 2007 아시안컵 챔피언. 아랍권 전통 강호',
    "Qualified via intercontinental playoff; Aymen Hussein; 2007 Asian Cup champions"),

# ── OFC 오세아니아 (1) ───────────────────────────────────────────────────────
'NZL':('뉴질랜드','New Zealand','OFC',
    '올 화이츠. 오세아니아 대표. 크리스 우드(뉴캐슬). 플레이오프 통해 본선 진출. 럭비의 나라',
    "All Whites; Oceania representative; Chris Wood (Newcastle); qualified via playoff; rugby nation"),
}

# UK 팀은 admin_0_map_units에서 가져옴
UK_TEAMS = {'ENG', 'SCO'}

# ── 지도 설정 ─────────────────────────────────────────────────────────────────
W, H, PAD = 960, 480, 8
LON0, LON1, LAT0, LAT1 = -170, 180, -57, 80

# ── 투영 (등장방형도법) ──────────────────────────────────────────────────────
def proj(lon, lat):
    x = PAD + (lon - LON0) / (LON1 - LON0) * (W - 2*PAD)
    y = H - PAD - (lat - LAT0) / (LAT1 - LAT0) * (H - 2*PAD)
    return round(x, 1), round(y, 1)

# ── Douglas-Peucker ──────────────────────────────────────────────────────────
def _dist(px,py,ax,ay,bx,by):
    dx,dy=bx-ax,by-ay
    if dx==0 and dy==0: return math.hypot(px-ax,py-ay)
    t=max(0,min(1,((px-ax)*dx+(py-ay)*dy)/(dx*dx+dy*dy)))
    return math.hypot(px-(ax+t*dx),py-(ay+t*dy))

def dp(pts, eps):
    if len(pts)<3: return pts
    dmax,idx=0,0
    a,b=pts[0],pts[-1]
    for i in range(1,len(pts)-1):
        d=_dist(pts[i][0],pts[i][1],a[0],a[1],b[0],b[1])
        if d>dmax: dmax,idx=d,i
    if dmax>=eps:
        return dp(pts[:idx+1],eps)[:-1]+dp(pts[idx:],eps)
    return [pts[0],pts[-1]]

MIN_SZ = 7   # 소국 최소 표시 크기(px)
SKIP_BG = 2  # 배경에서 이 크기 이하 링은 건너뜀
SKIP_WC = 2  # WC 출전국에서 소도서 건너뜀 임계값

def bbox_wh(pts):
    if len(pts)<2: return 0,0
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    return max(xs)-min(xs), max(ys)-min(ys)

def ring_path(pts):
    if len(pts)<3: return ''
    return 'M'+' '.join(f'{x},{y}' for x,y in pts)+'Z'

def get_polys(geom):
    if geom['type']=='Polygon': return [geom['coordinates']]
    if geom['type']=='MultiPolygon': return geom['coordinates']
    return []

def geom_to_bg(geom, eps=2.5):
    """배경용: 작은 링은 그냥 건너뜀 (박스 없음)"""
    parts=[]
    for poly in get_polys(geom):
        raw=[proj(lon,lat) for lon,lat,*_ in poly[0]
             if LON0-20<=lon<=LON1+20]
        simp=dp(raw,eps)
        if len(simp)<3: continue
        w,h=bbox_wh(simp)
        if w<SKIP_BG and h<SKIP_BG: continue  # 너무 작으면 그냥 건너뜀
        parts.append(ring_path(simp))
    return ' '.join(parts)

def geom_to_wc(geom, eps=0.8):
    """출전국용: 나라 전체가 작을 때만 확장, 소도서는 건너뜀"""
    all_rings=[]
    all_raw=[]   # DP 전 원본 좌표 (bbox 체크용)
    for poly in get_polys(geom):
        raw=[proj(lon,lat) for lon,lat,*_ in poly[0]
             if LON0-20<=lon<=LON1+20]
        if raw: all_raw.extend(raw)
        simp=dp(raw,eps)
        if len(simp)>=3:
            all_rings.append(simp)
    if not all_raw: return ''

    # 나라 전체 bbox는 원본 좌표로 판단 (DP 후 점이 없어도 체크 가능)
    w,h=bbox_wh(all_raw)
    if w<MIN_SZ and h<MIN_SZ:
        # 소국(퀴라소·카보베르데 등) → 전체를 작은 사각형으로
        cx=sum(p[0] for p in all_raw)/len(all_raw)
        cy=sum(p[1] for p in all_raw)/len(all_raw)
        r=MIN_SZ/2
        return ring_path([(cx-r,cy-r),(cx+r,cy-r),(cx+r,cy+r),(cx-r,cy+r),(cx-r,cy-r)])

    # 큰 나라 → 링별로 작은 소도서는 건너뜀
    parts=[]
    for simp in all_rings:
        rw,rh=bbox_wh(simp)
        if rw<SKIP_WC and rh<SKIP_WC: continue
        parts.append(ring_path(simp))

    if not parts:
        # 군도 국가(Cape Verde 등): 섬 개별론 너무 작지만 국가 중심에 사각형 표시
        cx=sum(p[0] for p in all_raw)/len(all_raw)
        cy=sum(p[1] for p in all_raw)/len(all_raw)
        r=MIN_SZ/2
        return ring_path([(cx-r,cy-r),(cx+r,cy-r),(cx+r,cy+r),(cx-r,cy+r),(cx-r,cy-r)])
    return ' '.join(parts)

# ── Curaçao 수동 위치 (NE에 없을 경우 폴백) ──────────────────────────────────
def cuw_manual():
    """퀴라소 수동 좌표 (카리브해 네덜란드령)"""
    cx,cy=proj(-68.95, 12.2); r=MIN_SZ/2
    return f'M{cx-r},{cy-r} {cx+r},{cy-r} {cx+r},{cy+r} {cx-r},{cy+r}Z'

# ── 데이터 로드 ────────────────────────────────────────────────────────────────
def load(cache, url=None):
    if not os.path.exists(cache):
        print(f'Downloading {cache}...',flush=True)
        urllib.request.urlretrieve(url, cache)
    with open(cache,encoding='utf-8') as f:
        return json.load(f)

countries_data = load(NE_COUNTRIES_CACHE)
map_units_data = load(NE_MAP_UNITS_CACHE, NE_MAP_UNITS_URL)

# ── 배경 (전 세계 국가, 흐리게) ──────────────────────────────────────────────
print('배경 국가 생성 중...',flush=True)
bg_paths=[]
for feat in countries_data['features']:
    g=feat.get('geometry');
    if not g: continue
    d=geom_to_bg(g)
    if d: bg_paths.append(f'<path d="{d}"/>')

# ── 출전국 레이어 ─────────────────────────────────────────────────────────────
wc_paths=[]
regions=[]
found=set()

NAME_FIX_COUNTRIES={'France':'FRA','Norway':'NOR','Kosovo':'XKX'}

# 잉글랜드·스코틀랜드: map_units에서
for feat in map_units_data['features']:
    props=feat['properties']
    gu=props.get('GU_A3','').strip()
    name=props.get('NAME','').strip()
    tid=None
    if gu in UK_TEAMS: tid=gu
    elif name=='England': tid='ENG'
    elif name=='Scotland': tid='SCO'
    if not tid or tid in found or tid not in WC_TEAMS: continue
    g=feat.get('geometry');
    if not g: continue
    d=geom_to_wc(g,eps=0.5)
    if not d: continue
    ko,en,conf,kh,eh=WC_TEAMS[tid]
    found.add(tid)
    wc_paths.append(f'<path id="r{tid}" data-id="{tid}" data-ko="{ko}" data-en="{en}" data-grp="{conf}" d="{d}"/>')
    regions.append({'id':tid,'svgPathId':f'r{tid}','names':{'ko':ko,'en':en},'hints':{'ko':kh,'en':eh}})

# 나머지: countries에서
for feat in countries_data['features']:
    props=feat['properties']
    iso=props.get('ISO_A3','').strip()
    name=props.get('NAME','').strip()
    if name in NAME_FIX_COUNTRIES: iso=NAME_FIX_COUNTRIES[name]
    if iso not in WC_TEAMS or iso in UK_TEAMS or iso in found: continue
    ko,en,conf,kh,eh=WC_TEAMS[iso]
    g=feat.get('geometry');
    if not g: continue
    d=geom_to_wc(g)
    if not d: continue
    found.add(iso)
    wc_paths.append(f'<path id="r{iso}" data-id="{iso}" data-ko="{ko}" data-en="{en}" data-grp="{conf}" d="{d}"/>')
    regions.append({'id':iso,'svgPathId':f'r{iso}','names':{'ko':ko,'en':en},'hints':{'ko':kh,'en':eh}})

# 퀴라소 폴백
if 'CUW' not in found:
    ko,en,conf,kh,eh=WC_TEAMS['CUW']
    d=cuw_manual(); found.add('CUW')
    wc_paths.append(f'<path id="rCUW" data-id="CUW" data-ko="{ko}" data-en="{en}" data-grp="{conf}" d="{d}"/>')
    regions.append({'id':'CUW','svgPathId':'rCUW','names':{'ko':ko,'en':en},'hints':{'ko':kh,'en':eh}})
    print('  퀴라소: 수동 좌표 사용')

# ── SVG 출력 ──────────────────────────────────────────────────────────────────
os.makedirs('maps/world',exist_ok=True)
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">\n'
       f'<g id="bg-countries" pointer-events="none">\n'
       +'\n'.join(bg_paths)
       +'\n</g>\n<g id="regions">\n'
       +'\n'.join(wc_paths)
       +'\n</g>\n</svg>')
with open('maps/world/worldcup2026.svg','w',encoding='utf-8') as f:
    f.write(svg)

# ── JSON 출력 ─────────────────────────────────────────────────────────────────
quiz={'meta':{'id':'worldcup2026','mapSvg':'/maps/world/worldcup2026.svg','defaultLang':'ko','totalRegions':len(regions)},'regions':regions}
with open('data/quiz-worldcup2026.json','w',encoding='utf-8') as f:
    json.dump(quiz,f,ensure_ascii=False,indent=2)

print(f'\n완료: {len(regions)}/48개국')
missing=set(WC_TEAMS)-found
if missing: print(f'누락: {sorted(missing)}')
