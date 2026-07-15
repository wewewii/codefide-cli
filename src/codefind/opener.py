from __future__ import annotations

import subprocess
from codefind.scanner import SearchResult


def build_vim_command(result: SearchResult) -> list[str]:
    return ["vim", f"+{result.line_number}", str(result.file_path)]


def open_vim_result(result: SearchResult) -> None:
    subprocess.run(build_vim_command(result), check=False)
