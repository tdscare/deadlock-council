// Shared hero stat loader (audit root-cause fix): spirit per level from game data, never a hardcoded 1.1.
const fs=require('fs'),path=require('path');
const V=fs.readFileSync(path.resolve(__dirname,'../../gt/repo/game/citadel/pak01_dir/scripts/heroes.vdata'),'utf8');
exports.spiritPerLevel=hk=>{const i=V.indexOf('\n\t'+hk+' = ');if(i<0)throw new Error('hero not in heroes.vdata: '+hk);
 let j=V.indexOf('\n\thero_',i+5);if(j<0)j=V.length;const m=V.slice(i,j).match(/MODIFIER_VALUE_TECH_POWER = ([0-9.]+)/);if(!m)throw new Error('no TECH_POWER for '+hk);return +m[1]};
