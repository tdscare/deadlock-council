// generates council/evidence/cost/<id>.md for chunk3 builds. usage: node council/tools/cost_gen.js
process.chdir(__dirname+'/../..');
const fs=require('fs');let src=fs.readFileSync('audit/walk2.js','utf8');src=src.slice(0,src.indexOf('const id=process.argv[2]'));
const {B,IT,C,walk}=new Function('require',src+';return {B,IT,C,walk}')(require);
const G=JSON.parse(fs.readFileSync('audit/items_full.json'));const POS=JSON.parse(fs.readFileSync('council/evidence/cost/_pos.json'));
const M=require('./cost_manual.js');
const ids=fs.readFileSync('council/evidence/cost/chunk3.txt','utf8').split('\n').map(s=>s.trim()).filter(Boolean);
const COL={w:'gun',s:'spirit',v:'health'};
const KS=[['TechPower','SP'],['BonusHealth','HP'],['BonusFireRate','fire rate %'],['BaseAttackDamagePercent','weapon dmg %'],['BulletResist','bullet resist'],['TechResist','spirit resist'],['BonusClipSizePercent','clip %'],['Stamina','stamina'],['BonusMoveSpeed','move m/s'],['BonusSprintSpeed','sprint m/s'],['BulletLifestealPercent','bullet LS %'],['AbilityLifestealPercentHero','spirit LS %']];
const num=v=>{const m=String(v).match(/^-?[\d.]+/);return m?parseFloat(m[0]):0};
function per1k(n){const g=G[n];const cost=C[g.tier];const out=[];for(const [k,l] of KS){const v=num((g.stats||{})[k]);if(v>0)out.push(l+' '+(v/cost*1000).toFixed(1))}return out.slice(0,4).join(', ')||'effect only'}
const med=a=>{a=a.slice().sort((x,y)=>x-y);return a[Math.floor(a.length/2)]};
const rows=[];
for(const id of ids){const b=B.find(x=>x.id===id);const m=M[id];if(!m){console.log('NO MANUAL',id);continue}
 let owned=[],souls=0,n=0;const lines=[];const cross={w:{},s:{},v:{}};
 for(const r of b.rows)for(const [t,d,o,items] of r){if(!/^(Early|Mid|Late)/.test(t))continue;
  for(const [nm,note] of items){const g=G[nm];const have=g.components.filter(c=>owned.includes(c));const net=C[g.tier]-have.reduce((a,c)=>a+C[G[c].tier],0);souls+=net;owned=owned.filter(x=>!have.includes(x));owned.push(nm);
   const sm=(note||'').match(/Sell ([A-Z][^.]*?) (?:for this|first)/);let sold='';if(sm){const i=owned.indexOf(sm[1]);if(i>=0){owned.splice(i,1);sold=' (sells '+sm[1]+')'}}
   const inv={w:0,s:0,v:0};owned.forEach(x=>inv[IT[x].c]+=C[IT[x].t]);
   for(const k in inv)if(inv[k]>=4800&&cross[k].t==null)cross[k].t=souls;
   const oth=(POS[nm]||[]).filter(x=>x.id!==id);const pos=oth.length?`${oth.length} builds, ${Math.min(...oth.map(x=>x.s))}-${Math.max(...oth.map(x=>x.s))}, med ${med(oth.map(x=>x.s))}`:'only build';
   let v=m.ovr[nm];if(!v){v='OK'+(have.length?' - upgrade of '+have.join('+'):'')}
   lines.push(`| ${++n} | ${nm} (${t.replace(/ · .*/,'').replace(/ \(.*/,'')}) | ${C[g.tier]}${have.length?' (net '+net+')':''} | ${souls} | ${inv.w}/${inv.s}/${inv.v} | ${per1k(nm)} | ${pos} | ${v}${sold} |`)}}
 const {flags}=walk(b);
 const cs=['w','s','v'].map(k=>`${COL[k]} ${cross[k].t==null?'never':'@'+cross[k].t}`).join(', ');
 let md=`# ${id}: ${b.name} (${b.desc||'no desc'})\n\nCost-efficiency audit. Verdict: **${m.verdict}**\n\nwalk1 flags: ${flags.length?flags.join('; '):'none'}. 4.8k invest crossings (souls spent): ${cs}. Core ends ${souls} souls, ${owned.length} slots.\n\n`;
 md+=`## Swap / Instead-of / sell-for boxes (re-walked)\n${m.swaps.map(s=>'- '+s).join('\n')}\n\n`;
 md+=`## Flags\n${m.flags.length?m.flags.map(s=>'- '+s).join('\n'):'- none'}\n\n`;
 md+=`## Proposed fix\n${m.fix.length?m.fix.map(s=>'- '+s).join('\n'):'- none'}\n\n`;
 md+=`## Items in buy order\nInvest column = gun/spirit/health souls spent after the buy. Stats are per 1000 souls of the item's full price. "Other builds" = same item elsewhere in data.js (souls at purchase from the walk).\n\n| # | Item (box) | Price | Souls after | Invest g/s/h | Stats per 1000 | Other builds | Verdict |\n|---|---|---|---|---|---|---|---|\n${lines.join('\n')}\n`;
 fs.writeFileSync(`council/evidence/cost/${id}.md`,md);
 rows.push(`| ${id} | ${m.flagCount} | ${m.summaryFix} |`);}
const sf='council/evidence/cost/SUMMARY_3.md';
if(!fs.existsSync(sf))fs.writeFileSync(sf,'# Cost-efficiency summary, chunk3\n\n| build | flags | proposed fix |\n|---|---|---|\n');
fs.appendFileSync(sf,rows.join('\n')+'\n');console.log('wrote',rows.length);
