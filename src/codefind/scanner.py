from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable, Optional

DEFAULT_IGNORE_DIRS = {
    ".git", "node_modules", "dist", "build", "venv", ".venv", "__pycache__", ".mypy_cache", ".pytest_cache"
}
DEFAULT_TEXT_EXTENSIONS = {
    "py", "js", "ts", "tsx", "jsx", "go", "java", "c", "cpp", "h", "hpp", "rs",
    "md", "txt", "json", "yaml", "yml", "env", "toml", "ini", "cfg", "sh", "sql", "html", "css"
}


@dataclass(frozen=True)
class SearchOptions:
    keyword: str
    root: Path
    extensions: Optional[set[str]] = None
    context: int = 3
    ignore_dirs: set[str] | None = None
    case_sensitive: bool = False
    regex: bool = False


@dataclass(frozen=True)
class SearchResult:
    file_path: Path
    line_number: int
    matched_line: str
    context_lines: list[tuple[int, str]]


def should_skip_dir(path: Path, ignore_dirs: set[str]) -> bool:
    return path.name in ignore_dirs


def is_text_candidate(path: Path, extensions: Optional[set[str]]) -> bool:
    suffix = path.suffix.lstrip(".")
    if extensions is not None:
        return suffix in extensions
    return suffix in DEFAULT_TEXT_EXTENSIONS or path.name in {"Dockerfile", "Makefile", ".env"}


def iter_files(root: Path, ignore_dirs: set[str]) -> Iterable[Path]:
    for current, dirs, files in root.walk():
        dirs[:] = [d for d in dirs if not should_skip_dir(Path(d), ignore_dirs)]
        for filename in files:
            yield current / filename


def read_lines_safely(path: Path) -> list[str] | None:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except (UnicodeDecodeError, PermissionError, OSError):
        return None


def search_directory(options: SearchOptions) -> Iterable[SearchResult]:
    ignore_dirs = DEFAULT_IGNORE_DIRS | (options.ignore_dirs or set())
    flags = 0 if options.case_sensitive else re.IGNORECASE
    pattern = re.compile(options.keyword if options.regex else re.escape(options.keyword), flags)

    for file_path in iter_files(options.root, ignore_dirs):
        if not is_text_candidate(file_path, options.extensions):
            continue
        lines = read_lines_safely(file_path)
        if lines is None:
            continue
        for idx, line in enumerate(lines, start=1):
            if pattern.search(line):
                start = max(1, idx - options.context)
                end = min(len(lines), idx + options.context)
                context = [(num, lines[num - 1]) for num in range(start, end + 1)]
                yield SearchResult(file_path=file_path, line_number=idx, matched_line=line, context_lines=context)
