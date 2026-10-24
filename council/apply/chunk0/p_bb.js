const L=require('./lib');
let b=L.load('bebop_bomb');
b.name="Rizuhble's Clingy Ex Bebop";
L.add(b,"Cost pass: renamed Clingy Ex Bebop (Mystic Expansion move skipped: it slips health 4.8k by 800 souls).");
L.save(b);
b=L.load('bebop_support');
const sw=L.find(b,'Knockdown');sw.item[0]='Spirit Rend';sw.item[1]='Instead of Heroic Aura when your team has no gun heroes.';
L.add(b,"Cost pass: Spirit Rend (gun) replaces Knockdown in the Heroic Aura swap so gun 4.8k holds.");
L.save(b);
