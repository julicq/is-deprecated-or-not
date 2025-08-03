# Examples of using Deprecated Checker

## Base functionality

### Check current directory 
```bash
python deprecated_checker.py check
```

### Check some directory
```bash
python deprecated_checker.py check --path /path/to/project
```

### Verbose output
```bash
python deprecated_checker.py check --verbose
```

## Export reports

### JSON format
```bash
python deprecated_checker.py check --export json
```

### YAML format
```bash
python deprecated_checker.py check --export yaml
```

### Save to file
```bash
python deprecated_checker.py check --export json --output report.json
```

## Working with DB

### List all deprecated packages
```bash
python deprecated_checker.py list-db
```

### Search some package
```bash
python deprecated_checker.py search requests
```

## Output examples

### Text report
```
🔍 Report on deprecated dependancies
==================================================
📁 Checked files: requirements.txt
📊 Total packeges: 8
❌ Deprecated: 2
✅ Safe: 6

❌ Found deprecated packages:
  • requests==2.31.0 (requirements.txt)
    Reason: Recommended to use httpx for best performance and async support
    Alternatives:
      - httpx: Modern HTTP libraty with async/await support
        Guide: https://www.python-httpx.org/migration/
      - aiohttp: Async HTTP library
        Guide: https://docs.aiohttp.org/

✅ Safe packages:
  • fastapi==0.104.0 (requirements.txt)
  • pydantic==2.4.0 (requirements.txt)
```

### JSON report
```json
{
  "summary": {
    "total_packages": 8,
    "deprecated_count": 2,
    "safe_count": 6,
    "files_checked": ["requirements.txt"]
  },
  "deprecated_packages": [
    {
      "name": "requests",
      "current_version": "2.31.0",
      "file_source": "requirements.txt",
      "deprecated_since": "2023-01-01",
      "reason": "Recommended to use httpx for best performance and async support",
      "alternatives": [
        {
          "name": "httpx",
          "reason": "Modern HTTP libraty with async/await support",
          "migration_guide": "https://www.python-httpx.org/migration/"
        }
      ]
    }
  ],
  "safe_packages": [
    {
      "name": "fastapi",
      "version": "0.104.0",
      "file_source": "requirements.txt"
    }
  ]
}
```

## Supported files

This utility automatically finds and analyses the following files:

- `requirements.txt`
- `requirements-dev.txt`
- `setup.py`
- `pyproject.toml`

## CI/CD integration

### GitHub Actions
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

### GitLab CI
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

## DB extension

To add deprecated packages edit file `data/deprecated_packages.yaml`:

```yaml
new-package:
  deprecated_since: "2024-01-01"
  reason: "Reason of deprecation"
  alternatives:
    - name: "alternative-package"
      reason: "Why better"
      migration_guide: "https://example.com/migration"
```

## Automation

### Pre-commit hook
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
```

### Makefile
```makefile
check-deps:
	python deprecated_checker.py check --verbose

check-deps-json:
	python deprecated_checker.py check --export json --output deps-report.json

update-db:
	python deprecated_checker.py list-db
``` 