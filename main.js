const difficultySelector = document.getElementById('difficulty-selector');
const quizContainer = document.getElementById('quiz-container');
const level1Btn = document.getElementById('level-1-btn');
const level2Btn = document.getElementById('level-2-btn');

const questionTextElement = document.getElementById('question-text');
const optionsArea = document.getElementById('options-area');
const feedbackTextElement = document.getElementById('feedback-text');
const progressArea = document.getElementById('progress-area');
const currentQuestionElement = document.getElementById('current-question');
const totalQuestionsElement = document.getElementById('total-questions');
const nextQuestionBtn = document.getElementById('next-question-btn');
const restartBtn = document.getElementById('restart-btn');
const mapErrorInfo = document.getElementById('map-error-info');

let map;
let marker;
let geoJsonLayer; 



// --- 데이터 시작 ---
const locations = [
    // 특별시/광역시/특별자치시 (8개)
    { name: "서울", lat: 37.5665, lng: 126.9780, zoom: 9, geoName: "서울특별시" },
    { name: "부산", lat: 35.1796, lng: 129.0756, zoom: 9, geoName: "부산광역시" },
    { name: "인천", lat: 37.4563, lng: 126.7052, zoom: 9, geoName: "인천광역시" },
    { name: "대구", lat: 35.8714, lng: 128.6014, zoom: 9, geoName: "대구광역시" },
    { name: "광주", lat: 35.1601, lng: 126.8515, zoom: 9, geoName: "광주광역시" },
    { name: "대전", lat: 36.3504, lng: 127.3845, zoom: 9, geoName: "대전광역시" },
    { name: "울산", lat: 35.5384, lng: 129.3114, zoom: 9, geoName: "울산광역시" },
    { name: "세종", lat: 36.4801, lng: 127.2890, zoom: 10, geoName: "세종특별자치시" },
    
    // 경기도 (28개 시)
    { name: "수원시", lat: 37.2636, lng: 127.0286, zoom: 10, geoName: "수원시" },
    { name: "성남시", lat: 37.4200, lng: 127.1269, zoom: 10, geoName: "성남시" },
    { name: "고양시", lat: 37.6584, lng: 126.8320, zoom: 10, geoName: "고양시" },
    { name: "용인시", lat: 37.2410, lng: 127.1779, zoom: 10, geoName: "용인시" },
    { name: "부천시", lat: 37.4986, lng: 126.7830, zoom: 11, geoName: "부천시" },
    { name: "안산시", lat: 37.3219, lng: 126.8309, zoom: 10, geoName: "안산시" },
    { name: "안양시", lat: 37.3943, lng: 126.9568, zoom: 11, geoName: "안양시" },
    { name: "평택시", lat: 36.9923, lng: 127.1127, zoom: 10, geoName: "평택시" },
    { name: "화성시", lat: 37.1995, lng: 126.8313, zoom: 10, geoName: "화성시" },
    { name: "남양주시", lat: 37.6360, lng: 127.2165, zoom: 10, geoName: "남양주시" },
    { name: "의정부시", lat: 37.7380, lng: 127.0336, zoom: 11, geoName: "의정부시" },
    { name: "시흥시", lat: 37.3800, lng: 126.8029, zoom: 10, geoName: "시흥시" },
    { name: "파주시", lat: 37.7600, lng: 126.7799, zoom: 10, geoName: "파주시" },
    { name: "김포시", lat: 37.6153, lng: 126.7157, zoom: 10, geoName: "김포시" },
    { name: "광명시", lat: 37.4786, lng: 126.8650, zoom: 11, geoName: "광명시" },
    { name: "군포시", lat: 37.3616, lng: 126.9350, zoom: 11, geoName: "군포시" },
    { name: "광주시", lat: 37.4292, lng: 127.2550, zoom: 10, geoName: "광주시" }, 
    { name: "이천시", lat: 37.2799, lng: 127.4340, zoom: 10, geoName: "이천시" },
    { name: "양주시", lat: 37.7853, lng: 127.0458, zoom: 10, geoName: "양주시" },
    { name: "오산시", lat: 37.1499, lng: 127.0776, zoom: 11, geoName: "오산시" },
    { name: "구리시", lat: 37.5939, lng: 127.1406, zoom: 11, geoName: "구리시" },
    { name: "안성시", lat: 37.0080, lng: 127.2797, zoom: 10, geoName: "안성시" },
    { name: "포천시", lat: 37.8949, lng: 127.2000, zoom: 10, geoName: "포천시" },
    { name: "의왕시", lat: 37.3448, lng: 126.9688, zoom: 11, geoName: "의왕시" },
    { name: "하남시", lat: 37.5393, lng: 127.2147, zoom: 11, geoName: "하남시" },
    { name: "여주시", lat: 37.2983, lng: 127.6370, zoom: 10, geoName: "여주시" },
    { name: "동두천시", lat: 37.9036, lng: 127.0576, zoom: 11, geoName: "동두천시" },
    { name: "과천시", lat: 37.4292, lng: 126.9878, zoom: 11, geoName: "과천시" },

    // 강원특별자치도 (7개 시)
    { name: "춘천시", lat: 37.8813, lng: 127.7298, zoom: 10, geoName: "춘천시" },
    { name: "원주시", lat: 37.3425, lng: 127.9202, zoom: 10, geoName: "원주시" },
    { name: "강릉시", lat: 37.7519, lng: 128.8761, zoom: 10, geoName: "강릉시" },
    { name: "동해시", lat: 37.5217, lng: 129.1139, zoom: 10, geoName: "동해시" },
    { name: "속초시", lat: 38.2070, lng: 128.5918, zoom: 10, geoName: "속초시" },
    { name: "삼척시", lat: 37.4498, lng: 129.1653, zoom: 10, geoName: "삼척시" },
    { name: "태백시", lat: 37.1656, lng: 128.9856, zoom: 10, geoName: "태백시" },

    // 충청북도 (3개 시)
    { name: "청주시", lat: 36.6424, lng: 127.4891, zoom: 10, geoName: "청주시" },
    { name: "충주시", lat: 36.9712, lng: 127.9299, zoom: 10, geoName: "충주시" },
    { name: "제천시", lat: 37.1325, lng: 128.1922, zoom: 10, geoName: "제천시" },
    
    // 충청남도 (8개 시)
    { name: "천안시", lat: 36.8151, lng: 127.1139, zoom: 10, geoName: "천안시" },
    { name: "공주시", lat: 36.4525, lng: 127.1200, zoom: 10, geoName: "공주시" },
    { name: "보령시", lat: 36.3334, lng: 126.6102, zoom: 10, geoName: "보령시" },
    { name: "아산시", lat: 36.7898, lng: 127.0020, zoom: 10, geoName: "아산시" },
    { name: "서산시", lat: 36.7800, lng: 126.4500, zoom: 10, geoName: "서산시" },
    { name: "논산시", lat: 36.1868, lng: 127.0847, zoom: 10, geoName: "논산시" },
    { name: "계룡시", lat: 36.2741, lng: 127.2492, zoom: 11, geoName: "계룡시" },
    { name: "당진시", lat: 36.8933, lng: 126.6300, zoom: 10, geoName: "당진시" },

    // 전북특별자치도 (6개 시)
    { name: "전주시", lat: 35.8242, lng: 127.1480, zoom: 10, geoName: "전주시" },
    { name: "군산시", lat: 35.9700, lng: 126.7100, zoom: 10, geoName: "군산시" },
    { name: "익산시", lat: 35.9461, lng: 126.9578, zoom: 10, geoName: "익산시" },
    { name: "정읍시", lat: 35.5700, lng: 126.8500, zoom: 10, geoName: "정읍시" },
    { name: "남원시", lat: 35.4000, lng: 127.3800, zoom: 10, geoName: "남원시" },
    { name: "김제시", lat: 35.8000, lng: 126.8800, zoom: 10, geoName: "김제시" },

    // 전라남도 (5개 시)
    { name: "목포시", lat: 34.8119, lng: 126.3917, zoom: 10, geoName: "목포시" },
    { name: "여수시", lat: 34.7604, lng: 127.6622, zoom: 10, geoName: "여수시" },
    { name: "순천시", lat: 34.9500, lng: 127.4800, zoom: 10, geoName: "순천시" },
    { name: "나주시", lat: 35.0100, lng: 126.7100, zoom: 10, geoName: "나주시" },
    { name: "광양시", lat: 34.9400, lng: 127.6900, zoom: 10, geoName: "광양시" },

    // 경상북도 (10개 시)
    { name: "포항시", lat: 36.0190, lng: 129.3435, zoom: 10, geoName: "포항시" },
    { name: "구미시", lat: 36.1190, lng: 128.3445, zoom: 10, geoName: "구미시" },
    { name: "경주시", lat: 35.8562, lng: 129.2240, zoom: 10, geoName: "경주시" },
    { name: "안동시", lat: 36.5600, lng: 128.7200, zoom: 10, geoName: "안동시" },
    { name: "김천시", lat: 36.1300, lng: 128.1100, zoom: 10, geoName: "김천시" },
    { name: "영주시", lat: 36.8000, lng: 128.6300, zoom: 10, geoName: "영주시" },
    { name: "상주시", lat: 36.4100, lng: 128.1600, zoom: 10, geoName: "상주시" },
    { name: "영천시", lat: 35.9700, lng: 128.9300, zoom: 10, geoName: "영천시" },
    { name: "문경시", lat: 36.5900, lng: 128.1900, zoom: 10, geoName: "문경시" },
    { name: "경산시", lat: 35.8200, lng: 128.7300, zoom: 10, geoName: "경산시" },
    
    // 경상남도 (8개 시)
    { name: "창원시", lat: 35.2280, lng: 128.6811, zoom: 10, geoName: "창원시" },
    { name: "김해시", lat: 35.2326, lng: 128.8800, zoom: 10, geoName: "김해시" },
    { name: "진주시", lat: 35.1800, lng: 128.0800, zoom: 10, geoName: "진주시" },
    { name: "통영시", lat: 34.8400, lng: 128.4300, zoom: 10, geoName: "통영시" },
    { name: "사천시", lat: 35.0800, lng: 128.0600, zoom: 10, geoName: "사천시" },
    { name: "밀양시", lat: 35.5000, lng: 128.7400, zoom: 10, geoName: "밀양시" },
    { name: "거제시", lat: 34.8800, lng: 128.6200, zoom: 10, geoName: "거제시" },
    { name: "양산시", lat: 35.3300, lng: 129.0300, zoom: 10, geoName: "양산시" },

    // 제주특별자치도 (2개 시)
    { name: "제주시", lat: 33.4996, lng: 126.5312, zoom: 9, geoName: "제주시" },
    { name: "서귀포시", lat: 33.2543, lng: 126.5600, zoom: 9, geoName: "서귀포시" },

    // --- 신규 추가: 군(郡) 단위 (82개) ---

    // 인천광역시 (군)
    { name: "강화군", lat: 37.7479, lng: 126.4872, zoom: 10, geoName: "강화군" },
    { name: "옹진군", lat: 37.4475, lng: 126.1408, zoom: 9, geoName: "옹진군" },

    // 대구광역시 (군) - 2023년 편입
    { name: "군위군", lat: 36.2422, lng: 128.5725, zoom: 10, geoName: "군위군" },

    // 울산광역시 (군)
    { name: "울주군", lat: 35.5611, lng: 129.1411, zoom: 10, geoName: "울주군" },
    
    // 경기도 (군)
    { name: "가평군", lat: 37.8318, lng: 127.5096, zoom: 10, geoName: "가평군" },
    { name: "양평군", lat: 37.4916, lng: 127.4879, zoom: 10, geoName: "양평군" },
    { name: "연천군", lat: 38.0964, lng: 127.0744, zoom: 10, geoName: "연천군" },
    
    // 강원특별자치도 (군)
    { name: "고성군", lat: 38.3804, lng: 128.4678, zoom: 10, geoName: "고성군" },
    { name: "양구군", lat: 38.1093, lng: 127.9893, zoom: 10, geoName: "양구군" },
    { name: "양양군", lat: 38.0763, lng: 128.6219, zoom: 10, geoName: "양양군" },
    { name: "영월군", lat: 37.1866, lng: 128.4633, zoom: 10, geoName: "영월군" },
    { name: "인제군", lat: 38.0691, lng: 128.1704, zoom: 10, geoName: "인제군" },
    { name: "정선군", lat: 37.3822, lng: 128.6607, zoom: 10, geoName: "정선군" },
    { name: "철원군", lat: 38.1468, lng: 127.3134, zoom: 10, geoName: "철원군" },
    { name: "평창군", lat: 37.3705, lng: 128.3916, zoom: 10, geoName: "평창군" },
    { name: "홍천군", lat: 37.6900, lng: 127.8853, zoom: 10, geoName: "홍천군" },
    { name: "화천군", lat: 38.1065, lng: 127.7082, zoom: 10, geoName: "화천군" },
    
    // 충청북도 (군)
    { name: "괴산군", lat: 36.8152, lng: 127.7863, zoom: 10, geoName: "괴산군" },
    { name: "단양군", lat: 36.9840, lng: 128.3659, zoom: 10, geoName: "단양군" },
    { name: "보은군", lat: 36.4883, lng: 127.7294, zoom: 10, geoName: "보은군" },
    { name: "영동군", lat: 36.1746, lng: 127.7786, zoom: 10, geoName: "영동군" },
    { name: "옥천군", lat: 36.3057, lng: 127.5727, zoom: 10, geoName: "옥천군" },
    { name: "음성군", lat: 36.9383, lng: 127.6896, zoom: 10, geoName: "음성군" },
    { name: "증평군", lat: 36.7844, lng: 127.5824, zoom: 10, geoName: "증평군" },
    { name: "진천군", lat: 36.8562, lng: 127.4422, zoom: 10, geoName: "진천군" },
    
    // 충청남도 (군)
    { name: "금산군", lat: 36.1037, lng: 127.4891, zoom: 10, geoName: "금산군" },
    { name: "부여군", lat: 36.2795, lng: 126.9122, zoom: 10, geoName: "부여군" },
    { name: "서천군", lat: 36.0792, lng: 126.6908, zoom: 10, geoName: "서천군" },
    { name: "예산군", lat: 36.6801, lng: 126.8451, zoom: 10, geoName: "예산군" },
    { name: "청양군", lat: 36.4022, lng: 126.8013, zoom: 10, geoName: "청양군" },
    { name: "태안군", lat: 36.7533, lng: 126.2995, zoom: 10, geoName: "태안군" },
    { name: "홍성군", lat: 36.5984, lng: 126.6631, zoom: 10, geoName: "홍성군" },
    
    // 전북특별자치도 (군)
    { name: "고창군", lat: 35.4357, lng: 126.7027, zoom: 10, geoName: "고창군" },
    { name: "무주군", lat: 36.0076, lng: 127.6601, zoom: 10, geoName: "무주군" },
    { name: "부안군", lat: 35.7323, lng: 126.7320, zoom: 10, geoName: "부안군" },
    { name: "순창군", lat: 35.3748, lng: 127.1408, zoom: 10, geoName: "순창군" },
    { name: "완주군", lat: 35.9149, lng: 127.2456, zoom: 10, geoName: "완주군" },
    { name: "임실군", lat: 35.6190, lng: 127.2842, zoom: 10, geoName: "임실군" },
    { name: "장수군", lat: 35.6476, lng: 127.5215, zoom: 10, geoName: "장수군" },
    { name: "진안군", lat: 35.7925, lng: 127.4288, zoom: 10, geoName: "진안군" },
    
    // 전라남도 (군)
    { name: "강진군", lat: 34.6401, lng: 126.7695, zoom: 10, geoName: "강진군" },
    { name: "고흥군", lat: 34.6069, lng: 127.2757, zoom: 10, geoName: "고흥군" },
    { name: "곡성군", lat: 35.2825, lng: 127.2917, zoom: 10, geoName: "곡성군" },
    { name: "구례군", lat: 35.2057, lng: 127.4628, zoom: 10, geoName: "구례군" },
    { name: "담양군", lat: 35.3217, lng: 126.9850, zoom: 10, geoName: "담양군" },
    { name: "무안군", lat: 34.9928, lng: 126.4822, zoom: 10, geoName: "무안군" },
    { name: "보성군", lat: 34.7712, lng: 127.0811, zoom: 10, geoName: "보성군" },
    { name: "신안군", lat: 34.8322, lng: 126.1193, zoom: 9, geoName: "신안군" },
    { name: "영광군", lat: 35.2778, lng: 126.5132, zoom: 10, geoName: "영광군" },
    { name: "영암군", lat: 34.8000, lng: 126.6967, zoom: 10, geoName: "영암군" },
    { name: "완도군", lat: 34.3100, lng: 126.7578, zoom: 10, geoName: "완도군" },
    { name: "장성군", lat: 35.3022, lng: 126.7813, zoom: 10, geoName: "장성군" },
    { name: "장흥군", lat: 34.6833, lng: 126.9042, zoom: 10, geoName: "장흥군" },
    { name: "진도군", lat: 34.4869, lng: 126.2635, zoom: 10, geoName: "진도군" },
    { name: "함평군", lat: 35.0667, lng: 126.5167, zoom: 10, geoName: "함평군" },
    { name: "해남군", lat: 34.5739, lng: 126.5986, zoom: 10, geoName: "해남군" },
    { name: "화순군", lat: 35.0614, lng: 126.9858, zoom: 10, geoName: "화순군" },
    
    // 경상북도 (군)
    { name: "고령군", lat: 35.7289, lng: 128.2619, zoom: 10, geoName: "고령군" },
    { name: "봉화군", lat: 36.8929, lng: 128.7360, zoom: 10, geoName: "봉화군" },
    { name: "성주군", lat: 35.9198, lng: 128.2839, zoom: 10, geoName: "성주군" },
    { name: "영덕군", lat: 36.4136, lng: 129.3653, zoom: 10, geoName: "영덕군" },
    { name: "영양군", lat: 36.6656, lng: 129.1136, zoom: 10, geoName: "영양군" },
    { name: "예천군", lat: 36.6534, lng: 128.4523, zoom: 10, geoName: "예천군" },
    { name: "울릉군", lat: 37.4851, lng: 130.9056, zoom: 10, geoName: "울릉군" },
    { name: "울진군", lat: 36.9946, lng: 129.4022, zoom: 10, geoName: "울진군" },
    { name: "의성군", lat: 36.3533, lng: 128.6983, zoom: 10, geoName: "의성군" },
    { name: "청도군", lat: 35.6473, lng: 128.7344, zoom: 10, geoName: "청도군" },
    { name: "청송군", lat: 36.4353, lng: 129.0583, zoom: 10, geoName: "청송군" },
    { name: "칠곡군", lat: 35.9947, lng: 128.4018, zoom: 10, geoName: "칠곡군" },
    
    // 경상남도 (군)
    { name: "거창군", lat: 35.6874, lng: 127.9096, zoom: 10, geoName: "거창군" },
    { name: "고성군", lat: 34.9758, lng: 128.3241, zoom: 10, geoName: "고성군" },
    { name: "남해군", lat: 34.8361, lng: 127.8922, zoom: 10, geoName: "남해군" },
    { name: "산청군", lat: 35.4150, lng: 127.8735, zoom: 10, geoName: "산청군" },
    { name: "의령군", lat: 35.3223, lng: 128.2612, zoom: 10, geoName: "의령군" },
    { name: "창녕군", lat: 35.5458, lng: 128.4913, zoom: 10, geoName: "창녕군" },
    { name: "하동군", lat: 35.0673, lng: 127.7516, zoom: 10, geoName: "하동군" },
    { name: "함안군", lat: 35.2754, lng: 128.4059, zoom: 10, geoName: "함안군" },
    { name: "함양군", lat: 35.5201, lng: 127.7249, zoom: 10, geoName: "함양군" },
    { name: "합천군", lat: 35.5667, lng: 128.1658, zoom: 10, geoName: "합천군" }
];
// --- 데이터 끝 ---


