"""Страница к эфиру Андрея с Димой Провоторовым 17.09.2026 (DM 7606): та же презентация, но живая —
рилсы играют с сайта, карусели листаются целиком, тексты постов раскрываются. CT DS v4. python3 build.py → index.html"""
import os, html
HERE = os.path.dirname(os.path.abspath(__file__))
DS = os.path.expanduser("~/workspace/design_system")

def post_text(path):
    t = open(os.path.join(DS, path), encoding="utf-8").read().strip().split("\n---")[0].strip()
    return "".join(f"<p>{html.escape(p.strip())}</p>" for p in t.split("\n\n") if p.strip())

def video(src, label, poster=None):
    poster = poster or src.replace(".mp4", ".jpg")
    return f'<figure class="vid"><video controls playsinline preload="metadata" poster="{poster}" src="{src}"></video><figcaption>{label}</figcaption></figure>'

def carousel(cid, items, caption):
    cells = "".join(
        (f'<div class="cell"><video muted loop playsinline preload="none" poster="{p}" data-src="{v}"></video></div>' if v else f'<div class="cell"><img loading="lazy" src="{p}" alt=""></div>')
        for p, v in items)
    return (f'<div class="car" id="{cid}"><div class="track">{cells}</div>'
            f'<div class="ctl"><button data-d="-1" aria-label="назад">←</button><span class="cnt">1 / {len(items)}</span><button data-d="1" aria-label="вперёд">→</button><em>{caption}</em></div></div>')

def tl(items):
    return '<div class="tl">' + "".join(f'<div class="ti {k}"><b>{t}</b><span>{x}</span></div>' for t, x, k in items) + '</div>'

hooks = carousel("c-hooks", [(f"img/hooks_{i}.jpg", None) for i in range(8)], "белл хукс · обложка + 7 цитат · листается")
sm = carousel("c-sm", [(f"img/sm_{i}.jpg", f"v/sm_{i}.mp4") for i in range(11)], "Смешарики · 11 анимированных слайдов · видео играет на активном")
cusk = carousel("c-cusk", [(f"img/cusk_{i}.jpg", None) for i in range(9)], "Рейчел Каск · обложка + 8 цитат")

