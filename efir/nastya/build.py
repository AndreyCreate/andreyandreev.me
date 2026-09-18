"""Страница к эфиру Андрея с Настей Фокиной 18.09.2026 12:00 МСК (DM 7657, лум Насти 2:46–3:47):
что внутри AI-маркетолога, кейс рилсов, кейс каруселей с трафиком, участницы-нетехнари.
Визуальный язык и JS — efir/v2 (Hey Sash). Ассеты: ../img, ../v. python3 build.py → index.html"""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
V2 = open(os.path.join(HERE, "..", "v2", "index.html"), encoding="utf-8").read()
CSS = re.search(r"<style>(.*?)</style>", V2, re.S).group(1)
JS = re.findall(r"<script>(.*?)</script>", V2, re.S)[-1]
CSS += """
.chain{display:grid;gap:8px}.chain div{display:grid;grid-template-columns:34px 1fr;gap:12px;align-items:baseline;background:#2b2b2b;border-radius:10px;padding:12px 14px}.chain b{font-family:'JetBrains Mono',monospace;font-weight:400;color:#8cc4ff;font-size:13px}.chain span{font-size:15.5px;color:#eee}.chain small{display:block;font-family:'JetBrains Mono',monospace;font-size:12px;color:#aaa;margin-top:2px}
.bk ul{margin:6px 0 0 16px}.bk li{font-family:'JetBrains Mono',monospace;font-size:13px;line-height:1.5;color:#eee;margin:3px 0}
.q{background:#2b2b2b;padding:22px;position:relative}.q .who{font-family:'JetBrains Mono',monospace;font-size:12.5px;color:#8cc4ff;text-transform:uppercase;letter-spacing:.03em}.q .who b{display:block;color:#fff;font-size:15px;text-transform:none;letter-spacing:0;margin-bottom:2px;font-weight:500}.q p{font-size:17px;line-height:1.4;margin-top:12px;color:#fff}.q p+p{margin-top:8px;color:#ddd;font-size:15.5px}
.tbl{border-top:1px solid var(--line)}.tbl div{display:grid;grid-template-columns:1fr 110px 90px 90px;gap:12px;padding:12px 0;border-bottom:1px solid var(--line);font-size:15.5px;align-items:baseline}.tbl div b{font-family:'JetBrains Mono',monospace;font-weight:400;font-size:14px;text-align:right}.tbl div.h b,.tbl div.h span{font-family:'JetBrains Mono',monospace;font-size:11.5px;color:var(--mut);text-transform:uppercase}
.cs img{width:64px;height:64px;border-radius:50%;object-fit:cover;display:block;margin-bottom:14px;border:2px solid #444}.cs i{width:64px;height:64px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#3a3a3a;color:#ccc;font-style:normal;font-family:'JetBrains Mono',monospace;font-size:13px;margin-bottom:14px}
.cases{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:26px}.cs{background:#2b2b2b;padding:18px}.cs b{display:block;font-size:26px;font-weight:400;letter-spacing:-.03em;line-height:1.05}.cs span{display:block;font-family:'JetBrains Mono',monospace;font-size:12px;color:#ccc;margin-top:8px;line-height:1.5}
section:not(.dark) .bk{background:var(--grey)}section:not(.dark) .bk span{border-color:var(--ink)}section:not(.dark) .bn,section:not(.dark) .bk p,section:not(.dark) .bk li{color:var(--ink)}section:not(.dark) .bk .cap{color:var(--bl)}
.m0{right:auto;left:29vw;top:.45em}.nums.sm b{font-size:clamp(26px,2.6vw,40px)}.dark .nums span{color:#bbb}.dark .nums,.dark .nums div+div{border-color:#444}
.bks.big .bk{min-height:0;padding:30px 28px 34px}.cv{width:100%;max-width:560px;aspect-ratio:560/760;border-radius:14px;background:#1b1b1b;display:block;margin-top:22px}.bks.big .bk h3{font-size:clamp(30px,3.2vw,44px);margin:12px 0 10px}.bks.big .bk .cap{font-size:13px}.bks.big .bk p{font-family:Inter,system-ui,sans-serif;font-size:19px;line-height:1.4}
.flow{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-top:28px;font-family:'JetBrains Mono',monospace;font-size:14px}.flow span{background:#2b2b2b;border-radius:99px;padding:12px 18px}.flow i{font-style:normal;color:#8cc4ff}
.rt{border-top:1px solid #444;columns:2;column-gap:40px;margin-top:26px}.rt div{display:grid;grid-template-columns:1fr 44px 1.15fr;gap:12px;padding:9px 0;border-bottom:1px solid #3a3a3a;font-size:15px;break-inside:avoid}.rt div b{font-family:'JetBrains Mono',monospace;font-weight:400;font-size:12.5px;color:#8cc4ff}.rt div em{font-style:normal;color:#ccc}.rt div.h span,.rt div.h b,.rt div.h em{font-family:'JetBrains Mono',monospace;font-size:11px;color:#888;text-transform:uppercase}.rt div.it em:after{content:' · из IT';color:#F0695F}
.prog{display:grid;grid-template-columns:1.35fr 1fr;gap:40px;margin-top:34px;align-items:start}.pb{border-top:2px solid var(--ink);padding-top:18px}.pb .bn{font-family:'JetBrains Mono',monospace;font-size:12.5px;color:var(--bl);text-transform:uppercase;letter-spacing:.03em}.pb h3{font-size:clamp(30px,3.2vw,44px);font-weight:400;letter-spacing:-.03em;margin:10px 0 6px}.pb .cap{font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--mut);margin-bottom:14px}.ls div{display:grid;grid-template-columns:40px 1fr;gap:10px;padding:11px 0;border-bottom:1px solid var(--line);font-size:16.5px;line-height:1.35;align-items:baseline}.ls div b{font-family:'JetBrains Mono',monospace;font-weight:400;font-size:13px;color:var(--bl)}.ls div.x{color:var(--mut)}.ls div.x b{color:var(--mut)}
.ig{display:inline-flex;align-items:center;gap:6px;font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--bl);text-decoration:none;border:1px solid currentColor;border-radius:99px;padding:7px 14px;margin:12px 8px 0 0;white-space:nowrap}.ig:hover{background:var(--bl);color:#fff}.dark .ig{color:#8cc4ff}.dark .ig:hover{background:#8cc4ff;color:#111}.ig+blockquote,.ig+.rows{margin-top:24px}.tbl div span a{color:inherit;text-decoration:underline;text-decoration-color:var(--bl);text-underline-offset:4px}.nums span a,figcaption a{color:var(--bl)}.dark .nums span a{color:#8cc4ff}
@media(max-width:980px){.prog{grid-template-columns:1fr;gap:48px}}
@media(max-width:980px){.rt{columns:1}.cases{grid-template-columns:1fr 1fr}.tbl div{grid-template-columns:1fr 90px 70px 70px;font-size:14px}}
"""

