#  Quick Start Guide

Welcome to **AutoXSS v5.0** - Your enterprise-grade XSS discovery framework!

## First Time? Start Here

### 1 Installation (Choose One)

#### Option A: Python (Simplest)
```bash
pip install -r requirements.txt
python xssgen.py
```

#### Option B: Docker (Recommended)
```bash
docker build -t autoxss:latest .
docker run -it autoxss:latest https://example.com --mode quick
```

#### Option C: Docker Compose (Full Stack)
```bash
docker-compose up xss-scanner
```

### 2 Your First Scan

#### Interactive Mode
```bash
python xssgen.py
# Follow the prompts
```

#### Quick Scan
```bash
python xssgen.py https://target.com --mode quick --profile all
```

#### Config File Mode
```bash
cp config.yaml.example config.yaml
# Edit config.yaml with your settings
python xssgen.py --config config.yaml
```

---

## Documentation Map

**Choose your path:**

### "I want to scan targets"
→ [DEPLOYMENT.md](DEPLOYMENT.md) - Configuration and usage

### "I need compliance & legal info"
→ [SECURITY.md](SECURITY.md) - Authorization and responsible disclosure

### "I want to integrate/automate"
→ [FEATURES.md](FEATURES.md) - REST API and integration

### "I want to develop/contribute"
→ [CONTRIBUTING.md](CONTRIBUTING.md) - Development setup and guidelines

### "Tell me about the improvements"
→ [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - What was added

---

## Common Tasks

### Run Quick Scan
```bash
python xssgen.py https://example.com --mode quick --profile quick
```

### Run With Configuration File
```bash
cp config.yaml.example my-scan.yaml
# Edit my-scan.yaml
python xssgen.py --config my-scan.yaml
```

### Use REST API
```bash
python api_server.py
# Open http://localhost:8000/docs in browser
```

### Run Tests
```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

### Check Code Quality
```bash
black xssgen.py lib_*.py
flake8 .
mypy xssgen.py lib_*.py
```

### View Audit Trail
```bash
cat .audit_logs/*.jsonl | python -m json.tool
```

---

## Key Features

### Compliance
- Legal disclaimer system
- Audit logging (immutable)
- OWASP/CWE mapping
- CVSS scoring

### Logging
- JSON + text logs
- Structured output
- Performance metrics
- Event tracking

### Configuration
- YAML/JSON files
- Non-interactive mode
- Multiple profiles
- Environment variables

### API
- REST endpoints
- Async operations
- Swagger UI
- Integration-ready

### DevOps
- Docker image
- Docker Compose
- GitHub Actions
- Kubernetes-ready

---

## Configuration Methods

### 1. Interactive Wizard (Default)
```bash
python xssgen.py
```

### 2. Configuration File
```bash
python xssgen.py --config config.yaml
```

### 3. Command Line Arguments
```bash
python xssgen.py https://target.com --mode deep --threads 10 --timeout 15
```

### 4. Environment Variables
```bash
export TARGET_URL=https://example.com
export SCAN_MODE=standard
python xssgen.py
```

---

## Reports & Logs

### Find Your Reports
```
reports/                    # Generated scan reports
├── xss_report_*.json      # Machine-readable results
├── xss_report_*.html      # Browser-viewable report
└── xss_report_*.txt       # Text summary

logs/                       # Scan logs
├── xssgen_*.log           # Text logs
└── xssgen_*.jsonl         # JSON logs (one per line)

.audit_logs/                # Compliance records
└── YYYYMMDD_HHMMSS_SSS.jsonl  # Immutable audit trail
```

### Example: View Findings
```bash
# See all vulnerabilities found
cat reports/xss_report_*.json | python -m json.tool

# Pretty-print audit trail
cat .audit_logs/*.jsonl | python -m json.tool

# Search logs
grep "vulnerability_found" logs/*.jsonl
```

---

## Security Notes

  **IMPORTANT:**
1.  **Get written authorization** before testing
2.  **Type "yes"** when prompted to confirm authorization
3.  **Keep audit trails** for compliance
4.  **Use HTTPS** only
5.  **Secure your reports** - they contain sensitive data

---

## Troubleshooting

### "Authorization DENIED"
```
Solution: Type "yes" when prompted for authorization confirmation
```

### "Module not found"
```bash
Solution: pip install -r requirements.txt
```

### "Permission denied" (Docker)
```bash
Solution: sudo usermod -aG docker $USER && newgrp docker
```

### "SSL certificate error"
```bash
# Use with caution (dev only):
python xssgen.py https://self-signed.example.com --no-verify
```

---

## Tips & Tricks

### Profile Your Target
```bash
# Quick check
python xssgen.py https://target.com --mode quick

# If found vulnerabilities, run deeper scan
python xssgen.py https://target.com --mode deep --profile all
```

### Test With Proxy
```bash
# Route through Burp Suite for deeper inspection
python xssgen.py https://target.com --proxy http://127.0.0.1:8080 --verbose
```

### Automate Scans
```bash
# Create a schedule with cron (Unix) or Task Scheduler (Windows)
# Example: Run daily scan at 2 AM
0 2 * * * cd /app && python xssgen.py --config daily-scan.yaml
```

### Integrate With CI/CD
```yaml
# GitHub Actions example
- name: Run XSS Scan
  run: |
    pip install -r requirements.txt
    python xssgen.py https://myapp.com --mode quick
```

---

## Need Help?

- **Documentation**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Examples**: Look in `config.yaml.example`
- **Security Issues**: Read [SECURITY.md](SECURITY.md)
- **Development**: Check [CONTRIBUTING.md](CONTRIBUTING.md)
- **GitHub**: Open an issue on the repository

---

## What's New in v5.0

AutoXSS v5.0 adds enterprise features:

| Feature | Purpose |
|---------|---------|
|  **Compliance Module** | Legal authorization & audit trails |
|  **Structured Logging** | JSON + text logs for integration |
|  **Config Files** | YAML/JSON non-interactive scanning |
|  **REST API** | Automated integration endpoint |
|  **Docker** | Containerized deployment |
|  **CI/CD** | GitHub Actions workflows |
|  **Tests** | Comprehensive test suite |
|  **Documentation** | Deployment, security, development guides |

**Total**: 5000+ lines of new code and documentation!

---

## Next Steps

1. **Run first scan**: `python xssgen.py` → Follow prompts
2. **Check results**: `cat reports/xss_report_*.json`
3. **Review logs**: `tail -f logs/xssgen_*.log`
4. **Read docs**: [DEPLOYMENT.md](DEPLOYMENT.md) for advanced usage
5. **Configure**: Copy `config.yaml.example` → customize → reuse

---

**Thank you for using AutoXSS!** 

For more information, visit:
-  [README.md](README.md) - Overview
-  [DEPLOYMENT.md](DEPLOYMENT.md) - Setup & usage
-  [FEATURES.md](FEATURES.md) - Enterprise features
-  [SECURITY.md](SECURITY.md) - Legal & compliance
-  [CONTRIBUTING.md](CONTRIBUTING.md) - Development
