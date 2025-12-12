import json
import logging
from datetime import datetime


# ----------------------
# Safe simple formatter
# ----------------------

class SafeExtraFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        for field in ("method", "path", "query", "status_code"):
            if not hasattr(record, field):
                setattr(record, field, "-")
        return super().format(record)


# ----------------------
# JSON formatter
# ----------------------

class JsonFormatter(logging.Formatter):
    @staticmethod
    def format(record: logging.LogRecord) -> str:
        log = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "method": getattr(record, "method", None),
            "path": getattr(record, "path", None),
            "status_code": getattr(record, "status_code", None),
        }
        return json.dumps(log)


# ----------------------
# Log Handler
# ----------------------

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())


logger = logging.getLogger("aurora")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False
