# Security Policy & Responsible Disclosure

## 🛡️ Security Principles

This tool is designed for **authorized security testing ONLY**. Use responsibly and legally.

### Legal Requirements

**BEFORE using this tool:**
1. ✅ **Get written authorization** from the system owner
2. ✅ **Verify you have permission** to test the target
3. ✅ **Understand local laws** regarding security testing
4. ✅ **Follow your organization's policies** for testing
5. ✅ **Keep findings confidential** until disclosed responsibly

### Prohibited Uses

❌ **DO NOT use against:**
- Systems you don't own or have explicit permission for
- Production systems without approval
- Competition's systems or research
- Government systems without authorization
- Any system where testing is illegal in your jurisdiction

### Permitted Uses

✅ **Only use for:**
- Your own websites and applications
- Authorized penetration testing engagements
- Bug bounty programs with explicit rules
- Educational institutions with proper authorization
- Security research with written permission
- Approved CI/CD security scanning pipelines

## 🔐 Operational Security

### Sensitive Data Handling

```bash
# ❌ DON'T: Commit credentials to git
git add config.yaml  # If contains credentials!

# ✅ DO: Use environment variables
export API_TOKEN="secret"
python xssgen.py --config config.yaml

# ✅ DO: Use .env files (add to .gitignore)
cat > .env << EOF
COOKIES="session=abc123"
API_TOKEN="secret"
EOF

python xssgen.py --config config.yaml
```

### Proxy & MITM Protection

```bash
# If using proxy (Burp, ZAP), understand:
# 1. Your traffic is visible to proxy operator
# 2. Use HTTPS to encrypt payload contents
# 3. Only use trusted proxy servers

# For production: Use VPN + proxy
python xssgen.py https://target.com \
  --proxy http://127.0.0.1:8080  # Local Burp
```

### Log Safety

```bash
# Logs contain sensitive information
logs/
├── xssgen_*.log        # Contains payloads, parameters, findings
└── *.jsonl             # Structured logs with similar data

# ✅ DO: Encrypt logs
# ✅ DO: Restrict file permissions
chmod 600 logs/*.log
chmod 600 .audit_logs/*.jsonl

# ❌ DON'T: Commit logs to repository
```

### Audit Trail Security

```yaml
# The audit trail (.audit_logs/) contains:
# - All scanned URLs
# - Timestamps of testing
# - Usernames/sessions
# - Discovered vulnerabilities
# 
# Security measures:
# - One file per session (immutable)
# - Append-only logging
# - Timestamp based integrity
# - Access control important

# Review audit trail to:
# - Verify who tested what
# - Document testing timeline
# - Create evidence for reports
# - Demonstrate due diligence
```

## 🚨 Vulnerability Disclosure

### Timeline (Recommended)

Follow responsible disclosure practices:

```
Day 0:   Vulnerability discovered → Log in audit trail
Day 1:   Initial contact with security team
Day 7:   Follow-up if no acknowledgment
Day 30:  Expected patch/fix timeline
Day 60:  Status check
Day 90:  Deadline for patching
Day 91:  Consider public disclosure if unpatched
```

### Disclosure Process

1. **Identify the right contact**
   ```bash
   # Look for security.txt
   https://example.com/.well-known/security.txt
   
   # Or find security team email
   security@example.com
   ```

2. **Use responsible disclosure template**
   ```python
   from lib_compliance import ResponsibleDisclosureTemplate
   
   template = ResponsibleDisclosureTemplate.generate_template(
       target_url="https://example.com",
       vulnerabilities=[...],
       findings_date="2026-04-13"
   )
   ```

3. **Encrypt if sending email**
   ```bash
   # If org has PGP key, use it
   gpg --encrypt --recipient security@example.com disclosure.txt
   ```

4. **Document everything**
   - Date of discovery
   - Vulnerability details
   - Proof of concept steps
   - Recommended fixes
   - Your contact information

## 🔍 Detection & Prevention

### Detecting Scanner Activity

Organizations can detect this tool via:

```
1. HTTP User-Agent: Mozilla/5.0 (X11; Linux x86_64)...
2. Payload patterns: <script>, alert(), etc.
3. Request frequency: Burst of similar requests
4. Parameter testing: Systematic fuzzing patterns
5. Audit logs: Check for authorization warnings
```

### If Caught Without Permission

```
If discovered testing without authorization:
1. STOP immediately
2. Don't delete logs or evidence
3. Contact legal team
4. Fully cooperate with investigation
5. This is a serious legal matter
```

## 📋 Audit & Compliance

### Using Audit Trail

