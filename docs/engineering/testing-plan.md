# Testing Plan

## Unit Tests

- Search match
- No match
- Case-insensitive match
- Context at beginning of file
- Context at end of file
- Ignore directory
- Extension filter
- Binary/unreadable file skip

## Manual Tests

```bash
codefind "login" .
codefind "login" . --ext py,ts
codefind "JWT_SECRET" ./src
codefind "invalid token" .
```

## Regression Checklist

- help command still works
- output remains readable
- no traceback for normal bad input
- tests pass before every commit
