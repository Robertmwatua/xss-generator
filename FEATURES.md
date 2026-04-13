# AutoXSS v5.0 - Enterprise Features

## Overview

AutoXSS is now an enterprise-grade XSS discovery framework with compliance, logging, API integration, and security best practices built-in.

## Compliance & Legal

### Authorization Module
- **Mandatory Disclaimer**: Legal warnings on startup
- **Authorization Check**: Requires explicit "yes" confirmation
- **Audit Logging**: All scans recorded with timestamps
- **Responsible Disclosure**: Template generator for reporting findings

### OWASP/CWE Mapping
- **OWASP Top 10 (2021)** classification
- **CWE References**: CVE mapping for findings
- **CVSS v3.1 Scoring**: Automatic vulnerability severity calculation
- **Risk Assessment**: Evidence-based severity ratings

```python
from lib_compliance import OWASPMapper

# Get OWASP classification
info = OWASPMapper.get_owasp_info("xss")
# Returns: {
#   "owasp": "A03:2021 – Injection",
#   "cwe": ["CWE-79: Improper Neutralization..."],
#   "cvss_base": 6.1
# }

# Generate CVSS vector
cvss = OWASPMapper.get_cvss_string("xss", "reflected")
# Returns: "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N"
```

## Audit & Logging

### Structured Logging
- **JSON Format**: Machine-readable logs for SIEM integration
- **Multiple Outputs**: Both text and JSON simultaneously
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Categorized Events**: scan_start, scan_end, vulnerability_found, etc.

```python
from lib_logging import StructuredLogger

logger = StructuredLogger("scanner")
logger.vulnerability_found(
    url="https://example.com/search",
    param="q",
    context="html",
    payload="<script>alert(1)</script>",
    severity="HIGH"
)
# Creates entries in both:
# - logs/scanner_YYYYMMDD_HHMMSS.log (text)
# - logs/scanner_YYYYMMDD_HHMMSS.jsonl (JSON)
```

### Audit Trail
- **Immutable Logging**: One JSONL file per session
- **Session Tracking**: Unique session ID for correlation
- **Compliance Records**: Who ran what, when, against whom
- **Evidence Preservation**: For pen testing reports

```python
from lib_compliance import ComplianceManager

compliance = ComplianceManager()
compliance.log_scan_start(
    url="https://target.com",
    mode="standard",
    profile="all"
)
compliance.log_vulnerability(
    url="https://target.com/search",
    param="q",
    payload="<script>alert(1)</script>",
    context="html"
)
compliance.log_scan_end({"duration": 45.2, "findings": 3})

# Audit trail in .audit_logs/YYYYMMDD_HHMMSS_SSS.jsonl
```

### Performance Metrics
- **Scan Duration**: Total time, per-request averages
- **Payload Throughput**: Payloads/second tested
- **Success Rate**: Percentage of payloads that triggered vulnerabilities
- **Request Statistics**: Total requests, timeouts, errors

```python
from lib_logging import PerformanceMetrics

metrics = PerformanceMetrics()
metrics.record_payload_test()
metrics.record_vulnerability()

summary = metrics.get_summary()
# {
#   "duration_seconds": 45.2,
#   "payloads_tested": 500,
#   "vulnerabilities_found": 3,
#   "requests_made": 510,
#   "payloads_per_second": 11.05,
#   "success_rate": 0.6
# }
```

## Configuration Management

### YAML/JSON Config Files
- **Non-Interactive Mode**: Automate scans without prompts
- **Profile Support**: Save multiple config profiles
- **Version Control**: Check configs into git
- **Dot Notation**: Hierarchical config access

```python
from lib_config import ConfigManager

# Load from file
cfg = ConfigManager("config.yaml")

# Get values with dot notation
url = cfg.get("target.url")
mode = cfg.get("scan.mode")
threads = cfg.get("scan.threads")

# Modify and save
cfg.set("scan.threads", 10)
cfg.save_config("config-updated.yaml", format="yaml")

# Validate configuration
is_valid, errors = cfg.validate()
```

### Config File Format

