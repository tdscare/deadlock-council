const fs=require('fs');
const {B}=new Function(fs.readFileSync('data.js','utf8')+';return {B};')();
const out=B.map(b=>{
  const core=[],opt=[];
  for(const row of b.rows) for(const bx of row){
    const [title,desc,optional,items]=bx;
    const its=items.map(i=>({n:i[0],note:i[1]||'',imb:i[2]||''}));
    if(!optional && /^(Early|Mid|Late)/.test(title)) core.push({title,items:its});
    else opt.push({title,desc,items:its});
  }
  return {id:b.id,hero:b.hero,name:b.name,desc:b.desc,abil:b.abil,order:b.order,core,opt,hk:b.hk};
});
fs.writeFileSync('council/sandbox/builds_ov.json',JSON.stringify(out,null,1));
console.log(out.length);
