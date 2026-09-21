import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as tickets from './ticket.mjs';
const {ticketDetails,ticketSVG,profileName}=tickets;
const template=readFileSync(new URL('./assets/ticket.svg',import.meta.url),'utf8');
test('exact immutable-position tier boundaries',()=>{
 for(const [position,tier,discount,number] of [[1,'gold',10,'001'],[50,'gold',10,'050'],[51,'silver',5,'051'],[250,'silver',5,'250'],[251,'bronze',3,'251']]) {
 const t=ticketDetails(position);assert.equal(t.tier,tier);assert.equal(t.discount,discount);assert.equal(t.number,number);assert.ok(t.caption.includes(discount+'%'));
 }
 for(const n of [0,-1,NaN,1.5,Number.MAX_SAFE_INTEGER+1])assert.throws(()=>ticketDetails(n));
});
test('original template: full bounded multiline Unicode names, escaping, fallback and both maximum serials',()=>{
 const user={first_name:'Андрей <&"',last_name:"O'Neil Юникод"};
 assert.equal(profileName(user),`Андрей <&" O'Neil Юникод`);
 const svg=ticketSVG(template,51,user);
 assert.ok(svg.includes('Андрей &lt;&amp;&quot; O&apos;Neil Юникод'));assert.equal(svg.split('>051<').length,3);
 for(const c of ['А','Ж','W','Ω','é']) {
  const long={first_name:c.repeat(64),last_name:c.repeat(64)};
  const output=ticketSVG(template,1,long); // Always the ORIGINAL placeholder-bearing template.
  assert.ok(!output.includes('Андрей Андреев'));
  const node=output.match(/<text[^>]*id="ticket-name"[^>]*>(.*?)<\/text>/s);
  assert.ok(node,'name must be a measurable multiline layout');
  const lines=[...node[1].matchAll(/<tspan[^>]*>(.*?)<\/tspan>/g)].map(x=>x[1]);
  assert.ok(lines.length>=2 && lines.length<=3);
  assert.equal(lines.join(''),profileName(long));
  assert.ok([...node[1].matchAll(/y="(\d+)"/g)].every(m=>Number(m[1])<=743),'name baselines must clear inner border at y=750');
  assert.ok(Number(node[0].match(/font-size="([\d.]+)"/)[1])>=18);
 }
 const unsupported={first_name:'李 👩🏽‍💻',last_name:'𓀀'};
 assert.equal(tickets.ticketCaption(1,unsupported),ticketDetails(1).caption+'\nИмя: '+profileName(unsupported));
 const fallback=ticketSVG(template,1,unsupported);
 assert.ok(fallback.includes('Имя — в подписи'));assert.ok(!fallback.includes('👩'));
 const huge=ticketSVG(template,Number.MAX_SAFE_INTEGER,user);
 const serials=[...huge.matchAll(/<text[^>]*font-size="([\d.]+)"[^>]*>9007199254740991<\/text>/g)];
 assert.equal(serials.length,2);assert.ok(Number(serials[0][1])<30);assert.ok(Number(serials[1][1])<72);
});
