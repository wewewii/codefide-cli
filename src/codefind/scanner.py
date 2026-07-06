from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Iterable

DEFAULT_IGNORE_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "venv",
    ".venv",
    "__pycache__",
}


@dataclass(frozen=True)
class SearchOptions:
    keyword: str
    root: Path
    extensions: set[str] | None = None
    ignore_dirs: set[str] | None = None
    context: int = 3


@dataclass(frozen=True)
class SearchResult:
    file_path: Path
    line_number: int
    matched_line: str
    context_lines: list[tuple[int, str]]


def should_skip_dir(path: Path, ignore_dirs: set[str]) -> bool:
    return path.name in ignore_dirs


def iter_files(root: Path, ignore_dirs: set[str]) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not should_skip_dir(Path(d), ignore_dirs)]
        current_path = Path(current)
        for filename in files:
            yield current_path / filename


def matches_extension(path: Path, extensions: set[str] | None) -> bool:
    if extensions is None:
        return True
    return path.suffix.lstrip(".").lower() in extensions


def read_lines_safely(path: Path) -> list[str] | None:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, PermissionError, OSError):
        return None


def search_directory(options: SearchOptions) -> Iterable[SearchResult]:
    keyword = options.keyword.casefold()
    ignore_dirs = DEFAULT_IGNORE_DIRS | (options.ignore_dirs or set())

    for file_path in iter_files(options.root, ignore_dirs):
        if not matches_extension(file_path, options.extensions):
            continue
        lines = read_lines_safely(file_path)
        if lines is None:
            continue
        for idx, line in enumerate(lines, start=1):
            if keyword in line.casefold():
                start = max(1, idx - options.context)
                end = min(len(lines), idx + options.context)
                context = [(num, lines[num - 1]) for num in range(start, end + 1)]
                yield SearchResult(
                    file_path=file_path,
                    line_number=idx,
                    matched_line=line,
                    context_lines=context,
                )
