from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from codefind.scanner import SearchOptions, search_directory
from codefind.formatter import print_results
from codefind.opener import open_selected_result

app = typer.Typer(help="Find text in a directory and show code context.")
console = Console()


@app.command()
def find(
    keyword: str = typer.Argument(..., help="Keyword or pattern to search."),
    path: Path = typer.Argument(Path("."), help="Directory to search."),
    ext: Optional[str] = typer.Option(None, "--ext", help="Comma-separated extensions, e.g. py,ts,tsx"),
    context: int = typer.Option(3, "--context", "-C", min=0, help="Context lines before/after."),
    ignore: Optional[str] = typer.Option(None, "--ignore", help="Comma-separated folders to ignore."),
    case_sensitive: bool = typer.Option(False, "--case-sensitive", help="Match case exactly."),
    regex: bool = typer.Option(False, "--regex", help="Treat keyword as regular expression."),
    open_editor: Optional[str] = typer.Option(None, "--open", help="Open a result in vim, code, or antigravity."),
):
    """Search KEYWORD inside PATH."""
    if not keyword:
        raise typer.BadParameter("keyword must not be empty")
    if not path.exists():
        raise typer.BadParameter(f"path does not exist: {path}")
    if not path.is_dir():
        raise typer.BadParameter(f"path must be a directory: {path}")

    extensions = {e.strip().lstrip(".") for e in ext.split(",")} if ext else None
    ignore_dirs = {x.strip() for x in ignore.split(",")} if ignore else set()

    options = SearchOptions(
        keyword=keyword,
        root=path,
        extensions=extensions,
        context=context,
        ignore_dirs=ignore_dirs,
        case_sensitive=case_sensitive,
        regex=regex,
    )
    results = list(search_directory(options))
    print_results(results, keyword=keyword, regex=regex, case_sensitive=case_sensitive)

    if open_editor and results:
        open_selected_result(results, open_editor)


@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        console.print("[bold]CodeFind CLI[/bold] - use `codefind find <keyword> <path>`")
        console.print("Example: codefind find login . --context 3")
