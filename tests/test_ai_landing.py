from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "ai" / "index.html"


def test_ai_landing_is_published_with_required_offer():
    html = PAGE.read_text(encoding="utf-8")

    assert '<html lang="ru">' in html
    assert "Делегируйте ведение блога и продажи" in html
    assert "Контентный AI-агент" in html
    assert "Продающий AI-агент" in html
    assert "69 990 ₽" in html
    assert "https://tadaa.createtoday.ru/hero/get/of_YmE8fLARaB6P" in html
    assert "https://t.me/team_fokina" in html
    assert "https://peach-bagpipe-497.notion.site/2b51a689ec9e805297f5f125dcc0fd7a" in html
    assert "https://peach-bagpipe-497.notion.site/2b21a689ec9e80cbb6c7f5bfbeae7e14" in html
    assert "https://createtoday.ru/politica" not in html
    assert "https://createtoday.ru/oferta/challenge" not in html
    assert 'href="https://andreyandreev.me/ai/"' in html


def test_ai_landing_local_assets_exist():
    html = PAGE.read_text(encoding="utf-8")
    refs = []
    for marker in ('src="', 'href="'):
        for chunk in html.split(marker)[1:]:
            refs.append(chunk.split('"', 1)[0])

    local_refs = [
        ref
        for ref in refs
        if ref and not urlparse(ref).scheme and not ref.startswith(("#", "/"))
    ]

    assert local_refs
    for ref in local_refs:
        assert (PAGE.parent / ref).resolve().is_file(), ref
