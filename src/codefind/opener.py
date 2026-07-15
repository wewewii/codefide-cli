from __future__ import annotations

import subprocess
from codefind.scanner import SearchResult


def build_vim_command(result: SearchResult) -> list[str]:
    return ["vim", f"+{result.line_number}", str(result.file_path)]


def build_code_command(result: SearchResult) -> list[str]:
    return ["code", "-g", f"{result.file_path}:{result.line_number}"]


def build_open_command(editor: str, result: SearchResult) -> list[str]:
    if editor == "vim":
        return build_vim_command(result)
    if editor == "code":
        return build_code_command(result)
    raise ValueError(f"unsupported editor: {editor}")


def open_result(result: SearchResult, editor: str) -> None:
    subprocess.run(build_open_command(editor, result), check=False)
