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
python -m twine check dist/*
```

Expected artifacts:

```txt
dist/codefind_cli-0.1.0.tar.gz
dist/codefind_cli-0.1.0-py3-none-any.whl
```

## Tag

```bash
git tag v0.1.0
git push origin v0.1.0
```
