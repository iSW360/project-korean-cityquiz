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

### 2.2 Style & Design
- **색상 팔레트:** 파란색, 보라색, 인디고색을 기반으로 한 그라데이션 배경을 사용합니다.
- **타이포그래피:** Inter 폰트를 기본으로 사용하며, 주요 텍스트에 강조를 줍니다.
- **컴포넌트:** 그림자와 둥근 모서리를 사용하여 현대적인 "Card" 스타일 UI를 구현합니다.

### 2.3 Technical Details
- **Framework:** Framework-less (Pure HTML, CSS, JS)
- **Libraries:** Tailwind CSS (via CDN), Leaflet.js (Map library)
- **Modularization:** HTML, CSS, JS 파일을 분리하여 코드의 가독성과 유지보수성을 높였습니다.

## 3. Current Task: HTML, JS, CSS Separation and Git Deployment

### 3.1 Plan
- `index.html`에 포함된 인라인 CSS와 JavaScript를 각각 `style.css`와 `main.js`로 분리합니다.
- `index.html`에서 외부 리소스 및 분리된 파일들을 올바르게 링크합니다.
- 변경 사항을 Git 저장소에 커밋하고 원격 저장소(`origin main`)로 푸시합니다.

### 3.2 Steps
1. `index.html`의 `<script>` 내용을 `main.js`로 이동.
2. `index.html`의 `<style>` 내용을 `style.css`로 이동 (기존 내용 유지/보완).
3. `index.html` 수정:
    - `<link rel="stylesheet" href="style.css">` 추가.
    - `<script src="main.js"></script>` 추가.
    - 인라인 `<style>` 및 `<script>` 블록 제거.
4. Git 작업:
    - `git add index.html main.js style.css`
    - `git commit -m "Separate HTML into HTML, JS, and CSS files"`
    - `git push origin main`
