const fs=require('fs');
function rv(b,o){let r=0n,s=0n,x;do{x=b[o++];r|=BigInt(x&127)<<s;s+=7n}while(x&128);return [r,o]}
function parse(b){const out=[];let o=0;while(o<b.length){let k;[k,o]=rv(b,o);const f=Number(k>>3n),t=Number(k&7n);let v;
 if(t==0){[v,o]=rv(b,o)}else if(t==2){let l;[l,o]=rv(b,o);l=Number(l);v=b.slice(o,o+l);o+=l}
 else if(t==5){v=b.readFloatLE(o);o+=4}else if(t==1){v=b.readDoubleLE(o);o+=8}out.push([f,t,v])}return out}
module.exports={parse,rv};
if(require.main===module){
const top=parse(fs.readFileSync(process.argv[2]));
const det=top.find(x=>x[0]==10)[2];
for(const [f,t,v] of parse(det)){ if(f!=1)continue; const c=parse(v);
 const g=n=>c.filter(x=>x[0]==n).map(x=>x[2]);
 console.log(JSON.stringify(g(2)[0]+''),'items',g(1).length,'w',g(4)[0],'h',g(5)[0],'opt',g(6)[0]+'',
  g(1).map(m=>{const p=parse(m);return p.map(x=>x[0]+'').join('')}).join(' '));}
}
