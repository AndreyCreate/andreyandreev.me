from pathlib import Path
import re


PAGE = Path(__file__).resolve().parents[1] / "ai-agents" / "index.html"


def test_ai_agents_page_has_current_september_offer():
    html = PAGE.read_text(encoding="utf-8")
    visible = re.sub(r"<[^>]+>", " ", html)
    visible = re.sub(r"\s+", " ", visible)

    assert "21 сентября" in visible
    assert "до 8 участников" in visible.lower()
    assert "165 000 ₽" in visible
    assert "три недели" in visible.lower()
    assert "два общих zoom" in visible.lower()
    assert "три индивидуальные встречи" in visible.lower()


def test_ai_agents_page_has_no_legacy_offer():
    html = PAGE.read_text(encoding="utf-8")
    legacy = (
        "39 900",
        "49 900",
        "20 мест",
        "7 сентября",
        "31 августа",
        "две недели",
        "три общих Zoom",
        "куратор",
    )
    for marker in legacy:
        assert marker.casefold() not in html.casefold(), marker


def test_ai_agents_page_offers_checkout_and_personal_dialogue():
    html = PAGE.read_text(encoding="utf-8")
    checkout_url = "https://andreyandreev.createtoday.ru/hero/get/of_r6-pemaaf45z"

    assert html.count(f'href="{checkout_url}"') >= 2
    assert html.count('data-action="checkout"') >= 2
    assert "Оплатить участие" in html
    assert html.count('href="https://t.me/andrey_andreev"') >= 2
    assert "Написать Андрею" in html
    assert "Можно оплатить сразу или сначала коротко сверить с Андреем задачу и формат." in html


def test_canonical_page_preserves_approved_v2_assets():
    source = PAGE.parent.parent / "ai-agents-v2"
    for file in source.rglob("*"):
        if file.is_file() and file.name != "index.html":
            assert (PAGE.parent / file.relative_to(source)).read_bytes() == file.read_bytes()


def test_approved_v2_preserves_media_noindex_and_tracking():
    html = PAGE.read_text(encoding="utf-8")
    assert '<meta name="robots" content="noindex, nofollow">' in html
    assert '<style>' in html
    assert '109255989' in html
    assert 'data-event="ai-agents-cta"' in html
    assert 'data-placement="hero"' in html
    assert html.count('data-video="https://kinescope.io/embed/') == 3
    videos = re.findall(r'<video\b[^>]*>', html)
    assert len(videos) == 5
    for video in videos:
        for attribute in ('autoplay', 'muted', 'loop', 'playsinline', 'poster='):
            assert attribute in video
    for asset in re.findall(r'(?:src|poster)="(assets/[^"]+)"', html):
        assert (PAGE.parent / asset).is_file()