PAGE = f"""<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Как я работаю с агентом — эфир 17.09</title><link rel="icon" href="/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{--ink:#111;--mut:#6b6b6b;--line:#e8e8e8;--blue:#BFDDFB;--bl:#2F80ED;--coral:#E8563F;--grey:#F5F5F5}}
*{{box-sizing:border-box;margin:0;padding:0}}html{{scroll-behavior:smooth}}body{{font-family:Inter,system-ui,sans-serif;color:var(--ink);background:#fff;line-height:1.5;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:1240px;margin:0 auto;padding:0 28px}}
nav{{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.93);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}}nav .wrap{{display:flex;gap:24px;padding-top:14px;padding-bottom:14px;overflow:auto;white-space:nowrap}}nav a{{color:var(--ink);text-decoration:none;font-size:15px;font-weight:500}}nav a span{{font-family:'JetBrains Mono',monospace;color:var(--coral);margin-right:6px}}
.kick{{font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--mut);text-transform:uppercase;letter-spacing:.04em}}.kick:before{{content:"✳ ";color:var(--coral)}}
h1{{font-weight:500;font-size:clamp(42px,7vw,92px);letter-spacing:-.04em;line-height:1.02;margin:18px 0 22px}}h2{{font-weight:500;font-size:clamp(30px,4.4vw,56px);letter-spacing:-.035em;line-height:1.06;margin:14px 0 26px}}h3{{font-weight:500;font-size:clamp(22px,2.6vw,32px);letter-spacing:-.02em;margin:0 0 12px}}
u{{text-decoration:none;box-shadow:inset 0 -.12em 0 var(--bl)}}.mono{{font-family:'JetBrains Mono',monospace}}
.lead{{font-size:clamp(18px,2vw,24px);color:#333;max-width:900px}}header{{padding:70px 0 46px}}section{{padding:70px 0;border-top:1px solid var(--line)}}
.acts{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:40px}}.acts a{{display:block;text-decoration:none;color:inherit;background:var(--grey);border-radius:22px;padding:24px}}.acts a.bl{{background:var(--blue)}}.acts i{{font-style:normal;font-family:'JetBrains Mono',monospace;color:var(--coral);font-size:14px}}.acts b{{display:block;font-size:28px;font-weight:500;letter-spacing:-.02em;margin:4px 0}}.acts span{{font-size:15.5px;color:#333}}
.grid{{display:grid;grid-template-columns:auto auto 1fr;gap:28px;align-items:start}}.grid.two{{grid-template-columns:auto 1fr}}.grid.wide{{grid-template-columns:minmax(0,520px) 1fr}}
.vid{{width:300px}}.vid video{{width:100%;aspect-ratio:9/16;border-radius:20px;background:#000;display:block}}.vid figcaption,.ctl em{{font-style:normal;font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--mut);text-transform:uppercase;letter-spacing:.03em;margin-top:10px;display:block}}
.txt p{{font-size:18px;margin-bottom:14px;color:#222}}.txt ul{{margin:4px 0 16px 22px}}.txt li{{font-size:17px;margin:7px 0;color:#222}}.big{{font-size:clamp(40px,5vw,68px);font-weight:500;letter-spacing:-.035em;line-height:1;margin-bottom:16px}}
.res{{background:var(--blue);border-radius:18px;padding:18px 20px;font-size:17.5px!important}}blockquote{{border-left:3px solid var(--coral);padding:2px 0 2px 16px;font-size:20px;margin:0 0 18px}}
.tl{{display:flex;flex-direction:column;gap:8px;margin-bottom:18px}}.ti{{display:grid;grid-template-columns:74px 1fr;gap:12px;align-items:baseline;background:var(--grey);border-radius:14px;padding:11px 15px}}.ti b{{font-family:'JetBrains Mono',monospace;font-weight:500;font-size:17px;color:var(--mut)}}.ti span{{font-size:16.5px}}.ti.ok{{background:#fff;border:1.5px solid var(--bl)}}.ti.ok b{{color:var(--bl)}}.tl.fin{{display:grid;grid-template-columns:repeat(3,1fr)}}
.car{{min-width:0}}.track{{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;border-radius:20px}}.track::-webkit-scrollbar{{display:none}}.cell{{flex:0 0 100%;scroll-snap-align:center}}.cell img,.cell video{{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:20px;display:block;border:1px solid var(--line);background:var(--grey)}}
.ctl{{display:flex;align-items:center;gap:12px;margin-top:12px;flex-wrap:wrap}}.ctl button{{width:44px;height:44px;border-radius:50%;border:1px solid var(--line);background:#fff;font-size:18px;cursor:pointer}}.ctl button:hover{{background:var(--blue)}}.cnt{{font-family:'JetBrains Mono',monospace;font-size:14px;min-width:60px;text-align:center}}.ctl em{{margin:0 0 0 6px}}
details{{margin-top:16px;border:1px solid var(--line);border-radius:16px;padding:14px 18px}}summary{{cursor:pointer;font-weight:500;font-size:16px}}details p{{font-size:16px;margin-top:12px;color:#222}}
.nums{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:20px}}.nums div{{background:var(--grey);border-radius:18px;padding:18px}}.nums .bl{{background:var(--blue)}}.nums b{{display:block;font-size:clamp(30px,3.6vw,52px);font-weight:500;letter-spacing:-.035em;line-height:1}}.nums span{{font-size:14.5px;color:#333;display:block;margin-top:8px}}
.cards{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}.c{{background:var(--grey);border-radius:20px;padding:22px}}.c.bl{{background:var(--blue);grid-column:1/3}}.c.dk{{background:#111;color:#fff}}.c.dk p{{color:#ddd}}.c i{{font-style:normal;font-family:'JetBrains Mono',monospace;font-size:13px;text-transform:uppercase;color:var(--coral);display:block;margin-bottom:8px}}.c p{{font-size:17px}}.c blockquote{{font-size:18.5px;margin:12px 0 0}}
.story{{width:300px}}.story img{{width:100%;border-radius:20px;display:block}}
footer{{padding:36px 0 70px;border-top:1px solid var(--line);font-size:13px;color:var(--mut)}}
@media(max-width:940px){{.grid,.grid.two,.grid.wide{{grid-template-columns:1fr}}.acts,.nums,.cards,.tl.fin{{grid-template-columns:1fr}}.c.bl{{grid-column:auto}}.vid,.story{{width:min(100%,360px)}}.pair{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}.pair .vid{{width:100%}}}}
</style></head><body>
<nav><div class="wrap"><a href="#reels"><span>01</span>Рилсы</a><a href="#content"><span>02</span>Контент</a><a href="#bots"><span>03</span>Боты</a><a href="#day"><span>04</span>Одно утро</a></div></nav>

<header><div class="wrap"><div class="kick">эфир · 17 сентября 2026 · Андрей Андреев × Дима Провоторов</div>
<h1>Как я работаю с агентом:<br><u>рилсы</u>, контент, боты</h1>
<p class="lead"><span class="mono">::</span> Без теории. Три акта, в каждом живой пример с часами: во сколько я написал и во сколько получил результат. Видео играют прямо здесь, карусели листаются целиком.</p>
<div class="acts"><a href="#reels"><i>01</i><b>Рилсы</b><span>разобрать чужой монтаж до склеек и собрать свой тем же рецептом</span></a><a class="bl" href="#content"><i>02</i><b>Контент</b><span>карусель и текст поста по одному сообщению</span></a><a href="#bots"><i>03</i><b>Боты</b><span>рутина, которая делается сама, и кнопка, без которой ничего не уходит</span></a></div></div></header>

<section id="reels"><div class="wrap"><div class="kick">акт 01 · рилсы</div><h2>Рилс Димы разобран <u>до склеек</u> и собран заново</h2>
<div class="grid"><div class="pair" style="display:contents">{video("v/dima_orig.mp4","оригинал Димы · «Антихрупкость»")}{video("v/dima_ours.mp4","наша сборка · версия 13")}</div>
<div class="txt"><div class="big">69 с · 7 склеек</div><p>16 сентября: «Дима выпустил этот рилз, сравни с нашим: звук, монтаж, цвет, эффекты, длительность».</p>
<ul><li>один статичный план, крупности сделаны кропом и работают как склейки</li><li>субтитры печатаются по словам, с курсором</li><li>врезки на имена: обложки книг и карточка «выступление на TED»</li><li>цвет не тронут: у Димы цветокора нет</li></ul>
<p class="res">Тринадцать версий за три дня → «отлично, фиксирую как скилл». Теперь это рецепт, который собирает рилс из сырого дубля.</p></div></div>
<h2 style="margin-top:70px">Рилс о том, <u>как сделан пост</u></h2>
<div class="grid two">{video("v/post13.mp4","«дизайнерский пост за 13 минут»")}
<div class="txt"><div class="big">49 269 просмотров</div><p>Столько собрал пост. Рилс показывает, как он сделан за 13 минут без дизайнера, и сам становится контентом.</p>
<ul><li>говорящая голова сверху, экран доказательств снизу: график, обложки, шаги процесса</li><li>паузы вырезаны, субтитры по словам</li><li>один ролик → три хука → по три версии на хук в пробные рилсы</li><li>через сутки агент сам снимает цифры: где пролистывают, какой хук держит</li></ul>
<p class="res">Монтаж перестал быть событием. Это конвейер: записал дубль → получил девять версий.</p></div></div></div></section>

<section id="content"><div class="wrap"><div class="kick">акт 02 · контент · сегодня утром</div><h2>Карусель по <u>одному сообщению</u></h2>
<div class="grid wide">{hooks}<div class="txt"><blockquote>«Берём 2, 3, 6, 7, 8, 9, 15. На обложку 5. Верстай»</blockquote>
{tl([("9:34","«Хукс, цитаты» — 17 цитат со страницами книги",""),("9:41","выбрал номера",""),("9:43","8 слайдов готовы","ok"),("9:59","текст поста, факты сверены по источникам","ok")])}
<p class="res">Одну цитату агент снял сам: на 60-й странице это оказались слова Терренса Рила, а не автора. Скорость без проверки фактов не нужна.</p>
<details><summary>Текст поста целиком</summary>{post_text("hooks_stutz_style/hooks_post_text.txt")}</details></div></div>

<h2 style="margin-top:70px">От голосового до <u>анимированной</u> карусели</h2>
<div class="grid wide">{sm}<div class="txt">{tl([("10:10","голосом: «взрослые цитаты из Смешариков, 20 штук»",""),("10:13","двадцать цитат с героями и сериями","ok"),("10:20","«давай анимировано», выбрал девять",""),("10:35","10 видео-слайдов с героями","ok"),("10:37","текст поста","ok"),("10:50","финальный слайд с кадрами из серии","ok")])}
<p class="res">Герои — официальные, с сайта сериала. Сгенерированных картинок в постах нет: запрет с 21 августа.</p>
<details><summary>Текст поста целиком</summary>{post_text("smeshariki_stutz_style/smeshariki_post_text.txt")}</details></div></div>

<h2 style="margin-top:70px">Тот же конвейер, <u>рекорд</u> серии</h2>
<div class="grid wide">{cusk}<div class="txt"><div class="nums"><div><b>97 117</b><span>охват за два дня</span></div><div class="bl"><b>5 190</b><span>лайков</span></div><div><b>476</b><span>комментариев</span></div></div>
<p>В том же формате карусель про Резерфорд собрала 7 873 охвата. Вёрстка одинаковая.</p>
<p class="res">Вывод: решает герой, а не дизайн. Агент нужен, чтобы быстро перебрать героев и цитаты из самих книг; выбор остаётся за автором. Сегодня утром я за пять минут отказался от двух героев и взял третьего.</p>
<details><summary>Текст поста целиком</summary>{post_text("cusk_stutz_style/cusk_post_text.txt")}</details></div></div></div></section>

<section id="bots"><div class="wrap"><div class="kick">акт 03 · боты · сегодня утром</div><h2>Рутина, которая делается <u>сама</u></h2>
<div class="grid two"><figure class="story"><img src="img/dimon.jpg" alt="Димон"><figcaption class="kick" style="margin-top:10px">10:49 попросил → 10:53 готово</figcaption></figure>
<div class="cards"><div class="c bl"><i>дон Андрео</i><p>Банк присылает платёж → агент пишет партнёру уведомление. В 10:58 попросил «как в „Крёстном отце“», в 11:01 партнёр получил:</p><blockquote>«Сегодня, в день, когда на счёт упало ··· ₽, семья помнит о тебе. Конверт лежит где обычно. Дон Андрео просил передать: это не бизнес, это личное».</blockquote></div>
<div class="c"><i>вахта обещаний</i><p>После созвона агент сам вытаскивает из записи, что человек обещал сделать, и в нужный день приносит готовое сообщение ему.</p></div>
<div class="c dk"><i>кнопка «Отправить»</i><p>Агент готовит сообщение от моего имени, но без моего нажатия не уходит ничего. Этот блок про доверие, остальные про скорость.</p></div></div></div></div></section>

<section id="day"><div class="wrap"><div class="kick">итог</div><h2>Одно утро, <u>17 сентября</u></h2>
<div class="tl fin">{"".join(f'<div class="ti {k}"><b>{t}</b><span>{x}</span></div>' for t,x,k in [("9:25","отказ от двух героев серии",""),("9:43","карусель белл хукс","ok"),("9:59","текст поста","ok"),("10:13","20 цитат Смешариков","ok"),("10:35","анимированная карусель","ok"),("10:53","сторис «Димон»","ok"),("11:01","дон Андрео ушёл партнёру","ok"),("13:37","старт разбора блога психолога",""),("14:53","разбор, сайт, лендинг, воронка","ok")])}</div>
<p class="lead" style="margin-top:34px"><span class="mono">::</span> Агент не заменяет вкус. Он убирает расстояние между «придумал» и «сделано». Что брать, что выбросить и когда нажать «Отправить», решаю я.</p></div></section>

<footer><div class="wrap">Рабочая страница к эфиру 17.09.2026. Время московское, по меткам сообщений; цифры постов — из статистики Instagram. Рилс «Антихрупкость» — Дмитрий Провоторов, @provotorov.</div></footer>
<script>
document.querySelectorAll('.car').forEach(function(car){{
  var tr=car.querySelector('.track'),cells=[].slice.call(tr.children),cnt=car.querySelector('.cnt'),cur=0;
  function act(i){{cur=Math.max(0,Math.min(cells.length-1,i));cnt.textContent=(cur+1)+' / '+cells.length;
    cells.forEach(function(c,k){{var v=c.querySelector('video');if(!v)return;if(k===cur){{if(!v.src)v.src=v.dataset.src;v.play().catch(function(){{}})}}else{{v.pause()}}}})}}
  car.querySelectorAll('button').forEach(function(b){{b.addEventListener('click',function(){{var i=cur+parseInt(b.dataset.d,10);i=Math.max(0,Math.min(cells.length-1,i));tr.scrollTo({{left:cells[i].offsetLeft-tr.offsetLeft,behavior:'smooth'}});act(i)}})}});
  var t;tr.addEventListener('scroll',function(){{clearTimeout(t);t=setTimeout(function(){{var w=cells[0].offsetWidth+14;act(Math.round(tr.scrollLeft/w))}},120)}});
  new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting)act(cur);else cells.forEach(function(c){{var v=c.querySelector('video');if(v)v.pause()}})}})}},{{threshold:.4}}).observe(car);
}});
document.querySelectorAll('.vid video').forEach(function(v){{v.addEventListener('play',function(){{document.querySelectorAll('.vid video').forEach(function(o){{if(o!==v)o.pause()}})}})}});
</script></body></html>"""
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(PAGE)
print("ok", len(PAGE) // 1024, "KB")
