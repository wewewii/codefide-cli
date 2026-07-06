from __future__ import annotations

import re
from collections import Counter
from rich.console import Console
from rich.text import Text

from codefind.scanner import SearchResult

console = Console()


def _highlight(line: str, keyword: str, regex: bool, case_sensitive: bool) -> Text:
    text = Text(line)
    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = keyword if regex else re.escape(keyword)
    for match in re.finditer(pattern, line, flags):
        text.stylize("bold reverse", match.start(), match.end())
    return text


def print_results(results: list[SearchResult], keyword: str, regex: bool = False, case_sensitive: bool = False) -> None:
    if not results:
        console.print("[yellow]No matches found.[/yellow]")
        return

    for result in results:
        console.print(f"\n[bold cyan]{result.file_path}:{result.line_number}[/bold cyan]")
        for number, line in result.context_lines:
            marker = ">" if number == result.line_number else " "
            prefix = f"{marker} {number:>4} | "
            console.print(prefix, end="")
            console.print(_highlight(line, keyword, regex, case_sensitive))

    files = Counter(str(r.file_path) for r in results)
    console.print(f"\n[bold green]Found {len(results)} matches in {len(files)} files.[/bold green]")
