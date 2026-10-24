const fs=require('fs');const [f,id]=process.argv.slice(2);const s=fs.readFileSync(f,'utf8');
const B=new Function(s+';return B;')();const b=B.find(x=>x.id===id);console.log(JSON.stringify(b,null,1));
