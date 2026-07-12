from pathlib import Path

from codefind.scanner import (
    SearchOptions,
    is_binary_file,
    is_too_large,
    iter_files,
    scan_directory,
    search_directory,
)


def test_search_keyword_with_default_context(tmp_path: Path):
    file = tmp_path / "app.py"
    file.write_text("a\nb\nc\nlogin()\ne\nf\ng\nh\n", encoding="utf-8")

    results = list(search_directory(SearchOptions(keyword="login", root=tmp_path)))

    assert len(results) == 1
    assert results[0].line_number == 4
    assert results[0].matched_line == "login()"
    assert results[0].context_lines == [
        (1, "a"),
        (2, "b"),
        (3, "c"),
        (4, "login()"),
        (5, "e"),
        (6, "f"),
        (7, "g"),
    ]


def test_search_keyword_is_case_insensitive_by_default(tmp_path: Path):
    file = tmp_path / "auth.py"
    file.write_text("def LOGIN():\n    pass\n", encoding="utf-8")

    results = list(search_directory(SearchOptions(keyword="login", root=tmp_path)))

    assert len(results) == 1
    assert results[0].file_path == file
    assert results[0].line_number == 1


def test_no_match_returns_empty_list(tmp_path: Path):
    file = tmp_path / "app.py"
    file.write_text("logout()\n", encoding="utf-8")

    results = list(search_directory(SearchOptions(keyword="login", root=tmp_path)))

    assert results == []


def test_context_at_beginning_of_file(tmp_path: Path):
    file = tmp_path / "app.py"
    file.write_text("login()\nb\nc\nd\ne\n", encoding="utf-8")

    results = list(search_directory(SearchOptions(keyword="login", root=tmp_path)))

    assert len(results) == 1
    assert results[0].context_lines == [(1, "login()"), (2, "b"), (3, "c"), (4, "d")]


def test_context_at_end_of_file(tmp_path: Path):
    file = tmp_path / "app.py"
    file.write_text("a\nb\nc\nlogin()\n", encoding="utf-8")

    results = list(search_directory(SearchOptions(keyword="login", root=tmp_path)))

    assert len(results) == 1
    assert results[0].context_lines == [(1, "a"), (2, "b"), (3, "c"), (4, "login()")]


def test_custom_context_lines(tmp_path: Path):
    file = tmp_path / "app.py"
    file.write_text("a\nb\nlogin()\nd\ne\n", encoding="utf-8")

    results = list(search_directory(SearchOptions(keyword="login", root=tmp_path, context=1)))

    assert len(results) == 1
    assert results[0].context_lines == [(2, "b"), (3, "login()"), (4, "d")]


def test_zero_context_only_returns_matched_line(tmp_path: Path):
    file = tmp_path / "app.py"
    file.write_text("a\nlogin()\nc\n", encoding="utf-8")

    results = list(search_directory(SearchOptions(keyword="login", root=tmp_path, context=0)))

    assert len(results) == 1
    assert results[0].context_lines == [(2, "login()")]


def test_ignore_node_modules(tmp_path: Path):
    node = tmp_path / "node_modules"
    node.mkdir()
    (node / "x.js").write_text("login", encoding="utf-8")

    results = list(search_directory(SearchOptions(keyword="login", root=tmp_path)))

    assert results == []


def test_custom_ignore_directory_is_skipped(tmp_path: Path):
    vendor = tmp_path / "vendor"
    src = tmp_path / "src"
    vendor.mkdir()
    src.mkdir()
    (vendor / "auth.py").write_text("login\n", encoding="utf-8")
    (src / "auth.py").write_text("login\n", encoding="utf-8")

    results = list(
        search_directory(SearchOptions(keyword="login", root=tmp_path, ignore_dirs={"vendor"}))
    )

    assert len(results) == 1
    assert results[0].file_path == src / "auth.py"


def test_custom_ignore_combines_with_default_ignore(tmp_path: Path):
    node = tmp_path / "node_modules"
    vendor = tmp_path / "vendor"
    app = tmp_path / "app"
    node.mkdir()
    vendor.mkdir()
    app.mkdir()
    (node / "auth.js").write_text("login\n", encoding="utf-8")
    (vendor / "auth.py").write_text("login\n", encoding="utf-8")
    (app / "auth.py").write_text("login\n", encoding="utf-8")

    results = list(
        search_directory(SearchOptions(keyword="login", root=tmp_path, ignore_dirs={"vendor"}))
    )

    assert len(results) == 1
    assert results[0].file_path == app / "auth.py"


