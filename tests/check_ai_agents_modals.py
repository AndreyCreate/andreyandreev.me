"""Browser regression: run with Playwright Python; optional live URL and evidence dir."""
import functools
import http.server
import json
from pathlib import Path
import sys
import threading
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else '/home/hermes/work/ai-agents-local-modal-evidence')
OUT.mkdir(parents=True, exist_ok=True)
server = None
if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f'http://127.0.0.1:{server.server_port}/ai-agents/'
results = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for width in [1440, 390]:
        context = browser.new_context(viewport={'width': width, 'height': 900}, is_mobile=width == 390)
        page = context.new_page()
        page.goto(url, wait_until='domcontentloaded')
        assert page.locator('.ex[data-local-video]').count() == 3
        assert page.locator('.ex[data-video]').count() == 3
        assert page.locator('.hero video[src="assets/p5_films.mp4"]').count() == 1
        assert page.locator('a[href="https://t.me/andrey_andreev"]').count() == 2
        for asset in ['109', '125', '119']:
            card = page.locator(f'.ex[data-local-video="assets/{asset}.mp4"]')
            assert card.locator('.more').inner_text() == 'Смотреть →'
            assert card.get_attribute('target') is None
            for close_method in ['button', 'Escape', 'backdrop']:
                card.click()
                video = page.locator('#modal-video')
                assert video.is_visible()
                page.wait_for_function('document.querySelector("#modal-video").currentTime > 0.15')
                before = video.evaluate('(v) => v.currentTime')
                page.wait_for_timeout(350)
                state = video.evaluate('(v) => ({time:v.currentTime, paused:v.paused, muted:v.muted, volume:v.volume, controls:v.controls, loop:v.loop, inline:v.playsInline, src:v.getAttribute("src"), error:v.error})')
                assert state['time'] > before and not state['paused'], state
                assert state['controls'] and state['loop'] and state['inline'] and not state['muted'] and state['volume'] == 1
                assert state['src'] == f'assets/{asset}.mp4' and state['error'] is None
                assert page.url == url and len(context.pages) == 1
                if close_method == 'button':
                    page.screenshot(path=str(OUT / f'{width}-{asset}.png'))
                    page.locator('#modal-x').click()
                elif close_method == 'Escape':
                    page.keyboard.press('Escape')
                else:
                    page.locator('#modal').click(position={'x': 5, 'y': 5})
                assert not page.locator('#modal').is_visible()
                stopped = video.evaluate('(v) => ({paused:v.paused,src:v.getAttribute("src"),time:v.currentTime})')
                assert stopped['paused'] and stopped['src'] is None
                page.wait_for_timeout(200)
                assert video.evaluate('(v) => v.currentTime') == stopped['time']
                results.append({'width': width, 'asset': asset, 'close': close_method, 'playback': state, 'stopped': stopped, 'same_url': page.url == url, 'tabs':len(context.pages)})
                (OUT / 'results.json').write_text(json.dumps(results, ensure_ascii=False, indent=2))
        # Existing iframe path still opens and unloads; provider playback is outside this test.
        for card in page.locator('.ex[data-video]').all():
            src = card.get_attribute('data-video')
            card.click()
            assert page.locator('#modal-frame').is_visible()
            assert not page.locator('#modal-video').is_visible()
            assert page.locator('#modal-frame').get_attribute('src') == src + '?autoplay=1'
            page.locator('#modal-x').click()
            assert page.locator('#modal-frame').get_attribute('src') == ''
        context.close()
    browser.close()
if server:
    server.shutdown()
assert len(results) == 18
print(json.dumps({'passed':len(results),'url':url,'evidence':str(OUT)}))
