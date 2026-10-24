/* STAGED copy of enc.js: only change = optional 4th item element `sell` -> BuildModEntry.sell_priority (field 4). Byte-identical output when no item carries `sell` (tests/run_tests.js). NOT applied to the live site. */
/* build -> in-game clipboard code: protobuf (CMsgHeroBuild) -> zstd frame (raw blocks) -> base64 */
const PB={
  vint(n){n=BigInt.asUintN(64,BigInt(n));const o=[];do{let b=Number(n&127n);n>>=7n;if(n)b|=128;o.push(b)}while(n);return o},
  key(f,t){return PB.vint(f*8+t)},
  V(f,n){return [...PB.key(f,0),...PB.vint(n)]},
  L(f,v){const b=typeof v==="string"?[...new TextEncoder().encode(v)]:v;return [...PB.key(f,2),...PB.vint(b.length),...b]},
  F(f,x){const a=new Uint8Array(new Float32Array([x]).buffer);return [...PB.key(f,5),...a]}
};
function zstdRaw(data){
  const n=data.length,out=[0x28,0xB5,0x2F,0xFD];
  if(n<256){out.push(0x20,n)}else if(n<65792){const v=n-256;out.push(0x60,v&255,v>>8)}else{out.push(0xA0,n&255,(n>>8)&255,(n>>16)&255,(n>>>24)&255)}
  const MAX=131072;let i=0;
  do{const sz=Math.min(MAX,n-i),last=i+sz>=n?1:0,h=last|(0<<1)|(sz<<3);out.push(h&255,(h>>8)&255,(h>>16)&255);for(let k=0;k<sz;k++)out.push(data[i+k]);i+=sz}while(i<n);
  return out}
function b64(bytes){let s="";for(let i=0;i<bytes.length;i+=8192)s+=String.fromCharCode.apply(null,bytes.slice(i,i+8192));return btoa(s)}
function buildCode(b,hero,ITEMS){
  const ah=hero.ab.map(a=>a.id),cats=[];
  for(const row of b.rows)for(const [title,desc,opt,items] of row){
    const mods=[];
    for(const [n,note,imb,sell] of items){const it=ITEMS[n];if(!it)continue;let m=PB.V(1,it.id);if(note)m=m.concat(PB.L(2,note));if(sell)m=m.concat(PB.V(4,sell));if(imb&&ah[imb-1])m=m.concat(PB.V(5,ah[imb-1]));mods.push(...PB.L(1,m))}
    const w=Math.round(Math.max(84*items.length+22,170,Math.min(title.length*9+(opt?80:0)+(desc||"").length*3.1+30,700)));
    let c=mods.concat(PB.L(2,title),PB.L(3,desc||""),PB.F(4,w),PB.F(5,162+24*Math.min(3,Math.ceil((title.length*9+(opt?80:0)+(desc||"").length*6.2+30)/w)-1)));if(opt)c=c.concat(PB.V(6,1));
    cats.push(...PB.L(1,c))}
  let det=cats;
  if(b.order&&b.order.length){const cnt=[0,0,0,0,0];const ent=[];
    for(const i of b.order){if(!ah[i-1])continue;const c=cnt[i]++;if(c>3)continue;ent.push(...PB.L(1,[...PB.V(1,ah[i-1]),...PB.V(2,c===0?2:1),...PB.V(3,c===0?-1:[-1,-2,-5][c-1])]))}
    det=det.concat(PB.L(2,ent))}
  const now=Math.floor(Date.now()/1000);
  const msg=[...PB.V(1,b.bid||(910000+hero.id)),...PB.V(2,hero.id),...PB.V(3,300559836),...PB.V(4,now),...PB.L(5,b.name||"Build"),...PB.L(6,b.desc||""),...PB.V(7,0),...PB.V(8,1),...PB.V(9,0),...PB.L(10,det),...(b.tags||[0,0,0]).flatMap(t=>PB.V(11,t)),...PB.V(13,now)];
  return b64(zstdRaw(msg))}
if(typeof module!=="undefined")module.exports={buildCode,zstdRaw};
