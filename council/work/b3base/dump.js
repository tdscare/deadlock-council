const fs=require('fs');const src=fs.readFileSync(process.argv[2],'utf8');
const B=new Function(src+';return B')();
for(const id of process.argv.slice(3)){const b=B.find(x=>x.id===id);fs.writeFileSync(__dirname+'/base_'+id+'.json',JSON.stringify(b,null,1));}
