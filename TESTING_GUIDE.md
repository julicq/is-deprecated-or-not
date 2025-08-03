# Testing Guide

## Overview

This guide covers various testing approaches for the deprecated dependencies checker service.

## Service Architecture

### Core Components

1. **Checker** (`core/checker.py`)
   - Main logic for checking deprecated packages
   - Analyzes project dependencies
   - Generates reports

2. **Parser** (`core/parser.py`)
   - Parses dependency files (requirements.txt, setup.py, pyproject.toml)
   - Extracts package information

3. **Database** (`core/database.py`)
   - Stores deprecated package information
   - Provides search and export functionality

4. **CLI Interface** (`utils/cli.py`)
   - Command-line interface
   - Rich output formatting
   - Multiple export formats

## Testing Approaches

### 1. Manual Testing

#### Basic Commands
```bash
# Check version
python utils/cli.py version

# View database statistics
python utils/cli.py stats

# Search for specific package
python utils/cli.py search requests

# List all deprecated packages
python utils/cli.py list-db

# Validate database
python utils/cli.py validate-db
```

#### Project Testing
```bash
# Test with sample project
python utils/cli.py check --path test_project

# Test with verbose output
python utils/cli.py check --path test_project --verbose

# Test export to JSON
python utils/cli.py check --path test_project --export json --output report.json

# Test export to YAML
python utils/cli.py check --path test_project --export yaml --output report.yaml
```

#### Database Management
```bash
# Export database
python utils/cli.py export-db --format json --output db_export.json
python utils/cli.py export-db --format yaml --output db_export.yaml
python utils/cli.py export-db --format csv --output db_export.csv

# Clear cache
python utils/cli.py clear-cache

# Update database
python utils/cli.py update-db --source all
```

#### Scheduler Testing
```bash
# Check scheduler status
python utils/cli.py scheduler status

# Start scheduler
python utils/cli.py scheduler start --interval 24

# Stop scheduler
python utils/cli.py scheduler stop

# Force update
python utils/cli.py scheduler force-update
```

### 2. Automated Testing

#### Comprehensive Test Suite
```bash
# Run all tests
python test_cli_comprehensive.py
```

This test suite covers:
- ✅ Version command
- ✅ Stats command
- ✅ Search functionality
- ✅ Database listing
- ✅ Database validation
- ✅ Project checking
- ✅ JSON export
- ✅ YAML export
- ✅ Scheduler commands
- ✅ Cache clearing
- ✅ Database export

#### Individual Test Functions

```python
def test_version():
    """Test version command."""
    result = run_command("python utils/cli.py version")
    return result.returncode == 0

def test_stats():
    """Test stats command."""
    result = run_command("python utils/cli.py stats")
    return "Total packages:" in result.stdout

def test_search():
    """Test search command."""
    result = run_command("python utils/cli.py search requests")
    return "deprecated" in result.stdout
```

### 3. Integration Testing

#### Test Project Structure
```
test_project/
├── requirements.txt    # Contains deprecated packages
├── setup.py           # Contains more dependencies
└── pyproject.toml     # Modern Python project config
```

#### Sample Test Data
```yaml
# test_project/requirements.txt
requests==2.28.1
flask==2.2.3
django-cors-headers==3.14.0
psycopg2==2.9.5
pyyaml==6.0
fastapi==0.104.0
pydantic==2.4.0
```

### 4. Performance Testing

#### Large Project Testing
```bash
# Test with large project
python utils/cli.py check --path /path/to/large/project --verbose

# Measure execution time
time python utils/cli.py check --path test_project
```

#### Database Performance
```bash
# Test database operations
python utils/cli.py stats
python utils/cli.py list-db
python utils/cli.py search requests
```

### 5. Error Handling Testing

#### Invalid Paths
```bash
# Test with non-existent path
python utils/cli.py check --path /non/existent/path

# Test with invalid package
python utils/cli.py search nonexistent_package
```

#### Invalid Commands
```bash
# Test invalid export format
python utils/cli.py export-db --format invalid

# Test invalid scheduler action
python utils/cli.py scheduler invalid_action
```