let shuffledGameLocations = [];
let currentQuestionIndex = 0;
let score = 0;
let correctAnswerName = '';
let numOptions = 4; // 보기 개수 (기본값)
const MAX_QUESTIONS_PER_GAME = 10;
const PROVINCE_VIEW_ZOOM = 7;
const CITY_VIEW_DELAY = 1500;

const provinceHueMap = {
    '서울': 210, '부산': 10, '대구': 30, '인천': 270,
    '광주': 160, '대전': 340, '울산': 20, '세종': 200,
    '경기': 180, '강원': 120, '충북': 300, '충남': 320,
    '전북': 60, '전남': 90, '경북': 0, '경남': 50,
    '제주': 240
};

function getProvinceFromCode(code) {
    const prefix = code.substring(0, 2);
    const provinceCodeMap = {
        '11': '서울', '21': '부산', '22': '대구', '23': '인천',
        '24': '광주', '25': '대전', '26': '울산', '29': '세종',
        '31': '경기', '32': '강원', '33': '충북', '34': '충남',
        '35': '전북', '36': '전남', '37': '경북', '38': '경남',
        '39': '제주'
    };
    return provinceCodeMap[prefix] || '기타';
}

function getColorForRegion(name, code) {
    const province = getProvinceFromCode(code);
    const hue = provinceHueMap[province] || 0;
    let hash = 0;
    for (let i = 0; i < name.length; i++) {
        hash += name.charCodeAt(i);
    }
    const lightness = 40 + (hash % 30); // 40–70%
    return `hsl(${hue}, 60%, ${lightness}%)`;
}

