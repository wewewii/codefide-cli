from pathlib import Path

from codefind.opener import build_vim_command, open_vim_result
from codefind.scanner import SearchResult


def make_result() -> SearchResult:
    return SearchResult(
        file_path=Path("src/app.py"),
        line_number=12,
        matched_line="login()",
        context_lines=[(12, "login()")],
    )


def test_build_vim_command_opens_file_at_line():
    assert build_vim_command(make_result()) == ["vim", "+12", "src/app.py"]


def test_open_vim_result_runs_command(monkeypatch):
    calls: list[tuple[list[str], bool]] = []

    def fake_run(command: list[str], check: bool) -> None:
        calls.append((command, check))

    monkeypatch.setattr("codefind.opener.subprocess.run", fake_run)

    open_vim_result(make_result())

    assert calls == [(["vim", "+12", "src/app.py"], False)]
