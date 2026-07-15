from pathlib import Path

from typer.testing import CliRunner

from codefind.main import app


runner = CliRunner()


def test_cli_searches_with_extension_filter(tmp_path: Path):
    py_file = tmp_path / "app.py"
    md_file = tmp_path / "README.md"
    py_file.write_text("login()\n", encoding="utf-8")
    md_file.write_text("login\n", encoding="utf-8")

    result = runner.invoke(app, ["login", str(tmp_path), "--ext", "py"])

    assert result.exit_code == 0
    assert "app.py:1" in result.output
    assert "README.md" not in result.output


def test_cli_searches_with_custom_ignore(tmp_path: Path):
    vendor = tmp_path / "vendor"
    app_dir = tmp_path / "app"
    vendor.mkdir()
    app_dir.mkdir()
    (vendor / "auth.py").write_text("login\n", encoding="utf-8")
    (app_dir / "auth.py").write_text("login\n", encoding="utf-8")

    result = runner.invoke(app, ["login", str(tmp_path), "--ignore", "vendor"])

    assert result.exit_code == 0
    assert "app/auth.py:1" in result.output
    assert "vendor/auth.py" not in result.output


def test_cli_searches_with_zero_context(tmp_path: Path):
    file = tmp_path / "app.py"
    file.write_text("before\nlogin()\nafter\n", encoding="utf-8")

    result = runner.invoke(app, ["login", str(tmp_path), "--context", "0"])

    assert result.exit_code == 0
    assert "login()" in result.output
    assert "before" not in result.output
    assert "after" not in result.output


def test_cli_reports_skipped_large_files(tmp_path: Path):
    file = tmp_path / "large.py"
    file.write_text("login\n", encoding="utf-8")

    result = runner.invoke(app, ["login", str(tmp_path), "--max-file-size", "1"])

    assert result.exit_code == 0
    assert "No matches found." in result.output
    assert "Skipped 1 files: 1 too large." in result.output


def test_cli_opens_single_result_with_vim(tmp_path: Path, monkeypatch):
    file = tmp_path / "app.py"
    file.write_text("before\nlogin()\n", encoding="utf-8")
    opened: list[tuple[Path, str]] = []

    def fake_open_selected_result(results, editor: str):
        result = results[0]
        opened.append((result.file_path, editor))

    monkeypatch.setattr("codefind.main.open_selected_result", fake_open_selected_result)

    result = runner.invoke(app, ["login", str(tmp_path), "--open", "vim"])

    assert result.exit_code == 0
    assert opened == [(file, "vim")]


def test_cli_opens_single_result_with_code(tmp_path: Path, monkeypatch):
    file = tmp_path / "app.py"
    file.write_text("before\nlogin()\n", encoding="utf-8")
    opened: list[tuple[Path, str]] = []

    def fake_open_selected_result(results, editor: str):
        result = results[0]
        opened.append((result.file_path, editor))

    monkeypatch.setattr("codefind.main.open_selected_result", fake_open_selected_result)

    result = runner.invoke(app, ["login", str(tmp_path), "--open", "code"])

    assert result.exit_code == 0
    assert opened == [(file, "code")]


def test_cli_opens_single_result_with_antigravity(tmp_path: Path, monkeypatch):
    file = tmp_path / "app.py"
    file.write_text("before\nlogin()\n", encoding="utf-8")
    opened: list[tuple[Path, str]] = []

    def fake_open_selected_result(results, editor: str):
        result = results[0]
        opened.append((result.file_path, editor))

    monkeypatch.setattr("codefind.main.open_selected_result", fake_open_selected_result)

    result = runner.invoke(app, ["login", str(tmp_path), "--open", "antigravity"])

    assert result.exit_code == 0
    assert opened == [(file, "antigravity")]


def test_cli_rejects_unsupported_open_editor(tmp_path: Path):
    file = tmp_path / "app.py"
    file.write_text("login()\n", encoding="utf-8")

    result = runner.invoke(app, ["login", str(tmp_path), "--open", "emacs"])

    assert result.exit_code != 0
    assert "--open currently supports only vim, code, or antigravity" in result.output


def test_cli_open_passes_multiple_results_for_selection(tmp_path: Path, monkeypatch):
    first = tmp_path / "first.py"
    second = tmp_path / "second.py"
    first.write_text("login()\n", encoding="utf-8")
    second.write_text("login()\n", encoding="utf-8")
    opened: list[tuple[list[Path], str]] = []

    def fake_open_selected_result(results, editor: str):
        opened.append(([result.file_path for result in results], editor))

    monkeypatch.setattr("codefind.main.open_selected_result", fake_open_selected_result)

    result = runner.invoke(app, ["login", str(tmp_path), "--open", "vim"])

    assert result.exit_code == 0
    assert len(opened) == 1
    assert set(opened[0][0]) == {first, second}
    assert opened[0][1] == "vim"


def test_cli_case_sensitive_search(tmp_path: Path):
    file = tmp_path / "auth.py"
    file.write_text("LOGIN()\n", encoding="utf-8")

    result = runner.invoke(app, ["login", str(tmp_path), "--case-sensitive"])

    assert result.exit_code == 0
    assert "No matches found." in result.output


def test_cli_regex_search(tmp_path: Path):
    file = tmp_path / "auth.py"
    file.write_text("login()\nlogout()\n", encoding="utf-8")

    result = runner.invoke(app, ["log(in|out)", str(tmp_path), "--regex"])

    assert result.exit_code == 0
    assert "auth.py:1" in result.output
    assert "auth.py:2" in result.output


def test_cli_invalid_regex_shows_clear_error(tmp_path: Path):
    file = tmp_path / "auth.py"
    file.write_text("login()\n", encoding="utf-8")

    result = runner.invoke(app, ["(", str(tmp_path), "--regex"])

    assert result.exit_code != 0
    assert "invalid regex:" in result.output