def video(src, label, poster=None):
    poster = poster or src.replace(".mp4", ".jpg")
    return (f'<figure class="vid"><video controls playsinline preload="metadata" poster="{poster}" src="{src}"></video>'
            f'<figcaption>{label}</figcaption></figure>')

def carousel(cid, items, caption):
    cells = "".join(f'<div class="cell"><img loading="lazy" src="{p}" alt=""></div>' for p in items)
    return (f'<div class="car" id="{cid}"><div class="track">{cells}</div>'
            f'<div class="ctl"><button data-d="-1" aria-label="назад">←</button><span class="cnt">1 / {len(items)}</span>'
            f'<button data-d="1" aria-label="вперёд">→</button><em>{caption}</em></div></div>')

def rows(items):
    return '<div class="rows">' + "".join(f'<div class="rw {k}"><b>{t}</b><span>{x}</span></div>' for t, x, k in items) + "</div>"

def bk(n, title, cap, body):
    return (f'<div class="bk"><span class="c1"></span><span class="c2"></span><span class="c3"></span><span class="c4"></span>'
            f'<div class="bn">▢ {n}</div><h3>{title}</h3><div class="cap">{cap}</div>{body}</div>')

ROSTER = [
 ("1","Галина Фёдорова","трансперсональный психолог",0),("1","Наталья Мальцева","обучает коучей и психологов продажам",0),("1","Таня Меламори","ментор, сооснователь ProstoMeditation, ex-Google",1),("1","Виктория Индюкова","эксперт по травмам и отношениям",0),("1","Михаил Тесленко","финансовый консалтинг на маркетплейсах",0),("1","Настя Шадрина","психолог",0),("1","Нелли Чернова","обучение и индивидуальные консультации",0),("1","Татьяна Новикова","кофаундер документ-сервиса",1),
 ("2","Инга Маккарти","блог о жизни и доброте",0),("2","Снежана Будько","PCC-коуч, mindfulness, дыхательные практики",0),("2","Виктория Шевчук","клуб по методу Фельденкрайза",0),("2","Виктория Лопатина","—",0),("2","Елена Губернаторова","коучинг денежного мышления",0),("2","Илья","AI-автоматизация контента",1),("2","Ольга Павленко","бизнес-коуч, «Деньги в голове»",0),("2","Ольга Фёдорова","психолог, расстановщик",0),("2","Ярослав Капустинский","ритриты, фотограф, предприниматель",0),
 ("3","Екатерина Сёренсен","executive-коуч",0),("3","Женя Нечитайленко","маркетинг и деньги",0),("3","Олеся","нутрициолог, натуропат",0),("3","Софья Преображенская","психолог",0),
 ("4","Ирина Пестова","эмбодимент-фасилитатор",0),("4","Ирина Сорокина","—",0),("4","Катя Кеннеди","—",0),("4","Мария","личный бренд, коучинг",0),("4","Элина Гелашвили","event-продюсер",0),("4","Юлия Морозова","карьерный ментор",0),
 ("5","Анастасия Гречановская","ивент-бизнес, караоке-игры",0),("5","Даша Морозова","маркетолог, ex-Яндекс",0),("5","Ирина Решетова","туристическая компания",0),("5","Маша Адушкина","психолог, гештальт-терапевт",0),("5","Ольга Георгиевская","недвижимость в Дубае",0),("5","Таисия Крохмаль","клинический психолог",0),("5","Юлия Оздемир","биодинамика, мастер рэйки",0),
 ("6","Екатерина Павлова","—",0),("6","Екатерина Рязанова","фотограф",0),("6","Лида","магазин тканей, 13 лет в бизнесе",0),
]
def roster_table():
    rows_ = "".join(f'<div{" class=it" if it else ""}><span>{n}</span><b>П{p}</b><em>{w}</em></div>' for p,n,w,it in ROSTER)
    return f'<div class="rt"><div class="h"><span>участница / участник</span><b>поток</b><em>чем занимается</em></div>{rows_}</div>'

