// node variant.js <buildid> <out.js> "Old=>New" ...   (what-if copy of a build in data.js; does not touch data.js)
const fs=require('fs');const [id,out,...sw]=process.argv.slice(2);
const B=new Function(fs.readFileSync('data.js','utf8')+';return B')();const w=JSON.parse(JSON.stringify(B.find(b=>b.id===id)));delete w.changes;
for(const s of sw){const [a,b]=s.split('=>');for(const r of w.rows)for(const box of r)for(const it of box[3])if(it[0]===a)it[0]=b}
fs.writeFileSync(out,JSON.stringify(w,null,1));