def test_iter_files_recurses_into_subdirectories(tmp_path: Path):
    nested = tmp_path / "src" / "codefind"
    nested.mkdir(parents=True)
    file = nested / "scanner.py"
    file.write_text("login\n", encoding="utf-8")

    files = list(iter_files(tmp_path, ignore_dirs=set()))

    assert files == [file]


def test_binary_file_is_skipped(tmp_path: Path):
    file = tmp_path / "image.bin"
    file.write_bytes(b"\xff\xfe\x00login")

    results = list(search_directory(SearchOptions(keyword="login", root=tmp_path)))

    assert results == []


def test_binary_detection_finds_null_bytes(tmp_path: Path):
    file = tmp_path / "image.bin"
    file.write_bytes(b"abc\0def")

    assert is_binary_file(file) is True


def test_binary_detection_allows_text_files(tmp_path: Path):
    file = tmp_path / "app.py"
    file.write_text("login()\n", encoding="utf-8")

    assert is_binary_file(file) is False


def test_large_file_is_skipped(tmp_path: Path):
    file = tmp_path / "large.py"
    file.write_text("login\n", encoding="utf-8")

    results = list(
        search_directory(SearchOptions(keyword="login", root=tmp_path, max_file_size=1))
    )

    assert results == []


def test_file_within_max_file_size_is_searched(tmp_path: Path):
    file = tmp_path / "small.py"
    file.write_text("login\n", encoding="utf-8")

    results = list(
        search_directory(SearchOptions(keyword="login", root=tmp_path, max_file_size=100))
    )

    assert len(results) == 1
    assert results[0].file_path == file


def test_is_too_large_uses_byte_size(tmp_path: Path):
    file = tmp_path / "app.py"
    file.write_text("login\n", encoding="utf-8")

    assert is_too_large(file, max_file_size=1) is True
    assert is_too_large(file, max_file_size=100) is False
    assert is_too_large(file, max_file_size=None) is False


def test_scan_report_counts_skipped_files(tmp_path: Path):
    binary_file = tmp_path / "binary.bin"
    large_file = tmp_path / "large.py"
    unreadable_file = tmp_path / "broken.txt"
    match_file = tmp_path / "app.py"
    binary_file.write_bytes(b"abc\0login")
    large_file.write_text("login\n" * 5, encoding="utf-8")
    unreadable_file.write_bytes(b"\xff\xfe login")
    match_file.write_text("login", encoding="utf-8")

    report = scan_directory(SearchOptions(keyword="login", root=tmp_path, max_file_size=10))

    assert len(report.results) == 1
    assert report.results[0].file_path == match_file
    assert report.summary.skipped_binary == 1
    assert report.summary.skipped_large == 1
    assert report.summary.skipped_unreadable == 1
    assert report.summary.skipped_total == 3


def test_extension_filter_searches_matching_extensions(tmp_path: Path):
    py_file = tmp_path / "app.py"
    md_file = tmp_path / "README.md"
    py_file.write_text("login()\n", encoding="utf-8")
    md_file.write_text("login\n", encoding="utf-8")

    results = list(
        search_directory(SearchOptions(keyword="login", root=tmp_path, extensions={"py"}))
    )

    assert len(results) == 1
    assert results[0].file_path == py_file


def test_extension_filter_accepts_multiple_extensions(tmp_path: Path):
    py_file = tmp_path / "app.py"
    ts_file = tmp_path / "auth.ts"
    md_file = tmp_path / "README.md"
    py_file.write_text("login()\n", encoding="utf-8")
    ts_file.write_text("login()\n", encoding="utf-8")
    md_file.write_text("login\n", encoding="utf-8")

    results = list(
        search_directory(SearchOptions(keyword="login", root=tmp_path, extensions={"py", "ts"}))
    )

    assert {result.file_path for result in results} == {py_file, ts_file}


def test_extension_filter_matches_uppercase_file_suffix(tmp_path: Path):
    file = tmp_path / "APP.PY"
    file.write_text("login()\n", encoding="utf-8")

    results = list(
        search_directory(SearchOptions(keyword="login", root=tmp_path, extensions={"py"}))
    )

    assert len(results) == 1
    assert results[0].file_path == file
