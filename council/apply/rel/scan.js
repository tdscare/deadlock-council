const fs=require('fs');const B=new Function(fs.readFileSync('data.js','utf8')+';return B;')();
const T=JSON.parse(fs.readFileSync('council/apply/rel/itemtags.json','utf8'));
const ids=process.argv.slice(2);
for(const b of B){ if(ids.length&&!ids.includes(b.id))continue;
 let lines=[];
 b.rows.forEach(r=>r.forEach(bx=>{const items=bx[3].map(i=>{const t=T[i[0]];if(!t)return i[0]+'[?]';const s=t[1][0];const tg=t[2].filter(x=>!/^WDMG|SPIRIT|CHARGE/.test(x));return i[0]+'('+s+t[0]+(tg.length?' '+tg.join(','):'')+')';});lines.push('  '+bx[0].slice(0,22)+': '+items.join('; '));}));
 console.log('## '+b.id+' | '+b.desc+' | '+b.name);console.log(lines.join('\n'));}
