# Contributing to AutoXSS

Thank you for your interest in contributing to AutoXSS! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Use this tool only for **authorized security testing**
- Respect responsible disclosure principles
- Report security vulnerabilities privately
- Be respectful and constructive in discussions

## How to Contribute

### 1. Report Bugs

Found a bug? Please create an issue with:
- **Title**: Clear, concise description
- **Environment**: Python version, OS, tool version
- **Steps to Reproduce**: Detailed steps
- **Actual vs Expected Behavior**: What happened vs. what should happen
- **Logs**: Any error messages or stack traces

### 2. Suggest Features

Have an idea? Submit an issue with:
- **Description**: What you want and why
- **Use Cases**: How would this help?
- **Implementation Ideas**: Any suggestions on how to build it?

### 3. Submit Code Changes

#### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/Robertmwatua/xss-generator.git
cd xss-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### Code Guidelines

1. **Python Style**: Follow PEP 8 with black formatting
   ```bash
   black xssgen.py lib_*.py tests/
   ```

2. **Type Hints**: Add type annotations to new functions
   ```python
   def scan_url(url: str, payload: str) -> Tuple[bool, str]:
       """Scan URL with payload. Returns (is_vulnerable, response)."""
   ```

3. **Documentation**: Add docstrings
   ```python
   def your_function(param1: str, param2: int) -> bool:
       """
       Brief description of what the function does.
       
       Args:
           param1: Description of param1
           param2: Description of param2
       
       Returns:
           Description of return value
       """
   ```

4. **Testing**: Write tests for new features
   ```bash
   pytest tests/ -v --cov
   ```

5. **Commit Messages**: Follow conventional commits
   ```
   feat: add support for JSON payload import
   fix: resolve timeout issue in stealth mode
   docs: update API documentation
   test: add unit tests for new config module
   ```

#### Pull Request Process

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Make** your changes with tests
4. **Run** linting and tests:
   ```bash
   black . && isort . && flake8 . && pytest
   ```
5. **Commit** with clear messages
6. **Push** to your fork
7. **Submit** a Pull Request with:
   - Clear description of changes
   - Linked issues (if any): `Closes #123`
   - Screenshots (if UI changes)
   - Testing notes

### 4. Submit Payload Templates

Want to contribute new XSS payloads?

1. Create a file: `payloads/[category].txt`
2. One payload per line
3. Test payloads before submitting
4. Include comment explaining the technique:
   ```txt
   # Template tag injection bypass (mutations)
   <noscript><p title="</noscript><img src=x onerror=alert(1)>">
   ```

### 5. Improve Documentation

- Fix typos and unclear explanations
- Add usage examples
- Improve README sections
- Create tutorials or guides

## Development Workflow

### Running Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_config.py

# With coverage
pytest --cov=. --cov-report=html

# Specific test function
pytest tests/test_config.py::TestConfigManager::test_default_config
```

### Code Quality Checks

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Type checking
mypy xssgen.py lib_*.py

# Security audit
bandit -r .

# All at once
black . && isort . && flake8 . && mypy xssgen.py lib_*.py
```

### Building Docker Image

```bash
# Build
docker build -t autoxss:dev .

# Run
docker run --rm -it autoxss:dev https://example.com --mode quick
```

## Architecture & Modules

- **xssgen.py**: Main entry point and wizard
- **lib_compliance.py**: Authorization and audit logging
- **lib_logging.py**: Structured logging and metrics
- **lib_config.py**: Configuration file management
- **api_server.py**: REST API interface
- **payloads/**: XSS payload database
- **tests/**: Unit tests (pytest)

## Context Map

The tool supports multiple injection contexts:
- **HTML Body**: Script tags, event handlers
- **HTML Attributes**: Breaking out of quotes
- **JavaScript Context**: String escapes, template literals
- **URL Context**: Protocol handlers
- **DOM**: Source/sink analysis

## Adding New Features

### Adding a New Payload Category

1. Create file: `payloads/[category].txt`
2. Update `PAYLOADS` dict in xssgen.py
3. Add category to relevant `PROFILE_CATS`
4. Test with: `python xssgen.py --profile all`

### Adding New Logging

Use the `StructuredLogger`:
```python
from lib_logging import StructuredLogger

logger = StructuredLogger("module_name")
logger.info("Message", key=value)
logger.vulnerability_found(url="...", param="...", payload="...", context="...")
```

### Adding New API Endpoint

Edit `api_server.py` and add a route:
```python
@app.get("/your-endpoint")
async def your_endpoint():
    """Your endpoint description."""
    return {"status": "ok"}
```

## Questions?

- **Discussions**: GitHub Discussions tab
- **Issues**: Create an issue for bugs/features
- **Email**: [Author contact if provided]

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for making AutoXSS better! 🎯
