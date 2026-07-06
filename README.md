# CodeFind CLI

CodeFind คือ CLI tool สำหรับค้นหาข้อความใน directory หลายไฟล์ แล้วแสดงผลแบบอ่านง่าย พร้อม file path, line number และ context รอบบรรทัดที่เจอ

> Status: Software Design Package + Project Skeleton

## Target MVP

```bash
codefind "login" .
codefind "JWT_SECRET" ./backend
codefind "invalid token" .
```

## Install for Development

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
codefind --help
pytest
```

## Documentation Map

- `docs/project-brief/` — product vision, requirements, use cases, user flow
- `docs/phase-1/` — MVP CLI scope, architecture, tasks, acceptance criteria
- `docs/phase-2/` — search robustness, ignore rules, file filtering
- `docs/phase-3/` — editor open flow, JSON output, regex
- `docs/phase-4/` — polish, packaging, performance, release
- `docs/engineering/` — coding standard, branch strategy, test plan
- `docs/release/` — release checklist and roadmap

## Project Structure

```txt
codefind-cli/
  docs/
  src/codefind/
  tests/
  scripts/
  pyproject.toml
  README.md
```
