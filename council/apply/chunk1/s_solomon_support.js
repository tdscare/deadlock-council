const L=require('./lib');const b=L.load('solomon_support');
const sw=L.box(b,'Swap for Heroic Aura');sw[3]=[['Hollow Point','Instead of Heroic Aura when your team has no gun heroes.']];
const c=L.box(b,'Counters');c[3].push(['Knockdown',"Flyers keep getting away."]);
L.note(b,'Refresher',"Sell Enchanter's Emblem for this.");
b.changes.push("Cost pass: Heroic Aura swap is now Hollow Point (same gun colour and price, gun 4.8k kept); Knockdown moved to Counters; Refresher sells Enchanter's Emblem instead of Opening Rounds.");
L.save(b,'solomon_support');
