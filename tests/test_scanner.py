from pathlib import Path

from codefind.scanner import SearchOptions, search_directory


def test_search_keyword_with_context(tmp_path: Path):
    file = tmp_path / "app.py"
    file.write_text("a\nb\nlogin()\nd\ne\n", encoding="utf-8")

    results = list(search_directory(SearchOptions(keyword="login", root=tmp_path, context=1)))

    assert len(results) == 1
    assert results[0].line_number == 3
    assert results[0].matched_line == "login()"
    assert results[0].context_lines == [(2, "b"), (3, "login()"), (4, "d")]


def test_ignore_node_modules(tmp_path: Path):
    node = tmp_path / "node_modules"
    node.mkdir()
    (node / "x.js").write_text("login", encoding="utf-8")

    results = list(search_directory(SearchOptions(keyword="login", root=tmp_path)))

    assert results == []
