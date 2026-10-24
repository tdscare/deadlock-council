const fs=require('fs');process.chdir(__dirname+'/../../..');
const B=new Function(fs.readFileSync('data.js','utf8')+';return B')();const G=JSON.parse(fs.readFileSync('audit/items_full.json'));
const names=Object.keys(G).sort((a,b)=>b.length-a.length);const q=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
let n=0;
for(const b of B){const have={};b.rows.forEach(r=>r.forEach(([t,d,o,it])=>it.forEach(i=>{(have[i[0]]=have[i[0]]||[]).push(t)})));
 const claim={};
 (b.changes||[]).forEach((c,ci)=>{for(const it of names){const e=q(it);
  let m;
  if(new RegExp(e+' (out|removed|dropped|is out|gone)\\b|(dropped|removed|cut|drop|remove) '+e+'\\b|'+e+' → [A-Z]|'+e+' out of').test(c))claim[it]={k:'out',ci,txt:(c.match(new RegExp('.{0,60}'+e+'.{0,60}'))||[''])[0]};
  else if(new RegExp(e+' (in|added)\\b[^a-z]|(added|adds|add) '+e+'\\b|'+e+' (now|moved)|moved '+e+'\\b').test(c))claim[it]={k:'in',ci,txt:(c.match(new RegExp('.{0,60}'+e+'.{0,60}'))||[''])[0]}}});
 for(const it in claim){const c=claim[it];const present=!!have[it];
  if(c.k==='out'&&present&&c.ci>=(b.changes.length-8)){n++;console.log(`${b.id} | line ${c.ci+1}/${b.changes.length} says ${it} OUT but it is in ${have[it].join(',')} | "${c.txt.replace(/\s+/g,' ')}"`)}
  if(c.k==='in'&&!present&&c.ci>=(b.changes.length-8)){n++;console.log(`${b.id} | line ${c.ci+1}/${b.changes.length} says ${it} IN/moved but it is absent | "${c.txt.replace(/\s+/g,' ')}"`)}}}
console.log(n)
