# Release Checklist

## Before Release

- [x] Confirm version `0.1.0` in `pyproject.toml` and `codefind.__version__`
- [x] Update `CHANGELOG.md` and release notes
- [x] Confirm README installation and usage examples
- [x] Run `ruff check .`
- [x] Run `mypy src`
- [x] Run `pytest`
- [x] Build wheel and source distribution
- [x] Run strict distribution metadata validation
- [x] Test install in clean virtualenv
- [x] Test `codefind --help`
- [x] Test common commands manually

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

Create the release tag only after Phase 4 is merged into `develop`, then into `main`, and CI passes
on the final `main` commit.

```bash
git switch main
git pull --ff-only origin main
git tag -a v0.1.0 -m "CodeFind CLI v0.1.0"
git push origin v0.1.0
```

## Publish

Pushing the tag triggers `.github/workflows/release.yml`, which validates the tag, builds both
distributions, and creates the GitHub release with the artifacts attached.

- [ ] Merge `feature/phase-4` into `develop`
- [ ] Merge `develop` into `main`
- [ ] Confirm CI passes on `main`
- [ ] Create and push annotated tag `v0.1.0`
- [ ] Confirm the Release workflow succeeds
- [ ] Verify the GitHub release notes and attached distributions
