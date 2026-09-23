import {readFileSync} from 'node:fs';
import assert from 'node:assert/strict';
const read=p=>readFileSync(new URL('../'+p,import.meta.url),'utf8');
const network=read('lib/network.ts');
assert.match(network,/id: 61997/);
assert.match(network,/https:\/\/studio-next\.genlayer\.com\/api/);
for(const p of ['app/api/campaign/route.ts','components/wallet-actions.tsx']){
 const s=read(p);assert.match(s,/chain:STUDIO_NEXT/);assert.doesNotMatch(s,/testnetBradbury|explorer-bradbury/);
}
assert.doesNotMatch(read('lib/live-campaign.ts'),/0xd46dF8|0xf6Bb13/);
assert.match(read('components/wallet-actions.tsx'),/base.submit\(q,t\)/);
console.log('Studio Next routing and quoted submission checks passed.');
