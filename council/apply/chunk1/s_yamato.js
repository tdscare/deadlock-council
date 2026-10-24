const L=require('./lib');const b=L.load('yamato');
const [m,mi]=L.find(b,'Mystic Reverb'),[l,li]=L.find(b,'Boundless Spirit');
const rv=m[3][mi],bs=l[3][li];m[3][mi]=bs;l[3][li]=rv;
b.changes.push('Cost pass: Boundless Spirit and Mystic Reverb swapped so Reverb is bought with more spirit power behind it.');
L.save(b,'yamato');
