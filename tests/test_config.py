"""
Unit tests for lib_config module
"""

import pytest
import json
import tempfile
from pathlib import Path
from lib_config import ConfigManager, ConfigGenerator


class TestConfigManager:
    """Test ConfigManager class."""

    def test_default_config(self):
        """Test that default config is properly initialized."""
        cfg = ConfigManager()
        
        assert cfg.config is not None
        assert "target" in cfg.config
        assert "scan" in cfg.config
        assert "auth" in cfg.config
    
    def test_config_get_default(self):
        """Test getting config values with dot notation."""
        cfg = ConfigManager()
        
        assert cfg.get("scan.mode") == "standard"
        assert cfg.get("scan.threads") == 5
        assert cfg.get("nonexistent", "default") == "default"
    
    def test_config_set_value(self):
        """Test setting config values."""
        cfg = ConfigManager()
        cfg.set("target.url", "https://example.com")
        
        assert cfg.get("target.url") == "https://example.com"
    
    def test_save_json_config(self):
        """Test saving config to JSON."""
        cfg = ConfigManager()
        cfg.set("target.url", "https://test.com")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            path = str(Path(tmpdir) / "config.json")
            cfg.save_config(path, format="json")
            
            assert Path(path).exists()
            
            # Verify saved content
            with open(path, "r") as f:
                saved = json.load(f)
                assert saved["target"]["url"] == "https://test.com"
    
    def test_validate_config(self):
        """Test config validation."""
        cfg = ConfigManager()
        
        # No URL should fail
        is_valid, errors = cfg.validate()
        assert not is_valid
        assert any("url" in e.lower() for e in errors)
        
        # With URL should pass
        cfg.set("target.url", "https://example.com")
        is_valid, errors = cfg.validate()
        assert is_valid


class TestConfigGenerator:
    """Test ConfigGenerator class."""
    
    def test_quickstart_template(self):
        """Test quick-start template generation."""
        template = ConfigGenerator.generate_quick_start()
        
        assert "target:" in template
        assert "scan:" in template
        assert "url:" in template
        assert "mode: standard" in template
