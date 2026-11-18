"""#192: the architecture page's Side by side tab drills into each part of the picture. Each of the five lines names a
part and carries that part's box (fractions of the picture's width and height), the box lies inside the picture, and
the page stays self-contained."""
import re
from pathlib import Path

PAGE = Path(__file__).resolve().parents[1] / "docs" / "architecture" / "index.html"
PARTS = ["projects", "agent", "cause", "scored", "showed"]


def html() -> str:
    return PAGE.read_text(encoding="utf-8")


def lines() -> list[tuple[str, list[float]]]:
    found = re.findall(r'<li[^>]*data-part="([a-z]+)"[^>]*data-box="([0-9.,]+)"', html())
    return [(part, [float(v) for v in box.split(",")]) for part, box in found]


def test_each_of_the_five_lines_names_its_part_once_in_order():
    assert [part for part, _ in lines()] == PARTS


def test_each_box_lies_inside_the_picture_and_has_size():
    for part, (x, y, w, h) in lines():
        assert len((x, y, w, h)) == 4, part
        assert 0 <= x < 1 and 0 <= y < 1 and w > 0.05 and h > 0.05, part
        assert x + w <= 1.0001 and y + h <= 1.0001, part


def test_the_side_view_has_a_whole_picture_button_and_a_zoomable_figure():
    page = html()
    assert 'id="side-whole"' in page and 'id="side-viewer"' in page and 'id="side-mark"' in page


def test_a_chosen_part_is_kept_in_the_address():
    assert "#side-by-side/" in html()


def test_the_page_loads_nothing_from_elsewhere():
    page = html()
    assert not re.search(r'<script[^>]+src=', page)
    assert not re.search(r'<link[^>]+href="https?://', page)
