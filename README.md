# CodeFind CLI

CodeFind is a command-line tool for searching text across a project directory. It displays
matching file paths, line numbers, highlighted matches, and surrounding context in a readable
terminal format. Results can also be exported as JSON or opened directly in a supported editor.

## Features

- Recursive, case-insensitive text search by default
- File extension and custom directory filters
- Configurable context lines around every match
- Default exclusions for common generated and dependency directories
- Binary, oversized, and unreadable file handling
- Case-sensitive and regular-expression search modes
- Human-readable terminal output with highlighted matches
- Machine-readable JSON output
- Editor integration for Vim, Visual Studio Code, and Antigravity
- Interactive result selection when an editor is requested and multiple matches are found

## Requirements

- Python 3.11 or newer
- macOS or Linux

Windows is not a primary target for the current release.

## Installation

### Install from source

```bash
git clone https://github.com/wewewii/codefide-cli.git
cd codefide-cli
python3.11 -m venv .venv
source .venv/bin/activate
pip install .
```

Verify the installation:

```bash
codefind --help
```

### Install for development

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

```text
codefind [OPTIONS] KEYWORD [PATH]
```

- `KEYWORD` is the text or pattern to search for.
- `PATH` is the directory to search and defaults to the current directory.

### Basic search

```bash
codefind "login" .
codefind "JWT_SECRET" ./backend
codefind "invalid token" .
```

Searches are case-insensitive unless `--case-sensitive` is provided.

### Example output

```text
src/auth.py:12
    9 | def authenticate(user):
   10 |     if user is None:
   11 |         return False
>  12 |     return login(user)
   13 |
   14 |
   15 | def logout(user):

Found 1 matches in 1 files.
```

The matched text is highlighted when the output is displayed in a color-capable terminal.

## Options

| Option | Description |
| --- | --- |
| `--ext EXTENSIONS` | Search only comma-separated file extensions, such as `py,ts,tsx`. |
| `--ignore DIRECTORIES` | Ignore additional comma-separated directory names. |
| `--context`, `-C NUMBER` | Set the number of lines shown before and after a match. Defaults to `3`. |
| `--max-file-size BYTES` | Skip files larger than the specified number of bytes. |
| `--open EDITOR` | Open a selected result in `vim`, `code`, or `antigravity`. |
| `--case-sensitive` | Match uppercase and lowercase characters exactly. |
| `--regex` | Treat the keyword as a Python regular expression. |
| `--json` | Return results and the search summary as JSON. |
| `--help` | Display the command help. |

## Search Examples

### Filter by extension

```bash
codefind "useAuth" ./frontend --ext ts,tsx
```

Extension matching is case-insensitive, so `--ext py` also includes files ending in `.PY`.

### Ignore additional directories

```bash
codefind "login" . --ignore vendor,coverage,tmp
```

CodeFind always ignores these directory names by default:

```text
.git  node_modules  dist  build  venv  .venv  __pycache__
```

Custom exclusions are added to the default list.

### Change context size

```bash
codefind "login" . --context 1
codefind "login" . -C 0
```

Using zero context displays only matching lines.

### Case-sensitive search

```bash
codefind "LOGIN" . --case-sensitive
```

### Regular-expression search

```bash
codefind "log(in|out)" . --regex
codefind "^class .*Service" ./src --regex --ext py
```

Invalid regular expressions produce a clear command-line error instead of a traceback.

### Skip oversized files

```bash
codefind "login" . --max-file-size 1048576
```

Skipped binary, oversized, and unreadable files are included in the search summary.

## JSON Output

Use `--json` for scripts and other automation:

```bash
codefind "login" ./src --context 1 --json
```

Example response:

```json
{
  "results": [
    {
      "file_path": "src/auth.py",
      "line_number": 12,
      "matched_line": "return login(user)",
      "context_lines": [
        {"line_number": 11, "text": "        return False"},
        {"line_number": 12, "text": "    return login(user)"},
        {"line_number": 13, "text": ""}
      ]
    }
  ],
  "summary": {
    "matches": 1,
    "files": 1,
    "skipped_total": 0,
    "skipped_binary": 0,
    "skipped_large": 0,
    "skipped_unreadable": 0
  }
}
```

## Open Results in an Editor

```bash
codefind "TODO" . --open vim
codefind "TODO" . --open code
codefind "TODO" . --open antigravity
```

When one match is found, CodeFind opens it immediately. When multiple matches are found, the CLI
prompts for a result number before opening the editor. Vim and Visual Studio Code open the file at
the matched line; Antigravity currently opens the file without a line number.

The selected editor command must be installed and available on `PATH`.

## Development

Install the project with its development dependencies, then run all quality checks:

```bash
source .venv/bin/activate
bash scripts/dev-check.sh
```

The script runs:

```bash
ruff check .
mypy src
pytest
```

Run only the tests with:

```bash
pytest
```

## Project Structure

```text
codefind-cli/
├── src/codefind/        # CLI, scanner, formatter, and editor integration
├── tests/               # Unit and CLI integration tests
├── docs/                # Requirements, architecture, plans, and release documentation
├── scripts/             # Development utilities
├── pyproject.toml       # Package and tool configuration
└── README.md
```

## Current Limitations

- Files are decoded as UTF-8; files using other encodings are skipped.
- Binary detection is based on null bytes in the first 4,096 bytes.
- `.gitignore` files are not interpreted yet.
- Files are scanned sequentially and are not indexed in advance.
- Search results count matching lines rather than every occurrence on a line.
- JSON output and editor opening are separate workflows; `--json` does not open an editor.

## Documentation

- [`docs/project-brief`](docs/project-brief/) — product vision, requirements, and use cases
- [`docs/phase-1`](docs/phase-1/) — MVP architecture and implementation plan
- [`docs/phase-2`](docs/phase-2/) — robust search options and file handling
- [`docs/phase-3`](docs/phase-3/) — editor workflow and advanced search
- [`docs/phase-4`](docs/phase-4/) — packaging, benchmarking, and release preparation
- [`docs/engineering`](docs/engineering/) — coding standards, branch strategy, and testing
- [`docs/release`](docs/release/) — roadmap and release checklist

## Roadmap

Planned improvements include `.gitignore` support, a project configuration file, parallel
scanning, improved exit codes, and optional ripgrep integration.