The audit trail provides evidence of authorized testing:

```json
// .audit_logs/YYYYMMDD_HHMMSS_SSS.jsonl contains:
{
  "timestamp": "2026-04-13T10:30:00Z",
  "session_id": "abc123",
  "event_type": "scan_start",
  "details": {
    "url": "https://authorized-target.com",
    "mode": "standard",
    "profile": "all"
  }
}

// Use in reports to show:
// ✓ When testing occurred
// ✓ What was tested
// ✓ Methodical approach
// ✓ Timing of discoveries
// ✓ Attribution (who ran it)
```

### Authorization Documentation

Keep proof of authorization:

```
Required documentation:
✓ Written authorization email
✓ Signed scope document
✓ Testing agreement/contract
✓ Authorization approval with dates
✓ Scope definition (URLs, IPs, methods)
✓ Rules of Engagement
```

### Reporting Vulnerabilities

Use the structured output:

```python
# Example report entry
{
  "url": "https://target.com/search",
  "parameter": "q",
  "vulnerability_type": "Reflected XSS",
  "severity": "HIGH",
  "cvss_score": 6.1,
  "owasp": "A03:2021 – Injection",
  "cwe": "CWE-79",
  "discovery_date": "2026-04-13T10:30:00Z",
  "affected_versions": "1.2.3",
  "proof_of_concept": "<script>alert(document.domain)</script>",
  "remediation": "Use HTML entity encoding for user input"
}
```

## 🛠️ Security Configuration

### Minimal Permission Mode

```yaml
# config.yaml - Minimal impact testing
compliance:
  require_authorization: true  # Must confirm
  audit_log: true              # Document everything

scan:
  threads: 1                   # Slow, less impact
  delay: 2                     # 2 second delay
  mode: "stealth"              # WAF evasion

output:
  verbose: true                # Show what's happening
  save_json: true              # For compliance
```

### Secure API Mode

```python
# If running API server, add security:

from fastapi import HTTPBasicAuth
from fastapi_limiter import FastAPILimiter

# 1. Add authentication
app = FastAPI()

@app.post("/scan")
async def start_scan(credentials=Depends(HTTPBasicAuth)):
    # Verify user is authorized
    ...

# 2. Add rate limiting
limiter = FastAPILimiter()

@app.post("/scan")
@limiter.limit("5/minute")
async def start_scan():
    ...

# 3. Log all API calls
logger.info("API call", user=user, endpoint="/scan", ip=ip)
```

## 🔐 Secrets Management

### Never commit secrets

```bash
# .env - Local secrets (in .gitignore)
COOKIES="JSESSIONID=abc123"
PROXY_PASSWORD="secret"
API_TOKEN="xyz789"

# Load from environment
export $(cat .env | xargs)
python xssgen.py --config config.yaml
```

### GitHub Secrets (for Actions)

```yaml
# .github/workflows/security-scan.yml
- name: Run XSS Scan
  env:
    COOKIES: ${{ secrets.TEST_COOKIES }}
    PROXY: ${{ secrets.PROXY_URL }}
  run: |
    python xssgen.py ${{ secrets.TARGET_URL }}
```

## 📞 Security Contacts

### Report Issues

- **GitHub Issues**: security issues (but check policy first)
- **Private email**: For sensitive vulnerability disclosure
- **Bug bounty**: Use platform's responsible disclosure process

### This Project

For security issues in AutoXSS itself:

1. **DO NOT** create public GitHub issue
2. **INSTEAD** email: [author-email-here]
3. **Include**:
   - Type of vulnerability
   - Steps to reproduce
   - Proof of concept
   - Proposed fix (optional)

## ⚖️ Legal Disclaimer

```
This tool is provided AS-IS for authorized security testing only.

BY USING THIS TOOL, YOU:
✓ Accept full responsibility for your actions
✓ Confirm you have written authorization
✓ Agree to follow all applicable laws
✓ Release the authors from liability
✓ Understand unauthorized access is illegal

The authors are NOT responsible for:
✗ Illegal use of this tool
✗ Damage caused by misuse
✗ Unauthorized system access
✗ Data breaches or loss
✗ Legal action from testing without permission
```

## 📚 References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE - Cross-Site Scripting](https://cwe.mitre.org/data/definitions/79.html)
- [Responsible Disclosure](https://www.eff.org/issues/responsible-disclosure)
- [EC-Council Code of Ethics](https://www.eccouncil.org/)
- [SANS Code of Conduct](https://www.giac.org/code-of-ethics)

---

**Remember**: With great power comes great responsibility. Test wisely. Test legally. Test ethically.
