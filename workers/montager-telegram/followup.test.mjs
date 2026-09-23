import {test} from 'node:test';
import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import {readFileSync} from 'node:fs';
import {createWorker} from './worker.mjs';
const worker=createWorker(async()=>new Uint8Array([137,80,78,71]));
const text='Кейсы и примеры того, что можно делать с AI-агентами, я показываю в Telegram-канале «Андрей, бесишь!».\n\nПосмотрите, как это работает на практике: от задачи до готового результата.';
const button={inline_keyboard:[[{text:'Открыть канал',url:'https://t.me/mbga_materials'}]]};
function fixture(){
 const sql=new DatabaseSync(':memory:');sql.exec(readFileSync(new URL('./schema.sql',import.meta.url),'utf8'));
 const DB={prepare(q){return {q,args:[],bind(...args){this.args=args;return this},async first(){return sql.prepare(q).get(...this.args)},async run(){return sql.prepare(q).run(...this.args)}}},async batch(ss){sql.exec('BEGIN');try{for(const s of ss)sql.prepare(s.q).run(...s.args);sql.exec('COMMIT')}catch(e){sql.exec('ROLLBACK');throw e}}};
 return {sql,env:{DB,WEBHOOK_SECRET:'test',BOT_TOKEN:'test',BOT_USERNAME:'test_bot'}};
}
const req=(id=1)=>new Request('https://test/telegram',{method:'POST',headers:{'X-Telegram-Bot-Api-Secret-Token':'test'},body:JSON.stringify({update_id:id,message:{from:{id:1001,is_bot:false},chat:{id:1001,type:'private'},text:'/start montager_site'}})});
test('confirmation then exact channel message, retry resumes only followup, no existing-user backfill',async()=>{
 const {sql,env}=fixture(),old=globalThis.fetch,calls=[];let failFirst=true,failSecond=true;
 globalThis.fetch=async(url,opts)=>{if(url.endsWith('/getChatMember'))return Response.json({ok:true,result:{status:'member'}});const isPhoto=url.endsWith('/sendPhoto');assert.ok(isPhoto||url.endsWith('/sendMessage'));const body=isPhoto?{text:opts.body.get('caption')}:JSON.parse(opts.body);if(isPhoto){assert.equal(opts.body.get('photo').type,'image/png');assert.equal(opts.body.get('chat_id'),'1001')}calls.push(body);return Response.json({ok:isPhoto?!failFirst:!failSecond})};
 try{
  assert.equal((await worker.fetch(req(),env)).status,503);assert.equal(calls.length,1);assert.notEqual(calls[0].text,text);
  failFirst=false;
  assert.equal((await worker.fetch(req(),env)).status,503);assert.equal(calls.length,3);
  assert.equal(calls[1].text,'Ваш золотой билет №001. Скидка 10% на обучающую программу по настройке агента-монтажёра. Когда откроется запись, напишу сюда.\nИмя: Участник');
  assert.deepEqual(calls[2],{chat_id:1001,text,reply_markup:button});
  assert.equal(sql.prepare('SELECT sent FROM updates').get().sent,0);
  failSecond=false;
  assert.equal((await worker.fetch(req(),env)).status,200);assert.equal(calls.length,4);assert.deepEqual(calls[3],calls[2]);
  assert.equal((await worker.fetch(req(),env)).status,200);assert.equal(calls.length,4);
  assert.equal((await worker.fetch(req(2),env)).status,200);assert.equal(calls.length,5);assert.equal(calls[4].text,calls[0].text);
  assert.deepEqual({...sql.prepare('SELECT COUNT(*) n,MAX(position) p FROM queue').get()},{n:1,p:1});
 }finally{globalThis.fetch=old;sql.close()}
});
test('additive migration preserves legacy rows and defaults to no channel followup',()=>{
 const sql=new DatabaseSync(':memory:');
 sql.exec(`CREATE TABLE queue(position INTEGER PRIMARY KEY,telegram_id INTEGER UNIQUE,source TEXT,created_at INTEGER);CREATE TABLE updates(update_id INTEGER PRIMARY KEY,telegram_id INTEGER NOT NULL,sent INTEGER NOT NULL DEFAULT 0 CHECK(sent IN (0,1)),lease TEXT,lease_until INTEGER NOT NULL DEFAULT 0);INSERT INTO queue VALUES(7,1001,'site',123);INSERT INTO updates VALUES(1,1001,1,NULL,0),(2,1001,0,NULL,0);`);
 const before=sql.prepare('SELECT * FROM updates').all();
 sql.exec(readFileSync(new URL('./migrations/0002-channel-followup.sql',import.meta.url),'utf8'));
 assert.deepEqual(sql.prepare('SELECT update_id,telegram_id,sent,lease,lease_until FROM updates').all(),before);
 assert.ok(sql.prepare('SELECT * FROM updates').all().every(r=>r.confirmation_sent===0&&r.followup_required===0));
 assert.equal(sql.prepare('SELECT position FROM queue').get().position,7);
 assert.equal(sql.prepare('PRAGMA integrity_check').get().integrity_check,'ok');sql.close();
});
