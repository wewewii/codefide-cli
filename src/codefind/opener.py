from __future__ import annotations

import subprocess
from codefind.scanner import SearchResult


def build_open_command(editor: str, result: SearchResult) -> list[str]:
    path = str(result.file_path)
    line = str(result.line_number)
    if editor == "vim":
        return ["vim", f"+{line}", path]
    if editor == "code":
        return ["code", "-g", f"{path}:{line}"]
    if editor == "antigravity":
        return ["antigravity", path]
    raise ValueError(f"unsupported editor: {editor}")


def open_selected_result(results: list[SearchResult], editor: str) -> None:
    if len(results) == 1:
        selected = results[0]
    else:
        print("\nResults:")
        for idx, result in enumerate(results, start=1):
            print(f"[{idx}] {result.file_path}:{result.line_number}")
        raw = input("Open result number: ").strip()
        selected = results[int(raw) - 1]
    subprocess.run(build_open_command(editor, selected), check=False)
