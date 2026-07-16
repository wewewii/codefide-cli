# Phase 1 Architecture

## Module Overview

```txt
main.py       CLI layer: parse args, validate input, call scanner, call formatter
scanner.py    Search core: walk files, read, match, build result
formatter.py  Terminal output: rich display, highlight, summary
opener.py     Reserved for Phase 3 editor integration
tests/        Unit tests for scanner
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
```

## Core Data Structures

```python
SearchOptions(
    keyword: str,
    root: Path,
    context: int,
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
