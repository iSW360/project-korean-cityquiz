# -*- coding: utf-8 -*-
import json

# id, ko name, en name, ko hint, en hint
PREFS = [
("HOK","홋카이도","Hokkaido","일본 최북단 섬 전체가 하나의 도(道). 삿포로 눈축제. 라멘·해산물·라벤더밭","Japan's northernmost island; Sapporo Snow Festival; famous ramen, seafood, and lavender fields"),
("AOM","아오모리현","Aomori","혼슈 최북단. 네부타 마츠리(등불축제). 사과 생산 일본 1위","Honshu's northernmost prefecture; Nebuta lantern festival; Japan's top apple producer"),
("IWT","이와테현","Iwate","혼슈에서 가장 넓은 현. 히라이즈미(세계유산). 잔소바 국수","Honshu's largest prefecture by area; Hiraizumi World Heritage site; jajamen and wanko-soba noodles"),
("MYG","미야기현","Miyagi","도호쿠 지방 중심 도시 센다이. 마츠시마(일본 3경). 2011년 동일본대지진 피해지","Home to Sendai, Tohoku's largest city; Matsushima, one of Japan's Three Views; hit hard by the 2011 earthquake/tsunami"),
("AKT","아키타현","Akita","나마하게 축제(도깨비 분장). 아키타견의 고향. 쌀·사케 산지","Namahage demon festival; birthplace of the Akita dog breed; rice and sake region"),
("YMG","야마가타현","Yamagata","체리(사쿠란보) 생산 일본 1위. 자오 온천 스키장. 장기말(쇼기고마) 생산지","Japan's top cherry producer; Zao hot spring ski resort; center of shogi piece production"),
("FKS","후쿠시마현","Fukushima","2011년 원전사고 지역. 아이즈와카마츠 사무라이 역사. 복숭아 생산 유명","Site of the 2011 nuclear accident; Aizuwakamatsu samurai history; famous peach production"),
("IBR","이바라키현","Ibaraki","낫토의 고향(미토 낫토). 국화 쓰쿠바산. 우주항공연구개발기구(JAXA) 쓰쿠바 우주센터","Home of Mito natto; Mt. Tsukuba; JAXA's Tsukuba Space Center"),
("TCG","도치기현","Tochigi","닛코 세계유산(도쇼구 신사). 딸기 생산 일본 1위","Nikko World Heritage site (Toshogu Shrine); Japan's top strawberry producer"),
("GNM","군마현","Gunma","구사츠 온천. 도미오카 제사공장(세계유산, 근대 제사업). 다루마 인형 생산지","Kusatsu hot springs; Tomioka Silk Mill World Heritage site; center of daruma doll production"),
("SIT","사이타마현","Saitama","도쿄 위성도시. 가와고에 '작은 에도' 거리. J리그 우라와 레즈 연고지","Tokyo commuter suburb prefecture; Kawagoe's 'Little Edo' streets; home of J-League club Urawa Reds"),
("CHB","지바현","Chiba","도쿄 디즈니랜드·나리타 국제공항 소재지. 낙화생(땅콩) 생산 유명","Home to Tokyo Disneyland and Narita International Airport; famous peanut production"),
("TKY","도쿄도","Tokyo","일본의 수도. 인구 최다 도시권. 시부야·아사쿠사·아키하바라","Japan's capital; the world's most populous metropolitan area; Shibuya, Asakusa, Akihabara"),
("KNG","가나가와현","Kanagawa","요코하마·가마쿠라 소재. 대불(가마쿠라 다이부츠). 하코네 온천 관광지","Home to Yokohama and Kamakura; the Great Buddha of Kamakura; Hakone hot spring resort"),
("NGT","니가타현","Niigata","쌀·사케 명산지(고시히카리). 폭설 지대. 사도가시마 섬(금광 유적)","Famous rice (Koshihikari) and sake region; heavy snowfall area; Sado Island gold mine heritage site"),
("TYM","도야마현","Toyama","구로베 협곡·다테야마 쿠로베 알펜루트. 반다이지마 반딧불오징어","Kurobe Gorge and the Tateyama Kurobe Alpine Route; famous firefly squid of Toyama Bay"),
("ISK","이시카와현","Ishikawa","가나자와 겐로쿠엔(일본 3대 정원). 와지마 칠기 공예","Kanazawa's Kenrokuen, one of Japan's Three Great Gardens; Wajima lacquerware craft"),
("FKI","후쿠이현","Fukui","공룡 화석 발굴지(가쓰야마). 안경테 생산 일본 1위(사바에시)","Major dinosaur fossil site in Katsuyama; Japan's top eyeglass frame producer (Sabae)"),
("YNS","야마나시현","Yamanashi","후지산 북쪽 기슭. 포도·복숭아 생산 유명. 야마나카 호수","Northern foot of Mt. Fuji; famous grape and peach production; Lake Yamanaka"),
("NGN","나가노현","Nagano","1998년 나가노 동계올림픽 개최지. 일본 알프스. 소바 명산지","Host of the 1998 Nagano Winter Olympics; Japanese Alps; famous soba noodle region"),
("GIF","기후현","Gifu","시라카와고 갓쇼즈쿠리 마을(세계유산). 우카이 가마우지 낚시. 세키시 칼 제조","Shirakawa-go gassho-style village, a World Heritage site; traditional cormorant fishing; Seki knife-making"),
("SZO","시즈오카현","Shizuoka","후지산 남쪽 기슭. 녹차 생산 일본 1위. 하마마츠 오토바이 산업(야마하·혼다)","Southern foot of Mt. Fuji; Japan's top green tea producer; Hamamatsu motorcycle industry (Yamaha, Honda)"),
("AIC","아이치현","Aichi","나고야 소재. 도요타 자동차 본사. 일본 3대 도시권 중 하나","Home to Nagoya; Toyota Motor headquarters; one of Japan's three major metropolitan areas"),
("MIE","미에현","Mie","이세신궁(일본 신도 총본산). 진주 양식의 발상지(미키모토)","Ise Grand Shrine, Shinto's most sacred site; birthplace of cultured pearls (Mikimoto)"),
("SIG","시가현","Shiga","비와호(일본 최대 호수) 소재. 히코네 성","Home to Lake Biwa, Japan's largest lake; Hikone Castle"),
("KYT","교토부","Kyoto","일본의 옛 수도(헤이안쿄). 기요미즈데라·후시미이나리·금각사","Japan's ancient capital (Heian-kyo); Kiyomizu-dera, Fushimi Inari, Kinkaku-ji temples"),
("OSK","오사카부","Osaka","일본 2대 도시. 오사카성. 다코야키·오코노미야키의 본고장","Japan's second-largest metropolis; Osaka Castle; birthplace of takoyaki and okonomiyaki"),
("HYG","효고현","Hyogo","고베 소재. 고베규(와규) 유명. 히메지성(세계유산)","Home to Kobe; famous Kobe beef; Himeji Castle World Heritage site"),
("NAR","나라현","Nara","일본 최초의 수도(헤이조쿄). 도다이지 대불·사슴공원","Japan's first capital (Heijo-kyo); Todai-ji Great Buddha and the deer park"),
("WKY","와카야마현","Wakayama","고야산(불교 성지, 세계유산). 판다 서식 아드벤처월드","Mt. Koya Buddhist sanctuary, World Heritage site; Adventure World famous for its pandas"),
("TTR","돗토리현","Tottori","일본 인구 최소 현. 돗토리 사구(모래언덕)","Japan's least populous prefecture; the famous Tottori Sand Dunes"),
("SMN","시마네현","Shimane","이즈모타이샤(일본 최고 신사 중 하나). 이와미 은광(세계유산)","Izumo-taisha, one of Japan's most important shrines; Iwami Ginzan Silver Mine World Heritage site"),
("OKY","오카야마현","Okayama","모모타로(복숭아 동자) 전설의 고장. 구라시키 옛 거리","Legendary home of Momotaro the Peach Boy; Kurashiki's historic canal district"),
("HRS","히로시마현","Hiroshima","1945년 원자폭탄 투하 도시. 원폭돔·미야지마 이쓰쿠시마신사(세계유산)","City hit by the 1945 atomic bomb; Atomic Bomb Dome and Itsukushima Shrine on Miyajima, World Heritage sites"),
("YGC","야마구치현","Yamaguchi","혼슈 최서단. 메이지유신 주역들의 고향(조슈번). 후구(복어) 요리 명산지","Westernmost tip of Honshu; birthplace of Meiji Restoration leaders (Choshu domain); famous fugu (pufferfish) cuisine"),
("TKS","도쿠시마현","Tokushima","아와오도리 춤 축제. 나루토 해협의 소용돌이","Awa Odori dance festival; the famous Naruto whirlpools"),
("KGW","가가와현","Kagawa","일본에서 가장 작은 현. 사누키 우동의 본고장","Japan's smallest prefecture by area; home of Sanuki udon noodles"),
("EHM","에히메현","Ehime","도고온천(일본에서 가장 오래된 온천 중 하나). 감귤 생산 유명","Dogo Onsen, one of Japan's oldest hot springs; famous citrus (mikan) production"),
("KCH","고치현","Kochi","가다랑어(가츠오) 요리 유명. 사카모토 료마(메이지유신 지사)의 고향","Famous bonito (katsuo) cuisine; birthplace of Meiji Restoration hero Sakamoto Ryoma"),
("FKO","후쿠오카현","Fukuoka","규슈 최대 도시(후쿠오카시·기타큐슈). 하카타 라멘·모츠나베","Kyushu's largest city area (Fukuoka, Kitakyushu); famous Hakata ramen and motsunabe hot pot"),
("SAG","사가현","Saga","아리타 도자기(일본 최초의 자기) 산지. 요시노가리 유적","Arita porcelain, Japan's first porcelain ware; Yoshinogari archaeological site"),
("NGS","나가사키현","Nagasaki","1945년 원자폭탄 투하 도시. 에도시대 유일한 서양 무역창구(데지마)","City hit by the 1945 atomic bomb; Dejima, Japan's sole window to the West during the Edo period"),
("KMM","구마모토현","Kumamoto","구마모토성. 아소산(세계 최대급 칼데라) 활화산","Kumamoto Castle; Mt. Aso, one of the world's largest calderas and an active volcano"),
("OIT","오이타현","Oita","벳푸·유후인 온천(일본 최대 온천지). 온천 용출량 일본 1위","Beppu and Yufuin hot spring resorts; Japan's largest volume of hot spring water"),
("MYZ","미야자키현","Miyazaki","일본 건국신화의 무대(다카치호). 프로야구·축구 스프링캠프 명소","Setting of Japan's creation myths (Takachiho Gorge); popular spring training site for pro baseball and soccer"),
("KGS","가고시마현","Kagoshima","사쿠라지마 활화산. 사쓰마번(메이지유신 주역). 흑돼지 요리","Active volcano Sakurajima; Satsuma domain, key player in the Meiji Restoration; famous black pork cuisine"),
("OKN","오키나와현","Okinawa","옛 류큐왕국. 일본 유일 아열대 기후. 슈리성(세계유산)·산호초 다이빙","Former Ryukyu Kingdom; Japan's only subtropical prefecture; Shuri Castle World Heritage site and coral reef diving"),
]

regions = []
for rid, ko, en, ko_hint, en_hint in PREFS:
    regions.append({
        "id": rid,
        "svgPathId": f"r{rid}",
        "names": {"ko": ko, "en": en},
        "hints": {"ko": ko_hint, "en": en_hint}
    })

out = {
    "meta": {
        "id": "japan",
        "mapSvg": "/maps/world/japan.svg",
        "defaultLang": "ko",
        "totalRegions": len(regions)
    },
    "regions": regions
}

with open("data/quiz-japan.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"Wrote data/quiz-japan.json with {len(regions)} prefectures")
