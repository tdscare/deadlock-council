const fs=require('fs');const D='council/apply/chunk2/';
const src=fs.readFileSync('data.js','utf8');const B=new Function(src+';return B;')();
const R=JSON.parse(fs.readFileSync('council/evidence/names/renames.json'));
const core=bx=>/^(Early|Mid|Late)/.test(bx[0]);
const boxes=b=>b.rows.flat();
function find(b,n){for(const bx of boxes(b)){const i=bx[3].findIndex(x=>x[0]===n);if(i>=0)return {bx,i,it:bx[3][i]}}throw Error('no '+n+' in '+b.id)}
function mv(b,n,after,before){const cb=boxes(b).filter(core);const sizes=cb.map(x=>x[3].length);let seq=cb.flatMap(x=>x[3]);
 const i=seq.findIndex(x=>x[0]===n);if(i<0)throw Error('mv no '+n);const [it]=seq.splice(i,1);
 const j=seq.findIndex(x=>x[0]===(after||before));if(j<0)throw Error('mv anchor');seq.splice(after?j+1:j,0,it);
 let p=0;cb.forEach((x,k)=>{x[3]=seq.slice(p,p+sizes[k]);p+=sizes[k]})}
const note=(b,n,t)=>{find(b,n).it[1]=t};
const desc=(b,title,t)=>{const bx=boxes(b).find(x=>x[0]===title);if(!bx)throw Error('box '+title);bx[1]=t};
const rm=(b,n)=>{const f=find(b,n);f.bx[3].splice(f.i,1)};
const rep=(b,n,m)=>{const f=find(b,n);f.it[0]=m};
const E={
mcginnis_ult:b=>{mv(b,'Boundless Spirit','Unstoppable');return ['Boundless Spirit now right after Unstoppable (8.8k souls earlier); Lightning Scroll, Superior Duration, Greater Expansion follow.']},
paradox:b=>{mv(b,'Mystic Burst','Express Shot');return ['Mystic Burst bought together with Tankbuster instead of sitting alone; health 4.8k and the Express Shot spike land about 800 souls earlier.']},
paradox_bomb:b=>{mv(b,'Spirit Lifesteal','Duration Extender');
 note(b,'Focus Lens','Sell Warp Stone for this.');note(b,'Cheat Death','Sell Veil Walker for this.');
 return ['Spirit Lifesteal moved after Duration Extender so spirit 4.8k lands at 4.8k instead of 6.4k.','Focus Lens now sells Warp Stone and Cheat Death sells Veil Walker, so health never drops below 9,600.']},
apollo:b=>{note(b,'Ethereal Shift','Sell Torment Pulse for this.');note(b,'Echo Shard','On Flawless Advance. Sell Tankbuster for this.');
 return ['Ethereal Shift sells Torment Pulse (spirit for spirit) so it no longer cuts the 11.2k health tier; Echo Shard sells Tankbuster.']},
apollo_melee:b=>{mv(b,'Healing Booster','Lifestrike');return ['Healing Booster moved after Lifestrike: gun 4.8k now lands at 6.4k instead of 7.2k.']},
silver:b=>{note(b,'Phantom Strike','Sell Berserker for this.');return ['Phantom Strike sells Berserker instead of Slowing Hex, so spirit 4.8k is kept.']},
celeste:b=>{rep(b,"Restorative Locket","Enchanter's Emblem");note(b,'Boundless Spirit',"Sell Enchanter's Emblem for this.");rm(b,'Rapid Recharge');
 return ["Restorative Locket swapped for Enchanter's Emblem (same price and colour, adds spirit power).",'Removed Rapid Recharge from the T4-only rich box (it is a T3).']},
celeste_carry:b=>{desc(b,'Counters','Get after Fortitude if needed. Ahead? Skip it until you\'re dying. Sell Healing Booster for it.');return ['Counters sell Healing Booster instead of Kinetic Dash, which kept the gun 4.8k spike intact.']},
baba:b=>{note(b,'Healbane','Their healer keeps your target alive. Sell Reactive Barrier for this.');rm(b,'Spirit Rend');
 return ['Healbane sells Reactive Barrier (T2 for T2) so health 4.8k is kept.','Removed Spirit Rend from the T4-only rich box (it is a T3).']},
warden:b=>{desc(b,'Counters','Get after Enduring Speed if needed. Ahead? Skip it until you\'re dying. Sell Bullet Lifesteal for it.');return ['Counters sell Bullet Lifesteal instead of Fleetfoot, which held the gun 6.4k spike.']},
lash:b=>{mv(b,'Mystic Burst','Extra Spirit');note(b,'Cheat Death','Sell Warp Stone for this.');note(b,'Lightning Scroll','Sell Greater Expansion for this.');note(b,'Ethereal Shift','They burst you the second you land. Sell Cold Front for this.');
 return ['Mystic Burst bought after Extra Spirit (3rd item) so its threshold is met when you buy it.','Cheat Death sells Warp Stone and Lightning Scroll sells Greater Expansion, keeping the gun 4.8k spike.','Ethereal Shift sells Cold Front (spirit for spirit) so health 4.8k stays on time.']},
pocket:b=>{note(b,'Escalating Exposure','Sell Greater Expansion for this.');note(b,'Mystic Reverb','On Enchanter\'s Satchel. Sell Superior Duration for this.');
 return ['Escalating Exposure sells Greater Expansion and Mystic Reverb sells Superior Duration, keeping the gun 4.8k spike.']},
vyper:b=>{mv(b,'Boundless Spirit','Leech');desc(b,'Counters','Get after Spirit Lifesteal if needed. Ahead? Skip it until you\'re dying. Sell Bullet Lifesteal for it.');
 return ['Boundless Spirit moved to right after Leech (spirit 11.2k tier 25k souls earlier).','Counters sell Bullet Lifesteal instead of Cold Front, which held spirit 4.8k.']},
vyper_gun:b=>{desc(b,'Counters','Get after Stamina Mastery if needed. Ahead? Skip it until you\'re dying. Sell Spirit Shielding for it.');return ['Counters sell Spirit Shielding instead of Split Shot, so the Split Shot + Ricochet pairing and gun tiers are kept.']},
sinclair:b=>{
 const sw=boxes(b).find(x=>x[0]==='Swap for Hollow Point');const li=sw[3].findIndex(x=>x[0]==='Lifestrike');const [L]=sw[3].splice(li,1);
 L[1]='Instead of Alchemical Fire when you keep dying in long fights. Hexed rabbits are easy heavy melee hits.';
 for(const r of b.rows){const k=r.indexOf(sw);if(k>=0){r.splice(k+1,0,['Swap for Alchemical Fire','',true,[L]]);break}}
 desc(b,'Counters','Get after Fortitude if needed. Ahead? Skip it until you\'re dying. Sell Reactive Barrier for it.');
 mv(b,'Crushing Fists','Hollow Point'); 
 return ['Lifestrike swap now replaces Alchemical Fire (not Hollow Point) so the weapon 16k tier is kept.','Counters sell Reactive Barrier instead of Cultist Sacrifice, which held weapon 4.8k.','Crushing Fists moved before Arctic Blast (32.0k instead of 36.8k).']},
doorman_support:b=>{mv(b,'Rescue Beam','Trophy Collector');note(b,'Cheat Death','Sell Warp Stone for this.');
 return ['Rescue Beam moved to right after Trophy Collector (12.8k instead of 20.8k).','Cheat Death sells Warp Stone instead of Opening Rounds, keeping the gun 4.8k tier.']},
};
const ids=process.argv.slice(2);
for(const id of ids){const b=JSON.parse(JSON.stringify(B.find(x=>x.id===id)));
 const ch=E[id]?E[id](b):[];
 if(R[id])b.name=R[id].new, ch.unshift('Renamed from '+R[id].old.replace("Rizuhble's ",'')+'.');
 if(ch.length)b.changes=(b.changes||[]).concat(['Cost audit: '+ch.join(' ')]);
 fs.writeFileSync(D+'out/'+id+'.js',JSON.stringify(b,null,1));console.log('wrote',id,b.name)}
