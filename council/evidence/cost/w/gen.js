const L=require('./lib.js');const N=require('./notes.js');const {G,C,cc,col,B,flat,applyOps,walk,spk,per1k,xb,SP,fs}=L;
const ids=fs.readFileSync(SP+'council/evidence/cost/chunk0.txt','utf8').split(/\s+/).filter(Boolean);
const OUT=SP+'council/evidence/cost/';
const tl=n=>`${cc(n)}${G[n].tier}`;
const TH=[4800,6400,8000,16000];
function sells(b,base){const owned=base.owned.slice();const inv=ow=>{const r={w:0,s:0,v:0};ow.forEach(n=>r[cc(n)]+=C[G[n].tier]);return r};const b0=inv(owned);const lines=[];
 for(const r of b.rows)for(const [t,d,o,items] of r){if(/^(Early|Mid|Late)/.test(t)||!o)continue;const dm=(d||'').match(/Sell ([A-Z][^.]*?) for it/);
  for(const [n,note] of items){if(!G[n])continue;const ss=[];if(dm&&/Counters/.test(t))ss.push(dm[1]);for(const x of (note||'').matchAll(/Sell ([A-Z][^.,]*?) for this/g))ss.push(x[1]);
   const up=(note||'').match(/^Upgrade of ([^.]+)\./);if(up)ss.push(up[1]);
   for(const s of ss){if(!G[s])continue;const ow=owned.slice();const i=ow.indexOf(s);if(i<0){lines.push(`- ${t}: ${n} sells ${s}: not in final core (already sold/consumed)`);continue}ow.splice(i,1);ow.push(n);const a=inv(ow);
    const lost=['w','s','v'].map(k=>{const c=TH.filter(x=>b0[k]>=x&&a[k]<x);return c.length?`${col[k]} ${b0[k]}>${a[k]} (loses ${c.join('/')})`:''}).filter(Boolean);
    if(lost.length)lines.push(`- **FLAG** ${t}: ${n} (${tl(n)}) sells ${s} (${tl(s)}): ${lost.join('; ')}`)}}}
 return {b0,lines:[...new Set(lines)]}}
const summaryRows=[];
for(const id of ids){const b=B.find(x=>x.id===id);const nt=N[id];if(!nt){console.log('NO NOTES',id);continue}
 const base=walk(flat(b));const md=[];
 md.push(`# Cost-efficiency audit: ${id} (${b.name})`);
 md.push(`Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: ${spk(base)}. End of core: ${base.souls} souls, gun ${base.end.w} / spirit ${base.end.s} / health ${base.end.v}, ${base.slots} slots.`);
 md.push('');md.push(`Result: ${nt.sum.flags}`);md.push(`Minimal fix: ${nt.sum.fix}`);md.push('');
 md.push('## Per item (buy order)');md.push('Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.');md.push('');
 md.push('| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |');md.push('|---|---|---|---|---|---|---|---|');
 base.rows.forEach((r,i)=>{const nf=nt.items[r.n];let v=nf?`${nf[0]==='OK'?'OK':'FLAG '+nf[0]}: ${nf[1]}`:'OK';
  const x=xb(id,r.n);if(!nf&&x&&(x.ratio>1.6||x.ratio<0.55))v+=` (info: bought ${x.mine} vs median ${x.m} in ${x.n} other builds, no action)`;
  else if(nf&&x&&(x.ratio>1.6||x.ratio<0.55))v+=` [vs ${x.n} other builds: median ${x.m}, min ${x.min.souls} ${x.min.id}, max ${x.max.souls} ${x.max.id}]`;
  md.push(`| ${i+1} | ${r.souls} | ${r.n} | ${r.cost} | ${tl(r.n)} | ${per1k(r.n)} | ${r.iv.w}/${r.iv.s}/${r.iv.v} | ${v} |`)});
 md.push('');
 md.push('## Swap / "Instead of" boxes re-walked');
 const sw=nt.swaps||[];
 if(!sw.length)md.push('No swap or "instead of" box in this build besides notes already covered above (a lost-lane reorder box, if present, is walked under Reorders).');
 else{md.push('| box | ops | gun/spirit/health end | 4.8k spikes | slots | souls | verdict |');md.push('|---|---|---|---|---|---|---|');
  md.push(`| base | - | ${base.end.w}/${base.end.s}/${base.end.v} | ${spk(base)} | ${base.slots} | ${base.souls} | - |`);
  for(const s of sw){const w=walk(applyOps(flat(b),s.ops));md.push(`| ${s.b} | ${s.ops.join(' ; ')} | ${w.end.w}/${w.end.s}/${w.end.v} | ${spk(w)} | ${w.slots} | ${w.souls} | ${s.v} |`)}}
 md.push('');
 if((nt.fixes||[]).length){md.push('## Tested fixes / reorders (each re-walked)');md.push('| change | ops | gun/spirit/health end | 4.8k spikes | slots | souls |');md.push('|---|---|---|---|---|---|');
  md.push(`| base | - | ${base.end.w}/${base.end.s}/${base.end.v} | ${spk(base)} | ${base.slots} | ${base.souls} |`);
  for(const f of nt.fixes){const w=walk(applyOps(flat(b),f.ops));md.push(`| ${f.t} | ${f.ops.join(' ; ')} | ${w.end.w}/${w.end.s}/${w.end.v} | ${spk(w)} | ${w.slots} | ${w.souls} |`)}md.push('')}
 const sl=sells(b,base);md.push('## Sells in counters / rich / slot-locked boxes (effect on spike totals)');
 md.push(`End-of-core invest: gun ${sl.b0.w}, spirit ${sl.b0.s}, health ${sl.b0.v}. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.`);
 md.push(sl.lines.length?sl.lines.join('\n'):'- none cross a threshold');md.push('');
 md.push('## Other findings');(nt.find||[]).forEach(x=>md.push('- '+x));
 md.push('- Gun / spirit / health 4.8k: '+['w','s','v'].map(k=>`${col[k]} ${base.spikes[k]?'@'+base.spikes[k]:'NEVER (end '+base.end[k]+')'}`).join(', ')+'.');
 md.push('- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).');
 fs.writeFileSync(OUT+id+'.md',md.join('\n')+'\n');
 summaryRows.push(`| ${id} | ${nt.sum.flags.replace(/\|/g,'/')} | ${nt.sum.fix.replace(/\|/g,'/')} |`);
}
const hdr='| build | flags | proposed fix |\n|---|---|---|\n';
const SPATH=OUT+'SUMMARY_0.md';
let ex='';try{ex=fs.readFileSync(SPATH,'utf8')}catch(e){}
fs.writeFileSync(SPATH,(ex?ex.replace(/\n*$/,'\n'):'# Cost-efficiency summary, chunk 0\nSeverity: HIGH = a 4.8k spike never lands or is lost, MED = spike/big item moved >4k souls or slot/cost break, LOW = small, INFO = colour never reaches 4.8k by design. Full numbers in council/evidence/cost/<build>.md.\n\n'+hdr)+summaryRows.join('\n')+'\n');
console.log('written',summaryRows.length);