```yaml
target:
  url: "https://example.com"
  endpoint: null
  known_param: null

scan:
  mode: "standard"           # quick|standard|deep|stealth|targeted
  profile: "all"             # all|waf_bypass|polyglot|dom|blind|quick
  depth: 2
  threads: 5
  delay: 0
  timeout: 10

auth:
  cookies: "session=abc123"
  headers: null
  proxy: "http://127.0.0.1:8080"

vectors:
  blind_callback: null
  skip_headers: false
  test_dom: true

output:
  verbose: false
  save_json: true
  save_html: true
  save_text: true

compliance:
  require_authorization: true
  audit_log: true
```

## REST API Interface

### API Server
- **Full REST API**: HTTP endpoints for all scanning functions
- **Async Operations**: Background task queue for scans
- **Swagger UI**: Interactive API documentation
- **OpenAPI Spec**: For client code generation

### Running the API Server

```bash
pip install fastapi uvicorn
python api_server.py

# Access at http://localhost:8000
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### API Endpoints

#### Health Check
```bash
GET /health
# Response: {"status": "healthy", "version": "5.0", "timestamp": "..."}
```

#### Start Scan
```bash
POST /scan
Content-Type: application/json

{
  "url": "https://example.com",
  "mode": "standard",
  "profile": "all",
  "depth": 2,
  "threads": 5
}

# Response: {"scan_id": "uuid", "status": "queued"}
```

#### Get Scan Status
```bash
GET /scan/{scan_id}
# Response: {"scan_id": "...", "status": "running", "target_url": "..."}
```

#### Get Results
```bash
GET /scan/{scan_id}/results
# Response: Complete scan results with vulnerabilities
```

#### List Active Scans
```bash
GET /scans/active
# Response: {"active_scans": 3, "completed_scans": 15, "scans": [...]}
```

### Client Integration Example

```python
import requests

api = "http://localhost:8000"

# Start scan
response = requests.post(f"{api}/scan", json={
    "url": "https://target.com",
    "mode": "quick",
    "profile": "all"
})
scan_id = response.json()["scan_id"]

# Poll for status
import time
while True:
    status = requests.get(f"{api}/scan/{scan_id}").json()
    if status["status"] == "completed":
        break
    print(f"Status: {status['status']}")
    time.sleep(2)

# Get results
results = requests.get(f"{api}/scan/{scan_id}/results").json()
print(f"Found {len(results['vulnerabilities'])} vulnerabilities")
```

## Docker & Containerization

### Docker Image
- **Lightweight**: Python 3.11-slim base (≈200MB)
- **Security**: Non-root user (scanner:1000)
- **Health Checks**: Built-in endpoint monitoring
- **Volumes**: Pre-mounted for reports and logs

### Docker Compose Stack

```yaml
services:
  xss-scanner:      # Main scanning service
  burp-proxy:       # Burp Suite (optional)
  zap-api:         # OWASP ZAP (optional)
  interactsh:      # Blind XSS callback server (optional)
```

### Usage

```bash
# Basic: XSS Scanner only
docker-compose up xss-scanner

# With Burp proxy
docker-compose --profile with-burp up

# With all services
docker-compose --profile with-burp --profile with-zap up

# Run specific command
docker run autoxss:latest \
  https://target.com \
  --mode quick \
  --profile all

# Interactive mode
docker run -it autoxss:latest
```

## CI/CD Integration

### GitHub Actions
- **Security Scanning**: Automatic XSS testing on push/PR
- **Code Quality**: Linting, type checking, security audit
- **Testing**: Pytest with coverage reporting
- **Docker Build**: Automated image creation
- **Integration Tests**: Against test servers

### Configuration

`.github/workflows/security-ci.yml` includes:
- Flake8 linting
- MyPy type checking
- Bandit security audit
- Pytest unit tests
- Code coverage tracking
- Docker image building
- Integration testing

### Usage in CI

```yaml
# .github/workflows/my-workflow.yml
name: Security Tests

on: [push, pull_request]

jobs:
  xss-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: python xssgen.py https://myapp.com --mode quick
      - uses: actions/upload-artifact@v3
        with:
          name: reports
          path: reports/
