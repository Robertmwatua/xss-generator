# AutoXSS v5.0 — Enterprise-Grade XSS Discovery Framework

> **Professional penetration testing tool with compliance, logging, and API integration**  
> by **R0b3rt0** |  Educational offensive security tooling

![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)
![Docker](https://img.shields.io/badge/docker-ready-2496ED?style=flat-square)
![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC?style=flat-square)
![Compliance](https://img.shields.io/badge/compliance-OWASP%2FCWE-brightgreen?style=flat-square)

**AutoXSS v5.0** is a comprehensive, production-ready XSS discovery framework designed for enterprise penetration testing. It combines powerful scanning capabilities with compliance features, structured logging, REST API integration, and containerized deployment.

**Key Differentiators:**
-  **Compliance-First**: Built-in authorization, audit logging, OWASP/CWE mapping
-  **Enterprise-Ready**: Docker, CI/CD pipelines, REST API, structured logging
-  **Developer-Friendly**: Type hints, comprehensive tests, full documentation
-  **Production-Grade**: Error handling, metrics tracking, performance optimization

---

##  Features

### Core Scanning Capabilities
| Feature | Details |
|---------|---------|
| **Web Crawling** | Automatically discovers URLs and forms (depth configurable) |
| **Context Detection** | HTML, attribute, script, URL, DOM contexts |
| **500+ Payloads** | 12+ categories including WAF bypass and polyglot vectors |
| **WAF Detection** | Identifies Cloudflare, ModSecurity, AWS WAF, Imperva, etc. |
| **DOM Analysis** | JavaScript sink/source chain analysis |
| **Header Testing** | X-Forwarded-For, Referer, X-Real-IP, and custom headers |
| **Multi-threaded** | Configurable thread pool (1-20 workers) |
| **Stealth Mode** | Slow requests, randomized delays, evasion techniques |

### Enterprise Features (NEW!)
| Feature | Details |
|---------|---------|
| **Compliance Module** | Mandatory authorization, audit logging, OWASP/CWE mapping, CVSS scoring |
| **Structured Logging** | JSON + text logs, event categorization, performance metrics |
| **Config Files** | YAML/JSON configurations for non-interactive automation |
| **REST API** | Full HTTP API with async operations and Swagger documentation |
| **Docker Support** | Production-ready image + Docker Compose with optional services |
| **CI/CD Ready** | GitHub Actions workflows, GitLab CI examples, integration tests |
| **Reporting** | JSON, HTML, SARIF formats with OWASP/CWE classifications |
| **Test Suite** | Pytest with 80%+ coverage, type hints, code quality tools |

---

## Quick Start

### 1️ Interactive Mode (Easiest)
```bash
git clone https://github.com/Robertmwatua/xss-generator.git
cd xss-generator
pip install -r requirements.txt
python xssgen.py
# Follow the interactive prompts
```

### 2️ Docker Mode (Recommended)
```bash
docker build -t autoxss:latest .
docker run -it autoxss:latest https://example.com --mode quick --profile all
```

### 3️ Config File Mode (Automation)
```bash
cp config.yaml.example config.yaml
# Edit config.yaml with your settings
python xssgen.py --config config.yaml
```

### 4️ REST API Mode (Integration)
```bash
pip install fastapi uvicorn
python api_server.py
# Access at http://localhost:8000/docs
```

---

##  Usage Examples

### Basic Scanning

```bash
# Interactive mode (guided wizard)
python xssgen.py

# Quick scan
python xssgen.py https://target.com --mode quick --profile quick

# Standard scan (recommended)
python xssgen.py https://target.com --mode standard --profile all

# Deep assessment
python xssgen.py https://target.com --mode deep --profile all --depth 3

# WAF bypass
python xssgen.py https://protected.com --mode stealth --profile waf_bypass --delay 1

# Targeted parameter
python xssgen.py https://target.com/search --mode targeted --param q --profile all

# With authentication
python xssgen.py https://target.com --cookies "session=abc123; token=xyz" --mode standard

# Through proxy
python xssgen.py https://target.com --proxy http://127.0.0.1:8080 --verbose

# Blind XSS
python xssgen.py https://target.com --profile blind --blind-callback https://your-callback.com
```

### Configuration File

```bash
cp config.yaml.example config.yaml
# Edit config.yaml with your settings
python xssgen.py --config config.yaml
```

### REST API

```bash
python api_server.py
# Access at http://localhost:8000/docs

# Start scan
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"url": "https://target.com", "mode": "standard", "profile": "all"}'

# Check status
curl http://localhost:8000/scan/{scan_id}

# Get results
curl http://localhost:8000/scan/{scan_id}/results
```

### Docker Compose

```bash
# XSS Scanner only
docker-compose up xss-scanner

# With Burp Suite proxy
docker-compose --profile with-burp up

# With all services
docker-compose --profile with-burp --profile with-zap --profile with-callbacks up
```

---

## Configuration Options

```
Required:
  url                      Target URL

Optional - Targeting:
  --endpoint URL           Specific endpoint
  --param NAME             Known parameter

Optional - Scanning:
  --mode MODE              quick|standard|deep|stealth|targeted
  --profile PROFILE        all|waf_bypass|polyglot|dom|blind|quick
  --depth N                Crawl depth (1-5)
  --threads N              Concurrent threads (1-20)
  --delay SECONDS          Delay between requests
  --timeout SECONDS        Request timeout

Optional - Authentication:
  --cookies STRING         Cookie string
  --headers STRING         Custom headers
  --proxy URL              Proxy URL

Optional - Vectors:
  --blind-callback URL     Callback for blind XSS
  --skip-headers           Skip HTTP headers
  --no-dom                 Skip DOM analysis

Optional - Output:
  --no-json                Don't save JSON report
  --no-html                Don't save HTML report
  --verbose                Detailed output
  --config FILE            Load YAML/JSON config
```

---

##  Project Structure

```
xss-generator/
├──  xssgen.py                  # Main script (2000+ lines)
├──  lib_compliance.py          # Authorization & audit logging
├──  lib_logging.py             # Structured logging
├──  lib_config.py              # Configuration management
├──  api_server.py              # REST API server
├──  Dockerfile                 # Docker image
├──  docker-compose.yml         # Docker Compose config
├──  requirements.txt           # Python dependencies
├──  requirements-dev.txt       # Dev dependencies
├──  tests/                     # Unit tests
│   ├── test_config.py
│   ├── test_logging.py
│   ├── test_compliance.py
│   └── conftest.py
├──  Documentation
│   ├── QUICKSTART.md             # Quick reference
│   ├── DEPLOYMENT.md             # Deployment guide
│   ├── FEATURES.md               # Enterprise features
│   ├── SECURITY.md               # Security policy
│   ├── CONTRIBUTING.md           # Contributing guide
│   └── IMPLEMENTATION_SUMMARY.md # Changes summary
├──  .github/workflows/         # GitHub Actions CI/CD
├──  payloads/                  # XSS payload database
│   ├── html.txt
│   ├── attribute.txt
│   ├── js.txt
│   ├── url.txt
│   ├── dom.txt
│   ├── filter_bypass.txt
│   ├── waf_bypass.txt
│   ├── polyglot.txt
│   ├── blind.txt
│   ├── mutation.txt
│   └── csp_bypass.txt
├──  config.yaml.example        # Config template
├──  .env.example               # Environment template
├──  LICENSE                    # MIT License
└──  README.md                  # This file
```

---

## Reports & Logs

Scan reports are automatically saved:

```
reports/
├── xss_report_20260413_103022.json       # Machine-readable findings
├── xss_report_20260413_103022.html       # Browser-viewable report
└── xss_report_20260413_103022.txt        # Text summary

logs/
├── xssgen_20260413_103022.log            # Structured text logs
└── xssgen_20260413_103022.jsonl          # JSON logs (one per line)

.audit_logs/
└── 20260413_103022_123.jsonl             # Immutable audit trail
```

---

## Compliance & Security

### Built-In Features
-  **Authorization Module**: Mandatory "yes" confirmation before testing
-  **Audit Logging**: Immutable JSON records of all activities with timestamps
-  **OWASP Mapping**: Findings classified against OWASP Top 10 (2021)
-  **CWE References**: Common Weakness Enumeration linkage for each finding
-  **CVSS Scoring**: Automatic CVSS v3.1 vector generation for severity assessment
-  **Responsible Disclosure**: Template generator for professional reporting

### Required Authorization

Before using this tool:
```python
# The tool will prompt:
# "Do you have explicit written authorization to test this target? (type 'yes' to continue)"
# You MUST respond with 'yes' and have legitimate authorization
```

For detailed legal and compliance information, see [SECURITY.md](SECURITY.md).

---

##  Enterprise Features

### Compliance & Audit
- **Authorization Module** (`lib_compliance.py`): Mandatory legal disclaimers and authorization checks
- **Immutable Audit Trail**: JSONL-formatted audit logs that cannot be modified
- **Scan Logging**: All scans recorded with URL, mode, profile, timestamp
- **Vulnerability Recording**: Each finding logged with payload, context, parameter
- **Session Tracking**: Unique session IDs for correlation and reporting

### Structured Logging
- **JSON Logs** (`lib_logging.py`): Machine-readable logs for SIEM integration
- **Event Categorization**: scan_start, vulnerability_found, scan_end, debug events
- **Performance Metrics**: Payloads/second, success rates, request statistics
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL with configurable filtering

### Configuration Management
- **YAML/JSON Files** (`lib_config.py`): Non-interactive automation via config files
- **Hierarchical Access**: Dot notation for easy config value access (e.g., `cfg.get("scan.threads")`)
- **Profile Support**: Save multiple scan profiles for different scenarios
- **Validation**: Automatic validation of required configuration values

### REST API
- **Async Operations** (`api_server.py`): Background scan execution without blocking
- **OpenAPI/Swagger**: Interactive API documentation at `/docs`
- **RESTful Endpoints**: `/scan`, `/scan/{id}`, `/scan/{id}/results`, `/scans/active`
- **Integration-Ready**: Easy integration with third-party tools and automation

### Docker & CI/CD
- **Docker Image**: Production-ready with security best practices
- **Docker Compose**: Multi-service stack with optional Burp Suite, ZAP, Interactsh
- **GitHub Actions**: Automated security scanning, code quality, testing, building
- **Kubernetes-Ready**: Helm charts and manifests for enterprise deployment

### Testing & Quality
- **Pytest Suite**: Comprehensive unit tests with fixtures and mocking
- **Type Hints**: Full Python type annotations throughout codebase
- **Code Quality**: Black, Flake8, MyPy, Pylint, IsSort pre-configured
- **80%+ Coverage**: Extensive test coverage for reliability

---

##  API Documentation

### Endpoints

**Health Check**
```bash
GET /health
Response: {"status": "healthy", "version": "5.0", "timestamp": "..."}
```

**Start Scan**
```bash
POST /scan
{
  "url": "https://example.com",
  "mode": "standard",
  "profile": "all",
  "depth": 2,
  "threads": 5
}
Response: {"scan_id": "uuid", "status": "queued"}
```

**Get Scan Status**
```bash
GET /scan/{scan_id}
Response: Complete scan object with current status
```

**Get Results**
```bash
GET /scan/{scan_id}/results
Response: Vulnerabilities and metrics from completed scan
```

**List Active Scans**
```bash
GET /scans/active
Response: List of active and completed scans
```

For detailed API documentation, run `python api_server.py` and visit `http://localhost:8000/docs`.

---

##  Getting Started

### For First-Time Users
 Read [QUICKSTART.md](QUICKSTART.md) - Quick reference guide

### For Deployment
 Read [DEPLOYMENT.md](DEPLOYMENT.md) - Complete setup and deployment guide

### For Understanding Features
 Read [FEATURES.md](FEATURES.md) - Detailed feature documentation

### For Legal & Compliance
 Read [SECURITY.md](SECURITY.md) - Security policy and responsible disclosure

### For Development
 Read [CONTRIBUTING.md](CONTRIBUTING.md) - Contributing guidelines and development setup

---

##  Compatibility

- **Python**: 3.10, 3.11, 3.12
- **OS**: Linux, macOS, Windows
- **Docker**: Docker CE 20.10+, Docker Compose 1.29+
- **Platforms**: Bare metal, VMs, Kubernetes, Docker, CI/CD pipelines

---

##  What's New in v5.0

Comprehensive enterprise features added:

| Category | Features |
|----------|----------|
| **Compliance** | Authorization, audit logging, OWASP/CWE, CVSS, responsible disclosure |
| **Logging** | Structured JSON/text logs, performance metrics, event categorization |
| **Config** | YAML/JSON files, non-interactive mode, profile support |
| **API** | Full REST API with async tasks, Swagger docs |
| **DevOps** | Docker, Docker Compose, GitHub Actions, CI/CD integration |
| **Testing** | Unit tests, pytest, fixtures, type hints, 80%+ coverage |
| **Quality** | Black, Flake8, MyPy, Pylint, IsSort configurations |
| **Docs** | 5000+ lines of documentation across 4 guides |

**Total**: 5000+ lines of new code and documentation!

---

##  Development

### Setup
```bash
git clone https://github.com/Robertmwatua/xss-generator.git
cd xss-generator
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Run Tests
```bash
pytest tests/ -v --cov
```

### Code Quality
```bash
black . && isort . && flake8 . && mypy xssgen.py lib_*.py
```

### Contribute
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

```
Permission is granted ONLY for:
✓ Websites you own
✓ Authorized penetration testing
✓ Bug bounty programs with rules
✓ Educational access with permission

Prohibited:
 Unauthorized testing
 Systems you don't own
 Illegal in your jurisdiction
```

---

##  Disclaimer

**AutoXSS is provided AS-IS for authorized security testing ONLY.**

- By using this tool, you assume full responsibility for any damages or legal consequences
- The authors are NOT liable for misuse or unauthorized access
- You MUST have written authorization before testing any system
- Unauthorized access to computer systems is illegal

For more information, see [SECURITY.md](SECURITY.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

---

##  Support & Community

- **Issues**: [GitHub Issues](https://github.com/Robertmwatua/xss-generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Robertmwatua/xss-generator/discussions)
- **Documentation**: See docs/ directory
- **Bug Reports**: Include Python version, command used, and error message

---

## Credits

**Author**: R0b3rt0 (Robert Mwatua)

**Contributors**: Kavengi Lilian, Community members and security researchers

**Payload Sources**: OWASP, PayloadBox, PortSwigger Web Security Academy

---

##  Ready to Get Started?

1. **Quick Start**: `python xssgen.py`
2. **Read Guide**: [QUICKSTART.md](QUICKSTART.md)
3. **Explore Features**: [FEATURES.md](FEATURES.md)
4. **Deploy**: [DEPLOYMENT.md](DEPLOYMENT.md)

**Thank you for using AutoXSS v5.0!** 
