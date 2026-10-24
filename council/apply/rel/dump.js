const fs=require('fs');const src=fs.readFileSync('data.js','utf8');const B=new Function(src+';return B;')();
let ids=process.argv.slice(2); if(ids[0]==='ALL') ids=B.map(b=>b.id);
for(const id of ids){const b=B.find(x=>x.id===id);fs.writeFileSync('council/apply/rel/w/'+id+'.js',JSON.stringify(b,null,1));
console.log('##',id,'|',b.hero,'|',b.name,'|',b.desc,'| order',b.order.join(''),'| abil',b.abil.join('/'));
b.rows.forEach((r,ri)=>r.forEach((bx,bi)=>console.log(` [${ri}.${bi}] ${bx[0]} | ${bx[1]} ::`,bx[3].map(i=>i[0]+(i[1]?' {'+i[1]+'}':'')).join(' ; '))));
if(process.env.CH) b.changes.forEach(c=>console.log('  CH:',c));}
