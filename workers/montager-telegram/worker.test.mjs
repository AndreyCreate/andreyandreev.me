import {test} from 'node:test';
import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import {readFileSync} from 'node:fs';
import {createWorker} from './worker.mjs';
const worker=createWorker(async()=>new Uint8Array([137,80,78,71]));
function fixture(){
 const sql=new DatabaseSync(':memory:'); sql.exec(readFileSync(new URL('./schema.sql',import.meta.url),'utf8'));
 const DB={prepare(q){return {args:[],bind(...args){this.args=args;return this},async first(){return sql.prepare(q).get(...this.args)},async run(){return sql.prepare(q).run(...this.args)},q}},async batch(stmts){sql.exec('BEGIN');try{for(const s of stmts)sql.prepare(s.q).run(...s.args);sql.exec('COMMIT')}catch(e){sql.exec('ROLLBACK');throw e}}};
 return {sql,env:{DB,WEBHOOK_SECRET:'local-test',BOT_TOKEN:'local-test',BOT_USERNAME:'synthetic_bot'}};
}
const req=(id,tid=1001,extra={})=>new Request('https://test/telegram',{method:'POST',headers:{'X-Telegram-Bot-Api-Secret-Token':'local-test'},body:JSON.stringify({update_id:id,message:{from:{id:tid,is_bot:false},chat:{id:tid,type:'private'},text:'/start montager_site',...extra}})});
test('auth, bounds, invalid identities and no public writes',async()=>{
 const {env,sql}=fixture();
 assert.equal((await worker.fetch(new Request('https://test/telegram',{method:'POST',body:'{}'}),env)).status,401);
 assert.equal((await worker.fetch(new Request('https://test/telegram',{method:'POST',headers:{'X-Telegram-Bot-Api-Secret-Token':'local-test'},body:'x'.repeat(17000)}),env)).status,413);
 for(const extra of [{chat:{id:1002,type:'private'}},{chat:{id:1001,type:'group'}},{text:'/start@wrong_bot'},{text:'hello'},{from:{id:1001,is_bot:true}}])assert.equal((await worker.fetch(req(1,1001,extra),env)).status,200);
 assert.equal((await worker.fetch(new Request('https://test/signup',{method:'POST'}),env)).status,404);
 assert.equal(sql.prepare('SELECT COUNT(*) n FROM queue').get().n,0);
});
test('real SQLite concurrent unique signup, duplicate delivery, repeat start, failure retry',async()=>{
 const {env,sql}=fixture();let sends=0;const old=globalThis.fetch;
 globalThis.fetch=async(url)=>{if(url.endsWith('/getChatMember'))return Response.json({ok:true,result:{status:'member'}});sends++;return Response.json({ok:true})};
 try{
  const results=await Promise.all(Array.from({length:30},(_,i)=>worker.fetch(req(i,1001+i),env)));
  assert.ok(results.every(r=>r.status===200));
  assert.deepEqual({...sql.prepare('SELECT count(*) n,count(DISTINCT position) p,max(position) m FROM queue').get()},{n:30,p:30,m:30});
  await Promise.all(Array.from({length:20},()=>worker.fetch(req(31,1001),env)));
  assert.equal(sends,61);
  await worker.fetch(req(31,1001),env);assert.equal(sends,61);
  await worker.fetch(req(32,1001),env);assert.equal(sends,62);
  assert.equal(sql.prepare('SELECT position FROM queue WHERE telegram_id=1001').get().position,1);
  globalThis.fetch=async(url)=>url.endsWith('/getChatMember')?Response.json({ok:true,result:{status:'member'}}):Response.json({ok:false},{status:500});
  assert.equal((await worker.fetch(req(33,2001),env)).status,503);
  assert.equal(sql.prepare('SELECT sent FROM updates WHERE update_id=33').get().sent,0);
  globalThis.fetch=async()=>Response.json({ok:true,result:{status:'member'}});
  assert.equal((await worker.fetch(req(33,2001),env)).status,200);
  const response=await worker.fetch(new Request('https://test/count'),env);
  assert.deepEqual(await response.json(),{count:31});assert.equal(response.headers.get('access-control-allow-origin'),'https://andreyandreev.me');
 }finally{globalThis.fetch=old;sql.close()}
});
