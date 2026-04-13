# Deployment & Setup Guide

## Quick Start

### Option 1: Direct Python Installation

```bash
# Clone repository
git clone https://github.com/Robertmwatua/xss-generator.git
cd xss-generator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run interactive wizard
python xssgen.py

# Or use config file
python xssgen.py --config config.yaml
```

### Option 2: Docker (Recommended)

```bash
# Build image
docker build -t autoxss:latest .

# Run basic scan
docker run --rm autoxss:latest https://example.com --mode quick

# Interactive mode (edit docker-compose first to enable)
docker-compose run --rm xss-scanner

# With all optional services
docker-compose --profile with-burp --profile with-zap up
```

### Option 3: Docker Compose

```bash
# Copy example if you haven't already
cp docker-compose.yml docker-compose.override.yml

# Start XSS Scanner + Burp + ZAP
docker-compose --profile with-burp --profile with-zap up -d

# View logs
docker-compose logs -f xss-scanner

# Stop
docker-compose down
```

## Configuration Methods

### 1. Interactive Wizard (Default)

```bash
python xssgen.py
# Follow prompts to configure scan
```

### 2. Configuration File

```bash
# Copy example
cp config.yaml.example config.yaml

# Edit config.yaml with your settings
nano config.yaml

# Run with config
python xssgen.py --config config.yaml
```

### 3. Command-Line Arguments

```bash
python xssgen.py \
  https://target.com \
  --mode standard \
  --profile all \
  --depth 2 \
  --threads 5 \
  --verbose
```

### 4. Environment Variables

Create `.env` file:
```env
DEFAULT_THREADS=5
DEFAULT_TIMEOUT=10
LOG_LEVEL=INFO
```

Load and run:
```bash
load_env=true python xssgen.py
```

## REST API Server

```bash
# Start API server
pip install -r requirements.txt
pip install fastapi uvicorn pydantic

python api_server.py
# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### API Examples

```bash
# Check health
curl http://localhost:8000/health

# Start scan
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "mode": "quick",
    "profile": "all"
  }'

# Get scan status
curl http://localhost:8000/scan/{scan_id}

# Get results
curl http://localhost:8000/scan/{scan_id}/results
```

## Production Deployment

### Kubernetes

```bash
# Create configmap from config file
kubectl create configmap autoxss-config --from-file=config.yaml

# Deploy (helm chart available in charts/ directory)
helm install autoxss ./charts/autoxss \
  -f values.yaml \
  --namespace security
```

### Docker Swarm

```bash
# Create service
docker service create \
  --name autoxss \
  --publish 8000:8000 \
  --mount type=bind,source=/data/reports,target=/app/reports \
  autoxss:latest

# Scale
docker service scale autoxss=3
```

## CI/CD Integration

### GitHub Actions

Already configured in `.github/workflows/`:

```yaml
# Add to your workflow
- name: Run XSS Scan
  run: |
    pip install -r requirements.txt
    python xssgen.py https://myapp.com --mode quick --profile all
```

### GitLab CI

```yaml
# .gitlab-ci.yml
security_scan:
  image: autoxss:latest
  script:
    - autoxss https://myapp.com --mode standard --profile all
  artifacts:
    reports:
      sast: xss_report.json
```

## Monitoring & Logging

### Structured Logs

All scans are logged to `logs/` directory:

```bash
# View logs
tail -f logs/xssgen_*.log

# View JSON logs (for log aggregation)
cat logs/xssgen_*.jsonl | jq .

# Parse audit trail
python -c "
import json
with open('.audit_logs/session_*.jsonl') as f:
    for line in f:
        print(json.dumps(json.loads(line), indent=2))
"
```

### Audit Trail

Compliance audit logs stored in `.audit_logs/`:
- All scans logged with timestamp
- Vulnerabilities recorded with payload
- Compliance authorization tracked
- Search index available

### Metrics

After each scan, metrics available:
```python
from lib_logging import PerformanceMetrics

metrics = PerformanceMetrics()
summary = metrics.get_summary()
# {
#   "duration_seconds": 45.2,
#   "payloads_tested": 500,
#   "vulnerabilities_found": 3,
#   "success_rate": 0.6,
#   "payloads_per_second": 11.05
# }
```

## Proxy & Network Configuration

### Burp Suite

```bash
# Run with Burp proxy
python xssgen.py https://target.com --proxy http://127.0.0.1:8080

# Docker compose includes Burp automatically
docker-compose --profile with-burp up
```

### OWASP ZAP

```bash
# Run with ZAP proxy
python xssgen.py https://target.com --proxy http://127.0.0.1:8091
```

### mitmproxy

```bash
# Run with mitmproxy
python xssgen.py https://target.com --proxy http://127.0.0.1:8888
```

## Customization

### Custom Payloads

1. Create payload file: `payloads/custom_context.txt`
2. One payload per line
3. Use in profile: `--profile all` (will include all categories)

### Custom Config Profile

Edit `config.yaml` and save multiple versions:
```bash
config-aggressive.yaml  # Deep + all payloads
config-stealth.yaml     # Slow, evasive
config-quick.yaml       # Fast check
```

## Troubleshooting

### Issue: Authorization Required

```
Error: Authorization DENIED. Tool will not proceed without authorization.
```

**Solution**: Type "yes" when prompted, or set:
```yaml
compliance:
  require_authorization: false  # For automated scans
```

### Issue: Proxy Connection Failed

```
Error: Unable to connect to proxy http://127.0.0.1:8080
```

**Solution**: 
- Verify proxy is running: `curl http://127.0.0.1:8080`
- Check firewall rules
- Use `--verbose` for debugging

### Issue: SSL Certificate Errors

```
Error: SSL: CERTIFICATE_VERIFY_FAILED
```

**Solution**:
```bash
# Disable verification (dev only!)
export PYTHONHTTPSVERIFY=0

# Or use with config
# Note: Not recommended for production
```

### Issue: Docker Permission Denied

```
Error: docker: permission denied
```

**Solution**:
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

## Security Best Practices

1. **Always use HTTPS** for target URLs
2. **Get authorization** before testing any system
3. **Use VPN/Proxy** for testing remote systems
4. **Rotate credentials** used in tests
5. **Use separate accounts** for security tests
6. **Review audit logs** after each scan
7. **Secure reports** with encryption
8. **Use environment variables** for sensitive data (not config files)

## Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: README.md and docs/
- **Examples**: examples/ directory

## License

MIT License - See LICENSE file for details
