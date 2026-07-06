from codefind.main import parse_extensions, parse_ignore_dirs


def test_parse_extensions_returns_none_when_missing():
    assert parse_extensions(None) is None


def test_parse_extensions_normalizes_comma_separated_values():
    assert parse_extensions("py, .TS,tsx") == {"py", "ts", "tsx"}


def test_parse_ignore_dirs_returns_empty_set_when_missing():
    assert parse_ignore_dirs(None) == set()


def test_parse_ignore_dirs_parses_comma_separated_values():
    assert parse_ignore_dirs("vendor, tmp ,coverage") == {"vendor", "tmp", "coverage"}
