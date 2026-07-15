from pathlib import Path
import json

from codefind.formatter import format_json_report, print_results
from codefind.scanner import SearchReport, SearchResult, SearchSummary


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


def test_format_json_report_outputs_parseable_results():
    result = SearchResult(
        file_path=Path("app.py"),
        line_number=2,
        matched_line="login()",
        context_lines=[(1, "before"), (2, "login()")],
    )
    report = SearchReport(
        results=[result],
        summary=SearchSummary(skipped_binary=1, skipped_large=2, skipped_unreadable=3),
    )

    payload = json.loads(format_json_report(report))

    assert payload == {
        "results": [
            {
                "file_path": "app.py",
                "line_number": 2,
                "matched_line": "login()",
                "context_lines": [
                    {"line_number": 1, "text": "before"},
                    {"line_number": 2, "text": "login()"},
                ],
            }
        ],
        "summary": {
            "matches": 1,
            "files": 1,
            "skipped_total": 6,
            "skipped_binary": 1,
            "skipped_large": 2,
            "skipped_unreadable": 3,
        },
    }
