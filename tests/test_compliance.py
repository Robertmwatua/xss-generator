"""
Unit tests for lib_compliance module
"""

import pytest
import json
import tempfile
from pathlib import Path
from lib_compliance import ComplianceManager, OWASPMapper, ResponsibleDisclosureTemplate


class TestComplianceManager:
    """Test ComplianceManager class."""
    
    def test_compliance_initialization(self):
        """Test compliance manager initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            comp = ComplianceManager(audit_log_dir=tmpdir)
            
            assert comp.session_id is not None
            assert Path(tmpdir).exists()
    
    def test_audit_logging(self):
        """Test audit logging functionality."""
        with tempfile.TemporaryDirectory() as tmpdir:
            comp = ComplianceManager(audit_log_dir=tmpdir)
            
            comp.log_audit("test_event", {"key": "value"})
            
            # Check audit file exists
            audit_file = Path(tmpdir) / f"{comp.session_id}.jsonl"
            assert audit_file.exists()
            
            # Verify content
            with open(audit_file, "r") as f:
                line = f.readline()
                record = json.loads(line)
                assert record["event_type"] == "test_event"
                assert record["details"]["key"] == "value"
    
    def test_scan_logging(self):
        """Test scan-specific logging."""
        with tempfile.TemporaryDirectory() as tmpdir:
            comp = ComplianceManager(audit_log_dir=tmpdir)
            
            comp.log_scan_start(
                url="https://example.com",
                mode="quick",
                profile="all"
            )
            
            audit_trail = comp.get_audit_trail()
            assert len(audit_trail) > 0
            assert audit_trail[0]["event_type"] == "scan_start"
    
    def test_vulnerability_logging(self):
        """Test vulnerability logging."""
        with tempfile.TemporaryDirectory() as tmpdir:
            comp = ComplianceManager(audit_log_dir=tmpdir)
            
            comp.log_vulnerability(
                url="https://example.com/search",
                param="q",
                payload="<script>alert(1)</script>",
                context="html"
            )
            
            audit_trail = comp.get_audit_trail()
            assert any(r["event_type"] == "vulnerability_found" for r in audit_trail)


class TestOWASPMapper:
    """Test OWASPMapper class."""
    
    def test_get_owasp_info(self):
        """Test getting OWASP classification."""
        info = OWASPMapper.get_owasp_info("xss")
        
        assert "owasp" in info
        assert "A03:2021" in info["owasp"]
        assert "cwe" in info
    
    def test_cvss_string(self):
        """Test CVSS vector generation."""
        cvss = OWASPMapper.get_cvss_string("xss")
        
        assert cvss.startswith("CVSS:3.1")
        assert "AV:N" in cvss  # Network accessible
        assert "AC:L" in cvss  # Low complexity
    
    def test_cwe_list(self):
        """Test CWE retrieval."""
        cwes = OWASPMapper.get_cwe_list("xss")
        
        assert len(cwes) > 0
        assert "CWE-79" in cwes[0]


class TestResponsibleDisclosureTemplate:
    """Test ResponsibleDisclosureTemplate class."""
    
    def test_template_generation(self):
        """Test template generation."""
        vulnerabilities = [
            {
                "url": "https://example.com/search",
                "parameter": "q",
                "severity": "HIGH"
            }
        ]
        
        template = ResponsibleDisclosureTemplate.generate_template(
            target_url="https://example.com",
            vulnerabilities=vulnerabilities,
            findings_date="2026-04-13"
        )
        
        assert "RESPONSIBLE DISCLOSURE REPORT" in template
        assert "https://example.com" in template
        assert "OWASP" in template
        assert "CWE" in template
