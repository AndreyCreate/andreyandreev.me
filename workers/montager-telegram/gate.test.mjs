import {test} from 'node:test';
import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import {readFileSync} from 'node:fs';
import {createWorker} from './worker.mjs';
const worker=createWorker(async()=>new Uint8Array([137,80,78,71]));
function fixture(){
 const sql=new DatabaseSync(':memory:');sql.exec(readFileSync(new URL('./schema.sql',import.meta.url),'utf8'));
 const DB={prepare(q){return {q,args:[],bind(...args){this.args=args;return this},async first(){return sql.prepare(q).get(...this.args)},async run(){return sql.prepare(q).run(...this.args)}}},async batch(ss){sql.exec('BEGIN');try{for(const s of ss)sql.prepare(s.q).run(...s.args);sql.exec('COMMIT')}catch(e){sql.exec('ROLLBACK');throw e}}};
 return {sql,env:{DB,WEBHOOK_SECRET:'test',BOT_TOKEN:'test',BOT_USERNAME:'test_bot'}};
}
const start=(id,text='/start montager_channel')=>({update_id:id,message:{from:{id:1001,is_bot:false},chat:{id:1001,type:'private'},text}});
const cb=(id,data='montager:program')=>({update_id:id,callback_query:{id:'test-query',data,from:{id:1001,is_bot:false},message:{message_id:10,from:{is_bot:true,username:'test_bot'},chat:{id:1001,type:'private'}}}});
test('failed gate delivery can retry as membership signup with exactly one followup',async()=>{
 const {sql,env}=fixture(),old=globalThis.fetch;let member=false,fail=true;const delivered=[];
 globalThis.fetch=async(url,opts)=>{
  if(url.endsWith('/getChatMember'))return Response.json({ok:true,result:{status:member?'member':'left'}});
  if(url.endsWith('/sendMessage')&&fail)return Response.json({ok:false});
  if(url.endsWith('/sendMessage')||url.endsWith('/sendPhoto'))delivered.push(url.split('/').at(-1));
  return Response.json({ok:true});
 };
 try {
  const u=start(101,'/start montager_site');
  assert.equal((await worker.fetch(req(u),env)).status,503);
  assert.equal(sql.prepare('SELECT count(*) n FROM queue').get().n,0);
  member=true;fail=false;
  assert.equal((await worker.fetch(req(u),env)).status,200);
  const row=sql.prepare('SELECT * FROM queue').get();
  assert.deepEqual(delivered,['sendPhoto','sendMessage']);
  assert.equal(sql.prepare('SELECT followup_required,sent FROM updates').get().followup_required,1);
  assert.equal(sql.prepare('SELECT sent FROM updates').get().sent,1);
  assert.equal((await worker.fetch(req(u),env)).status,200);
  assert.deepEqual(delivered,['sendPhoto','sendMessage']);
  assert.deepEqual(sql.prepare('SELECT * FROM queue').get(),row);
 }finally{globalThis.fetch=old;sql.close()}
});

for (const failed of ['sendPhoto','sendMessage']) for (const unverified of ['error','left']) {
 test(`pending ${failed} survives ${unverified} and concurrent member recovery`,async()=>{
  const {sql,env}=fixture(),old=globalThis.fetch,calls=[],delivered=[];
  let phase='failure';
  globalThis.fetch=async(url)=>{
   const method=url.split('/').at(-1);calls.push(method);
   if(method==='getChatMember') {
    if(phase==='unverified'&&unverified==='error')throw new Error('membership outage');
    return Response.json({ok:true,result:{status:phase==='unverified'?'left':'member'}});
   }
   if(method==='sendPhoto'||method==='sendMessage'){
    if(phase==='failure'&&method===failed)return Response.json({ok:false});
    delivered.push(method);
   }
   return Response.json({ok:true});
  };
  try {
   const u=cb(101,'montager:site');
   assert.equal((await worker.fetch(req(u),env)).status,503);
   const queue=sql.prepare('SELECT * FROM queue').get();
   const pending=sql.prepare('SELECT * FROM updates').get();
   assert.equal(pending.sent,0);assert.equal(pending.confirmation_sent,failed==='sendPhoto'?0:1);
   phase='unverified';const before=delivered.slice();
   for(let i=0;i<3;i++) {
    assert.equal((await worker.fetch(req(u),env)).status,503);
    assert.deepEqual(sql.prepare('SELECT * FROM updates').get(),pending,'unverified retry must preserve pending delivery and release lease');
   }
   assert.deepEqual(delivered,before,'no ticket, followup, or negative-prompt retry spam');
   assert.deepEqual(sql.prepare('SELECT * FROM queue').get(),queue);
   phase='recovery';
   const responses=await Promise.all(Array.from({length:15},()=>worker.fetch(req(u),env)));
   assert.ok(responses.some(r=>r.status===200));
   assert.deepEqual(delivered,['sendPhoto','sendMessage'],'one successful photo and followup despite concurrent retry');
   assert.deepEqual(sql.prepare('SELECT * FROM queue').all(),[queue]);
   const done=sql.prepare('SELECT * FROM updates').get();
   assert.equal(done.sent,1);assert.equal(done.confirmation_sent,1);assert.equal(done.lease,null);assert.equal(done.lease_until,0);
   const count=calls.length;
   assert.equal((await worker.fetch(req(u),env)).status,200);
   assert.equal(calls.length,count,'completed duplicate has zero provider effects');
  } finally {globalThis.fetch=old;sql.close()}
 });
}

