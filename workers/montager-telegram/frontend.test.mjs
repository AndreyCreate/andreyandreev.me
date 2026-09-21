import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const html=readFileSync(new URL('../../montager/index.html',import.meta.url),'utf8');
test('Telegram CTA attribution, honest count, no email or cached position',async()=>{
 assert.ok(!/montager_pos|montager-waitlist|type="email"|id="done"|is-done/.test(html));
 const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
 for(const [query,src] of [['','site'],['?src=ig','reel'],['?src=newsletter','other']]){
  const button={addEventListener(){}};const count={};
  const context={location:{search:query},URLSearchParams,Number,Error,window:{},document:{getElementById(id){return id==='telegram-signup'?button:count}},fetch:async()=>({ok:true,json:async()=>({count:0})})};
  vm.runInNewContext(script,context);await new Promise(resolve=>setImmediate(resolve));
  assert.equal(button.href,'https://t.me/reels_by_Andrey_bot?start=montager_'+src);
  assert.equal(count.textContent,'В Telegram-предзаписи: 0 человек');
  context.fetch=async()=>{throw Error('offline')};vm.runInNewContext(script,context);await new Promise(resolve=>setImmediate(resolve));
  assert.equal(count.textContent,'Не удалось загрузить число участников Telegram-предзаписи');
 }
});
