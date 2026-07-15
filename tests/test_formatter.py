from pathlib import Path

from codefind.formatter import print_results
from codefind.scanner import SearchResult, SearchSummary


def test_print_results_includes_skipped_summary(capsys):
    result = SearchResult(
        file_path=Path("app.py"),
        line_number=1,
        matched_line="login()",
        context_lines=[(1, "login()")],
    )
    summary = SearchSummary(skipped_binary=1, skipped_large=2, skipped_unreadable=3)

    print_results([result], keyword="login", summary=summary)

    output = capsys.readouterr().out
    assert "Skipped 6 files: 1 binary, 2 too large, 3 unreadable." in output


def test_print_results_includes_skipped_summary_with_no_matches(capsys):
    summary = SearchSummary(skipped_binary=1)

    print_results([], keyword="login", summary=summary)

    output = capsys.readouterr().out
    assert "No matches found." in output
    assert "Skipped 1 files: 1 binary." in output


def test_print_results_highlights_regex(capsys):
    result = SearchResult(
        file_path=Path("app.py"),
        line_number=1,
        matched_line="login()",
        context_lines=[(1, "login()")],
    )

    print_results([result], keyword="log(in|out)", regex=True)

    output = capsys.readouterr().out
    assert "login()" in output
