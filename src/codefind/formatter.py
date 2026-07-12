from __future__ import annotations

import re
from collections import Counter
from rich.console import Console
from rich.text import Text

from codefind.scanner import SearchResult, SearchSummary

console = Console()


def _highlight(line: str, keyword: str) -> Text:
    text = Text(line)
    for match in re.finditer(re.escape(keyword), line, re.IGNORECASE):
        text.stylize("bold reverse", match.start(), match.end())
    return text


def _format_skipped_summary(summary: SearchSummary) -> str:
    parts: list[str] = []
    if summary.skipped_binary:
        parts.append(f"{summary.skipped_binary} binary")
    if summary.skipped_large:
        parts.append(f"{summary.skipped_large} too large")
    if summary.skipped_unreadable:
        parts.append(f"{summary.skipped_unreadable} unreadable")
    return ", ".join(parts)


def _print_skipped_summary(summary: SearchSummary | None) -> None:
    if summary is None or summary.skipped_total == 0:
        return
    console.print(
        f"[yellow]Skipped {summary.skipped_total} files: {_format_skipped_summary(summary)}.[/yellow]"
    )


def print_results(
    results: list[SearchResult],
    keyword: str,
    summary: SearchSummary | None = None,
) -> None:
    if not results:
        console.print("[yellow]No matches found.[/yellow]")
        _print_skipped_summary(summary)
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
    _print_skipped_summary(summary)
