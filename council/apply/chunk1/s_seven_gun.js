const L=require('./lib');const b=L.load('seven_gun');
const e=L.take(b,"Enchanter's Emblem");L.after(b,'Cultist Sacrifice',e);
L.after(b,'Enduring Speed',['Improved Spirit','']);
b.changes.push("Cost pass: Enchanter's Emblem moved after Cultist Sacrifice (gun 4.8k lands earlier); Improved Spirit added in Mid after Enduring Speed so Boundless Spirit costs 1.6k less.");
L.save(b,'seven_gun');
