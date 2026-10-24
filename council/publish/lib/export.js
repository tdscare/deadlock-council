// record -> game export (same exportBuild shape as the site) and code, using the STAGED enc.js (site_patch/enc.js).
const C=require('./common');const {fs,path,SP,PUB}=C;const G=require('./gamefmt');
const SUFFIX=' (Fully Annotated)';
const BR=JSON.parse(fs.readFileSync(path.join(PUB,'branding.json'),'utf8'));
// per-hero legacy tag defaults (from mkimport.js T): used ONLY when a record has no build-specific `tg` (flagged by the lint as hero-default)
const T=require(SP+'/mkimport.js');
let META={};try{META=new Function(C.rd('meta.js')+';return META')()}catch(e){}
function tagsOf(content){if(content.tg)return {tg:content.tg,source:'record'};const t=T[content.id]||T[content.id.split('_')[0]];return t?{tg:t,source:'hero-default'}:{tg:null,source:'none'}}
function tagIds(tg,hero,ITEMS){return tg.map((t,i)=>{if(G.TAG_ID[t])return G.TAG_ID[t];if(ITEMS[t])return ITEMS[t].id;const a=hero.ab.find(x=>x.n===t);if(a)return a.id;throw new Error('unsupported tag: '+t)})}
function bidFor(content,B,HEROES,hero){if(META[content.id])return META[content.id].bid;const same=B.filter(x=>x.hero===content.hero);const idx=same.findIndex(x=>x.id===content.id);return 910000+HEROES.indexOf(hero)+100*(idx>=0?idx:same.length)}
function gameDesc(rec,opts={}){const d=(rec.content.desc||'').trim();const parts=[d];if(opts.creator!==false)parts.push(BR.game_line);if(opts.rev!==false)parts.push('Rev '+rec.revision.ref.split('@')[1]);return parts.filter(Boolean).join('\n')}
function gameName(content){const n=content.name;return /\(Fully Annotated\)$/.test(n)?n:n+SUFFIX}
function toGameBuild(rec,ctx,opts={}){const {ITEMS,HEROES}=ctx;const c=rec.content,hero=C.heroOf(HEROES,c);if(!hero)throw new Error('hero '+c.hero);
 const {B}=ctx.data||C.loadData();const t=tagsOf(c);
 return {bid:bidFor(c,B,HEROES,hero),tags:t.tg?tagIds(t.tg,hero,ITEMS):[0,0,0],tagNames:t.tg,tagSource:t.source,name:gameName(c),desc:gameDesc(rec,opts),order:c.order,
  rows:c.rows.map(r=>r.map(([ti,d,o,its])=>[ti,d,o,its.map(([n,note,imb,sell])=>[n,note||'',C.imbIndex(imb,c,hero),(c.sell&&c.sell[n])||sell||0])])),hero}}
function loadEnc(){global.btoa=global.btoa||(s=>Buffer.from(s,'binary').toString('base64'));global.TextEncoder=global.TextEncoder||TextEncoder;
 const E={};new Function('module',fs.readFileSync(path.join(PUB,'site_patch/enc.js'),'utf8'))({set exports(v){Object.assign(E,v)}});return E}
function exportCode(rec,ctx,opts={}){const E=loadEnc();const gb=toGameBuild(rec,ctx,opts);const {hero}=gb;const code=E.buildCode(gb,hero,ctx.ITEMS);return {code,game:gb}}
module.exports={toGameBuild,exportCode,gameName,gameDesc,tagsOf,SUFFIX,BR,bidFor,loadEnc,META};
