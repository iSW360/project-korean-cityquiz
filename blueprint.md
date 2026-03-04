# 대한민국 도시 퀴즈 (Korean City Quiz) Blueprint

## 1. Project Overview
대한민국 도시 퀴즈는 사용자가 지도를 보며 대한민국의 도시 이름을 맞히는 웹 기반 인터랙티브 퀴즈 애플리케이션입니다. Leaflet.js 라이브러리를 사용하여 인터랙티브 지도를 제공하고, Tailwind CSS를 사용하여 현대적이고 반응형인 UI를 구현합니다.

## 2. Project Outline (Current Version)

### 2.1 Features
- **난이도 선택:** 난이도 1(보기 4개)과 난이도 2(보기 8개)를 제공합니다.
- **인터랙티브 지도:** Leaflet.js를 기반으로 지도를 표시하고, 특정 지역을 하이라이트합니다.
- **퀴즈 시스템:** 무작위로 10개의 도시가 선택되며, 보기를 통해 정답을 선택합니다.
- **피드백 및 결과:** 각 문제마다 정답 여부를 즉시 피드백하며, 최종 점수를 보여줍니다.
- **반응형 디자인:** 모바일과 웹 모두에서 잘 작동하도록 Tailwind CSS를 활용한 반응형 레이아웃을 제공합니다.
- **분석 도구:** Google Analytics (gtag.js) 및 Microsoft Clarity를 통합하여 사용자 활동 및 행동을 분석합니다.

### 2.2 Style & Design
- **색상 팔레트:** 파란색, 보라색, 인디고색을 기반으로 한 그라데이션 배경을 사용합니다.
- **타이포그래피:** Inter 폰트를 기본으로 사용하며, 주요 텍스트에 강조를 줍니다.
- **컴포넌트:** 그림자와 둥근 모서리를 사용하여 현대적인 "Card" 스타일 UI를 구현합니다.

### 2.3 Technical Details
- **Framework:** Framework-less (Pure HTML, CSS, JS)
- **Libraries:** Tailwind CSS (via CDN), Leaflet.js (Map library)
- **Analytics:** Google Analytics (gtag.js), Microsoft Clarity
- **Modularization:** HTML, CSS, JS 파일을 분리하여 코드의 가독성과 유지보수성을 높였습니다.

## 3. Current Task: Analytics Integration (Google Analytics & MS Clarity)

### 3.1 Plan
- Google Analytics (gtag.js) 및 Microsoft Clarity 추적 코드를 `index.html`의 `<head>` 섹션에 추가합니다.
- 변경 사항을 `blueprint.md`에 기록합니다.
- Git을 통해 변경 사항을 커밋하고 푸시합니다.

### 3.2 Steps
1. `index.html`에 Google Analytics 및 MS Clarity 스크립트 추가.
2. `blueprint.md` 업데이트.
3. Git 작업:
    - `git add index.html blueprint.md`
    - `git commit -m "Add Google Analytics and MS Clarity tags"`
    - `git push origin main`
