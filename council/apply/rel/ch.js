const fs=require('fs');const B=new Function(fs.readFileSync('data.js','utf8')+';return B;')();
const [id,...kw]=process.argv.slice(2);const b=B.find(x=>x.id===id);
const re=new RegExp(kw.join('|'),'i');
console.log('##',id,'changes',b.changes.length);
b.changes.forEach((c,i)=>{if(!kw.length||re.test(c)){console.log(' ['+i+'] '+c.slice(0,1500));}});
