"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    COMPLIANCE & AUTHORIZATION MODULE                        ║
║   Ensure ethical use, provide audit trails, and enforce legal disclaimers   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path


class ComplianceManager:
    """Manages compliance checks, authorization, and audit logging."""

    def __init__(self, audit_log_dir: str = ".audit_logs"):
        self.audit_log_dir = Path(audit_log_dir)
        self.audit_log_dir.mkdir(exist_ok=True)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]

    def print_disclaimer(self) -> None:
        """Print legal disclaimer."""
        disclaimer = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                     LEGAL DISCLAIMER & AUTHORIZATION                         ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  AutoXSS is designed for AUTHORIZED PENETRATION TESTING ONLY.                ║
║                                                                               ║
║  !!! DO NOT use this tool against:                                            ║
║      • Websites you do not own or have explicit permission to test           ║
║      • Systems without written authorization from the owner/manager          ║
║      • Production environments without prior approval                        ║
║      • Any target in a jurisdiction where it's illegal                       ║
║                                                                               ║
║   PERMITTED USES:                                                           ║
║      • Your own websites and applications                                    ║
║      • Authorized bug bounty programs                                        ║
║      • Penetration tests with signed contracts                               ║
║      • Educational environments explicitly for learning                      ║
║      • Approved CI/CD security scanning pipelines                            ║
║                                                                               ║
║   DISCLAIMER:                                                              ║
║      By using this tool, you assume full responsibility for any damage,      ║
║      legal action, or harm caused by its use. The authors are NOT liable     ║
║      for misuse, unauthorized access, or violation of applicable laws.       ║
║                                                                               ║
║      This tool is provided AS-IS for educational & authorized testing only.  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
        """
        print(disclaimer)

    def get_authorization(self) -> bool:
        """
        Prompt user to acknowledge they have authorization.
        Returns True if acknowledged, False otherwise.
        """
        self.print_disclaimer()
        print()
        response = input(
            "Do you have explicit written authorization to test this target? "
            "(type 'yes' to continue): "
        ).strip().lower()

        if response != "yes":
            print("\n X Authorization DENIED. Tool will not proceed without authorization.\n")
            return False

        print(" Authorization acknowledged. Proceeding with scan.\n")
        return True

    def log_audit(self, event_type: str, details: Dict[str, Any]) -> None:
        """
        Log an audit event to the audit trail.

        Args:
            event_type: Type of event (e.g., 'scan_start', 'vuln_found', 'scan_end')
            details: Dictionary of event details
        """
        audit_record = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "event_type": event_type,
            "details": details,
        }

        audit_file = self.audit_log_dir / f"{self.session_id}.jsonl"
        try:
            with open(audit_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(audit_record) + "\n")
        except Exception as e:
            print(f"!  Warning: Failed to write audit log: {e}")

    def log_scan_start(
        self,
        url: str,
        mode: str,
        profile: str,
        endpoint: Optional[str] = None,
        param: Optional[str] = None,
    ) -> None:
        """Log the start of a scan."""
        self.log_audit(
            "scan_start",
            {
                "url": url,
                "mode": mode,
                "profile": profile,
                "endpoint": endpoint,
                "parameter": param,
            },
        )

    def log_vulnerability(
        self,
        url: str,
        param: str,
        payload: str,
        context: str,
        method: str = "GET",
    ) -> None:
        """Log a discovered vulnerability."""
        self.log_audit(
            "vulnerability_found",
            {
                "url": url,
                "parameter": param,
                "payload": payload,
                "context": context,
                "method": method,
            },
        )

    def log_scan_end(self, summary: Dict[str, Any]) -> None:
        """Log the end of a scan with summary."""
        self.log_audit("scan_end", summary)

    def get_audit_trail(self) -> list:
        """Retrieve all audit logs for current session."""
        audit_file = self.audit_log_dir / f"{self.session_id}.jsonl"
        records = []
        if audit_file.exists():
            with open(audit_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        records.append(json.loads(line))
        return records


class OWASPMapper:
    """Maps findings to OWASP Top 10 and CWE categories."""

    OWASP_2021_MAP = {
        "xss": {
            "owasp": "A03:2021 – Injection",
            "cwe": ["CWE-79: Improper Neutralization of Input During Web Page Generation"],
            "cvss_base": 6.1,
        },
        "dom_xss": {
            "owasp": "A03:2021 – Injection",
            "cwe": ["CWE-79", "CWE-94: Improper Control of Generation of Code"],
            "cvss_base": 6.1,
        },
        "blind_xss": {
            "owasp": "A03:2021 – Injection",
            "cwe": ["CWE-79"],
            "cvss_base": 5.4,
        },
    }

    CVSS_QUALIFIERS = {
        "reflected": "AV:N/AC:L/PR:N/UI:R",  # Network, Low complexity, No privilege needed
        "dom": "AV:N/AC:L/PR:N/UI:R",
        "stored": "AV:N/AC:L/PR:N/UI:R",  # Could be higher if no auth needed
    }

    @staticmethod
    def get_owasp_info(vuln_type: str) -> Dict[str, Any]:
        """Get OWASP classification for vulnerability type."""
        return OWASPMapper.OWASP_2021_MAP.get(vuln_type.lower(), {})

    @staticmethod
    def get_cvss_string(vuln_type: str, attack_vector: str = "reflected") -> str:
        """Generate CVSS v3.1 vector string."""
        base = OWASPMapper.CVSS_QUALIFIERS.get(attack_vector, "AV:N/AC:L/PR:N/UI:R")
        return f"CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N"

    @staticmethod
    def get_cwe_list(vuln_type: str) -> list:
        """Get CWE list for vulnerability type."""
        info = OWASPMapper.OWASP_2021_MAP.get(vuln_type.lower(), {})
        return info.get("cwe", [])


class ResponsibleDisclosureTemplate:
    """Generates responsible disclosure report template."""

    @staticmethod
    def generate_template(
        target_url: str,
        vulnerabilities: list,
        findings_date: str,
    ) -> str:
        """
        Generate a responsible disclosure report template.

        Args:
            target_url: Target being tested
            vulnerabilities: List of findings
            findings_date: Date findings were discovered

        Returns:
            Formatted disclosure template
        """
        template = f"""
