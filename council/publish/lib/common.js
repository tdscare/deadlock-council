// Shared helpers for the publish pipeline. READ-ONLY with respect to data.js and every gate/other-agent file.
const fs=require('fs'),path=require('path'),cr=require('crypto');
const SP=path.resolve(__dirname,'../../..');
const PUB=path.join(SP,'council/publish');
const sha=b=>cr.createHash('sha256').update(b).digest('hex');
const shaFile=f=>sha(fs.readFileSync(f));
// canonical JSON (sorted keys) so hashes never depend on key order
const canon=o=>JSON.stringify(o,(k,v)=>v&&typeof v==='object'&&!Array.isArray(v)?Object.keys(v).sort().reduce((a,x)=>(a[x]=v[x],a),{}):v);
const rd=f=>fs.readFileSync(path.isAbsolute(f)?f:path.join(SP,f),'utf8');
const loadData=(file='data.js')=>{const s=rd(file);const o=new Function(s+';return {B,CN}')();return o};
const loadGame=()=>new Function(rd('gamedata.js')+';return {ITEMS,HEROES}')();
const heroOf=(HEROES,b)=>HEROES.find(h=>h.key===b.hk)||HEROES.find(h=>h.name===b.hero);
const COST={1:800,2:1600,3:3200,4:6400};
const isCore=t=>/^(Early|Mid|Late)/.test(t);
function mm2(s,seed=0x31415926){const d=Buffer.from(s);const m=0x5bd1e995;let l=d.length,h=(seed^l)>>>0,i=0;
 while(l-i>=4){let k=d.readUInt32LE(i);k=Math.imul(k,m)>>>0;k^=k>>>24;k=Math.imul(k,m)>>>0;h=Math.imul(h,m)>>>0;h=(h^k)>>>0;i+=4}
 const r=l-i;if(r>=3)h^=d[i+2]<<16;if(r>=2)h^=d[i+1]<<8;if(r>=1){h^=d[i];h=Math.imul(h,m)>>>0}
 h^=h>>>13;h=Math.imul(h,m)>>>0;h^=h>>>15;return h>>>0}
// walk a build's items: [{box, row, boxIdx, core, opt, name, note, imb}]
const items=b=>{const o=[];b.rows.forEach((r,ri)=>r.forEach((bx,bi)=>bx[3].forEach((it,ii)=>o.push({ri,bi,ii,title:bx[0],bdesc:bx[1],opt:!!bx[2],core:isCore(bx[0]),name:it[0],note:it[1]||'',imb:it[2]||0}))));return o};
// same imbue normalisation the live site applies (app.js imbIndex)
function imbIndex(v,b,hero){if(v==null||v===''||v===0)return 0;if(typeof v==='number')return v;if(/^[1-4]$/.test(v))return +v;if(/^ult$/i.test(v))return 4;
 const t=v.toLowerCase(),names=(hero?hero.ab.map(a=>a.n):[]).concat(b.abil||[]);for(let i=0;i<names.length;i++)if(names[i].toLowerCase().includes(t))return i%4+1;return 0}
module.exports={imbIndex,SP,PUB,sha,shaFile,canon,rd,loadData,loadGame,heroOf,COST,isCore,mm2,items,fs,path};
