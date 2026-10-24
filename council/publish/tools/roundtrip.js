#!/usr/bin/env node
// Round trip + record-integrity checks. record -> export code -> INDEPENDENT decode -> compare every supported field.
// usage: node roundtrip.js <id> [--record file.json] [--json]       (default: record of data.js entry)
const C=require('../lib/common');const R=require('../lib/record');const X=require('../lib/export');const G=require('../lib/gamefmt');
const ctx=C.loadGame();
const esc=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
function checks(rec,code,game,opts={}){const out=[];const add=(check,ok,detail)=>out.push({check,ok:!!ok,detail:ok?(detail||''):detail});
 const c=rec.content,hero=C.heroOf(ctx.HEROES,c);let d;
 try{d=G.decode(code,ctx)}catch(e){add('decode',false,e.message);return out}
 add('decode',true,d.bytes+' bytes protobuf');
 add('size<=16000',d.bytes<=G.LIMITS.totalBytes.max,d.bytes);
 add('hero',d.hero===hero.name,`${d.hero} vs ${hero.name}`);add('build_id',d.build_id===game.bid,`${d.build_id} vs ${game.bid}`);
 add('name',d.name===game.name,`"${d.name}" vs "${game.name}"`);add('name_length<=50 (UI maxchars)',d.name.length<=G.LIMITS.name.max,`${d.name.length} chars; game UI limit 50, whether a pasted code is truncated/rejected is UNVERIFIED`);
 add('description',d.desc===game.desc&&d.desc.length<=G.LIMITS.description.max,`${d.desc.length}/${G.LIMITS.description.max} chars; equal=${d.desc===game.desc}`);
 // categories in row-major box order
 const boxes=c.rows.flat();add('category_count',d.categories.length===boxes.length,`${d.categories.length} vs ${boxes.length}`);
 let mism=[],miss=[],dups=[];const seenCore=new Set();
 boxes.forEach((bx,i)=>{const dc=d.categories[i];if(!dc){miss.push('category '+bx[0]);return}
  if(dc.name!==bx[0])mism.push(`title[${i}] "${dc.name}"!="${bx[0]}"`);if(dc.desc!==(bx[1]||''))mism.push(`desc[${bx[0]}] differs`);if(dc.optional!==!!bx[2])mism.push(`optional[${bx[0]}]`);
  if(dc.mods.length!==bx[3].length)mism.push(`items[${bx[0]}] ${dc.mods.length}!=${bx[3].length}`);
  bx[3].forEach((it,j)=>{const m=dc.mods[j];if(!m){miss.push(bx[0]+': '+it[0]);return}
   if(m.item!==it[0])mism.push(`item[${bx[0]}#${j}] ${m.item}!=${it[0]}`);if(m.note!==(it[1]||''))mism.push(`caption[${it[0]}] differs`);
   const want=C.imbIndex(it[2],c,hero);if(m.imbue!==want)mism.push(`imbue[${it[0]}] ability#${m.imbue}!=ability#${want}`);
   const ws=(c.sell&&c.sell[it[0]])||it[3]||0;if(m.sell!==ws)mism.push(`sell_priority[${it[0]}] ${m.sell}!=${ws}`);
   if((m.note||'').length>G.LIMITS.annotation.max)mism.push(`caption too long [${it[0]}] ${m.note.length}>200`);
   if(!ctx.ITEMS[it[0]])miss.push('unknown item '+it[0]);
   if(isCore(bx[0])&&!bx[2]){if(seenCore.has(it[0]))dups.push(it[0]);seenCore.add(it[0])}})});
 add('categories_and_items_and_captions',!mism.length&&!miss.length,[...mism,...miss.map(x=>'MISSING '+x)].slice(0,8).join(' | '));
 add('no_duplicate_core_purchase',!dups.length,'duplicate: '+dups.join(', '));
 // ability order
 const eo=G.expectedOrder(c.order||[]);const ok=JSON.stringify(eo.map(e=>[e.ab,e.type,e.delta]))===JSON.stringify(d.order.map(e=>[e.ab,e.type,e.delta]));
 add('ability_order',ok,`expected ${eo.length} entries, decoded ${d.order.length}`);
 // tags
 const want=game.tagNames?game.tagNames.map(t=>ctx.ITEMS[t]?{item:t}:hero.ab.find(a=>a.n===t)?{ability:t}:t):[];
 add('tags',JSON.stringify(want)===JSON.stringify(d.tags),`decoded ${JSON.stringify(d.tags)} vs ${JSON.stringify(want)}`);
 add('tag_slots<=3',d.tags.length<=3,d.tags.length);
 // sale-instruction and ability-info consistency inside captions
 const all=C.items(c);const names=new Set(all.map(i=>i.name));const own=new Set(hero.ab.map(a=>a.n.toLowerCase()));
 const foreign=[];for(const h of ctx.HEROES)if(h!==hero)for(const a of h.ab)if(a.n.length>5&&!own.has(a.n.toLowerCase())&&!ctx.ITEMS[a.n])foreign.push(a.n);
 const badSale=[],badAb=[];
 for(const it of all){const re=/\bSell ([A-Z][A-Za-z'’\- ]+?)(?= for\b| once\b| late\b| after\b| when\b| if\b| to\b|[.,;]|$)/g;let m;
  while((m=re.exec(it.note))){const t=m[1].trim();if(/^(it|them|this|one|the|either|whichever|something|one of them)$/i.test(t))continue;if(!ctx.ITEMS[t]){badSale.push(`${it.name}: sells unknown "${t}"`);continue}
   if(!names.has(t))badSale.push(`${it.name}: sells ${t} which is not in this build`);else if(t===it.name&&false)badSale.push('self')}
  let nn=it.note;for(const a of hero.ab)nn=nn.split(a.n).join(' ');for(const n of names)nn=nn.split(n).join(' ');for(const f of foreign)if(new RegExp('\\b'+esc(f)+'\\b').test(nn))badAb.push(`${it.name}: mentions another hero's ability "${f}"`)}
 add('sale_instructions_reference_real_items',!badSale.length,badSale.slice(0,5).join(' | '));
 add('ability_references_belong_to_hero',!badAb.length,badAb.slice(0,5).join(' | '));
 const ac={};for(const i of c.order||[])ac[i]=(ac[i]||0)+1;add('ability_points_valid',(c.order||[]).length<=16&&Object.values(ac).every(n=>n<=4),`points=${(c.order||[]).length}, per ability ${JSON.stringify(ac)}`);
 return out}
function isCore(t){return C.isCore(t)}
function run(rec,opts){const {code,game}=X.exportCode(rec,ctx,opts);return {code,game,checks:checks(rec,code,game,opts)}}
module.exports={checks,run};
if(require.main===module){const a=process.argv.slice(2);const id=a[0];const rf=a.indexOf('--record')>0?a[a.indexOf('--record')+1]:null;
 const rec=rf?JSON.parse(require('fs').readFileSync(rf,'utf8')):R.liveRecord(id);const r=run(rec);
 if(a.includes('--json'))console.log(JSON.stringify(r.checks,null,1));else{console.log('RECORD',rec.revision.ref,'slot='+rec.slot);r.checks.forEach(c=>console.log((c.ok?'PASS ':'FAIL ')+c.check+(c.detail?'  '+c.detail:'')))}
 process.exit(r.checks.every(c=>c.ok)?0:1)}
