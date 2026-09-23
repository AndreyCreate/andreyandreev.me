import {ticketCaption} from './ticket.mjs';
import {telegram, membership, gateReply} from './gate.mjs';
const ORIGIN = 'https://andreyandreev.me';
const reply = (status, text) => new Response(text, {status});
export async function boundedJSON(request) {
  if (Number(request.headers.get('content-length')) > 16384) throw new Error('large');
  const reader = request.body?.getReader();
  if (!reader) throw new Error('json');
  let size = 0; const chunks = [];
  while (true) {
    const {done, value} = await reader.read(); if (done) break;
    size += value.byteLength;
    if (size > 16384) { await reader.cancel(); throw new Error('large'); }
    chunks.push(value);
  }
  const bytes = new Uint8Array(size); let offset = 0;
  for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
  return JSON.parse(new TextDecoder().decode(bytes));
}
export function createWorker(renderTicket) { return {
 async fetch(request, env) {
  const path = new URL(request.url).pathname;
  if (path === '/count' && request.method === 'GET') {
    const row = await env.DB.prepare('SELECT COUNT(*) AS count FROM queue').first();
    return Response.json({count: row.count}, {headers: {
      'Access-Control-Allow-Origin': ORIGIN, 'Vary':'Origin', 'Cache-Control':'no-store'
    }});
  }
  if (path !== '/telegram' || request.method !== 'POST') return reply(404, 'Not found');
  if (!env.WEBHOOK_SECRET || request.headers.get('X-Telegram-Bot-Api-Secret-Token') !== env.WEBHOOK_SECRET)
    return reply(401, 'Unauthorized');
  let update;
  try { update = await boundedJSON(request); }
  catch (e) { return reply(e.message === 'large' ? 413 : 400, 'Invalid body'); }
  const cb = update?.callback_query;
  const m = cb ? {chat:cb.message?.chat,from:cb.from} : update?.message;
  if (!Number.isSafeInteger(update?.update_id) || update.update_id < 0 ||
      !m || m.chat?.type !== 'private' || m.from?.is_bot !== false ||
      !Number.isSafeInteger(m.from?.id) || m.from.id <= 0 || m.from.id !== m.chat.id)
    return reply(200, 'Ignored');
  let mode, source = 'site';
  if (cb) {
    if (!['montager:program','montager:site'].includes(cb.data) ||
        typeof cb.id !== 'string' || cb.message?.from?.is_bot !== true ||
        cb.message.from.username?.toLowerCase() !== env.BOT_USERNAME.toLowerCase()) return reply(200,'Ignored');
    mode = cb.data === 'montager:site' ? 'site' : 'program';
  } else {
    const command = /^\/start(?:@([A-Za-z0-9_]+))?(?: (montager_(?:site|channel|reel|other)))?$/.exec(m.text || '');
    if (!command || (command[1] && command[1].toLowerCase() !== env.BOT_USERNAME.toLowerCase())) return reply(200,'Ignored');
    mode = command[2] === 'montager_site' ? 'site' : 'program';
  }
  const uid = update.update_id, tid = m.from.id;
  try {
    const previous = await env.DB.prepare('SELECT telegram_id,sent FROM updates WHERE update_id=?').bind(uid).first();
    if (previous && previous.telegram_id !== tid) return reply(409,'Conflict');
    if (previous?.sent) return reply(200,'OK');
    if (cb) {
      // An expired callback acknowledgement must not prevent a safe retry.
      try { await telegram(env,'answerCallbackQuery',{callback_query_id:cb.id}); } catch (_) {}
    }
    const verified = (cb || mode === 'site') ? await membership(env,tid) : false;
    if (mode === 'program' || !verified) return await gateReply(env,uid,tid,mode,verified);
    // Claim before registration: an in-flight gate delivery owns this update too.
    await env.DB.prepare('INSERT INTO updates(update_id,telegram_id) VALUES(?,?) ON CONFLICT(update_id) DO NOTHING').bind(uid,tid).run();
    const lease = crypto.randomUUID();
    const acquired = await env.DB.prepare(`UPDATE updates SET lease=?,lease_until=unixepoch()+60
      WHERE update_id=? AND telegram_id=? AND sent=0 AND lease_until<=unixepoch() RETURNING update_id`).bind(lease,uid,tid).first();
    if (!acquired) return reply(503,'Retry');
    // Preserve retry eligibility, including an unsent negative gate becoming signup.
    await env.DB.batch([
      env.DB.prepare(`UPDATE updates SET followup_required=1 WHERE update_id=? AND lease=?
        AND NOT EXISTS(SELECT 1 FROM queue WHERE telegram_id=?)`).bind(uid,lease,tid),
      env.DB.prepare(`INSERT INTO queue(position,telegram_id,source)
        SELECT COALESCE(MAX(position),0)+1,?,? FROM queue
        HAVING NOT EXISTS(SELECT 1 FROM queue WHERE telegram_id=?)
        AND EXISTS(SELECT 1 FROM updates WHERE update_id=? AND telegram_id=?)`).bind(tid,source,tid,uid,tid)
    ]);
    const state = await env.DB.prepare('SELECT telegram_id,sent FROM updates WHERE update_id=?').bind(uid).first();
    if (state.telegram_id !== tid) return reply(409,'Conflict');
    if (state.sent) return reply(200,'OK');
    const claimed = await env.DB.prepare(`SELECT update_id,confirmation_sent,followup_required FROM updates
      WHERE update_id=? AND lease=? AND sent=0`).bind(uid,lease).first();
    if (!claimed) return reply(503,'Retry');
    const row = await env.DB.prepare('SELECT position FROM queue WHERE telegram_id=?').bind(tid).first();
    try {
      const send = async (body) => {
        const response = await fetch('https://api.telegram.org/bot'+env.BOT_TOKEN+'/sendMessage', {
          method:'POST', headers:{'Content-Type':'application/json'}, signal:AbortSignal.timeout(10000),
          body:JSON.stringify({chat_id:tid,...body})
        });
        const result = await response.json();
        if (!response.ok || !result.ok) throw new Error('delivery');
      };
      if (!claimed.confirmation_sent) {
        const photo=await renderTicket(row.position,m.from);
        const form=new FormData();
        form.set('chat_id',String(tid));
        form.set('caption',ticketCaption(row.position,m.from));
        form.set('photo',new Blob([photo],{type:'image/png'}),'ticket.png');
        const response=await fetch('https://api.telegram.org/bot'+env.BOT_TOKEN+'/sendPhoto',{
          method:'POST',body:form,signal:AbortSignal.timeout(10000)
        });
        const result=await response.json();
        if (!response.ok || !result.ok) throw new Error('delivery');
        const saved = await env.DB.prepare(`UPDATE updates SET confirmation_sent=1
          WHERE update_id=? AND lease=? AND sent=0 RETURNING update_id`).bind(uid,lease).first();
        if (!saved) throw new Error('lease');
      }
      if (claimed.followup_required) {
        await send({
          text:'Кейсы и примеры того, что можно делать с AI-агентами, я показываю в Telegram-канале «Андрей, бесишь!».\n\nПосмотрите, как это работает на практике: от задачи до готового результата.',
          reply_markup:{inline_keyboard:[[{text:'Открыть канал',url:'https://t.me/mbga_materials'}]]}
        });
      }
      await env.DB.prepare('UPDATE updates SET sent=1,lease=NULL,lease_until=0 WHERE update_id=? AND lease=?').bind(uid,lease).run();
      return reply(200,'OK');
    } catch (_) {
      await env.DB.prepare('UPDATE updates SET lease=NULL,lease_until=0 WHERE update_id=? AND lease=? AND sent=0').bind(uid,lease).run();
      return reply(503,'Retry');
    }
  } catch (_) { return reply(503,'Retry'); }
 }
}; }
