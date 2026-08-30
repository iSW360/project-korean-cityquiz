/* quiz-engine.js — GeoQ 통합 엔진 */
const QE = (() => {
  const QUIZ_N = 10;   // 한 세션당 문제 수
  const CACHE_VER = 6; // 올리면 SVG·JSON 캐시 전체 무효화

  /* ── 지도별 sub-region 그룹 (색상 배분용) ── */
  const _GRP_MAP = {
    'us-states': {
      'US-NE':['CT','ME','MA','NH','RI','VT','NJ','NY','PA'],
      'US-MW':['IL','IN','MI','OH','WI','IA','KS','MN','MO','NE','ND','SD'],
      'US-SO':['DE','FL','GA','MD','NC','SC','VA','WV','AL','KY','MS','TN','AR','LA','OK','TX'],
      'US-WE':['AZ','CO','ID','MT','NV','NM','UT','WY','AK','CA','HI','OR','WA'],
    },
    'europe': {
      'EU-N':['ISL','NOR','SWE','FIN','DNK','EST','LVA','LTU'],
      'EU-W':['GBR','IRL','FRA','BEL','NLD','LUX','CHE','AUT','DEU','LIE','MCO','AND'],
      'EU-S':['PRT','ESP','ITA','GRC','MLT','CYP','SMR','VAT','MKD','ALB','MNE','BIH','HRV','SVN'],
      'EU-E':['RUS','BLR','UKR','MDA','ROU','BGR','SRB','SVK','HUN','POL','CZE','XKX','TUR'],
    },
    'africa': {
      'AF-N':['MAR','DZA','TUN','LBY','EGY','SDN','MRT'],
      'AF-W':['SEN','GMB','GNB','GIN','SLE','LBR','CIV','GHA','TGO','BEN','NGA','NER','BFA','MLI','CPV','STP'],
      'AF-C':['CMR','CAF','COG','COD','GAB','GNQ','TCD','RWA','BDI','AGO'],
      'AF-E':['ETH','ERI','DJI','SOM','KEN','UGA','TZA','MOZ','MWI','ZMB','MDG','COM','SYC','MUS','SSD'],
      'AF-S':['ZAF','LSO','SWZ','BWA','NAM','ZWE'],
    },
  };
  // 일본 도도부현은 SVG에 data-grp(8개 지방)가 이미 baked-in 되어 있어 _GRP_MAP 불필요

  function _trimTinySubpaths(){
    const svg=qs('#map-container svg');
    if(!svg) return;
    const ns='http://www.w3.org/2000/svg';
    svg.querySelectorAll('path[data-id]').forEach(path=>{
      const d=path.getAttribute('d');
      if(!d) return;
      // M 명령어 기준으로 sub-path 분리
      const subs=d.trim().split(/(?=M[\s\d\-\.])/).filter(s=>s.trim().length>2);
      if(subs.length<=1) return;
      // 각 sub-path의 면적 측정
      const measured=subs.map(sub=>{
        const tmp=document.createElementNS(ns,'path');
        tmp.setAttribute('d',sub);
        svg.appendChild(tmp);
        const bb=tmp.getBBox();
        svg.removeChild(tmp);
        return {sub, area:bb.width*bb.height};
      });
      const maxArea=Math.max(...measured.map(m=>m.area));
      // 최대 sub-path의 2% 미만이면 제거 (군소 섬 제거, 독립국 소국은 유지)
      const kept=measured.filter(m=>m.area>=maxArea*0.02).map(m=>m.sub);
      if(kept.length<measured.length) path.setAttribute('d',kept.join(' '));
    });
  }
  function _applyRegionColors(){
    const groups=_GRP_MAP[S.mapId];
    if(!groups) return;
    Object.entries(groups).forEach(([grp,ids])=>{
      ids.forEach(id=>{
        const el=document.getElementById('r'+id);
        if(el) el.setAttribute('data-grp',grp);
      });
    });
  }
  let S = {
    mapId:'korea-sigungoo', lang:'ko', level:1,
    regions:[], queue:[], idx:0, meta:null,
    score:0, correct:0, wrong:0, hintUsed:0,
    hintThis:false, answered:false,
    timer:null, timeLeft:15,
    autoNext:null, countInterval:null,
    initViewBox:'0 0 680 800',
  };
  const $=id=>document.getElementById(id);
  const qs=sel=>document.querySelector(sel);

  /* ── init ── */
  async function init(){
    const p=new URLSearchParams(location.search);
    S.mapId=p.get('map')||'korea-sigungoo';
    S.lang=p.get('lang')||I18n.getLang();
    S.level=parseInt(p.get('level')||'1');

    if(S.level===3) document.body.classList.add('lv3');

    // 헤더
    const mapEl=$('hd-map'); if(mapEl) mapEl.textContent=I18n.get(`maps.${S.mapId}`);
    const lvEl=$('hd-lv'); if(lvEl){
      const lnames={1:'Level 1 · 보기 4개',2:'Level 2 · 보기 8개 · 15초',3:'Level 3 · 지도 클릭'};
      const lnames_en={1:'Level 1 · 4 choices',2:'Level 2 · 8 choices · 15s',3:'Level 3 · Click map'};
      lvEl.textContent=S.lang==='ko'?lnames[S.level]:lnames_en[S.level];
    }

    // 언어 버튼
    $('btn-ko')?.classList.toggle('active',S.lang==='ko');
    $('btn-en')?.classList.toggle('active',S.lang==='en');

    _setupUI();
    await _loadData();
    await _loadMap();
    _buildQueue();
    _showQ();
  }

  function _setupUI(){
    // 타이머
    const tw=$('timer-wrap');
    if(tw) tw.classList.toggle('show',S.level===2);
    // 힌트 영역
    const ha=$('hint-area');
    if(ha) ha.style.display=S.level===3?'none':'block';
    // 선택지
    const ch=$('choices');
    if(ch) ch.style.display=S.level===3?'none':'grid';
    // lv3 안내
    const g=$('lv3-guide');
    if(g) g.classList.toggle('show',S.level===3);
    // 힌트 비용 레이블
    const hc=$('hint-cost');
    if(hc) hc.textContent=S.level===1?(S.lang==='ko'?'(선택)':'(opt)'):(S.lang==='ko'?'−0.5점':'−0.5pts');
  }

  async function _loadData(){
    const key=`qd_${S.mapId}_v${CACHE_VER}`;
    try{const c=sessionStorage.getItem(key);if(c){const p=JSON.parse(c);S.regions=p.regions;S.meta=p.meta||null;return;}}catch{}
    const d=await fetch(`/data/quiz-${S.mapId}.json`).then(r=>r.json());
    S.regions=d.regions; S.meta=d.meta||null;
    try{sessionStorage.setItem(key,JSON.stringify(d));}catch{}
  }

  async function _loadMap(){
    const cont=$('map-container'), sk=$('map-skeleton');
    if(sk) sk.style.display='block';
    const key=`sv_${S.mapId}_v${CACHE_VER}`;
    let svg=sessionStorage.getItem(key);
    if(!svg){
      const meta=await fetch(`/data/quiz-${S.mapId}.json`).then(r=>r.json()).catch(()=>null);
      svg=await fetch(meta?.meta?.mapSvg||'/maps/korea/sigungoo.svg').then(r=>r.text());
      try{sessionStorage.setItem(key,svg);}catch{}
    }
    cont.innerHTML=svg;
    _applyRegionColors();
    _trimTinySubpaths();
    const el=cont.querySelector('svg');
    if(el){el.setAttribute('width','100%');el.setAttribute('height','100%');S.initViewBox=el.getAttribute('viewBox')||'0 0 680 800';requestAnimationFrame(()=>el.classList.add('loaded'));}
    if(sk) sk.style.display='none';
    if(S.level===3) _bindMapClicks();
  }

  function _bindMapClicks(){
    $('map-container').querySelectorAll('path[data-id]').forEach(p=>{
      p.addEventListener('click',()=>{if(!S.answered)_onMapClick(p.getAttribute('data-id'));});
      // Level 3: 툴팁 비활성화 (지명 노출 방지)
      if(S.level!==3){
        p.addEventListener('mouseenter',()=>_showTip(p));
        p.addEventListener('mouseleave',()=>_hideTip());
      }
    });
  }

  function _onMapClick(cid){
    S.answered=true; _stopTimer();
    const correct=S.queue[S.idx];
    const ok=cid===correct.id;
    document.getElementById(correct.svgPathId)?.classList.add('correct');
    if(!ok) document.getElementById(`r${cid}`)?.classList.add('wrong');
    if(ok){S.score+=S.hintThis?.5:1;S.correct++;}else S.wrong++;
    _feedback(ok,correct);
    _showInfoHint(correct);
    _showNext();
    _updateScore();
  }

  function _buildQueue(){
    const a=[...S.regions];
    for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}
    S.queue=a.slice(0, Math.min(QUIZ_N, a.length));
    S.idx=0;S.score=0;S.correct=0;S.wrong=0;S.hintUsed=0;
    _updateScore();_updateProg();
  }


  function _showQ(){
    if(S.idx>=S.queue.length){_goResult();return;}
    S.answered=false;S.hintThis=false;
    const r=S.queue[S.idx];

    _clearMap();
    _zoomMap(r.svgPathId);
    // 레벨 1·2: 지역 강조 표시 (레벨 3은 직접 찾아야 하므로 강조 없음)
    if(S.level!==3) document.getElementById(r.svgPathId)?.classList.add('active');

    // 문제 텍스트
    const qt=$('question-text');
    if(qt){
      if(S.level===3){
        const n=_name(r);
        qt.innerHTML=S.lang==='ko'
          ?`<strong>${n}</strong>을(를) 지도에서 찾아 클릭하세요`
          :`Find <strong>${n}</strong> on the map`;
      } else {
        // meta.questionText가 있으면 커스텀 질문 사용
        const customQ=S.meta?.questionText?.[S.lang];
        qt.innerHTML=customQ||(S.lang==='ko'
          ?`<strong style="color:var(--gold)">강조된 지역</strong>의 이름은?`
          :`What is the name of the <strong style="color:var(--gold)">highlighted region</strong>?`);
      }
    }

    // 힌트 초기화
    const hb=$('hint-btn'),htxt=$('hint-box');
    if(hb) hb.disabled=false;
    if(htxt){htxt.classList.remove('show');htxt.textContent='';}

    if(S.level!==3) _buildChoices(r);

    const fb=$('feedback');
    if(fb){fb.className='feedback';fb.textContent='';}

    const nb=$('btn-next');
    if(nb) nb.style.display='none';

    if(S.level===2) _startTimer();

    _updateProg();

    const panel=$('quiz-panel');
    if(panel){panel.classList.remove('fade-up');void panel.offsetWidth;panel.classList.add('fade-up');}
  }

  function _buildChoices(correct){
    const n=S.level===1?4:8;
    const pool=S.regions.filter(r=>r.id!==correct.id).sort(()=>Math.random()-.5).slice(0,n-1);
    const list=[...pool,correct].sort(()=>Math.random()-.5);
    const cont=$('choices');
    if(!cont) return;
    cont.innerHTML='';
    cont.style.gridTemplateColumns=n>4?'repeat(4,1fr)':'1fr 1fr';
    cont.dataset.count=String(n);
    list.forEach(r=>{
      const b=document.createElement('button');
      b.className='choice';b.textContent=_name(r);b.dataset.id=r.id;
      b.addEventListener('click',()=>_onChoice(b,correct));
      cont.appendChild(b);
    });
  }

  function _onChoice(btn,correct){
    if(S.answered) return;
    S.answered=true; _stopTimer();
    const ok=btn.dataset.id===correct.id;
    document.querySelectorAll('.choice').forEach(b=>{
      b.disabled=true;
      if(b.dataset.id===correct.id) b.classList.add('correct');
    });
    if(!ok) btn.classList.add('wrong');
    _markMap(correct.svgPathId,ok);
    if(ok){S.score+=S.hintThis?.5:1;S.correct++;}else S.wrong++;
    _feedback(ok,correct);
    _showInfoHint(correct);
    _showNext();
    _updateScore();
  }

  function _startTimer(){
    S.timeLeft=15;_updateTimer(15);_stopTimer();
    S.timer=setInterval(()=>{
      S.timeLeft--;_updateTimer(S.timeLeft);
      if(S.timeLeft<=0){_stopTimer();if(!S.answered)_timeout();}
    },1000);
  }
  function _stopTimer(){if(S.timer){clearInterval(S.timer);S.timer=null;}}

  function _timeout(){
    S.answered=true;S.wrong++;
    const c=S.queue[S.idx];
    document.querySelectorAll('.choice').forEach(b=>{b.disabled=true;if(b.dataset.id===c.id)b.classList.add('correct');});
    _markMap(c.svgPathId,false);
    _feedback(false,c,true);
    _showInfoHint(c);
    _showNext();_updateScore();
  }

  function _updateTimer(t){
    const n=$('timer-num'),w=$('timer-wrap'),a=$('timer-arc');
    if(n) n.textContent=t;
    if(w) w.className='timer-wrap show'+(t<=5?' urgent':'');
    if(a){const c=2*Math.PI*20;a.style.strokeDashoffset=c*(1-t/15);}
  }

  function showHint(){
    if(S.hintThis) return;
    S.hintThis=true;S.hintUsed++;
    const r=S.queue[S.idx];
    const box=$('hint-box'),btn=$('hint-btn'),cnt=$('hint-count');
    if(box){box.textContent=_hint(r)||(S.lang==='ko'?'힌트 없음':'No hint');box.classList.add('show');}
    if(btn) btn.disabled=true;
    if(cnt) cnt.textContent=`(${S.hintUsed}회)`;
    if(S.level===2) showToast(S.lang==='ko'?'💡 정답 시 0.5점':'💡 +0.5 pts if correct');
  }

  /* 답 공개 후 지역 정보 힌트 표시 (점수에 무관) */
  function _showInfoHint(r){
    const h=_hint(r);if(!h) return;
    const box=$('hint-box'),btn=$('hint-btn');
    if(!box) return;
    if(!S.hintThis){              // 아직 힌트를 쓰지 않은 경우
      box.textContent=h;box.classList.add('show');
      if(btn) btn.disabled=true; // 점수 차감 없이 표시
    }
    // 힌트 영역 표시 (Level3 포함)
    const ha=$('hint-area');
    if(ha) ha.style.display='block';
  }

  function _feedback(ok,correct,timeout=false){
    const fb=$('feedback');
    if(!fb) return;
    fb.classList.add('show');
    if(timeout){
      fb.className='feedback show wrong';
      fb.textContent=`⏰ ${S.lang==='ko'?'시간 초과':'Time out'} — ${_name(correct)}`;
    } else if(ok){
      fb.className='feedback show correct';
      fb.textContent=S.lang==='ko'?`✓ 정답! ${S.hintThis?'(+0.5점)':'(+1점)'}`:`✓ Correct! ${S.hintThis?'(+0.5)':'(+1)'}`;
    } else {
      fb.className='feedback show wrong';
      fb.textContent=`✗ ${S.lang==='ko'?'오답':'Wrong'} — ${_name(correct)}`;
    }
  }

  function _showNext(){
    const nb=$('btn-next');
    if(!nb) return;
    nb.style.display='flex';
    const last=S.idx>=S.queue.length-1;
    const base=last?(S.lang==='ko'?'결과 보기':'See Result'):(S.lang==='ko'?'다음':'Next');
    // 카운트다운 초기화
    if(S.autoNext){clearTimeout(S.autoNext);S.autoNext=null;}
    if(S.countInterval){clearInterval(S.countInterval);S.countInterval=null;}
    let cd=3;
    nb.textContent=`${base} (${cd}) →`;
    S.countInterval=setInterval(()=>{
      cd--;
      if(cd>0){nb.textContent=`${base} (${cd}) →`;}
      else{clearInterval(S.countInterval);S.countInterval=null;}
    },1000);
    S.autoNext=setTimeout(()=>{
      if(S.countInterval){clearInterval(S.countInterval);S.countInterval=null;}
      nextQ();
    },3000);
  }

  function nextQ(){
    if(S.autoNext){clearTimeout(S.autoNext);S.autoNext=null;}
    if(S.countInterval){clearInterval(S.countInterval);S.countInterval=null;}
    _stopTimer();S.idx++;_showQ();
  }

  /* ── 지도 줌 ── */
  let _vbRaf=null;
  function _animateViewBox(svg,target,dur=320){
    if(_vbRaf){cancelAnimationFrame(_vbRaf);_vbRaf=null;}
    const vb=svg.viewBox.baseVal;
    const s={x:vb.x,y:vb.y,w:vb.width,h:vb.height};
    const [tx,ty,tw,th]=target.split(' ').map(Number);
    const d={x:tx-s.x,y:ty-s.y,w:tw-s.w,h:th-s.h};
    const t0=performance.now();
    function step(t){
      const p=Math.min((t-t0)/dur,1);
      const e=p<.5?2*p*p:-1+(4-2*p)*p;
      svg.setAttribute('viewBox',[s.x+d.x*e,s.y+d.y*e,s.w+d.w*e,s.h+d.h*e].map(v=>v.toFixed(1)).join(' '));
      if(p<1)_vbRaf=requestAnimationFrame(step);
    }
    _vbRaf=requestAnimationFrame(step);
  }
  function _resetMapZoom(){
    const svg=qs('#map-container svg');
    if(svg) _animateViewBox(svg,S.initViewBox,280);
  }
  function _zoomMap(pathId){
    if(S.meta&&S.meta.noZoom) return;
    const svg=qs('#map-container svg');
    if(!svg)return;
    requestAnimationFrame(()=>{
      const path=document.getElementById(pathId);
      if(!path)return;
      const bb=path.getBBox();
      if(!bb.width&&!bb.height){_resetMapZoom();return;}
      // 지도별 실제 viewBox 크기로 클램핑 (하드코딩 680×800 대신)
      const [,, IVW, IVH]=S.initViewBox.split(' ').map(Number);
      const aspect=IVH/IVW;
      const maxDim=Math.max(bb.width,bb.height);
      if(S.level===3){
        // 레벨3: 아주 작은 지역만 약하게 줌 (클릭할 수 있도록 넓은 시야 유지)
        if(maxDim>=70){_resetMapZoom();return;}
        const VW=Math.min(maxDim/0.12,IVW), VH=Math.min(VW*aspect,IVH);
        const cx=bb.x+bb.width/2, cy=bb.y+bb.height/2;
        const vx=Math.max(0,Math.min(cx-VW/2,IVW-VW));
        const vy=Math.max(0,Math.min(cy-VH/2,IVH-VH));
        _animateViewBox(svg,`${vx.toFixed(0)} ${vy.toFixed(0)} ${VW.toFixed(0)} ${VH.toFixed(0)}`);
        return;
      }
      // 레벨1·2: 지역 크기에 맞게 줌
      if(maxDim>=Math.min(IVW,IVH)*0.27){_resetMapZoom();return;}
      // 최소 viewBox = 지도 너비의 50% (작은 나라 주변 맥락 확보)
      const target=Math.max(maxDim/0.20, IVW*0.50);
      const VW=Math.min(target,IVW*0.85), VH=Math.min(target*aspect,IVH*0.85);
      const cx=bb.x+bb.width/2, cy=bb.y+bb.height/2;
      const vx=Math.max(0,Math.min(cx-VW/2,IVW-VW));
      const vy=Math.max(0,Math.min(cy-VH/2,IVH-VH));
      _animateViewBox(svg,`${vx.toFixed(0)} ${vy.toFixed(0)} ${VW.toFixed(0)} ${VH.toFixed(0)}`);
    });
  }

  let _markMapTimer=null;
  function _clearMap(){
    if(_markMapTimer){clearTimeout(_markMapTimer);_markMapTimer=null;}
    document.querySelectorAll('#map-container [data-id]').forEach(e=>e.classList.remove('active','correct','wrong','solved'));
  }

  function _markMap(id,ok){
    if(_markMapTimer){clearTimeout(_markMapTimer);_markMapTimer=null;}
    const el=document.getElementById(id);
    el?.classList.remove('active');
    el?.classList.add(ok?'correct':'wrong');
    _markMapTimer=setTimeout(()=>{el?.classList.remove('correct','wrong');el?.classList.add('solved');_markMapTimer=null;},2200);
  }

  function _showTip(path){
    const tip=$('map-tip');if(!tip) return;
    const n=S.lang==='ko'?path.getAttribute('data-ko'):path.getAttribute('data-en');
    if(!n) return;
    const cr=$('map-container').getBoundingClientRect();
    const pr=path.getBoundingClientRect();
    tip.textContent=n;
    tip.style.left=(pr.left-cr.left+pr.width/2)+'px';
    tip.style.top=(pr.top-cr.top)+'px';
    tip.classList.add('show');
  }
  function _hideTip(){$('map-tip')?.classList.remove('show');}

  function _name(r){return r.names?.[S.lang]||r.names?.ko||'';}
  function _hint(r){return r.hints?.[S.lang]||r.hints?.ko||'';}

  function _updateProg(){
    const t=S.queue.length,c=S.idx+1,pct=S.idx/t*100;
    const f=$('prog-fill'),l=$('prog-label');
    if(f) f.style.width=`${pct}%`;
    if(l) l.textContent=`${c} / ${t}`;
  }

  function _updateScore(){
    const el=$('score-display');
    if(el) el.textContent=`${S.score%1===0?S.score:S.score.toFixed(1)}${S.lang==='ko'?'점':' pts'}`;
  }

  function switchLevel(lv){_stopTimer();const p=new URLSearchParams(location.search);p.set('level',lv);location.search=p.toString();}
  function switchLang(lang){_stopTimer();localStorage.setItem('qlang',lang);const p=new URLSearchParams(location.search);p.set('lang',lang);location.search=p.toString();}
  function restart(){_stopTimer();_clearMap();_buildQueue();_showQ();}

  function _goResult(){
    _stopTimer();
    const p=new URLSearchParams({map:S.mapId,lang:S.lang,level:S.level,score:S.score,total:S.queue.length,correct:S.correct,wrong:S.wrong,hints:S.hintUsed});
    location.href=`/result?${p}`;
  }

  return{init,nextQ,showHint,switchLevel,switchLang,restart};
})();

window.QE=QE;

function showToast(msg,ms=2200){
  const el=document.getElementById('toast');
  if(!el) return;
  el.textContent=msg;el.classList.add('show');
  setTimeout(()=>el.classList.remove('show'),ms);
}
window.showToast=showToast;
