import widths from './assets/name-metrics.json' with {type:'json'};

export function ticketDetails(position) {
 if (!Number.isSafeInteger(position) || position < 1) throw new Error('position');
 const [tier,label,adjective,discount,color,grain,perf] = position <= 50
 ? ['gold','ЗОЛОТОЙ БИЛЕТ','золотой',10,'#d4ad58','#76613b','#75613c']
 : position <= 250 ? ['silver','СЕРЕБРЯНЫЙ БИЛЕТ','серебряный',5,'#bdc1c2','#676c70','#6b7073']
 : ['bronze','БРОНЗОВЫЙ БИЛЕТ','бронзовый',3,'#b68057','#694833','#684731'];
 const number=String(position).padStart(3,'0');
 return {tier,label,discount,number,color,grain,perf,caption:`Ваш ${adjective} билет №${number}. Скидка ${discount}% на обучающую программу по настройке агента-монтажёра. Когда откроется запись, напишу сюда.`};
}
export const xmlEscape = value => value.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
export function profileName(user) {
 return [user.first_name,user.last_name].filter(x=>typeof x==='string' && x.length).join(' ') || 'Участник';
}
export function ticketCaption(position,user) {
 return ticketDetails(position).caption+'\nИмя: '+profileName(user);
}
// Only scripts with verified simple horizontal layout are admitted to the image.
// Other scripts, missing glyphs and control/format characters use an explicit label;
// the unmodified identity is always preserved in the plain-text Telegram caption.
const imageSupported = name => Array.from(name).every(c =>
 widths[c.codePointAt(0)] !== undefined && !/[\p{C}\p{M}]/u.test(c) &&
 /[\x20-\x7E\p{Script=Latin}\p{Script=Greek}\p{Script=Cyrillic}\p{Number}\p{Punctuation}\p{Separator}]/u.test(c));
const width = text => Array.from(text).reduce((n,c)=>n+(widths[c.codePointAt(0)] ?? 1),0);
export function nameLayout(name) {
 if (!imageSupported(name)) return {lines:['Имя — в подписи'],size:30,fallback:true};
 for(let size=37;size>=18;size--) {
  const lines=[''];
  for(const c of name) {
   if(width(lines.at(-1)+c)*size>780) lines.push('');
   lines[lines.length-1]+=c;
  }
  if(lines.length<=3 && (lines.length===1 || size<=(lines.length===3?22:28))) return {lines,size,fallback:false};
 }
 return {lines:['Полное имя — в подписи'],size:30,fallback:true};
}
export function ticketSVG(template,position,user) {
 const t=ticketDetails(position),layout=nameLayout(profileName(user));
 const firstY=layout.lines.length===1?725:layout.lines.length===2?710:695;
 const nameNode=`<text id="ticket-name" font-family="Liberation Serif" font-weight="400" font-size="${layout.size}" text-anchor="middle" fill="#25251f" xml:space="preserve">${layout.lines.map((line,i)=>`<tspan x="805" y="${firstY+i*(layout.lines.length===3?24:30)}">${xmlEscape(line)}</tspan>`).join('')}</text>`;
 // Oswald digit advances are below 0.65em; allow extra bearing/rounding margin.
 const leftSize=Math.min(133,220/(t.number.length*0.65));
 const rightSize=Math.min(72,400/(t.number.length*0.65));
 return template.replaceAll('#d4ad58',t.color).replaceAll('#76613b',t.grain).replaceAll('#75613c',t.perf)
 .replace('ЗОЛОТОЙ БИЛЕТ',t.label)
 .replace(/<text[^>]*>Андрей Андреев<\/text>/,nameNode)
 .replace('font-size="133"',`font-size="${leftSize}"`)
 .replace('font-size="72"',`font-size="${rightSize}"`)
 .replaceAll('>001<','>'+t.number+'<');
}
