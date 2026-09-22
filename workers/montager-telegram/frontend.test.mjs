import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const html=readFileSync(new URL('../../montager/index.html',import.meta.url),'utf8');
const script=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]).find(s=>s.includes('function refreshCount'));
const flush=()=>new Promise(r=>setImmediate(r));
function harness(fetch,extra={}){
 const nodes=Object.fromEntries(['telegram-signup','count-text','ticket-status'].map(k=>[k,{addEventListener(){}}]));
 const tickets=['gold','silver','bronze'].map(tier=>({dataset:{tier},active:false,classList:{remove(){this.owner.active=false},toggle(_,v){this.owner.active=v}}}));tickets.forEach(t=>t.classList.owner=t);
 const timers=new Map(),events={};let seq=0;
 const context={location:{search:''},URLSearchParams,Number,Error,Promise,AbortController,fetch,
 setTimeout(fn){timers.set(++seq,fn);return seq},clearTimeout(id){timers.delete(id)},setInterval(fn){events.interval=fn},
 window:{addEventListener(k,fn){events[k]=fn}},document:{hidden:false,getElementById:k=>nodes[k],querySelectorAll:()=>tickets,addEventListener(k,fn){events[k]=fn}},...extra};
 vm.runInNewContext(script,context);
 return {context,nodes,tickets,events,timeout:()=>{for(const fn of [...timers.values()])fn()}};
}
const ok=count=>async()=>({ok:true,json:async()=>({count})});
test('attribution, real count and tier boundaries',async()=>{
 assert.ok(!/montager_pos|montager-waitlist|type="email"/.test(html));
 for(const [query,src] of [['','site'],['?src=ig','reel'],['?src=newsletter','other']]){
  const h=harness(ok(0),{location:{search:query}});await flush();assert.equal(h.nodes['telegram-signup'].href,'https://t.me/reels_by_Andrey_bot?start=montager_'+src);
 }
 for(const count of [0,49,50,249,250]){const h=harness(ok(count));await flush();assert.equal(h.nodes['count-text'].textContent,`В Telegram-предзаписи: ${count} человек`);assert.equal(h.tickets.find(t=>t.active).dataset.tier,count<50?'gold':count<250?'silver':'bronze')}
});
test('deadline terminates loading even when abort does not settle fetch; late result ignored',async()=>{
 let resolve;const h=harness(()=>new Promise(r=>resolve=r));await flush();h.timeout();await flush();assert.match(h.nodes['count-text'].textContent,/Не удалось/);resolve({ok:true,json:async()=>({count:7})});await flush();assert.match(h.nodes['count-text'].textContent,/Не удалось/);assert.ok(h.tickets.every(t=>!t.active));
});
test('missing AbortController does not prevent success or retry',async()=>{const h=harness(ok(7),{AbortController:undefined});await flush();assert.match(h.nodes['count-text'].textContent,/7 человек/)});
test('offline, HTTP, malformed data and hanging body clear stale tiers',async()=>{
 for(const bad of [()=>Promise.reject(Error('offline')),async()=>({ok:false}),ok(null),ok(-1),ok('7'),async()=>({ok:true,json:()=>new Promise(()=>{})})]){
  const h=harness(ok(7));await flush();assert.ok(h.tickets.some(t=>t.active));h.context.fetch=bad;h.events.interval();await flush();h.timeout();await flush();assert.match(h.nodes['count-text'].textContent,/Не удалось/);assert.ok(h.tickets.every(t=>!t.active));h.context.fetch=ok(50);h.events.pageshow({persisted:true});await flush();assert.equal(h.tickets.find(t=>t.active).dataset.tier,'silver');
 }
});
