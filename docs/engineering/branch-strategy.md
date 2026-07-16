# Branch Strategy

สำหรับทำคนเดียว ใช้แบบง่ายแต่มีวินัย

## Branches

- `main` — stable, runnable
- `feature/cf-xxx-short-name` — feature branch
- `fix/cf-xxx-short-name` — bug fix branch

## Commit Style

```txt
feat: add recursive file scanner
fix: skip unreadable files
refactor: separate formatter module
test: add ignore directory test
docs: update phase 1 acceptance criteria
```

## Merge Rule

ก่อน merge เข้า `main` ต้องผ่าน:

```bash
ruff check .
mypy src
pytest
```
