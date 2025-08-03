# PyPI Publishing Guide

## Overview

This guide explains how to publish the `deprecated-checker` package to PyPI.

## Prerequisites

### 1. PyPI Account
- Create account at https://pypi.org/account/register/
- Enable two-factor authentication
- Create API token at https://pypi.org/manage/account/token/

### 2. TestPyPI Account
- Create account at https://test.pypi.org/account/register/
- Create API token at https://test.pypi.org/manage/account/token/

### 3. Install Tools
```bash
pip install build twine
```

## Manual Publishing

### Step 1: Build Package
```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build package
python -m build
```

### Step 2: Check Package
```bash
# Validate package
python -m twine check dist/*
```

### Step 3: Upload to TestPyPI (Recommended First)
```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*
```

### Step 4: Test Installation from TestPyPI
```bash
# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ deprecated-checker

# Test the package
deprecated-checker --help
```

### Step 5: Upload to PyPI
```bash
# Upload to production PyPI
python -m twine upload dist/*
```

## Automated Publishing with GitHub Actions

### Setup Secrets

1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Add the following secrets:
   - `PYPI_API_TOKEN`: Your PyPI API token
   - `TEST_PYPI_API_TOKEN`: Your TestPyPI API token

### Trigger Publishing

Publishing is automatically triggered when you push a tag:

```bash
# Create and push a new tag
git tag -a v1.0.2 -m "Release v1.0.2"
git push origin v1.0.2
```

## Package Configuration

### pyproject.toml
```toml
[project]
name = "deprecated-checker"
version = "1.0.1"
description = "Tool for checking deprecated dependencies in Python projects and suggesting alternatives"
license = "MIT"
authors = [
    {name = "Iulian Pavlov", email = "iulian.pavlov@gmail.com"}
]
```

### Entry Points
```toml
[project.scripts]
deprecated-checker = "utils.cli:app"
```

### Dependencies
```toml
dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
    "pyyaml>=6.0",
    "requests>=2.28.0",
    "packaging>=23.0",
]
```

## Package Structure

```
deprecated_checker/
├── core/                    # Core functionality
│   ├── __init__.py
│   ├── checker.py
│   ├── database.py
│   └── parser.py
├── utils/                   # CLI interface
│   ├── __init__.py
│   └── cli.py
└── data/                    # Package data
    └── deprecated_packages.yaml
```

## Installation

### From PyPI
```bash
pip install deprecated-checker
```

### From TestPyPI
```bash
pip install --index-url https://test.pypi.org/simple/ deprecated-checker
```

### From Source
```bash
git clone https://github.com/julicq/is-deprecated-or-not.git
cd is-deprecated-or-not
pip install -e .
```

## Usage

### Command Line
```bash
# Check project for deprecated dependencies
deprecated-checker check --path /path/to/project

# Search for specific package
deprecated-checker search requests

# Export database
deprecated-checker export-db --format json
```

### Python API
```python
from deprecated_checker.core.checker import DeprecatedChecker

checker = DeprecatedChecker()
result = checker.check_project("/path/to/project")
```

## Version Management

### Semantic Versioning
- `MAJOR.MINOR.PATCH`
- Example: `1.0.1`

### Update Version
1. Update version in `pyproject.toml`
2. Update version in `utils/cli.py`
3. Update `CHANGELOG.md`
4. Create and push tag

```bash
# Update version
sed -i '' 's/version = "1.0.1"/version = "1.0.2"/' pyproject.toml

# Create tag
git tag -a v1.0.2 -m "Release v1.0.2"
git push origin v1.0.2
```

## Troubleshooting

### Common Issues

1. **Package Name Already Taken**
   - Check if name is available: https://pypi.org/project/deprecated-checker/
   - Consider alternative names

2. **Upload Errors**
   - Verify API tokens
   - Check package format with `twine check`
   - Ensure version is unique

3. **Import Errors**
   - Check entry points configuration
   - Verify package structure
   - Test locally with `pip install -e .`

### Validation Commands

```bash
# Check package format
python -m twine check dist/*

# Test installation
pip install dist/*.whl

# Test CLI
deprecated-checker --help
```

## Links

- **PyPI**: https://pypi.org/project/deprecated-checker/
- **TestPyPI**: https://test.pypi.org/project/deprecated-checker/
- **GitHub**: https://github.com/julicq/is-deprecated-or-not
- **Documentation**: https://github.com/julicq/is-deprecated-or-not#readme

## Next Steps

1. **First Release**: Upload to TestPyPI for testing
2. **Production Release**: Upload to PyPI after testing
3. **Documentation**: Update README with installation instructions
4. **Community**: Share package with Python community 