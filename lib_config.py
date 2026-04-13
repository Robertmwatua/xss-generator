"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         CONFIG MODULE                                       ║
║   YAML/JSON configuration file support for non-interactive usage            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigManager:
    """Manage YAML/JSON configuration files."""

    DEFAULT_CONFIG = {
        "target": {
            "url": None,
            "endpoint": None,
            "known_param": None,
        },
        "scan": {
            "mode": "standard",  # quick, standard, deep, stealth, targeted
            "profile": "all",  # all, waf_bypass, polyglot, dom, blind, quick
            "depth": 2,
            "threads": 5,
            "delay": 0.0,
            "timeout": 10,
        },
        "auth": {
            "cookies": None,
            "headers": None,
            "proxy": None,
        },
        "vectors": {
            "blind_callback": None,
            "skip_headers": False,
            "test_dom": True,
        },
        "output": {
            "verbose": False,
            "save_json": True,
            "save_html": True,
            "save_text": True,
        },
        "compliance": {
            "require_authorization": True,
            "audit_log": True,
            "audit_log_dir": ".audit_logs",
        },
    }

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or return defaults."""
        if not self.config_path:
            return self.DEFAULT_CONFIG.copy()

        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, "r") as f:
            if self.config_path.endswith(".json"):
                config = json.load(f)
            else:
                # Try YAML
                try:
                    import yaml
                    config = yaml.safe_load(f)
                except ImportError:
                    raise ImportError(
                        "PyYAML required for YAML config. Install: pip install pyyaml"
                    )

        # Merge with defaults
        return self._merge_configs(self.DEFAULT_CONFIG, config)

    @staticmethod
    def _merge_configs(defaults: Dict, overrides: Dict) -> Dict:
        """Deep merge override config with defaults."""
        result = defaults.copy()
        for key, value in overrides.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = ConfigManager._merge_configs(result[key], value)
            else:
                result[key] = value
        return result

    def save_config(self, path: str, format: str = "json") -> None:
        """Save current config to file."""
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

        if format == "json":
            with open(path, "w") as f:
                json.dump(self.config, f, indent=2)
        elif format == "yaml":
            try:
                import yaml
                with open(path, "w") as f:
                    yaml.dump(self.config, f, default_flow_style=False)
            except ImportError:
                raise ImportError("PyYAML required for YAML output")
        else:
            raise ValueError("Unsupported format. Use 'json' or 'yaml'")

    def get(self, path: str, default: Any = None) -> Any:
        """
        Get config value using dot notation.
        Example: get('target.url') returns config['target']['url']
        """
        parts = path.split(".")
        current = self.config
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return default
        return current if current is not None else default

    def set(self, path: str, value: Any) -> None:
        """Set config value using dot notation."""
        parts = path.split(".")
        current = self.config

        # Navigate to the parent dict
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]

        # Set the value
        current[parts[-1]] = value

    def to_dict(self) -> Dict[str, Any]:
        """Return config as dictionary."""
        return self.config.copy()

    def validate(self) -> tuple[bool, list]:
        """
        Validate required config values.
        Returns: (is_valid, list_of_errors)
        """
        errors = []

        if not self.get("target.url"):
            errors.append("target.url is required")

        if self.get("scan.depth") < 1 or self.get("scan.depth") > 5:
            errors.append("scan.depth must be between 1 and 5")

        if self.get("scan.threads") < 1 or self.get("scan.threads") > 20:
            errors.append("scan.threads must be between 1 and 20")

        return len(errors) == 0, errors


class ConfigGenerator:
    """Generate template configuration files."""

    @staticmethod
    def generate_template(path: str, format: str = "json") -> None:
        """Generate a template config file."""
        config_mgr = ConfigManager()
        config_mgr.save_config(path, format)
        print(f"Config template generated: {path}")

    @staticmethod
    def generate_quick_start() -> str:
        """Return quick-start YAML config example."""
        return """# AutoXSS Configuration - Quick Start

target:
  url: https://testsite.com
  endpoint: null          # Optional: specific endpoint to test
  known_param: null       # Optional: specific parameter name

scan:
  mode: standard          # quick, standard, deep, stealth, targeted
  profile: all            # all, waf_bypass, polyglot, dom, blind, quick
  depth: 2                # crawl depth (1-5)
  threads: 5              # concurrent threads (1-20)
  delay: 0                # delay between requests (seconds)
  timeout: 10             # request timeout (seconds)

auth:
  cookies: null           # "session=abc123; token=xyz"
  headers: null           # Custom headers (one per line)
  proxy: null             # "http://127.0.0.1:8080"

vectors:
  blind_callback: null    # Callback URL for blind XSS
  skip_headers: false     # Skip HTTP header injection testing
  test_dom: true          # Run DOM sink analysis

output:
  verbose: false          # Detailed logging
  save_json: true         # Save JSON report
  save_html: true         # Save HTML report
  save_text: true         # Save text report

compliance:
  require_authorization: true   # Require user to confirm authorization
  audit_log: true               # Enable audit logging
  audit_log_dir: .audit_logs    # Directory for audit logs
"""