async function initMap() {
    mapErrorInfo.textContent = '지도 및 행정구역 데이터 로딩 중...';
    if (map) {
        map.remove();
    }
    map = L.map('map').setView([36.5, 127.5], 7);

    const cartoTileUrl = 'https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png';
    const cartoAttribution = '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions" target="_blank">CARTO</a>';

    L.tileLayer(cartoTileUrl, {
        attribution: cartoAttribution,
        subdomains: 'abcd', maxZoom: 19,
        errorTileUrl: 'https://placehold.co/256x256/f0f0f0/cc0000?text=Map+Tile+Error'
    }).on('tileerror', function (event) {
        console.error('Tile loading error. Details:', {
            type: event.type, tileUrl: event.tile?.src, coords: event.coords
        });
        mapErrorInfo.textContent = '지도 타일 로딩에 실패했습니다. 인터넷 연결 또는 타일 서버 상태를 확인해주세요.';
    }).addTo(map);

    const geoJsonUrl = 'https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2018/json/skorea-municipalities-2018-geo.json';

    try {
        const response = await fetch(geoJsonUrl);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status} for GeoJSON`);
        const data = await response.json();
        if (geoJsonLayer && map.hasLayer(geoJsonLayer)) geoJsonLayer.remove();
        geoJsonLayer = L.geoJSON(data, {
            style: function (feature) {
                const name = feature.properties.name || '';
                const code = feature.properties.code || '';
                const color = getColorForRegion(name, code);
                return { color: color, weight: 1.2, opacity: 0.7, fillOpacity: 0.3, fillColor: color };
            },
            onEachFeature: function (feature, layer) {
                layer.on({
                    mouseover: function (e) {
                        const l = e.target;
                        l.setStyle({ weight: 3, fillOpacity: 0.4 });
                        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) l.bringToFront();
                    },
                    mouseout: function (e) {
                        if (geoJsonLayer) geoJsonLayer.resetStyle(e.target);
                    }
                });
            }
        }).addTo(map);
        mapErrorInfo.textContent = '';
    } catch (error) {
        console.error('Error loading or parsing GeoJSON data:', error);
        mapErrorInfo.textContent = '행정구역 외곽선 데이터 로딩에 실패했습니다.';
    }

    marker = L.marker([0, 0], {
        icon: L.icon({
            iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
            iconSize: [25, 41], iconAnchor: [12, 41], popupAnchor: [1, -34],
            shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png', shadowSize: [41, 41]
        })
    });
}


function highlightCurrentQuestionRegion(questionGeoName) {
    if (geoJsonLayer) {
        geoJsonLayer.eachLayer(function (layer) {
            const featureName = layer.feature.properties.name || '';
            if (featureName.startsWith(questionGeoName)) {
                layer.setStyle({
                    weight: 4,          
                    color: '#c00',        
                    fillOpacity: 0.6,   
                    fillColor: '#ffeb3b' 
                });
                if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
                    layer.bringToFront();
                }
            } else {
                geoJsonLayer.resetStyle(layer);
            }
        });
    }
}




function selectDifficulty(level) {
    numOptions = (level === 2) ? 8 : 4;
    difficultySelector.style.display = 'none';
    quizContainer.style.display = 'block';
    startGame();
}

function showDifficultyScreen() {
    quizContainer.style.display = 'none';
    difficultySelector.style.display = 'block';
    
    questionTextElement.textContent = '게임 시작 버튼을 눌러주세요!';
    progressArea.style.display = 'none';
    feedbackTextElement.textContent = '';
    optionsArea.innerHTML = '';
    nextQuestionBtn.style.display = 'none';
}

async function startGame() { 
    score = 0;
    currentQuestionIndex = 0;
    
    const allShuffledLocations = shuffleArray([...locations]);
    shuffledGameLocations = allShuffledLocations.slice(0, MAX_QUESTIONS_PER_GAME);
    
    totalQuestionsElement.textContent = shuffledGameLocations.length; 
    progressArea.style.display = 'block';
    
    questionTextElement.textContent = "지도 로딩 중... 잠시만 기다려주세요.";
    restartBtn.disabled = true; 
    
    if (!map) {
        try {
            await initMap(); 
        } catch (e) {
            console.error("Map initialization failed:", e);
            mapErrorInfo.textContent = "지도 초기화에 실패했습니다. 브라우저 콘솔을 확인해주세요.";
            questionTextElement.textContent = "지도 로딩 실패! 새로고침하거나 나중에 다시 시도해주세요.";
            restartBtn.disabled = false;
            return; 
        }
    } else {
         if (marker && map.hasLayer(marker)) marker.remove();
         if (geoJsonLayer) {
               geoJsonLayer.eachLayer(function(layer) { geoJsonLayer.resetStyle(layer); });
         }
    }
    
    restartBtn.disabled = false;
    restartBtn.textContent = '처음으로';
    nextQuestionBtn.style.display = 'none'; 
    
    if (map) {
        loadQuestion();
    } else {
        questionTextElement.textContent = "지도 로딩 실패! 게임을 진행할 수 없습니다.";
    }
}

function loadQuestion() {
    if (currentQuestionIndex >= shuffledGameLocations.length) {
        endGame();
        return;
    }

    const currentLocation = shuffledGameLocations[currentQuestionIndex];
    correctAnswerName = currentLocation.name;
    
    questionTextElement.textContent = "이 표시는 어느 지역을 나타낼까요?";
    currentQuestionElement.textContent = currentQuestionIndex + 1;

    if (geoJsonLayer) { 
        geoJsonLayer.eachLayer(function(layer) { geoJsonLayer.resetStyle(layer); });
    }
    if (currentLocation.geoName) { 
         highlightCurrentQuestionRegion(currentLocation.geoName);
    }

    const latLng = [currentLocation.lat, currentLocation.lng];
    if (marker) marker.setLatLng(latLng).addTo(map);
    else marker = L.marker(latLng).addTo(map);
    
    map.setView(latLng, PROVINCE_VIEW_ZOOM);
    
    setTimeout(() => {
        if (map) { 
            const adjustedZoom = (currentLocation.zoom || 10) - 2;
            const finalZoom = Math.max(adjustedZoom, PROVINCE_VIEW_ZOOM -1);
            map.flyTo(latLng, finalZoom , {duration: 1}); 
        }
    }, CITY_VIEW_DELAY);
    
    optionsArea.innerHTML = ''; 
    const options = generateOptions(correctAnswerName);
    
    options.forEach(optionName => {
        const button = document.createElement('button');
        button.textContent = optionName;
        button.className = "option-button w-full bg-white hover:bg-indigo-100 text-indigo-700 font-semibold py-2 px-3 border border-indigo-300 rounded-lg shadow-sm hover:shadow-md transition-all duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-400";
        button.onclick = () => handleAnswer(optionName, button); 
        optionsArea.appendChild(button);
    });

    feedbackTextElement.textContent = ''; 
    feedbackTextElement.className = 'text-md sm:text-lg font-medium';
    nextQuestionBtn.style.display = 'none';
}

function handleAnswer(selectedName, buttonElement) {
    Array.from(optionsArea.children).forEach(btn => {
        btn.disabled = true;
        btn.classList.remove('hover:bg-indigo-100');
        btn.classList.add('opacity-70', 'cursor-not-allowed');
    });

    if (selectedName === correctAnswerName) {
        score++;
        feedbackTextElement.textContent = '정답입니다! 🎉';
        feedbackTextElement.className = 'text-md sm:text-lg font-medium text-green-600';
        buttonElement.classList.remove('bg-white', 'text-indigo-700', 'border-indigo-300');
        buttonElement.classList.add('bg-green-500', 'text-white', 'border-green-700');
    } else {
        feedbackTextElement.textContent = `오답입니다. 정답은 ${correctAnswerName} 입니다. 😥`;
        feedbackTextElement.className = 'text-md sm:text-lg font-medium text-red-600';
        buttonElement.classList.remove('bg-white', 'text-indigo-700', 'border-indigo-300');
        buttonElement.classList.add('bg-red-500', 'text-white', 'border-red-700');

        Array.from(optionsArea.children).forEach(btn => {
            if (btn.textContent === correctAnswerName) {
                btn.classList.remove('bg-white', 'text-indigo-700', 'border-indigo-300', 'opacity-70');
                btn.classList.add('bg-green-500', 'text-white', 'border-green-700');
            }
        });
    }
    
    if (currentQuestionIndex < shuffledGameLocations.length - 1) {
        nextQuestionBtn.textContent = '다음 문제';
    } else {
        nextQuestionBtn.textContent = '결과 보기';
    }
    nextQuestionBtn.style.display = 'inline-block';
}

function moveToNextQuestion() {
    currentQuestionIndex++;
    loadQuestion();
}

function endGame() {
    questionTextElement.textContent = `게임 종료! 최종 점수: ${score} / ${shuffledGameLocations.length}`;
    optionsArea.innerHTML = '';
    feedbackTextElement.textContent = '수고하셨습니다! 다시 시작하려면 아래 버튼을 누르세요.';
    feedbackTextElement.className = 'text-md sm:text-lg font-medium text-purple-700';
    progressArea.style.display = 'none'; 
    
    if (marker && map && map.hasLayer(marker)) marker.remove();
    if (geoJsonLayer) { 
        geoJsonLayer.eachLayer(function(layer) { geoJsonLayer.resetStyle(layer); });
    }
    nextQuestionBtn.style.display = 'none';
    restartBtn.textContent = '처음으로';
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function generateOptions(correctAnswer) {
    const options = [correctAnswer];
    const distractors = locations
        .map(loc => loc.name)
        .filter(name => name !== correctAnswer); 
    
    shuffleArray(distractors); 

    for (let i = 0; i < numOptions - 1 && i < distractors.length; i++) {
        options.push(distractors[i]);
    }
    
    return shuffleArray(options); 
}

// --- Event Listeners ---
level1Btn.addEventListener('click', () => selectDifficulty(1));
level2Btn.addEventListener('click', () => selectDifficulty(2));
restartBtn.addEventListener('click', showDifficultyScreen);

nextQuestionBtn.addEventListener('click', () => {
    if (currentQuestionIndex < shuffledGameLocations.length - 1) {
         moveToNextQuestion();
    } else {
         endGame();
    }
});
