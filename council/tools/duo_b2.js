// builds batch-2 duo work files from data.js bases (never writes data.js)
process.chdir(__dirname+'/../..');
const fs=require('fs');const B=new Function(fs.readFileSync('data.js','utf8')+';return B')();
const base=id=>JSON.parse(JSON.stringify(B.find(b=>b.id==id)));
const box=(b,t)=>{for(const r of b.rows)for(const x of r)if(x[0]==t)return x;throw 'no box '+t};
const idx=(x,n)=>{const i=x[3].findIndex(i=>i[0]==n);if(i<0)throw 'no item '+n+' in '+x[0];return i};
const ins=(b,t,after,item)=>{const x=box(b,t);x[3].splice(idx(x,after)+1,0,item)};
const rep=(b,t,n,item)=>{const x=box(b,t);x[3].splice(idx(x,n),1,item)};
const del=(b,t,n)=>{const x=box(b,t);x[3].splice(idx(x,n),1)};
const note=(b,t,n,s)=>{const x=box(b,t);x[3][idx(x,n)][1]=s};
const dropBox=(b,t)=>{b.rows=b.rows.map(r=>r.filter(x=>x[0]!=t)).filter(r=>r.length)};
const mk=(b,id,name,desc,changes)=>{b.id=id;b.name=name;b.desc=desc;b.tag='New';b.changes=changes;
 fs.writeFileSync('council/work/'+id+'.js',JSON.stringify(b,null,1)+'\n');console.log('wrote',id)};

// ---- Pair B2-1: Victor + Haze (cross shred) ----
{const b=base('victor');
 ins(b,'Mid · L-R','Mystic Vulnerability',['Bullet Resist Shredder','For Haze: your aura keeps it on everyone near you.']);
 // keep boxes at 8: move Compress Cooldown to the start of Mid cont.
 const m=box(b,'Mid · L-R');const cc=m[3].splice(idx(m,'Compress Cooldown'),1)[0];box(b,'Mid · cont.')[3].unshift(cc);
 del(b,'Late · L-R','Witchmail');
 mk(b,'victor_duo_haze',"Rizuhble's Aura Shredder Victor",'Duo Victor for Haze',[
 "Duo (Haze): Bullet Resist Shredder in after Mystic Vulnerability (12.8k). Aura of Suffering ticks spirit damage every 0.25s on everyone within 8m (9m T3, pick 8) for an 8s channel on a 2s cooldown, so the -10% bullet resist (8s) never drops off anyone near Victor: Haze's gun does about +11% on the whole clump. Victor's own damage is spirit, so solo the item does almost nothing for him; it is only here for Haze.",
 "Duo (Haze): Witchmail out to keep 12 slots. Health spike still lands at 9.6k (walk1); late health spend 24k -> 17.6k. Compress Cooldown moved to the start of Mid · cont. so no box holds more than 8 items (same buy order).",
 "Rejected: dropping Torment Pulse or Warp Stone for the slot (Torment Pulse is his early damage plus 18% melee resist; Warp Stone is his engage). Rejected Spirit Shredder on Victor: it shreds spirit, which helps Victor himself, not Haze.",
 "Sandbox: duo_victor_haze_crossshred (H-B2-1.1..1.4). No result files yet: untested, kept on kit numbers."]);}

{const b=base('haze');
 ins(b,'Mid · L-R','Siphon Bullets',['Spirit Shredder','For Victor: his aura hurts more on whoever you shoot.']);
 rep(b,'Late · L-R','Silencer',['Spirit Rend','']);
 del(b,'Swaps','Phantom Strike');
 note(b,"I'm rich as fuck",'Inhibitor','Their carry heals a lot or out-damages you. Sell Lucky Shot for it.');
 mk(b,'haze_duo_victor',"Rizuhble's Brawl Buddy Haze",'Duo Haze for Victor',[
 "Duo (Victor): Spirit Shredder in right after Siphon Bullets (when Haze starts fighting). Her bullets put -8% spirit resist on the target for 8s and give her AND Victor 10% spirit lifesteal against it: Victor's aura, Torment Pulse, Scourge and Spirit Burn all hit that target ~8% harder and his aura heals him. Haze's own damage is gun, so solo the item does almost nothing for her.",
 "Duo (Victor): Silencer out, Spirit Rend in late (upgrade of Spirit Shredder, +1600). Spirit Rend adds up to 4 more stacks of -7% spirit resist from headshots (2s apart, 8s): with 4 stacks the target takes ~36% more from Victor. Same 12 slots; gun spike still at 4.8k (walk1).",
 "Duo (Victor): Phantom Strike swap removed (it replaced Silencer, which is gone; diving their back line leaves Victor's aura). Inhibitor now sells Lucky Shot.",
 "Rejected: Spirit Rend instead of Lucky Shot (Lucky Shot is ~+25% of her own gun, kept); Mystic Vulnerability on Haze (needs her spirit damage, she has almost none). Ricochet kept: split bullets carry the Shredder debuff onto more of the clump (untested, H-B2-1.3).",
 "Sandbox: duo_victor_haze_crossshred. No result files yet: untested, kept on kit numbers."]);}