const req=u=>new Request('https://test/telegram',{method:'POST',headers:{'X-Telegram-Bot-Api-Secret-Token':'test'},body:JSON.stringify(u)});
test('membership matrix: program never registers, site accepts only membership; API failure closed',async()=>{
 const old=globalThis.fetch;
 try {for(const member of [{status:'member'},{status:'creator'},{status:'administrator'},{status:'restricted',is_member:true},{status:'restricted',is_member:false},{status:'restricted',is_member:'true'},{status:'left'},{status:'kicked'},{status:'unknown'},null,'error','timeout']){
  const {sql,env}=fixture(),calls=[];
  const allowed=member&&(['member','creator','administrator'].includes(member.status)||(member.status==='restricted'&&member.is_member===true));
  globalThis.fetch=async(url,opts)=>{calls.push({method:url.split('/').at(-1),body:opts.body instanceof FormData?null:JSON.parse(opts.body)});if(url.endsWith('/getChatMember')){if(member==='timeout')throw new Error('timeout');return Response.json({ok:member!=='error',result:member})}return Response.json({ok:true})};
  for(const [id,text] of [[1,'/start montager_channel'],[2,'/start'],[3,'/start montager_reel']])assert.equal((await worker.fetch(req(start(id,text)),env)).status,200);
  assert.equal(calls.filter(c=>c.method==='getChatMember').length,0);
  assert.equal(sql.prepare('SELECT count(*) n FROM queue').get().n,0);
  assert.ok(calls.every(c=>!JSON.stringify(c.body).includes('andreyandreev.me')));
  assert.equal((await worker.fetch(req(cb(4)),env)).status,200);
  assert.equal(sql.prepare('SELECT count(*) n FROM queue').get().n,0);
  assert.equal(JSON.stringify(calls.at(-1).body).includes('https://andreyandreev.me/montager/'),!!allowed);
  assert.equal((await worker.fetch(req(start(5,'/start montager_site')),env)).status,200);
  assert.equal(sql.prepare('SELECT count(*) n FROM queue').get().n,allowed?1:0);
  assert.ok(calls.filter(c=>c.method==='getChatMember').every(c=>c.body.user_id===1001&&c.body.chat_id===-1004337647904));
  sql.close();
 }}finally{globalThis.fetch=old}
});
test('forged callbacks ignored; duplicate callbacks leased; retry membership and immutable position',async()=>{
 const {sql,env}=fixture(),old=globalThis.fetch;let status='left',sends=0;
 globalThis.fetch=async(url)=>{if(url.endsWith('/getChatMember'))return Response.json({ok:true,result:{status}});if(url.endsWith('/sendMessage')||url.endsWith('/sendPhoto'))sends++;return Response.json({ok:true})};
 try {
  const bad=[cb(1,'montager:site:1002'),cb(2),cb(3),cb(4),cb(5)];
  bad[1].callback_query.from.id=1002;bad[2].callback_query.message.chat.type='group';bad[3].callback_query.message.from.username='evil_bot';bad[4].callback_query.from.is_bot=true;
  for(const u of bad)assert.equal((await worker.fetch(req(u),env)).status,200);
  assert.equal(sends,0);assert.equal(sql.prepare('SELECT count(*) n FROM updates').get().n,0);
  await worker.fetch(req(start(10,'/start montager_site')),env);assert.equal(sends,1);
  status='member';await worker.fetch(req(start(10,'/start montager_site')),env);
  assert.equal(sql.prepare('SELECT count(*) n FROM queue').get().n,0,'replayed completed gate cannot register');
  await Promise.all(Array.from({length:15},()=>worker.fetch(req(cb(11,'montager:site')),env)));
  assert.equal(sql.prepare('SELECT count(*) n FROM queue').get().n,1);
  const original=sql.prepare('SELECT * FROM queue').get();
  await worker.fetch(req(cb(12,'montager:site')),env);assert.deepEqual(sql.prepare('SELECT * FROM queue').get(),original);
  const before=sends;await worker.fetch(req(cb(12,'montager:site')),env);assert.equal(sends,before);
  await Promise.all(Array.from({length:15},()=>worker.fetch(req(cb(13)),env)));
  assert.equal(sends,before+1,'one program send per concurrently delivered update');
  sql.exec('INSERT INTO updates(update_id,telegram_id,lease_until) VALUES(20,1001,unixepoch()+60)');
  assert.equal((await worker.fetch(req(cb(20)),env)).status,503);
  assert.deepEqual(sql.prepare('SELECT * FROM queue').get(),original);
 }finally{globalThis.fetch=old;sql.close()}
});
