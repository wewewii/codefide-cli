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

## Manual Tests

```bash
codefind "login" .
codefind "login" . --ext py,ts
codefind "login" . --ignore vendor,tmp
codefind "login" . --context 1
codefind "JWT_SECRET" ./src
codefind "invalid token" .
```

## Regression Checklist

- help command still works
- output remains readable
- no traceback for normal bad input
- tests pass before every commit
