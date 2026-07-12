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
BINARY_CHECK_BYTES = 4096


@dataclass(frozen=True)
class SearchOptions:
    keyword: str
    root: Path
    extensions: set[str] | None = None
    ignore_dirs: set[str] | None = None
    context: int = 3
    max_file_size: int | None = None


@dataclass(frozen=True)
class SearchResult:
    file_path: Path
    line_number: int
    matched_line: str
    context_lines: list[tuple[int, str]]


@dataclass(frozen=True)
class SearchSummary:
    skipped_binary: int = 0
    skipped_large: int = 0
    skipped_unreadable: int = 0

    @property
    def skipped_total(self) -> int:
        return self.skipped_binary + self.skipped_large + self.skipped_unreadable


@dataclass(frozen=True)
class SearchReport:
    results: list[SearchResult]
    summary: SearchSummary


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


def is_binary_file(path: Path) -> bool:
    try:
        with path.open("rb") as file:
            chunk = file.read(BINARY_CHECK_BYTES)
    except OSError:
        return False
    return b"\0" in chunk


def is_too_large(path: Path, max_file_size: int | None) -> bool:
    if max_file_size is None:
        return False
    try:
        return path.stat().st_size > max_file_size
    except OSError:
        return False


def read_lines_safely(path: Path) -> list[str] | None:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, PermissionError, OSError):
        return None


def scan_directory(options: SearchOptions) -> SearchReport:
    keyword = options.keyword.casefold()
    ignore_dirs = DEFAULT_IGNORE_DIRS | (options.ignore_dirs or set())
    results: list[SearchResult] = []
    skipped_binary = 0
    skipped_large = 0
    skipped_unreadable = 0

    for file_path in iter_files(options.root, ignore_dirs):
        if not matches_extension(file_path, options.extensions):
            continue
        if is_too_large(file_path, options.max_file_size):
            skipped_large += 1
            continue
        if is_binary_file(file_path):
            skipped_binary += 1
            continue
        lines = read_lines_safely(file_path)
        if lines is None:
            skipped_unreadable += 1
            continue
        for idx, line in enumerate(lines, start=1):
            if keyword in line.casefold():
                start = max(1, idx - options.context)
                end = min(len(lines), idx + options.context)
                context = [(num, lines[num - 1]) for num in range(start, end + 1)]
                results.append(
                    SearchResult(
                        file_path=file_path,
                        line_number=idx,
                        matched_line=line,
                        context_lines=context,
                    )
                )

    return SearchReport(
        results=results,
        summary=SearchSummary(
            skipped_binary=skipped_binary,
            skipped_large=skipped_large,
            skipped_unreadable=skipped_unreadable,
        ),
    )


def search_directory(options: SearchOptions) -> Iterable[SearchResult]:
    return scan_directory(options).results
