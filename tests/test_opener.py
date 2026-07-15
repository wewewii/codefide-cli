from pathlib import Path

from codefind.opener import build_code_command, build_open_command, build_vim_command, open_result
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


def test_build_code_command_opens_file_at_line():
    assert build_code_command(make_result()) == ["code", "-g", "src/app.py:12"]


def test_build_open_command_dispatches_supported_editors():
    result = make_result()

    assert build_open_command("vim", result) == ["vim", "+12", "src/app.py"]
    assert build_open_command("code", result) == ["code", "-g", "src/app.py:12"]


def test_build_open_command_rejects_unsupported_editor():
    result = make_result()

    try:
        build_open_command("antigravity", result)
    except ValueError as error:
        assert str(error) == "unsupported editor: antigravity"
    else:
        raise AssertionError("expected unsupported editor error")


def test_open_result_runs_command(monkeypatch):
    calls: list[tuple[list[str], bool]] = []

    def fake_run(command: list[str], check: bool) -> None:
        calls.append((command, check))

    monkeypatch.setattr("codefind.opener.subprocess.run", fake_run)

    open_result(make_result(), "code")

    assert calls == [(["code", "-g", "src/app.py:12"], False)]
