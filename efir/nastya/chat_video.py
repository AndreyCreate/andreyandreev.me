"""Ролики-переписки для карточек агентов на /efir/nastya/ (DM 7676, 18.09.2026):
диалог Андрея с ботом в стиле Telegram, сообщения появляются по одному. Тексты — реальные,
из переписки 17.09 (Тони Шарк: тред «Контент» NBA 13243–13267; Коби: личка 803914–803922).
python3 chat_video.py → ../v/chat_tony.mp4, ../v/chat_kobi.mp4 (+ .jpg постеры)"""
import os, html, subprocess, shutil, asyncio
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "v")
W, H, FPS = 560, 760, 24

TONY = dict(name="Тони Шарк", role="контентный агент", ava="Т", msgs=[
    ("me", "9:34", "Хукс цитаты", None),
    ("bot", "9:35", "белл хукс, «The Will to Change» (2004). Семнадцать цитат, все сверены по тексту книги, страницы настоящие, перевод мой.\n\n1. Патриархат ценит у мужчины ровно одну эмоцию — злость…", None),
    ("me", "9:41", "Берём 2, 3, 6, 7, 8, 9, 15.\nНа обложку 5.\n\nВерстай", None),
    ("bot", "9:41", "Верстаю: на обложке «Злость — лучшее укрытие для того, кто прячет боль», дальше 2, 3, 6, 7, 8, 9, 15 в твоём порядке. Сдам альбомом, следом текст поста.", None),
    ("bot", "9:43", "белл хукс, v1: обложка + 7 цитат", ["../img/hooks_0.jpg", "../img/hooks_1.jpg", "../img/hooks_2.jpg"]),
    ("me", "9:47", "Текст поста ещё каждый раз присылай после рендера", None),
    ("bot", "9:59", "Готово, текст выше. Все сцены взяты из самой книги, со страницами, биография сверена по Britannica и некрологам Washington Post и Guardian.", None),
])
KOBI = dict(name="Коби", role="продающий агент", ava="К", msgs=[
    ("me", "16:22", "а сделай мне ещё сообщение в мой канал про эфир, со мной согласуй сначала", None),
    ("bot", "16:23", "Вот черновик для канала. Пока не публикую.\n\nЗавтра в 12:00 МСК — эфир про агентов, которым можно делегировать контент и воронки. В пятницу, 18 сентября, вместе с Настей Фокиной покажем всё на живых примерах: монтаж Reels, посты за 15 минут вашим голосом, воронки без технических специалистов.\n\nДля тех, кто придёт на эфир, будет специальная цена.", None),
    ("me", "16:23", "Давай с картинкой, публикуй.", None),
    ("bot", "16:26", "Опубликовано с картинкой: t.me/mbga_materials/289\n\nПроверил текст, обложку с датой и временем и ссылку в бот эфира.", None),
])

