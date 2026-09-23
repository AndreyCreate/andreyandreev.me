export const CHANNEL_ID = -1004337647904;
export async function telegram(env, method, body) {
  const response = await fetch('https://api.telegram.org/bot'+env.BOT_TOKEN+'/'+method, {
    method:'POST', headers:{'Content-Type':'application/json'},
    signal:AbortSignal.timeout(10000), body:JSON.stringify(body)
  });
  const result = await response.json();
  if (!response.ok || result.ok !== true) throw new Error('telegram');
  return result.result;
}
export async function membership(env, tid) {
  try {
    const member = await telegram(env,'getChatMember',{chat_id:CHANNEL_ID,user_id:tid});
    return ['creator','administrator','member'].includes(member?.status) ||
      (member?.status === 'restricted' && member.is_member === true);
  } catch (_) { return false; }
}
export async function gateReply(env, uid, tid, mode, verified) {
  const fresh = await env.DB.prepare('INSERT INTO updates(update_id,telegram_id) VALUES(?,?) ON CONFLICT(update_id) DO NOTHING RETURNING update_id').bind(uid,tid).first();
  const state = await env.DB.prepare('SELECT telegram_id,sent FROM updates WHERE update_id=?').bind(uid).first();
  if (state.telegram_id !== tid) return new Response('Conflict',{status:409});
  if (state.sent) return new Response('OK');
  const lease = crypto.randomUUID();
  const claimed = await env.DB.prepare('UPDATE updates SET lease=?,lease_until=unixepoch()+60 WHERE update_id=? AND sent=0 AND lease_until<=unixepoch() RETURNING update_id,confirmation_sent,followup_required').bind(lease,uid).first();
  if (!claimed) return new Response('Retry',{status:503});
  try {
    // A negative gate must not acknowledge an admitted, unfinished ticket.
    // Check under the lease: registration may have raced the initial insert.
    if (mode === 'site' && !verified && (!fresh || claimed.confirmation_sent || claimed.followup_required) &&
        await env.DB.prepare('SELECT position FROM queue WHERE telegram_id=?').bind(tid).first()) {
      await env.DB.prepare('UPDATE updates SET lease=NULL,lease_until=0 WHERE update_id=? AND lease=? AND sent=0').bind(uid,lease).run();
      return new Response('Retry',{status:503});
    }
    await telegram(env,'sendMessage',verified ? {
      chat_id:tid, text:'Подписка подтверждена. Здесь вы можете посмотреть программу обучения «Монтажёр» и записаться в список ожидания.',
      reply_markup:{inline_keyboard:[[{text:'Посмотреть программу',url:'https://andreyandreev.me/montager/'}]]}
    } : {
      chat_id:tid, text:'Подпишитесь на Telegram-канал «Андрей, бесишь!» — там я показываю примеры работы AI-агентов и результаты участников.\n\nПосле подписки нажмите «Я подписался». Бот проверит подписку '+(mode === 'site' ? 'и выдаст ваш билет в список ожидания.' : 'и откроет программу обучения «Монтажёр».')+'\n\nЕсли подписку не удалось подтвердить, попробуйте ещё раз.',
      reply_markup:{inline_keyboard:[[{text:'Открыть канал',url:'https://t.me/mbga_materials'}],[{text:'Я подписался',callback_data:'montager:'+mode}]]}
    });
    await env.DB.prepare('UPDATE updates SET sent=1,lease=NULL,lease_until=0 WHERE update_id=? AND lease=?').bind(uid,lease).run();
    return new Response('OK');
  } catch (_) {
    await env.DB.prepare('UPDATE updates SET lease=NULL,lease_until=0 WHERE update_id=? AND lease=? AND sent=0').bind(uid,lease).run();
    return new Response('Retry',{status:503});
  }
}