## Test Scenarios

### Scenario 1: Basic Functionality
```bash
# 1. Check version
python utils/cli.py version

# 2. View database stats
python utils/cli.py stats

# 3. Search for known deprecated package
python utils/cli.py search requests

# 4. Check test project
python utils/cli.py check --path test_project
```

### Scenario 2: Export Testing
```bash
# 1. Export project report to JSON
python utils/cli.py check --path test_project --export json --output test_report.json

# 2. Export database to different formats
python utils/cli.py export-db --format json --output db.json
python utils/cli.py export-db --format yaml --output db.yaml
python utils/cli.py export-db --format csv --output db.csv

# 3. Verify exported files
ls -la *.json *.yaml *.csv
```

### Scenario 3: Database Management
```bash
# 1. Validate database
python utils/cli.py validate-db

# 2. List all deprecated packages
python utils/cli.py list-db

# 3. Clear cache
python utils/cli.py clear-cache

# 4. Update database
python utils/cli.py update-db --source all
```

### Scenario 4: Scheduler Testing
```bash
# 1. Check scheduler status
python utils/cli.py scheduler status

# 2. Start scheduler
python utils/cli.py scheduler start --interval 1

# 3. Check status again
python utils/cli.py scheduler status

# 4. Stop scheduler
python utils/cli.py scheduler stop
```

## Expected Results

### Successful Test Output
```
✅ Version command works
✅ Stats command works
✅ Search command works
✅ List-db command works
✅ Validate-db command works
✅ Project check works
✅ JSON export works
✅ YAML export works
✅ Scheduler status works
✅ Clear-cache command works
✅ Database export works

Test Results: 11/11 tests passed
🎉 All tests passed!
```

### Sample Project Check Output
```
╭─────────────────────────────────────────────── Statistics ───────────────────────────────────────────────╮
│ Checked files: requirements.txt, setup.py                                                                │
│ Total packages: 10                                                                                       │
│ Deprecated: 8                                                                                            │
│ Safe: 2                                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────╯

Found deprecated packages:
  • requests (2.28.1) → httpx, aiohttp
  • flask (2.2.3) → fastapi, starlette
  • django-cors-headers (3.14.0) → django-cors-headers 4.0+
  • psycopg2 (2.9.5) → psycopg, asyncpg
  • pyyaml (6.0) → ruamel.yaml, omegaconf

Safe packages:
  • fastapi (0.104.0)
  • pydantic (2.4.0)
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure you're in the project root
   cd /path/to/is-deprecated-or-not
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Database Issues**
   ```bash
   # Validate database
   python utils/cli.py validate-db
   
   # Clear cache and recreate
   python utils/cli.py clear-cache
   python utils/cli.py update-db --source all
   ```

3. **Permission Issues**
   ```bash
   # Check file permissions
   ls -la utils/cli.py
   
   # Make executable if needed
   chmod +x utils/cli.py
   ```

### Debug Mode
```bash
# Run with verbose output
python utils/cli.py check --path test_project --verbose

# Check logs
tail -f logs/checker.log
```

## Continuous Integration

### GitHub Actions Example
```yaml
name: Test CLI Interface

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: python test_cli_comprehensive.py
```

## Performance Benchmarks

### Expected Performance
- **Small project** (< 10 packages): < 1 second
- **Medium project** (10-50 packages): 1-3 seconds
- **Large project** (50+ packages): 3-10 seconds

### Memory Usage
- **Base memory**: ~50MB
- **Per 100 packages**: +10MB
- **Peak memory**: < 200MB for large projects

## Security Testing

### Input Validation
```bash
# Test with malicious input
python utils/cli.py search "'; DROP TABLE packages; --"

# Test with very long package names
python utils/cli.py search "a" * 1000
```

### File Access
```bash
# Test with symlinks
ln -s /etc/passwd test_project/requirements.txt
python utils/cli.py check --path test_project

# Test with non-regular files
python utils/cli.py check --path /dev/null
``` 