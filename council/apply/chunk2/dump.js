const fs=require('fs');const src=fs.readFileSync('data.js','utf8');const B=new Function(src+';return B;')();
const ids=process.argv.slice(2);
for(const id of ids){const b=B.find(x=>x.id===id);fs.writeFileSync('council/apply/chunk2/w/'+id+'.js',JSON.stringify(b,null,1));
console.log('##',id,b.name,'|',b.desc,'| nchanges',b.changes.length);
b.rows.forEach((r,ri)=>r.forEach((bx,bi)=>console.log(` [${ri}.${bi}] ${bx[0]} | ${bx[1]} | ${bx[2]} ::`,bx[3].map(i=>i[0]+(i[1]?' {'+i[1]+'}':'')+(i[2]?' #'+i[2]:'')).join(' ; '))));}
