import json
import logging

from app.logging_config import JsonFormatter


def _make_record(**extra: object) -> logging.LogRecord:
    record = logging.LogRecord(
        name="sensorhub",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="request completed",
        args=(),
        exc_info=None,
    )
    for key, value in extra.items():
        setattr(record, key, value)
    return record


def test_json_formatter_produces_valid_json_with_core_fields() -> None:
    formatter = JsonFormatter()
    record = _make_record(method="GET", path="/health", status_code=200)

    line = formatter.format(record)
    payload = json.loads(line)

    assert payload["level"] == "INFO"
    assert payload["logger"] == "sensorhub"
    assert payload["message"] == "request completed"
    assert payload["method"] == "GET"
    assert payload["path"] == "/health"
    assert payload["status_code"] == 200
    assert "timestamp" in payload


def test_json_formatter_omits_absent_extra_fields() -> None:
    formatter = JsonFormatter()
    record = _make_record()

    payload = json.loads(formatter.format(record))

    assert "method" not in payload
    assert "status_code" not in payload
