from pathlib import Path
from typing import Optional

import typer

from codefind.scanner import SearchOptions, scan_directory
from codefind.formatter import print_results

app = typer.Typer(help="Find text in a directory and show code context.", no_args_is_help=True)


def parse_extensions(ext: Optional[str]) -> set[str] | None:
    if ext is None:
        return None
    extensions = {item.strip().lstrip(".").lower() for item in ext.split(",") if item.strip()}
    return extensions or None


def parse_ignore_dirs(ignore: Optional[str]) -> set[str]:
    if ignore is None:
        return set()
    return {item.strip() for item in ignore.split(",") if item.strip()}


def _run_search(
    keyword: str,
    path: Path,
    ext: Optional[str],
    ignore: Optional[str],
    context: int,
    max_file_size: Optional[int],
) -> None:
    if not keyword:
        raise typer.BadParameter("keyword must not be empty")
    if not path.exists():
        raise typer.BadParameter(f"path does not exist: {path}")
    if not path.is_dir():
        raise typer.BadParameter(f"path must be a directory: {path}")

    options = SearchOptions(
        keyword=keyword,
        root=path,
        extensions=parse_extensions(ext),
        ignore_dirs=parse_ignore_dirs(ignore),
        context=context,
        max_file_size=max_file_size,
    )
    report = scan_directory(options)
    print_results(report.results, keyword=keyword, summary=report.summary)


@app.command()
def main(
    keyword: str = typer.Argument(..., help="Keyword or pattern to search."),
    path: Path = typer.Argument(Path("."), help="Directory to search."),
    ext: Optional[str] = typer.Option(None, "--ext", help="Comma-separated extensions, e.g. py,ts,tsx"),
    ignore: Optional[str] = typer.Option(None, "--ignore", help="Comma-separated folders to ignore."),
    context: int = typer.Option(3, "--context", "-C", min=0, help="Context lines before/after."),
    max_file_size: Optional[int] = typer.Option(
        None,
        "--max-file-size",
        min=1,
        help="Skip files larger than this size in bytes.",
    ),
) -> None:
    """Search KEYWORD inside PATH."""
    _run_search(keyword, path, ext, ignore, context, max_file_size)
