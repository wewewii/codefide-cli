from __future__ import annotations

import subprocess
from collections.abc import Callable
from codefind.scanner import SearchResult


def build_vim_command(result: SearchResult) -> list[str]:
    return ["vim", f"+{result.line_number}", str(result.file_path)]


def build_code_command(result: SearchResult) -> list[str]:
    return ["code", "-g", f"{result.file_path}:{result.line_number}"]


def build_antigravity_command(result: SearchResult) -> list[str]:
    return ["antigravity", str(result.file_path)]


def build_open_command(editor: str, result: SearchResult) -> list[str]:
    if editor == "vim":
        return build_vim_command(result)
    if editor == "code":
        return build_code_command(result)
    if editor == "antigravity":
        return build_antigravity_command(result)
    raise ValueError(f"unsupported editor: {editor}")


def open_result(result: SearchResult, editor: str) -> None:
    subprocess.run(build_open_command(editor, result), check=False)


def select_result(
    results: list[SearchResult],
    input_func: Callable[[str], str] | None = None,
) -> SearchResult | None:
    if not results:
        return None
    if len(results) == 1:
        return results[0]

    print("\nResults:")
    for index, result in enumerate(results, start=1):
        print(f"[{index}] {result.file_path}:{result.line_number}")

    if input_func is None:
        input_func = input
    selected = int(input_func("Open result number: ").strip())
    if selected < 1 or selected > len(results):
        raise ValueError(f"selection out of range: {selected}")
    return results[selected - 1]


def open_selected_result(results: list[SearchResult], editor: str) -> None:
    selected = select_result(results)
    if selected is not None:
        open_result(selected, editor)
