from pathlib import Path

import typer

from codefind.scanner import SearchOptions, search_directory
from codefind.formatter import print_results

app = typer.Typer(help="Find text in a directory and show code context.", no_args_is_help=True)


def _run_search(keyword: str, path: Path) -> None:
    if not keyword:
        raise typer.BadParameter("keyword must not be empty")
    if not path.exists():
        raise typer.BadParameter(f"path does not exist: {path}")
    if not path.is_dir():
        raise typer.BadParameter(f"path must be a directory: {path}")

    options = SearchOptions(keyword=keyword, root=path)
    results = list(search_directory(options))
    print_results(results, keyword=keyword)


@app.command()
def main(
    keyword: str = typer.Argument(..., help="Keyword or pattern to search."),
    path: Path = typer.Argument(Path("."), help="Directory to search."),
) -> None:
    """Search KEYWORD inside PATH."""
    _run_search(keyword, path)
