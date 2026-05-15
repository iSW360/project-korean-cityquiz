/* i18n.js */
const I18n=((()=>{
  let _lang='ko',_d={};
  async function init(lang){
    _lang=lang||_detect();
    try{_d=await fetch(`/locales/${_lang}.json`).then(r=>r.json());}catch{if(_lang!=='ko')_d=await fetch('/locales/ko.json').then(r=>r.json());}
    document.documentElement.lang=_lang;
    document.body.setAttribute('lang',_lang);
    _apply();return _lang;
  }
  function _detect(){return localStorage.getItem('qlang')||(navigator.language?.startsWith('ko')?'ko':'en');}
  function get(key,vars={}){
    const keys=key.split('.');let v=_d;
    for(const k of keys){v=v?.[k];if(v===undefined)return key;}
    return String(v).replace(/\{\{(\w+)\}\}/g,(_,k)=>vars[k]??'');
  }
  function _apply(){document.querySelectorAll('[data-t]').forEach(el=>el.textContent=get(el.dataset.t));}
  function getLang(){return _lang;}
  function setLang(lang){localStorage.setItem('qlang',lang);location.reload();}
  return{init,get,getLang,setLang};
}))();
window.I18n=I18n;