═══════════════════════════════════════════════════════════════════════════════
                    RESPONSIBLE DISCLOSURE REPORT
═══════════════════════════════════════════════════════════════════════════════

TO: [Security Team / Company Name]
DATE: {findings_date}
SUBJECT: Security Vulnerability Report - {target_url}

────────────────────────────────────────────────────────────────────────────────
EXECUTIVE SUMMARY
────────────────────────────────────────────────────────────────────────────────

During a security assessment of {target_url}, we discovered {len(vulnerabilities)} 
potential XSS vulnerability/ies that could allow attackers to execute arbitrary 
JavaScript in users' browsers.

────────────────────────────────────────────────────────────────────────────────
FINDINGS DETAIL
────────────────────────────────────────────────────────────────────────────────
"""
        for idx, vuln in enumerate(vulnerabilities, 1):
            template += f"""
[{idx}] VULNERABILITY
    Type: Cross-Site Scripting (XSS)
    Location: {vuln.get('url', 'N/A')}
    Parameter: {vuln.get('parameter', 'N/A')}
    Severity: {vuln.get('severity', 'HIGH')}
    OWASP: {OWASPMapper.get_owasp_info('xss').get('owasp', 'A03:2021')}
    CWE: {', '.join(OWASPMapper.get_cwe_list('xss'))}

    Description:
    The application fails to properly sanitize user input before reflecting it 
    in the HTML response, allowing an attacker to inject malicious JavaScript.

    Proof of Concept:
    [Provide PoC details here]

    Impact:
    - Session theft through cookie exfiltration
    - Credential harvesting via fake login prompts
    - Malware distribution
    - Website defacement
    - Phishing attacks

    Recommendation:
    1. Implement input validation for the vulnerable parameter
    2. Use proper output encoding (HTML entity encoding)
    3. Apply Content Security Policy (CSP) headers
    4. Use security libraries (e.g., DOMPurify for client-side)
"""
        template += """
────────────────────────────────────────────────────────────────────────────────
TIMELINE (SUGGESTED)
────────────────────────────────────────────────────────────────────────────────
Day 0: Initial Report Sent
Day 30: Follow-up (if no response)
Day 45: Disclosure with 90-day patch deadline
Day 90: Public disclosure if unpatched

────────────────────────────────────────────────────────────────────────────────
CONTACT INFORMATION
────────────────────────────────────────────────────────────────────────────────
Reporter: [Your Name/Organization]
Email: [Your Email]
PGP: [Optional PGP key]

════════════════════════════════════════════════════════════════════════════════
This report is provided in good faith for responsible disclosure purposes.
════════════════════════════════════════════════════════════════════════════════
"""
        return template
