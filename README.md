# XSSGen — XSS Payload Generator
> by **R0b3rt0** | Educational offensive security tooling

![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)

A CLI-based Cross-Site Scripting payload generator built for penetration testers and security researchers. Supports multiple injection contexts, encoding schemes, WAF-bypass mutations, and stealth wrapping — all from the terminal, zero external dependencies.

---

## Features

| Feature | Details |
|---|---|
| **Contexts** | `html`, `attribute`, `js`, `url`, `filter-bypass` |
| **Encodings** | Base64, URL, HTML entity, Unicode, none |
| **WAF Bypass** | 3-level mutation engine (case mangling, null bytes, CDATA, template literals) |
| **Stealth Mode** | Randomly wraps payloads in obfuscated HTML templates |
| **Random Sampling** | Pick N random payloads per run |
| **Output to File** | Save results for use in Burp, ffuf, or custom scripts |
| **Zero Dependencies** | Pure Python stdlib — runs anywhere |

---

## Usage

\`\`\`bash
python xssgen.py --context html
python xssgen.py --context js --encode base64
python xssgen.py --context filter-bypass --mutate 3
python xssgen.py --context attribute --stealth --out results.txt
python xssgen.py --context html --random 5
\`\`\`

### All flags

\`\`\`
--context       html | attribute | js | url | filter-bypass  (required)
--encode        none | base64 | url | html-entity | unicode   (default: none)
--mutate        0 | 1 | 2 | 3   WAF bypass mutation level     (default: 0)
--stealth       Wrap payloads in randomised stealth templates
--random N      Pick N random payloads from the list
--out FILE      Write output payloads to a file
--payload-dir   Path to custom payloads directory             (default: payloads/)
--list          List available contexts and encodings
\`\`\`

---

## File Structure

\`\`\`
xss-generator/
├── xssgen.py              # Main tool
├── requirements.txt
├── README.md
├── LICENSE
└── payloads/
    ├── html.txt           # HTML body injection
    ├── attribute.txt      # HTML attribute breakout
    ├── js.txt             # JavaScript context breakout
    ├── url.txt            # URL / href context
    └── filter_bypass.txt  # WAF evasion variants
\`\`\`

---

## Disclaimer

This tool is for **educational purposes and authorized penetration testing only**. Never test against systems you do not own or have explicit written permission to assess.

---

*Built by R0b3rt0 — cybersecurity student, CTF player, lifelong learner.*
