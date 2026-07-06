# Project Structure

```txt
codefind-cli/
  docs/
    project-brief/
    phase-1/
    phase-2/
    phase-3/
    phase-4/
    engineering/
    release/
  src/
    codefind/
      __init__.py
      main.py
      scanner.py
      formatter.py
      opener.py
  tests/
    test_scanner.py
    test_opener.py
  scripts/
    dev-check.sh
  pyproject.toml
  README.md
```

## Rule

- business logic ต้องอยู่ใน `scanner.py`
- output logic ต้องอยู่ใน `formatter.py`
- subprocess/editor logic ต้องอยู่ใน `opener.py`
- `main.py` ห้ามมี search logic หนัก ๆ
