const L=require('./lib');
let b=L.load('greytalon');
// Superior Cooldown before Indomitable
{const f=L.find(b,'Superior Cooldown');f.bx[3].splice(f.i,1);const t=L.box(b,'Late · L-R');const j=t[3].findIndex(x=>x[0]==='Indomitable');t[3].splice(j,0,f.item);}
L.note(b,'Refresher','Sell Stamina Mastery for this.');
L.add(b,"Cost pass: Superior Cooldown bought before Indomitable; Refresher sells Stamina Mastery instead of Sharpshooter (gun 4.8k holds).");
L.save(b);
b=L.load('greytalon_gun');
b.name="Rizuhble's Bow Optional Grey Talon";
L.add(b,"Cost pass: renamed Bow Optional Grey Talon; no item changes needed.");
L.save(b);
b=L.load('infernus');
b.name="Rizuhble's Slow Roast Infernus";
L.move(b,'Toxic Bullets','Early · L-R','Extended Magazine');
L.add(b,"Cost pass: renamed Slow Roast Infernus; Toxic Bullets right after Extended Magazine so gun 4.8k lands at 9.6k souls instead of 15.2k.");
L.cleanRows(b);L.save(b);
b=L.load('infernus_dash');
b.name="Rizuhble's Dine And Dash Infernus";
L.move(b,'Spiritual Overflow','Mid · L-R','Superior Duration');
L.add(b,"Cost pass: renamed Dine And Dash Infernus; Spiritual Overflow before Escalating Exposure so gun 4.8k lands at 24.0k instead of 51.2k.");
L.cleanRows(b);L.save(b);
