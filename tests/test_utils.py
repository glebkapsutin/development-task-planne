import pytest

from utils import parse_date


def test_parse_date_supports_two_formats():
    assert parse_date("24.09.2026").isoformat() == "2026-09-24"
    assert parse_date("2026-09-24").isoformat() == "2026-09-24"


def test_parse_invalid_date():
    with pytest.raises(ValueError, match="формате"):
        parse_date("31.02.2026")
