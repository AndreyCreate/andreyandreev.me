from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "sale" / "index.html"
CHECKOUT = "https://andreyandreev.createtoday.ru/hero/get/of_6JnvXPPgT8L5"


class SalePageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def parsed_page():
    html = PAGE.read_text(encoding="utf-8")
    parser = SalePageParser()
    parser.feed(html)
    return html, parser.tags


def attrs_with_class(tags, tag, class_name):
    return [
        attrs
        for found_tag, attrs in tags
        if found_tag == tag and class_name in attrs.get("class", "").split()
    ]


def test_sale_page_leads_with_three_result_routes():
    html, tags = parsed_page()

    assert "Соберите блог, который помогает" in html
    assert "Три маршрута — выберите тот, который нужен сейчас" in html
    routes = attrs_with_class(tags, "article", "route-card")
    assert [route["data-route"] for route in routes] == [
        "positioning",
        "content",
        "product",
    ]
    assert "Стать понятнее и упаковать профиль" in html
    assert "Выпускать контент и привлекать аудиторию" in html
    assert "Превратить экспертизу в продукт и продажи" in html


def test_sale_page_separates_three_flagships_from_eight_additions():
    html, tags = parsed_page()

    flagships = attrs_with_class(tags, "article", "flagship")
    additions = attrs_with_class(tags, "article", "pcard")
    assert [card["data-flagship"] for card in flagships] == [
        "brand",
        "reels",
        "signal",
    ]
    assert len(additions) == 8

    assert "48 уроков в 6 разделах" in html
    assert "44 урока в 7 разделах" in html
    assert "40 уроков в 6 блоках" in html
    assert "Как написать пост «Обо мне» без успешного успеха" in html
    assert "Как создавать Reels в формате сторителлингов и видеодневников" in html
    assert "Продукт: идея, формат, ценность" in html


def test_sale_page_includes_relevant_outcomes_without_unverified_profit_claim():
    html, tags = parsed_page()

    quotes = attrs_with_class(tags, "blockquote", "review")
    assert len(quotes) == 3
    assert "тысяче новых подписчиков менее чем за две недели" in html
    assert "ролик собрал 17 тысяч просмотров" in html
    assert "запуске на 115 участников" in html
    assert "чистой прибыли" not in html


def test_sale_page_is_honest_about_archived_self_paced_access():
    html, _ = parsed_page()

    assert "архивный самостоятельный формат" in html.lower()
    assert "Все записи и сохранённые материалы останутся у вас без ограничения по времени" in html
    assert "Новые уроки, живые встречи и личная обратная связь в пакет не входят" in html
    assert "Результат потребует самостоятельной работы" in html


def test_sale_page_keeps_active_checkout_and_distinct_cta_measurement():
    html, tags = parsed_page()

    checkout_links = [
        attrs
        for tag, attrs in tags
        if tag == "a" and attrs.get("href") == CHECKOUT and "js-buy" in attrs.get("class", "").split()
    ]
    assert [link["data-cta"] for link in checkout_links] == ["hero", "offer", "final"]
    assert all("is-off" not in link.get("class", "").split() for link in checkout_links)
    assert "sale_checkout_hero" in html
    assert "sale_checkout_offer" in html
    assert "sale_checkout_final" in html
    assert "window.location.search" in html
    assert "URLSearchParams" in html
    assert "white-space:nowrap" not in html


def test_sale_page_publishes_the_approved_deadline():
    html, _ = parsed_page()

    assert "6 августа 2026" not in html
    assert 'data-deadline-status="approved"' in html
    assert html.count("6 сентября 2026") >= 3
    assert "23:59 по московскому времени" in html
    assert ".deadline:before" not in html
    assert ".final .note{margin-top:14px;color:rgba(241,238,230,.75)}" in html


def test_sale_page_local_assets_exist():
    _, tags = parsed_page()
    refs = [attrs[key] for _, attrs in tags for key in ("src", "href") if key in attrs]
    local_refs = [
        ref
        for ref in refs
        if ref and not urlparse(ref).scheme and not ref.startswith(("#", "/", "data:"))
    ]

    assert local_refs
    for ref in local_refs:
        assert (PAGE.parent / ref).resolve().is_file(), ref