```

## Testing Framework

### Unit Tests
- **Pytest**: Comprehensive test suite
- **Coverage**: 80%+ code coverage tracking
- **Fixtures**: Reusable test data
- **Integration Tests**: Test against real servers

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/test_config.py::TestConfigManager::test_default_config

# Run slow tests only
pytest -m slow
```

### Test Files
- `tests/test_config.py`: Configuration module tests
- `tests/test_logging.py`: Logging module tests
- `tests/test_compliance.py`: Compliance module tests
- `tests/conftest.py`: Pytest fixtures and configuration

## Reporting & Export

### Report Formats
- **JSON**: Machine-readable, structured findings
- **HTML**: Interactive, browser-viewable report
- **Text**: Human-readable summary
- **SARIF**: GitHub Security scanning format

### Report Contents
- Executive summary
- Vulnerability details (URL, parameter, payload)
- OWASP/CWE classifications
- CVSS scores and vectors
- Screenshots/PoC details
- Remediation recommendations

### JSON Report Structure

```json
{
  "scan_id": "uuid",
  "timestamp": "2026-04-13T10:30:00Z",
  "target": "https://example.com",
  "summary": {
    "total_requests": 500,
    "vulnerabilities_found": 3,
    "duration_seconds": 45.2
  },
  "vulnerabilities": [
    {
      "url": "https://example.com/search",
      "parameter": "q",
      "payload": "<script>alert(1)</script>",
      "context": "html",
      "severity": "HIGH",
      "cvss": "6.1",
      "owasp": "A03:2021",
      "cwe": ["CWE-79"]
    }
  ]
}
```

## Development Features

### Type Hints
- **Modern Python**: Full type annotations
- **MyPy Check**: Static type verification
- **IDE Support**: Better autocomplete and error detection

```python
def scan_url(url: str, payloads: List[str]) -> List[Vulnerability]:
    """Scan URL with payloads.
    
    Args:
        url: Target URL
        payloads: List of XSS payloads to test
    
    Returns:
        List of discovered vulnerabilities
    """
```

### Code Quality Tools
- **Black**: Code formatting
- **Flake8**: Style checking
- **Pylint**: Advanced linting
- **IsSort**: Import organization

```bash
# Format code
black .

# Check types
mypy xssgen.py lib_*.py

# Security audit
bandit -r .

# All checks
black . && isort . && flake8 . && mypy xssgen.py lib_*.py
```

### Project Metadata

`pyproject.toml` includes:
- Package metadata
- Dependency specifications
- Tool configurations (black, mypy, pytest, etc.)
- Entry points for CLI commands

## Performance Optimizations

### Multi-threading
- Configurable thread pool (1-20 workers)
- Efficient request batching
- Non-blocking I/O

### Payload Optimization
- Smart deduplication
- Context-aware selection
- Encoding variations

### Caching
- Session reuse
- Request caching
- Response analysis optimization

## Security Best Practices

### Built-In
1. **Authorization**: Mandatory confirmation for testing
2. **Audit Trail**: Immutable logging of all activities
3. **Compliance**: OWASP/CWE mappings
4. **Secure Defaults**: TLS verification enabled

### Recommended
1. Use HTTPS only
2. Test with separate accounts
3. Review audit logs
4. Encrypt sensitive reports
5. Secure your API server (add auth, rate limiting)

## Enterprise Features Summary

| Feature | Tier | Details |
|---------|------|---------|
| XSS Discovery | Core | 500+ payloads, multiple contexts |
| Configuration Files | Standard | YAML/JSON support |
| Structured Logging | Standard | JSON + text logs |
| Audit Trail | Compliance | Immutable audit records |
| REST API | Integration | Full API with docs |
| Docker | DevOps | Containerized, docker-compose |
| CI/CD | DevOps | GitHub Actions, GitLab CI |
| Testing | Quality | 80%+ coverage, pytest |
| Type Hints | Quality | Full type annotations |
| OWASP/CWE | Reporting | Standard classifications |
| Responsible Disclosure | Legal | Template generator |

---

For detailed usage guides, see:
- [DEPLOYMENT.md](DEPLOYMENT.md) - Setup and deployment
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guide
- [README.md](README.md) - Overview and features
