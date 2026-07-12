# Testing Plan

## Unit Tests

- Search match
- No match
- Case-insensitive match
- Context at beginning of file
- Context at end of file
- Custom context count
- Ignore directory
- Custom ignore directory
- Extension filter
- Binary/unreadable file skip
- Max file size skip
- Skipped file warning summary

## CLI Integration Tests

- `--ext` filters output
- `--ignore` skips custom directories
- `--context 0` hides surrounding lines
- `--max-file-size` prints skipped summary

## Manual Tests

```bash
codefind "login" .
codefind "login" . --ext py,ts
codefind "login" . --ignore vendor,tmp
codefind "login" . --context 1
codefind "login" . --max-file-size 1048576
codefind "JWT_SECRET" ./src
codefind "invalid token" .
```

## Regression Checklist

- help command still works
- output remains readable
- no traceback for normal bad input
- tests pass before every commit
