from codefind.main import parse_extensions


def test_parse_extensions_returns_none_when_missing():
    assert parse_extensions(None) is None


def test_parse_extensions_normalizes_comma_separated_values():
    assert parse_extensions("py, .TS,tsx") == {"py", "ts", "tsx"}
