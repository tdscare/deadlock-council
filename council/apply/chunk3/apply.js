const fs=require('fs');const W='council/apply/chunk3/w/',O='council/apply/chunk3/out/';
const ld=id=>JSON.parse(fs.readFileSync(W+id+'.js'));
const boxes=b=>{const a=[];b.rows.forEach(r=>r.forEach(x=>a.push(x)));return a};
const find=(b,n)=>{for(const bx of boxes(b)){const i=bx[3].findIndex(x=>x[0]===n);if(i>=0)return [bx,i]}throw Error('no '+n)};
const take=(b,n)=>{const [bx,i]=find(b,n);return bx[3].splice(i,1)[0]};
const after=(b,ref,item)=>{const [bx,i]=find(b,ref);bx[3].splice(i+1,0,item)};
const before=(b,ref,item)=>{const [bx,i]=find(b,ref);bx[3].splice(i,0,item)};
const note=(b,n,t)=>{const [bx,i]=find(b,n);bx[3][i][1]=t};
const box=(b,t)=>boxes(b).find(x=>x[0]===t);
const addbox=(b,after_t,nb)=>{const ri=b.rows.findIndex(r=>r.some(x=>x[0]===after_t));b.rows.splice(ri+1,0,[nb])};
const ch=(b,l)=>{b.changes=b.changes||[];b.changes.push('Round 26 (cost): '+l)};
const save=b=>fs.writeFileSync(O+b.id+'.js',JSON.stringify(b,null,1));
let b,bx,i;
// abrams_melee
b=ld('abrams_melee');
let it=take(b,'Crushing Fists');after(b,"Hunter's Aura",it);
note(b,'Unstoppable','Sell Spirit Resilience for this.');
it=take(b,'Extra Health');before(b,'Colossus',it);
ch(b,"Crushing Fists moved after Hunter's Aura (it delayed the spirit 4.8k to 21.6k, now 16.8k); Unstoppable sells Spirit Resilience instead of Bullet Resist Shredder (kept the spirit 4.8k); Extra Health bought next to Colossus.");
save(b);
// holliday
b=ld('holliday');
b.name="Rizuhble's Long Shot Holliday";
const sw=box(b,'Swap for Bullet Resist Shredder');sw[0]='Swap for Sharpshooter';
sw[3][0][1]='Instead of Long Range, High-Velocity Rounds and Sharpshooter when your barrels keep hitting 2+ heroes. On Powder Keg.';
b.rows.forEach(r=>r.forEach(x=>{if(x[0]==='Counters'){x[1]='Get after Sharpshooter if needed. Ahead? Skip it until you\'re dying. Sell Stamina Mastery for it.'}}));
note(b,'Siphon Bullets','Sell Vampiric Burst for this.');
note(b,'Crippling Headshot','Sell Sharpshooter (or Ballistic Enchantment) for this.');
ch(b,"Ballistic Enchantment swap now replaces Long Range + High-Velocity Rounds + Sharpshooter (same gun colour, same cost) so the spirit 4.8k stays; counters sell Stamina Mastery instead of Rapid Recharge; Crippling Headshot sells Sharpshooter instead of Bullet Resist Shredder; Siphon Bullets sells Vampiric Burst so Stamina Mastery is free for the counters; renamed Long Shot Holliday.");
save(b);
// graves_tank
b=ld('graves_tank');
it=take(b,'Escalating Exposure');after(b,'Escalating Resilience',it);
ch(b,"Escalating Exposure moved after Escalating Resilience (tank defence first; spirit 6.4k/8k and gun 6.4k/8k land at 28.0k/23.2k, 4.8k spikes unchanged).");
save(b);
// drifter_spirit
b=ld('drifter_spirit');
b.name="Rizuhble's Cold Cuts Drifter";
it=take(b,'Fortitude');after(b,'Lifestrike',it);
it=take(b,'Superior Duration');
let m=box(b,'Mid · L-R');addbox(b,'Mid · L-R',['Mid · cont.','',false,[it]]);
ch(b,"Fortitude moved right after Lifestrike (Extra Health sat idle until the last buy; health 6.4k/8k now at 15.2k, 4.8k spikes unchanged); renamed Cold Cuts Drifter.");
save(b);
// calico_gun
b=ld('calico_gun');
b.name="Rizuhble's Nine Lives Calico";
take(b,'Melee Lifesteal');
after(b,'Point Blank',['Lifestrike','']);
b.rows.forEach(r=>r.forEach(x=>{if(x[0]==='Counters')x[1]=x[1].replace('Sell Melee Lifesteal for it','Sell Rapid Rounds for it')}));
note(b,'Crippling Headshot','Sell Close Quarters for this.');
ch(b,"Melee Lifesteal upgraded to Lifestrike after Point Blank (no extra slot, no longer a dead-end 800); counters sell Rapid Rounds and Crippling Headshot sells Close Quarters; renamed Nine Lives Calico.");
save(b);
// shiv
b=ld('shiv');
it=take(b,'Rapid Recharge');after(b,'Superior Cooldown',it);
it=take(b,'Healbane');
const mb=box(b,'Mid · cont.');mb[3].unshift(it);
ch(b,"Rapid Recharge moved up after Superior Cooldown (Extra Charge sat idle until the last buy; spirit 16k now at 24.0k); Healbane to Mid cont.");
save(b);
// shiv_gun
b=ld('shiv_gun');
note(b,'Crippling Headshot','Sell Berserker for this.');
ch(b,"Crippling Headshot sells Berserker instead of Bullet Resist Shredder (kept the spirit 4.8k).");
save(b);
// ivy
b=ld('ivy');
[bx,i]=find(b,'Monster Rounds');bx[3][i]=['Titanic Magazine',''];
note(b,'Cursed Relic','Sell Titanic Magazine for this, or Healbane if you took Rescue Beam.');note(b,'Refresher','Sell Siphon Bullets for this.');
ch(b,"Monster Rounds replaced by Titanic Magazine so the Rescue Beam swap keeps the gun at 4.8k (gun 4.8k now at 5.6k instead of 12.0k); Cursed Relic sells Titanic Magazine (Healbane if Rescue Beam was taken, so the gun stays at 4.8k); Refresher sells Siphon Bullets instead of Heroic Aura (kept gun 4.8k).");
save(b);
// ivy_carry
b=ld('ivy_carry');
it=take(b,'Headhunter');after(b,'Stamina Mastery',it);
it=take(b,'Intensifying Magazine');after(b,'Tesla Bullets',it);
take(b,'Extra Stamina');
ch(b,"Headhunter bought right after Stamina Mastery (was 23.2k); Intensifying Magazine moved into Early after Tesla Bullets instead of a fresh T2 at 20.8k; Extra Stamina folded into Stamina Mastery.");
save(b);
// drifter
b=ld('drifter');
it=take(b,'Lifestrike');after(b,'Bullet Lifesteal',it);
ch(b,"Lifestrike bought straight after Bullet Lifesteal (was 16.0k, now 12.0k).");
save(b);
// mokrill
b=ld('mokrill');
it=take(b,'Superior Duration');after(b,'Duration Extender',it);
const m1=box(b,'Mid · L-R'),m2=box(b,'Mid · cont.');
while(m1[3].length>8)m2[3].unshift(m1[3].pop());
ch(b,"Superior Duration bought straight after Duration Extender (it idled 21.6k souls).");
save(b);
