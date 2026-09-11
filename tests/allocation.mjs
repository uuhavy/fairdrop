import assert from 'node:assert/strict';
import {allocate,initialCampaign} from '../lib/fairdrop.ts';
const entry=(id,score)=>({id,scores:[score,0,0]});
assert.deepEqual(allocate(initialCampaign.entries,1000,60),{'sample-1':529,'sample-2':471});
assert.deepEqual(allocate([],1000,60),{});
assert.deepEqual(allocate([entry('a',59)],1000,60),{});
assert.deepEqual(allocate([entry('b',60),entry('a',60),entry('c',60)],1000,60),{a:334,b:333,c:333});
for(let pool=1;pool<=100;pool++){const result=allocate([entry('a',70),entry('b',80),entry('c',90)],pool,60);assert.equal(Object.values(result).reduce((a,b)=>a+b,0),pool);}
assert.throws(()=>allocate([],1.5,60));
console.log('Allocation checks passed: threshold, tie break, empty, conservation, invalid pool.');
