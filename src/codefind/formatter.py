from __future__ import annotations

import re
from collections import Counter
from rich.console import Console
from rich.text import Text

from codefind.scanner import SearchResult

console = Console()


def _highlight(line: str, keyword: str) -> Text:
    text = Text(line)
    for match in re.finditer(re.escape(keyword), line, re.IGNORECASE):
        text.stylize("bold reverse", match.start(), match.end())
    return text


def print_results(results: list[SearchResult], keyword: str) -> None:
    if not results:
        console.print("[yellow]No matches found.[/yellow]")
        return

    for result in results:
        console.print(f"\n[bold cyan]{result.file_path}:{result.line_number}[/bold cyan]")
        for number, line in result.context_lines:
            marker = ">" if number == result.line_number else " "
            prefix = f"{marker} {number:>4} | "
            console.print(prefix, end="")
            console.print(_highlight(line, keyword))

    files = Counter(str(r.file_path) for r in results)
    console.print(f"\n[bold green]Found {len(results)} matches in {len(files)} files.[/bold green]")
