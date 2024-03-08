import datetime as dt
import json
import logging
from typing import Dict

LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}


class JSONFormatter(logging.Formatter):
    # Inspired by https://www.youtube.com/watch?v=9L77QExPmI0&t=957s

    def __init__(self, *, fmt_keys: Dict[str, str] | None = None):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord) -> dict:
        message = self.create_message_with_configured_fields(record)
        JSONFormatter.add_optional_extra_keys(message, record)
        return message

    @staticmethod
    def add_optional_extra_keys(message: dict, record: logging.LogRecord) -> None:
        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                message[key] = val

    def create_message_with_configured_fields(self, record: logging.LogRecord):
        always_incl_fields = self._get_always_fields(record)
        message = {
            key: msg_val
            if (msg_val := always_incl_fields.pop(val, None)) is not None
            else getattr(record, val)
            for key, val in self.fmt_keys.items()
        }
        message.update(always_incl_fields)
        return message

    def _get_always_fields(self, record: logging.LogRecord) -> dict:
        always_incl_fields = {
            "message": record.getMessage(),
            "timestamp": JSONFormatter.get_formatted_timestamp_from_record(record),
        }
        if record.exc_info is not None:
            always_incl_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_incl_fields["stack_info"] = self.formatStack(record.stack_info)

        return always_incl_fields

    @staticmethod
    def get_formatted_timestamp_from_record(record: logging.LogRecord) -> str:
        return dt.datetime.fromtimestamp(
            record.created, tz=dt.timezone.utc
        ).isoformat()
