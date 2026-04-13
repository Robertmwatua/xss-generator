"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    STRUCTURED LOGGING MODULE                                ║
║   Provides JSON and text logging with multiple levels and outputs           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import json
import sys
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path
from enum import Enum


class LogLevel(Enum):
    """Log levels with numeric values."""
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


class StructuredLogger:
    """Structured logging with JSON and text output."""

    def __init__(
        self,
        name: str,
        log_dir: str = "logs",
        log_level: LogLevel = LogLevel.INFO,
        json_output: bool = True,
    ):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True, parents=True)
        self.log_level = log_level
        self.json_output = json_output
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"{name}_{self.session_id}.log"
        self.json_file = self.log_dir / f"{name}_{self.session_id}.jsonl"

    def _build_record(
        self,
        level: LogLevel,
        message: str,
        **context: Any,
    ) -> Dict[str, Any]:
        """Build a structured log record."""
        return {
            "timestamp": datetime.now().isoformat(),
            "level": level.name,
            "logger": self.name,
            "message": message,
            "context": context if context else None,
        }

    def _write_log(self, record: Dict[str, Any]) -> None:
        """Write log record to files."""
        # Plain text log
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                timestamp = record["timestamp"]
                level = record["level"]
                message = record["message"]
                f.write(f"[{timestamp}] {level}: {message}\n")
                if record["context"]:
                    f.write(f"  Context: {json.dumps(record['context'])}\n")
        except Exception as e:
            print(f"Error writing to log file: {e}", file=sys.stderr)

        # JSON log
        if self.json_output:
            try:
                with open(self.json_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(record) + "\n")
            except Exception as e:
                print(f"Error writing to JSON log file: {e}", file=sys.stderr)

    def log(self, level: LogLevel, message: str, **context: Any) -> None:
        """Generic log method."""
        if level.value >= self.log_level.value:
            record = self._build_record(level, message, **context)
            self._write_log(record)

    def debug(self, message: str, **context: Any) -> None:
        """Log DEBUG level."""
        self.log(LogLevel.DEBUG, message, **context)

    def info(self, message: str, **context: Any) -> None:
        """Log INFO level."""
        self.log(LogLevel.INFO, message, **context)

    def warning(self, message: str, **context: Any) -> None:
        """Log WARNING level."""
        self.log(LogLevel.WARNING, message, **context)

    def error(self, message: str, **context: Any) -> None:
        """Log ERROR level."""
        self.log(LogLevel.ERROR, message, **context)

    def critical(self, message: str, **context: Any) -> None:
        """Log CRITICAL level."""
        self.log(LogLevel.CRITICAL, message, **context)

    def scan_event(
        self,
        event: str,
        url: str,
        **details: Any,
    ) -> None:
        """Log a scan-related event."""
        self.info(
            f"Scan event: {event}",
            url=url,
            event=event,
            **details,
        )

    def vulnerability_found(
        self,
        url: str,
        param: str,
        context: str,
        payload: str,
        severity: str = "HIGH",
    ) -> None:
        """Log a discovered vulnerability."""
        self.info(
            f"Vulnerability found: XSS in {param}",
            url=url,
            parameter=param,
            context=context,
            payload=payload,
            severity=severity,
        )

    def get_log_file(self) -> str:
        """Get path to the log file."""
        return str(self.log_file)

    def get_json_file(self) -> str:
        """Get path to the JSON log file."""
        return str(self.json_file)


class PerformanceMetrics:
    """Track performance metrics for scans."""

    def __init__(self):
        self.start_time = datetime.now()
        self.payloads_tested = 0
        self.vulnerabilities_found = 0
        self.requests_made = 0
        self.errors = 0

    def record_payload_test(self) -> None:
        """Increment payload test counter."""
        self.payloads_tested += 1

    def record_vulnerability(self) -> None:
        """Increment vulnerability counter."""
        self.vulnerabilities_found += 1

    def record_request(self) -> None:
        """Increment request counter."""
        self.requests_made += 1

    def record_error(self) -> None:
        """Increment error counter."""
        self.errors += 1

    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        duration = (datetime.now() - self.start_time).total_seconds()
        return {
            "duration_seconds": duration,
            "payloads_tested": self.payloads_tested,
            "vulnerabilities_found": self.vulnerabilities_found,
            "requests_made": self.requests_made,
            "errors": self.errors,
            "payloads_per_second": (
                self.payloads_tested / duration if duration > 0 else 0
            ),
            "success_rate": (
                (self.vulnerabilities_found / self.payloads_tested * 100)
                if self.payloads_tested > 0
                else 0
            ),
        }
