"""
Pytest configuration and shared fixtures
"""

import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_url():
    """Provide a sample URL for testing."""
    return "https://example.com"


@pytest.fixture
def sample_payload():
    """Provide a sample XSS payload for testing."""
    return "<script>alert(1)</script>"


@pytest.fixture
def sample_config():
    """Provide a sample configuration dictionary."""
    return {
        "url": "https://example.com",
        "mode": "quick",
        "profile": "all",
        "depth": 2,
        "threads": 5,
    }
