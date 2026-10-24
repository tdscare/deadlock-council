const fs=require('fs');const SP=process.cwd();
const src=fs.readFileSync(SP+'/data.js','utf8');const B=new Function(src+';return B;')();
const ids=process.argv.slice(2);
for(const id of ids){const b=B.find(x=>x.id===id);fs.writeFileSync(SP+'/council/apply/chunk1/w/'+id+'.json',JSON.stringify(b,null,1));
console.log('==',id,b.name,'|',b.desc,'| changes:',JSON.stringify(b.changes).slice(0,200));
b.rows.forEach(r=>r.forEach(bx=>console.log(' ['+bx[0]+'] ('+bx[1]+') '+(bx[2]?'R':'')+'\n    '+bx[3].map(i=>i[0]+(i[1]?' {'+i[1]+'}':'')+(i[2]?'#'+i[2]:'')).join(' | '))))}
