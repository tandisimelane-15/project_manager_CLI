import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import generate_id, validate_date


def test_generate_id_is_unique():
    assert generate_id() != generate_id()


def test_validate_date_normalizes_format():
    assert validate_date("August 1 2026") == "2026-08-01"


def test_validate_date_handles_blank():
    assert validate_date("") is None


def test_validate_date_rejects_garbage():
    with pytest.raises(ValueError):
        validate_date("not a date")