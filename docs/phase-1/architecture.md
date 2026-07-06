# Phase 1 Architecture

## Module Overview

```txt
main.py       CLI layer: parse args, validate input, call scanner, call formatter/opener
scanner.py    Search core: walk files, filter, read, match, build result
formatter.py  Terminal output: rich display, highlight, summary
opener.py     Editor integration: vim/code/antigravity commands
tests/        Unit tests for scanner and opener
```

## Data Flow

```txt
CLI Args
  ↓
SearchOptions
  ↓
search_directory()
  ↓
list[SearchResult]
  ↓
print_results()
  ↓
optional open_selected_result()
```

## Core Data Structures

```python
SearchOptions(
    keyword: str,
    root: Path,
    extensions: set[str] | None,
    context: int,
    ignore_dirs: set[str],
    case_sensitive: bool,
    regex: bool,
)
```

```python
SearchResult(
    file_path: Path,
    line_number: int,
    matched_line: str,
    context_lines: list[tuple[int, str]],
)
```
