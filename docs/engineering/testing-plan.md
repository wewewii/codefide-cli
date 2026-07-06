# Testing Plan

## Unit Tests

- Search match
- No match
- Case-insensitive match
- Case-sensitive match
- Regex match
- Context at beginning of file
- Context at end of file
- Ignore directory
- Extension filter
- Binary/unreadable file skip

## Manual Tests

```bash
codefind find "login" .
codefind find "JWT_SECRET" ./src --ext py
codefind find "TODO" . --open vim
codefind find "login|logout" . --regex
```

## Regression Checklist

- help command still works
- output remains readable
- no traceback for normal bad input
- tests pass before every commit