def agent_card(n, title, cap, text, vid):
    return (f'<div class="bk ag"><span class="c1"></span><span class="c2"></span><span class="c3"></span><span class="c4"></span>'
            f'<div class="bt"><div class="bn">▢ {n}</div><h3>{title}</h3><div class="cap">{cap}</div><p>{text}</p>'
            f'<div class="cap" style="margin-top:18px;color:#aaa">переписка 17 сентября, как есть</div></div>'
            f'<video class="cv" autoplay muted loop playsinline preload="metadata" poster="{vid.replace(".mp4", ".jpg")}" src="{vid}"></video></div>')

def nums(items, cls=""):
    return f'<div class="nums {cls}">' + "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in items) + "</div>"

CONTENT = ["Введение: что будем делать и к чему должны прийти","Создаём AI-агента на базе Claude Code","Как собирать референсы в Pinterest","Дизайн-система для контента","Первые шаги в дизайне постов и нужные скиллы","Теория контента: ожидания, рубрики, эксперименты","Где брать темы. Исследование аудитории","Как работать с информацией. Notion","Как скопировать любой tone of voice","Секреты сторителлинга в текстах","Как создавать посты в Claude и в AI-агенте","Продвинутый агент, часть 1: подключаем ко всем чатам Телеграма","Продвинутый агент, часть 2: группа с темами в Телеграме"]
SALES = ["Введение: что будем делать и к чему должны прийти","Настраиваем агента-маркетолога","Разбираем свои текущие продукты","Продуктовая матрица: какой продукт следующий и почему","Мини-продукт и лид-магнит: когда нужны и как собрать"]
def lessons(n, title, cap, items, extra=None):
    body = "".join(f"<div><b>{i:02d}</b><span>{t}</span></div>" for i, t in enumerate(items, 1))
    if extra: body += f'<div class="x"><b>+</b><span>{extra}</span></div>'
    return f'<div class="pb"><div class="bn">▢ {n}</div><h3>{title}</h3><div class="cap">{cap}</div><div class="ls">{body}</div></div>'

def ig(code, label="открыть в Instagram", kind="p"):
    return f'<a class="ig" href="https://www.instagram.com/{kind}/{code}/" target="_blank" rel="noopener">{label} ↗</a>'

