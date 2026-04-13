"""
Unit tests for lib_logging module
"""

import pytest
import json
import tempfile
from pathlib import Path
from lib_logging import StructuredLogger, LogLevel, PerformanceMetrics


class TestStructuredLogger:
    """Test StructuredLogger class."""
    
    def test_logger_initialization(self):
        """Test logger initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = StructuredLogger("test", log_dir=tmpdir)
            
            assert logger.name == "test"
            assert logger.log_level == LogLevel.INFO
            assert Path(tmpdir).exists()
    
    def test_log_info(self):
        """Test logging at INFO level."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = StructuredLogger("test", log_dir=tmpdir)
            logger.info("Test message", key="value")
            
            # Check text log exists
            assert Path(logger.log_file).exists()
            with open(logger.log_file, "r") as f:
                content = f.read()
                assert "Test message" in content
                assert "INFO" in content
    
    def test_vulnerability_logging(self):
        """Test logging vulnerabilities."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = StructuredLogger("test", log_dir=tmpdir, json_output=True)
            logger.vulnerability_found(
                url="https://example.com",
                param="q",
                context="html",
                payload="<script>alert(1)</script>"
            )
            
            # Check JSON log
            assert Path(logger.json_file).exists()
            with open(logger.json_file, "r") as f:
                line = f.readline()
                record = json.loads(line)
                assert record["event_type"] == None or "Vulnerability" in record["message"]
    
    def test_log_levels(self):
        """Test different log levels."""
        with tempfile.TemporaryDirectory() as tmpdir:
            logger = StructuredLogger("test", log_dir=tmpdir, log_level=LogLevel.DEBUG)
            
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")
            
            with open(logger.log_file, "r") as f:
                content = f.read()
                assert "Debug message" in content
                assert "Info message" in content
                assert "Warning message" in content
                assert "Error message" in content


class TestPerformanceMetrics:
    """Test PerformanceMetrics class."""
    
    def test_metrics_initialization(self):
        """Test metrics initialization."""
        metrics = PerformanceMetrics()
        
        assert metrics.payloads_tested == 0
        assert metrics.vulnerabilities_found == 0
        assert metrics.requests_made == 0
    
    def test_increment_metrics(self):
        """Test incrementing metrics."""
        metrics = PerformanceMetrics()
        
        metrics.record_payload_test()
        metrics.record_payload_test()
        metrics.record_vulnerability()
        metrics.record_request()
        
        assert metrics.payloads_tested == 2
        assert metrics.vulnerabilities_found == 1
        assert metrics.requests_made == 1
    
    def test_metrics_summary(self):
        """Test getting metrics summary."""
        metrics = PerformanceMetrics()
        
        # Record some activity
        for _ in range(10):
            metrics.record_payload_test()
        
        metrics.record_vulnerability()
        metrics.record_vulnerability()
        
        summary = metrics.get_summary()
        
        assert summary["payloads_tested"] == 10
        assert summary["vulnerabilities_found"] == 2
        assert "duration_seconds" in summary
        assert "success_rate" in summary
        assert summary["success_rate"] == 20.0  # 2/10 * 100
