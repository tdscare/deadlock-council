const L=require('./lib');
let b=L.load('rem');
{const f=L.find(b,'Superior Duration');f.bx[3].splice(f.i,1);}
L.note(b,'Heroic Aura','Only if your team has gun heroes.');
L.move(b,'Trophy Collector','Mid · L-R','Compress Cooldown');
L.move(b,'Echo Shard','Mid · L-R','Healing Booster');
const sw=L.find(b,'Rescue Beam');sw.item[0]='Spirit Rend';sw.item[1]='Instead of Heroic Aura when your team has no gun heroes.';
L.add(b,"Cost pass: Opening Rounds kept (Heroic Aura no longer sells it) and Superior Duration dropped from core, so gun 4.8k lands at 34.4k; Echo Shard moved after Healing Booster; Trophy Collector right after Compress Cooldown; Spirit Rend (gun) replaces Rescue Beam in the Heroic Aura swap.");
L.save(b);