// ---- Pair B2-2: Rem + Abrams (Scourge relay) ----
{const b=base('rem');
 rep(b,'Late · L-R','Heroic Aura',['Scourge','Self-cast it while napping on Abrams: it lands on him and lasts longer. Sell Opening Rounds for this.']);
 del(b,"I'm rich as fuck",'Scourge');
 dropBox(b,'Swap for Heroic Aura');dropBox(b,'3+ gun heroes on your team?');
 mk(b,'rem_duo_abrams',"Rizuhble's Tank Rider Rem",'Duo Rem for Abrams',[
 "Duo (Abrams): Scourge moved from the rich box into core, in Heroic Aura's place (Abrams is not a gun hero, so Heroic Aura and its Rescue Beam swap and the 3+ gun heroes reorder box are gone). Tag Along says self-casts and items target the ally while napping, and Tag Along T2 (pick 6) gives +35% item duration: Scourge on Abrams lasts 13.5s instead of 10s (cd 35, so 39% uptime instead of 29%), with a 10m aura dealing 2.3% + 0.0055 x spirit of max health per second to every enemy near him.",
 "Duo (Abrams): Divine Barrier (already core, 600 barrier) lands on him at +35% = 810 while napping. Nap window 5.5s, Scourge cast delay 0.25s: one button, 5s spare.",
 "Rejected: keeping Heroic Aura too (13th slot, does nothing for a spirit tank). Rejected moving Scourge before Divine Barrier: Divine Barrier is the cheaper save and Scourge damage grows with spirit (Boundless after).",
 "Sandbox: duo_rem_abrams_scourge (H-B2-2.1..2.4). No result files yet: untested, kept on kit numbers."]);}

{const b=base('abrams');
 rep(b,'Late · L-R','Scourge',['Spirit Burn','']);
 del(b,"I'm rich as fuck",'Spirit Burn');
 mk(b,'abrams_duo_rem',"Rizuhble's Backpack Abrams",'Duo Abrams for Rem',[
 "Duo (Rem): Scourge out, Spirit Burn in at the same spot (35.2k). Rem's Scourge lands on Abrams for 13.5s (his own lasts 10s); two Scourges on the same hero should refresh, not stack (H-B2-2.2), so his own copy is a wasted 6400. Spirit Burn moves up from the rich box: -70% healing on everyone Siphon Life hits plus its burn.",
 "Spirit Burn threshold (500 in 5s): checked with a7/sp.js at the buy point, see designs_batch2.json pair B2-2. Spikes unchanged: spirit 5.6k, health 9.6k (walk1).",
 "Sandbox: duo_rem_abrams_scourge. No result files yet: untested, kept on kit numbers."]);}

// ---- Pair B2-3: Seven + Holliday (cross shred, back line) ----
{const b=base('seven');
 ins(b,'Mid · L-R','Mystic Vulnerability',['Bullet Resist Shredder','For Holliday: your balls and storm keep it on all of them.']);
 const m=box(b,'Mid · L-R');const me=m[3].splice(idx(m,'Mystic Expansion'),1)[0];
 del(b,'Late · L-R',"Diviner's Kevlar");box(b,'Late · L-R')[3].unshift(me);
 mk(b,'seven_duo_holliday',"Rizuhble's Shred Storm Seven",'Duo Seven for Holliday',[
 "Duo (Holliday): Bullet Resist Shredder in after Mystic Vulnerability (16k). Lightning Ball, Static Charge, Power Surge chains (4 targets, 10m) and the 30m Storm Cloud are all spirit damage on many targets, so -10% bullet resist (8s) sits on most of their team: Holliday's gun does about +11% on all of them. Seven's damage is spirit, so solo the item does almost nothing for him.",
 "Duo (Holliday): Diviner's Kevlar out to keep 12 slots; Unstoppable still guards the ult. Mystic Expansion moved to the start of Late so no box holds more than 8 items (same buy order). Spikes unchanged: spirit 5.6k, health 12.8k (walk1).",
 "Rejected: Bullet Resist Shredder in place of Healbane (Healbane is 1600 of his 4.8k health spike; swapping it pushes the spike past 30k).",
 "Sandbox: duo_seven_holliday_crossshred (H-B2-3.1..3.3). No result files yet: untested, kept on kit numbers."]);}

{const b=base('holliday');
 rep(b,'Mid · L-R','Bullet Resist Shredder',['Spirit Shredder','For Seven: his storm hurts more on whoever you shoot.']);
 ins(b,'Late · L-R','Lucky Shot',['Spirit Rend','']);
 dropBox(b,'Swap for Bullet Resist Shredder');
 note(b,"I'm rich as fuck",'Crippling Headshot','Sell Spirit Rend for this.');
 mk(b,'holliday_duo_seven',"Rizuhble's Shred Shot Holliday",'Duo Holliday for Seven',[
 "Duo (Seven): Bullet Resist Shredder out, Spirit Shredder in at the same spot (both 1600). Seven's spirit AoE now keeps -10% bullet resist on her targets far more often than her own Powder Keg did; a second copy of the same debuff should refresh, not stack (H-B2-3.2). Spirit Shredder puts -8% spirit resist on whoever she shoots and gives her and Seven 10% spirit lifesteal against them.",
 "Duo (Seven): Spirit Rend in after Lucky Shot (upgrade, +1600). Her headshot build stacks its -7% spirit resist x4 (one headshot per 2s keeps it full): her focus target takes up to ~36% more from Seven's storm, balls and surge. Ballistic Enchantment swap removed (it replaced Bullet Resist Shredder). Crippling Headshot now sells Spirit Rend (same job, bigger: -16% bullet and spirit).",
 "Spikes: gun 4.8k still at 5.6k, health at 12k; her incidental 4.8k spirit spike (was 18.4k) no longer lands, spirit spend 4.8k -> 3.2k (Powder Keg/Crackshot a little weaker, accepted for a gun build).",
 "Sandbox: duo_seven_holliday_crossshred. No result files yet: untested, kept on kit numbers."]);}
