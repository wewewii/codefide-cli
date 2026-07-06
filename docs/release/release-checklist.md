# Release Checklist

## Before Release

- [ ] Update version in `pyproject.toml`
- [ ] Update README examples
- [ ] Run `ruff check .`
- [ ] Run `mypy src`
- [ ] Run `pytest`
- [ ] Test install in clean virtualenv
- [ ] Test `codefind --help`
- [ ] Test common commands manually

## Build

```bash
python -m build
```

## Tag

```bash
git tag v0.1.0
git push origin v0.1.0
```
