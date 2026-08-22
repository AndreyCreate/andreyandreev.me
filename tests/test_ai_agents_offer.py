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


def test_ai_agents_page_has_no_legacy_offer_or_checkout():
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
        "andreyandreev.createtoday.ru/hero/get/",
        "data-action=\"checkout\"",
    )
    for marker in legacy:
        assert marker.casefold() not in html.casefold(), marker


def test_ai_agents_page_primary_conversion_is_personal_dialogue():
    html = PAGE.read_text(encoding="utf-8")
    assert html.count('href="https://t.me/andrey_andreev"') >= 2
    assert "Написать Андрею" in html