def page(chat):
    items = []
    for who, t, text, imgs in chat["msgs"]:
        body = "".join(f"<p>{html.escape(p)}</p>" for p in text.split("\n\n"))
        body = body.replace("\n", "<br>")
        pics = "".join(f'<img src="{p}">' for p in imgs) if imgs else ""
        items.append(f'<div class="row {who}"><div class="b">{pics}{body}<i>{t}</i></div></div>')
    return f"""<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=JetBrains+Mono&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#1b1b1b;font-family:Inter,system-ui,sans-serif;color:#fff}}
.hd{{position:absolute;top:0;left:0;right:0;z-index:2;display:flex;align-items:center;gap:14px;padding:20px 24px;background:#232323;border-bottom:1px solid #333}}
.hd .a{{width:48px;height:48px;border-radius:50%;background:#F0695F;display:flex;align-items:center;justify-content:center;font-weight:500;font-size:20px}}
.hd b{{display:block;font-weight:500;font-size:19px}}.hd span{{font-family:'JetBrains Mono',monospace;font-size:12.5px;color:#8cc4ff}}
.list{{position:absolute;left:0;right:0;bottom:0;max-height:calc(100% - 90px);overflow:hidden;padding:18px 20px 22px;display:flex;flex-direction:column;gap:10px;justify-content:flex-end}}
.row{{display:flex;opacity:0;transform:translateY(14px);transition:opacity .28s ease,transform .28s ease}}.row.on{{opacity:1;transform:none}}
.row.me{{justify-content:flex-end}}.b{{max-width:84%;background:#2b2b2b;border-radius:18px 18px 18px 6px;padding:12px 16px 10px;font-size:17px;line-height:1.36;position:relative}}
.me .b{{background:#F0695F;color:#161616;border-radius:18px 18px 6px 18px}}.b p+p{{margin-top:8px}}
.b i{{display:block;font-style:normal;font-family:'JetBrains Mono',monospace;font-size:11.5px;text-align:right;margin-top:6px;opacity:.6}}
.b img{{width:92px;aspect-ratio:4/5;object-fit:cover;border-radius:8px;margin:0 6px 8px 0;display:inline-block;vertical-align:top}}
.typing{{position:absolute;left:20px;bottom:22px;background:#2b2b2b;border-radius:18px;padding:12px 16px;display:none;gap:6px}}.typing.on{{display:flex}}
.typing s{{width:8px;height:8px;border-radius:50%;background:#8cc4ff;display:block;animation:bl 1s infinite}}.typing s:nth-child(2){{animation-delay:.2s}}.typing s:nth-child(3){{animation-delay:.4s}}
@keyframes bl{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
</style></head><body>
<div class="hd"><div class="a">{chat["ava"]}</div><div><b>{chat["name"]}</b><span>{chat["role"]} · Telegram</span></div></div>
<div class="list">{"".join(items)}</div><div class="typing"><s></s><s></s><s></s></div>
<script>
var rows=[].slice.call(document.querySelectorAll('.row'));
window.setT=function(t){{ // t в секундах; сообщения появляются по расписанию window.SCHED
  var n=0;for(var i=0;i<SCHED.length;i++){{if(t>=SCHED[i])n=i+1}}
  rows.forEach(function(r,k){{r.classList.toggle('on',k<n)}});
  var typ=document.querySelector('.typing');var nxt=rows[n];
  typ.classList.toggle('on', !!nxt && nxt.classList.contains('bot') && n>0 && t>=SCHED[n-1]+0.9);
}};
</script></body></html>"""

async def render(chat, out, sched):
    fdir = os.path.join(HERE, "_frames"); shutil.rmtree(fdir, ignore_errors=True); os.makedirs(fdir)
    htmlp = os.path.join(HERE, "_chat.html"); open(htmlp, "w", encoding="utf-8").write(page(chat))
    total = sched[-1] + 3.0
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": W, "height": H})
        await pg.goto("file://" + htmlp); await pg.wait_for_timeout(900)
        await pg.evaluate("window.SCHED=" + str(sched))
        n = int(total * FPS)
        for f in range(n):
            await pg.evaluate(f"setT({f / FPS:.3f})")
            await pg.wait_for_timeout(int(1000 / FPS) if f % FPS == 0 else 12)
            await pg.screenshot(path=os.path.join(fdir, f"f{f:05d}.png"))
        await b.close()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", os.path.join(fdir, "f%05d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "24", "-preset", "veryfast", "-movflags", "+faststart", out], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(total - 0.2), "-i", out, "-frames:v", "1", "-q:v", "4", out.replace(".mp4", ".jpg")], check=True)
    shutil.rmtree(fdir); os.remove(htmlp)

if __name__ == "__main__":
    asyncio.run(render(TONY, os.path.join(OUT, "chat_tony.mp4"), [0.6, 2.6, 5.4, 7.6, 10.2, 12.4, 14.8]))
    asyncio.run(render(KOBI, os.path.join(OUT, "chat_kobi.mp4"), [0.6, 2.8, 7.4, 9.6]))
    print("ok")
