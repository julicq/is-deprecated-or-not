# Installation and Setup for Deprecated Checker

## Quick Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/deprecated-checker.git
cd deprecated-checker
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Verify Installation
```bash
python deprecated_checker.py --help
```

## Alternative Installation Methods

### Install as Package
```bash
pip install -e .
```

After installation, you can use the command:
```bash
deprecated-checker check
```

### Install in Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

## Configuration

### 1. Database Configuration

The deprecated packages database is located in `data/deprecated_packages.yaml`. 
You can add new packages or modify existing ones:

```yaml
package-name:
  deprecated_since: "2024-01-01"
  reason: "Deprecation reason"
  alternatives:
    - name: "alternative-package"
      reason: "Why it's better"
      migration_guide: "https://example.com/migration"
```

### 2. CI/CD Setup

#### GitHub Actions
Create file `.github/workflows/deprecated-check.yml`:

```yaml
name: Check Deprecated Dependencies

on: [push, pull_request]

jobs:
  check-deps:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run deprecated checker
      run: |
        python deprecated_checker.py check --export json --output report.json
    - name: Upload report
      uses: actions/upload-artifact@v3
      with:
        name: dependency-report
        path: report.json
```

#### GitLab CI
Add to `.gitlab-ci.yml`:

```yaml
check_dependencies:
  image: python:3.11
  script:
    - pip install -r requirements.txt
    - python deprecated_checker.py check --export json --output report.json
  artifacts:
    reports:
      junit: report.json
```

### 3. Pre-commit hook

Create file `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: deprecated-checker
        name: Check deprecated dependencies
        entry: python deprecated_checker.py check
        language: system
        pass_filenames: false
        always_run: true
```

Install pre-commit:
```bash
pip install pre-commit
pre-commit install
```

### 4. Makefile

Create `Makefile` for convenience:

```makefile
.PHONY: check-deps check-deps-verbose check-deps-json update-db test

check-deps:
	python deprecated_checker.py check

check-deps-verbose:
	python deprecated_checker.py check --verbose

check-deps-json:
	python deprecated_checker.py check --export json --output deps-report.json

update-db:
	python deprecated_checker.py list-db

test:
	python test_checker.py

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -e .
```

## Usage

### Basic Commands

```bash
# Check current directory
python deprecated_checker.py check

# Check specific directory
python deprecated_checker.py check --path /path/to/project

# Verbose output
python deprecated_checker.py check --verbose

# Export to JSON
python deprecated_checker.py check --export json

# Export to YAML
python deprecated_checker.py check --export yaml

# Save report to file
python deprecated_checker.py check --export json --output report.json
```

### Database Operations

```bash
# View all deprecated packages
python deprecated_checker.py list-db

# Search for specific package
python deprecated_checker.py search requests
```

## Supported Files

The utility automatically detects and analyzes the following files:

- `requirements.txt`
- `requirements-dev.txt`
- `setup.py`
- `pyproject.toml`

## Troubleshooting

### Issue: "ModuleNotFoundError"
```bash
# Make sure all dependencies are installed
pip install -r requirements.txt
```

### Issue: "Permission denied"
```bash
# Set execution permissions
chmod +x deprecated_checker.py
```

### Issue: "No module named 'toml'"
```bash
# Install missing dependency
pip install toml
```

## Development

### Development Installation
```bash
git clone https://github.com/yourusername/deprecated-checker.git
cd deprecated-checker
pip install -e .
pip install -r requirements.txt
```

### Run Tests
```bash
python test_checker.py
```

### Adding New Tests
Create new tests in `test_checker.py` or create separate test files.

## License

MIT License - see LICENSE file for details.

## Support

If you have questions or issues:

1. Create an issue on GitHub
2. Check documentation in README.md
3. Look at examples in examples.md 