cusk = carousel("c-cusk", [f"../img/cusk_{i}.jpg" for i in range(9)], "Рейчел Каск · обложка + 8 цитат · 5 сентября")
dasha = carousel("c-dasha", [f"../img/dasha_puma_0{i}.jpg" for i in (1, 2, 3, 4, 7, 8)] + [f"../img/dasha_fomo_0{i}.jpg" for i in range(1, 8)],
                 "Даша Морозова · PUMA (3 сентября) и «ФОМО возможностей» (7 сентября)")

PAGE = f"""<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>AI-маркетолог изнутри — эфир 18.09</title><link rel="icon" href="/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="wrap"><div class="top"><div class="me"><i></i><span>Прямой эфир<br>Андреев × Фокина</span></div><div class="sp"></div><a class="pill" href="#inside">Внутри ➤</a><a class="pill" href="#carousels">Посты и карусели ➤</a><a class="pill" href="#reels">Рилсы и монтаж ➤</a><a class="pill" href="#people">Участницы ➤</a><a class="pill cta" href="#program">Программа</a></div>
<div class="hero"><div class="hgrid"><div><h1>hey, <u>маркетолог!</u><span class="m m0">+4 838<br>за 30 дней</span></h1></div>
<div class="meta"><div><b>когда</b><span>18 сентября 2026, 12:00 МСК<br>/ прямой эфир</span></div><div><b>формат</b><span>что внутри, два кейса с цифрами,<br>участницы и живое демо</span></div></div></div>
<div class="fl"><div class="pc a"><img src="../img/cusk_0.jpg" alt=""></div><div class="pc b"><img src="../img/dasha_puma_01.jpg" alt=""></div><span class="m m1">охват 140 694</span>
<p class="lead">Что внутри AI-маркетолога, сколько трафика дают рилсы и карусели, и кто из участниц уже делает это сам. Все цифры по моему аккаунту — из статистики Instagram на 17 сентября.</p>
<div class="pc c"><img src="../img/dasha_fomo_01.jpg" alt=""></div><div class="pc d"><img src="../v/post13.jpg" alt=""></div><span class="m m2">▶ 49 269</span><span class="m m3">1 ч 10 мин</span></div></div></div><div class="band"></div>

<section id="inside" class="dark"><div class="wrap"><div class="lab">Акт 01 · что внутри</div><h2>Два AI-агента <u>в Телеграме</u></h2>
<div class="bks big">{agent_card("Агент 01", "Контентный", "посты · карусели · рилсы", "Пишет и собирает контент моим голосом и в моей дизайн-системе. Рилс монтирует сам.", "../v/chat_tony.mp4")}
{agent_card("Агент 02", "Продающий", "офферы · воронки · лендинги", "Знает продукты, цены и аудиторию. Пишет прогревы, собирает воронку и лендинг.", "../v/chat_kobi.mp4")}</div>
<div class="flow"><span>голосовое в Телеграме</span><i>→</i><span>агент работает на сервере</span><i>→</i><span>пост, рилс, воронка, лендинг</span></div></div></section>

<section id="carousels"><div class="wrap"><div class="lab">Акт 02 · кейсы · посты и карусели</div><h2>Карусель по одному сообщению, <u>140 тысяч охвата</u></h2>
<div class="grid wide">{cusk}<div><div class="price">140 694 охвата</div><div class="sub">2 068 сохранений · 1 298 репостов · <b>479 комментариев</b></div>{ig("Dc5RMknEQLP", "карусель Каск в Instagram")}{ig("DdYRr7cEU1z", "белл хукс, 17 сентября")}
<blockquote>«Берём 2, 3, 6, 7, 8, 9, 15. На обложку 5. Верстай»</blockquote>
{rows([("9:34", "«цитаты» — агент приносит 17 цитат со страницами книги", ""), ("9:41", "я выбираю номера", ""), ("9:43", "8 слайдов готовы в моей дизайн-системе", "ok"), ("9:59", "текст поста, факты сверены по источникам", "ok")])}
<div class="note">Так собиралась вчерашняя карусель по белл хукс: 25 минут от первого сообщения до текста поста. Одну цитату агент снял сам: на 60-й странице это оказались слова другого автора. Скорость без проверки фактов не нужна.</div></div></div>

<h2 style="margin-top:96px">Что это даёт <u>в цифрах</u></h2>
{nums([("20", "цитатных каруселей за 55 дней: медиана охвата 22 998, сохранений 334"), ("166 002", "охвата у продающей карусели 22 августа, 1 437 комментариев"), ("+549", "подписчиков за день после неё; обычный день даёт 85–190")])}
<div class="tbl"><div class="h"><span>карусель</span><b>охват</b><b>сохр.</b><b>репосты</b></div>
<div><span><a href="https://www.instagram.com/p/DcWngewETa3/" target="_blank" rel="noopener">22.08 · Шестой поток: собираем двух AI-агентов ↗</a></span><b>166 002</b><b>4 539</b><b>1 636</b></div>
<div><span><a href="https://www.instagram.com/p/Dc5RMknEQLP/" target="_blank" rel="noopener">05.09 · Рейчел Каск ↗</a></span><b>140 694</b><b>2 068</b><b>1 298</b></div>
<div><span><a href="https://www.instagram.com/p/Dc0JVFZjFea/" target="_blank" rel="noopener">03.09 · Письмо в 2011 год ↗</a></span><b>121 551</b><b>2 611</b><b>1 317</b></div>
<div><span><a href="https://www.instagram.com/p/DcdrF_cjIKu/" target="_blank" rel="noopener">25.08 · Эндрю Соломон, докторантура ↗</a></span><b>101 838</b><b>2 281</b><b>1 339</b></div>
<div><span><a href="https://www.instagram.com/p/DcfhPGekVQv/" target="_blank" rel="noopener">26.08 · Анонс воркшопа по AI с Настей ↗</a></span><b>77 593</b><b>1 582</b><b>2 162</b></div>
<div><span><a href="https://www.instagram.com/p/DcdjR3ADC8h/" target="_blank" rel="noopener">25.08 · тот же анонс, без карусельной истории ↗</a></span><b>10 055</b><b>—</b><b>1 953</b></div></div>
<p class="big2">Общее у всех больших каруселей: год, имя, профессия и конкретное событие в первой строке. Никаких «5 признаков». Для агента это не пожелание, а правило в базе знаний, поэтому он не сползает в «полезный контент».</p></div></section>

<section id="reels"><div class="wrap"><div class="lab">Акт 03 · кейсы · рилсы и монтаж</div><h2>Рилс за 13 минут, <u>монтаж без монтажёра</u></h2>
<div class="week"><span>11 сентября</span><span>«Сними, как сделан этот пост» — процесс сам стал контентом</span></div>
<div class="grid two" style="margin-top:26px">{video("../v/post13.mp4", "«дизайнерский пост за 13 минут»")}<div><div class="price">49 269 просмотров</div><div class="sub">столько собрал пост, <b>о котором</b> снят рилс</div>{ig("DcWx7UCETp7", "тот самый пост в Instagram")}
<div class="bks">{bk("Приём 01", "Сплит-экран", "сверху голова, снизу доказательства", "<p>График, обложки постов, шаги процесса. Зритель видит и человека, и экран.</p>")}
{bk("Приём 02", "Без пауз", "паузы вырезаны, субтитры по словам", "<p>Монтаж по расшифровке: склейки попадают между фразами.</p>")}
{bk("Приём 03", "Три хука", "один ролик → девять версий", "<p>По три версии на хук уходят в пробные рилсы. Через сутки агент сам снимает цифры: какой хук держит.</p>")}
{bk("Приём 04", "Речь 1,2×", "правило с 13 сентября", "<p>Все рилсы ускорены. Субтитры печатаются по словам, с курсором.</p>")}</div></div></div>

<div class="week" style="margin-top:80px"><span>20 августа</span><span>«Сделай из последнего поста рилс» — одно сообщение, карусель про сериалы стала рилсом</span></div>
<div class="grid two" style="margin-top:26px">{video("../v/serialy.mp4", "«сериалы, к которым стоит присмотреться» · 37 секунд")}<div><div class="price">33 422 просмотра</div><div class="sub">1 138 сохранений · 468 репостов · <b>пролистывают 33 %</b></div>{ig("DcRaBI9xUuJ", "рилс в Instagram", "reel")}
{rows([("19:16", "сообщение агенту: «сделай из последнего поста рилс»", ""), ("—", "агент сам нарезал фрагменты трейлеров и сверстал плашки в моей дизайн-системе", ""), ("—", "звук исходников выровнен по громкости, склейки по 0,2 секунды, финал в тишине", ""), ("19:50", "готовое видео в Телеграме. Монтажную программу я не открывал", "ok")])}
<div class="note">Сохраняют как шпаргалку: одно сохранение на каждые 29 просмотров. Средний просмотр — 11,8 секунды.</div></div></div>

<div class="week" style="margin-top:80px"><span>16 сентября</span><span>Рилс клиента разобран до склеек и собран заново по его рецепту</span></div>
<div class="grid" style="margin-top:26px">{video("../v/dima_orig.mp4", "оригинал · Дмитрий Провоторов, «Антихрупкость» · <a href=\"https://www.instagram.com/reel/DdUFrEbCaa3/\" target=\"_blank\" rel=\"noopener\">в Instagram ↗</a>")}{video("../v/dima_ours.mp4", "наша сборка · версия 13")}
<div><div class="price">69 с · 7 склеек</div><div class="sub">тринадцать версий <b>за три дня</b> → «отлично, фиксирую как скилл»</div>
{rows([("01", "один статичный план, крупности сделаны кропом и работают как склейки", ""), ("02", "субтитры печатаются по словам, с курсором", ""), ("03", "врезки на имена: обложки книг и карточка «выступление на TED»", ""), ("04", "теперь это рецепт: сырой дубль на входе, готовый рилс на выходе", "ok")])}
<div class="note">Так выглядит «монтаж без монтажёра»: агент один раз выучил стиль, дальше каждый рилс собирается по правилу, а не с нуля.</div></div></div>

<div class="week" style="margin-top:80px"><span>14 сентября</span><span>«Вырежи моменты, где только я прыгаю сальто: чёрная футболка, бледно-зелёные шорты»</span></div>
<div class="grid two" style="margin-top:26px">{video("../v/salto.mp4", "гимнастика · 14 сальто за 59 секунд")}<div><div class="price">16 минут → 59 секунд</div><div class="sub">одно видео из зала, <b>1,6 ГБ</b>. Агент сам нашёл все прыжки и оставил только мои</div>
{rows([("01", "прошёл всё видео по движению в кадре: 80 подозрительных моментов", ""), ("02", "посмотрел каждый глазами, оставил 14 сальто", ""), ("03", "узнал меня по футболке и татуировке, чужие прыжки выкинул", ""), ("04", "склеил ролик, отдал файлом в Телеграм", "ok")])}
{nums([("70", "рилсов за 55 дней: 13 в ленте + 57 пробных"), ("39 061", "просмотр — <a href=\"https://www.instagram.com/reel/Db21dJ2sNUa/\" target=\"_blank\" rel=\"noopener\">лучший рилс в ленте ↗</a>, 10 августа"), ("47–60 %", "неподписчиков — у рилсов Даши Морозовой (ниже)")])}
<div class="note">Честно про трафик: медиана охвата рилса в ленте у меня — 5 673, и это на уровне карусели. Рилсы дают холодную аудиторию и конвейер, а мотор охвата и подписок — карусели из предыдущего акта.</div></div></div></div></section>

<section id="people" class="dark"><div class="wrap"><div class="lab">Акт 04 · пятый поток · август</div><h2>Психолог, мастер рэйки, турфирма, маркетолог. <u>Ни одного технаря</u></h2>
<div class="grid two">{video("../v/mbga5_reviews.mp4", "выпускной зум · 11 сентября · с согласия участниц")}<div><div class="price">37 человек, 6 потоков</div><div class="sub">без технического бэкграунда — <b>34 из 37</b>; ниже четверо из пятого потока, полный список под ними</div>
<div class="bks">
<div class="q"><div class="who"><b>Юлия Оздемир</b>мастер рэйки, открывает школу для мастеров</div><p>«Каждый рубль отбивается в сто тысяч раз»</p><p>«Манус сделал мне сайт с онлайн-записью — клиенты просто визжат от восторга, как им удобно»</p></div>
<div class="q"><div class="who"><b>Ирина Решетова</b>владелица туристической компании</div><p>«Агент подключился к Телеграму, собрал все мои голосовые и сделал полный клон голоса. Я в шоке»</p><p>«Пятьдесят пять чатов он с меня за сутки снял — в десять раз больше, чем до этого»</p></div>
<div class="q"><div class="who"><b>Таисия Крохмаль</b>психолог, Вена</div><p>«С методологом, целой командой писали тексты, снимали рилсы — в итоге ноль клиентов»</p><p>За три недели: второй бот, сайт, к сайту подключены Google-отзывы клиентов</p></div>
<div class="q"><div class="who"><b>Даша Морозова</b>маркетолог, десять лет в Яндексе</div><p>«Вспоминаю, когда появился интернет, компьютер, потом ютуб — вот примерно то же самое»</p><p>«Даже на клиентские проекты сейчас собираю. Это гениально»</p></div></div></div></div>

<h2 style="margin-top:96px">Кто прошёл программы: <u>потоки 1–5</u> и набор шестого</h2>
<p class="big2" style="margin-top:0">Психологи, коучи, нутрициолог, фотограф, турфирма, магазин тканей, недвижимость. Из IT — трое из тридцати семи. Остальные до программы не открывали ни терминал, ни Claude Code.</p>
{roster_table()}
<div class="week" style="margin-top:80px"><span>Даша</span><span>До программы — 5 постов за 7,5 месяца. После — 14 публикаций за 23 дня, и карусели по новостям день в день</span></div>
<div class="grid wide" style="margin-top:26px"><div>{dasha}<div>{ig("Dc1So_1jJ8Q", "PUMA")}{ig("Dc-tkTkjJm1", "ФОМО")}{ig("DdRuN_CsT5w", "рилс Hermès", "reel")}</div></div><div>{nums([("1 ч 10 мин", "карусель по кампании PUMA день в день: ресёрч 5 мин, сборка 30, правки 25"), ("35 мин", "фоновой работы агента — рилс Hermès, 130 лайков"), ("47–60 %", "охвата рилсов — неподписчики, у каруселей 15–26 %")], "sm")}
<blockquote>«Я бы вовсе не полезла делать карусель по свежей новости день в день, потому что руками собирать совсем не секси»</blockquote>
<div class="note">Комментарий подписчицы под третьим рилсом: «классные рилсы, только на половине заметила, что это ИИ-аватар». Это она сама, с ускорением 1,2×.</div></div></div>

<div class="week" style="margin-top:80px"><span>до агентов</span><span>Кейсы предыдущих потоков MBGA, опубликованы в @mbga_materials</span></div>
<div class="cases"><div class="cs"><img src="img/fedorova.jpg" alt=""><b>248 000</b><span>просмотров за неделю, +1 000 подписчиков, 70 000 ₽ · Галина Фёдорова, психолог</span></div><div class="cs"><img src="img/herd.jpg" alt=""><b>1 000 000</b><span>просмотров на одном посте · Маша Херд, про тело и эмоции</span></div><div class="cs"><img src="img/maltseva.jpg" alt=""><b>1 млн ₽</b><span>с одного поста: 2 110 комментариев → 900 регистраций → 100+ покупок · Наталья Мальцева, бизнес-психолог</span></div><div class="cs"><i>NDA</i><b>1,5 млн ₽</b><span>за неделю на холодную аудиторию, чек 20 000 ₽ · академия для психологов</span></div></div>
</div></section>

<section id="program"><div class="wrap"><div class="lab">Акт 05 · как построено обучение</div><h2>Два блока: сначала <u>контент</u>, потом <u>продажи</u></h2>
<p class="big2" style="margin-top:0">Уроки записаны и лежат на платформе, проходятся в своём темпе. В первом блоке собираем контентного агента и учим его вашему голосу и дизайну. Во втором — агента-маркетолога: продукты, офферы, воронка.</p>
<div class="prog">{lessons("Блок 01", "Контент", "13 уроков · агент, дизайн, тексты", CONTENT, "Дополнительно: создание базы знаний")}
{lessons("Блок 02", "Продажи", "агент-маркетолог, продукты, воронка", SALES, "Блок пополняется: следующие уроки выходят по ходу потока")}</div>
<p class="big2">Дальше — живое демо: агент получает задание голосом прямо в эфире.</p></div></section>

<footer><div class="wrap">Эфир 18.09.2026 · цифры по @andreyandreev.me — статистика Instagram (Graph API) на 17.09 · цитаты участниц — выпускной зум пятого потока 11.09, с их согласия · кейс Даши Морозовой — её публикации и чат потока · «Антихрупкость» — Дмитрий Провоторов, @provotorov</div></footer>
<script>{JS}</script></body></html>"""

open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(PAGE)
print("ok", len(PAGE))
