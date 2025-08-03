# CLI Interface Guide

## Overview

The CLI interface provides a convenient way to work with the deprecated dependencies checker through the command line.

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Main Commands

### 1. Project Checking

```bash
# Check current directory
python utils/cli.py check

# Check specific project
python utils/cli.py check --path /path/to/project

# Export result to JSON
python utils/cli.py check --export json --output report.json

# Verbose output
python utils/cli.py check --verbose
```

### 2. Database Management

```bash
# View database statistics
python utils/cli.py stats

# List all deprecated packages
python utils/cli.py list-db

# Search for information about specific package
python utils/cli.py search requests

# Validate database
python utils/cli.py validate-db

# Export database
python utils/cli.py export-db --format json --output db_export.json
```

### 3. Database Updates

```bash
# Update from all sources
python utils/cli.py update-db --source all

# Update from specific source
python utils/cli.py update-db --source pypi
python utils/cli.py update-db --source github
python utils/cli.py update-db --source security_advisories

# Force update
python utils/cli.py update-db --force
```

### 4. Update Scheduler

```bash
# Start scheduler
python utils/cli.py scheduler start --interval 24

# Stop scheduler
python utils/cli.py scheduler stop

# Check status
python utils/cli.py scheduler status

# Force update
python utils/cli.py scheduler force-update
```

### 5. Utilities

```bash
# Clear cache
python utils/cli.py clear-cache

# Version information
python utils/cli.py version
```

## Usage Examples

### Check project with detailed report

```bash
python utils/cli.py check --path ./my-project --verbose --export json --output report.json
```

### Monitor deprecated packages

```bash
# Start scheduler for automatic updates
python utils/cli.py scheduler start --interval 12

# Check status
python utils/cli.py scheduler status
```

### Export data for analysis

```bash
# Export to JSON
python utils/cli.py export-db --format json --output deprecated_packages.json

# Export to YAML
python utils/cli.py export-db --format yaml --output deprecated_packages.yaml

# Export to CSV
python utils/cli.py export-db --format csv --output deprecated_packages.csv
```

## Output Formats

### JSON
```json
{
  "files_checked": ["requirements.txt", "setup.py"],
  "total_deprecated": 2,
  "total_safe": 15,
  "deprecated_packages": [
    {
      "name": "requests",
      "current_version": "2.28.1",
      "file_source": "requirements.txt",
      "reason": "Recommended to use httpx",
      "deprecated_since": "2023-01-01",
      "alternatives": [
        {
          "name": "httpx",
          "reason": "Modern HTTP library",
          "migration_guide": "https://www.python-httpx.org/migration/"
        }
      ]
    }
  ]
}
```

### YAML
```yaml
files_checked:
  - requirements.txt
  - setup.py
total_deprecated: 2
total_safe: 15
deprecated_packages:
  - name: requests
    current_version: "2.28.1"
    file_source: requirements.txt
    reason: "Recommended to use httpx"
    deprecated_since: "2023-01-01"
    alternatives:
      - name: httpx
        reason: "Modern HTTP library"
        migration_guide: "https://www.python-httpx.org/migration/"
```

## Configuration

### Scheduler Configuration

The scheduler can be configured through a configuration file:

```yaml
# config/scheduler_config.yaml
scheduler:
  interval_hours: 24
  auto_start: true
  sources:
    - pypi
    - github
    - security_advisories
```

### Logging

Logs are saved in the `logs/` directory:

```bash
# View logs
tail -f logs/checker.log
```

## Troubleshooting

### Module Import Issues

```bash
# Make sure you are in the project root directory
cd /path/to/is-deprecated-or-not

# Check that all dependencies are installed
pip install -r requirements.txt
```

### Database Issues

```bash
# Validate database
python utils/cli.py validate-db

# Clear cache
python utils/cli.py clear-cache

# Recreate database
rm -rf cache/
python utils/cli.py update-db --source all
```

### Scheduler Issues

```bash
# Check status
python utils/cli.py scheduler status

# Restart scheduler
python utils/cli.py scheduler stop
python utils/cli.py scheduler start
```

## Demonstration

Run the demonstration script to explore the capabilities:

```bash
python demo_cli.py
```

## Support

If you encounter problems:

1. Check logs in the `logs/` directory
2. Make sure all dependencies are installed
3. Try clearing the cache: `python utils/cli.py clear-cache`
4. Recreate the database: `python utils/cli.py update-db --source all` 