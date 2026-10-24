const fs=require('fs');const P='council/apply/rel/';
for(const id of ['solomon','solomon_support']){
 const b=JSON.parse(fs.readFileSync(P+'w/'+id+'.js','utf8'));let n=0;
 for(const r of b.rows)for(const x of r)x[3].forEach(i=>{if(i[0]==='Hollow Point'){i[0]='Alchemical Fire';n++;}});
 if(n!==1)throw id+' '+n;
 b.changes.push(id==='solomon'
 ?"Relevance pass: Hollow Point (added in the cost pass only to land gun 4.8k) out for Alchemical Fire, same gun colour, same 3.2k, same spot, so every spike is unchanged. Hollow Point's +35% Weapon Damage and bullet-resist cut only work through your bullets, and every Solomon damage ability scales with spirit (Bishop 70 + 2.0x, Fork 50 + 1.3x, Queen 120 + 1.4x; none uses weapon damage). Alchemical Fire is a thrown 10m fire zone, 45 → 95 damage a second over 5s (+0.2x → +0.4x spirit), +10 spirit power and -7% bullet resist on enemies inside: AoE spirit damage for an AoE build."
 :"Relevance pass: Heroic Aura swap is now Alchemical Fire instead of Hollow Point (same gun colour and 3.2k, so gun 4.8k holds; same item Support Doorman uses here). Hollow Point's +35% Weapon Damage only adds to your own bullets, and this support's damage and healing scale with spirit; Alchemical Fire is a 10m fire zone that scales with spirit (45 → 95 a second, +0.2x → +0.4x spirit), +10 spirit power, and needs no gun.");
 fs.writeFileSync(P+'out/'+id+'.js',JSON.stringify(b,null,1));}
