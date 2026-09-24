import json

import pytest

from storage import load_records, save_records


def test_save_and_load_records(tmp_path):
    path = tmp_path / "data" / "records.json"
    records = [{"id": 1, "name": "Task Planner"}]
    save_records(path, records)
    assert load_records(path) == records


def test_missing_file_returns_empty_list(tmp_path):
    assert load_records(tmp_path / "missing.json") == []


def test_invalid_json_raises_clear_error(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{broken", encoding="utf-8")
    with pytest.raises(ValueError, match="Некорректный JSON"):
        load_records(path)


def test_non_list_json_is_rejected(tmp_path):
    path = tmp_path / "object.json"
    path.write_text(json.dumps({"id": 1}), encoding="utf-8")
    with pytest.raises(ValueError, match="список"):
        load_records(path)
