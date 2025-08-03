# Deprecated Checker

Tool for checking deprecated dependencies in Python projects and suggesting alternatives.

## Features

- Automatic detection of deprecated packages
- Analysis of requirements.txt, setup.py, pyproject.toml
- Suggestion of alternative packages
- Beautiful reports with Rich
- Fast checking via CLI
- Automatic update scheduler
- Data export in various formats

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### CLI Interface (Recommended)

```bash
# Check current directory
python utils/cli.py check

# Check specific project
python utils/cli.py check --path /path/to/project

# Export to JSON
python utils/cli.py check --export json --output report.json

# Verbose output
python utils/cli.py check --verbose

# View database statistics
python utils/cli.py stats

# Search for package information
python utils/cli.py search requests

# Update database
python utils/cli.py update-db --source all
```

### Demonstration

```bash
# Run demonstration of all capabilities
python demo_cli.py
```

### Legacy method (deprecated_checker.py)

```bash
# Check current directory
python deprecated_checker.py

# Check specific directory
python deprecated_checker.py --path /path/to/project

# Export to JSON
python deprecated_checker.py --export json

# Export to YAML
python deprecated_checker.py --export yaml
```

## Example Output

```
Checking deprecated dependencies...

Found deprecated packages:
  • django-cors-headers==3.14.0 → django-cors-headers>=4.0.0
  • requests==2.28.0 → httpx>=0.24.0 (recommended)

Safe packages:
  • fastapi==0.104.0
  • pydantic==2.4.0
```

## Project Structure

```
is-deprecated-or-not/
├── core/
│   ├── __init__.py
│   ├── checker.py          # Main checking logic
│   ├── config_manager.py   # Configuration management
│   ├── data_collector.py   # Data collection
│   ├── database.py         # Deprecated packages database
│   ├── parser.py           # Dependency file parsing
│   └── scheduler.py        # Update scheduler
├── data/
│   └── deprecated_packages.yaml
├── utils/
│   ├── __init__.py
│   └── cli.py             # CLI interface
├── config/
│   └── collector_config.yaml
├── cache/                  # Data cache
├── logs/                   # Logs
├── demo_cli.py            # Demonstration script
├── deprecated_checker.py  # Legacy interface
└── CLI_GUIDE.md          # CLI guide
```

## Documentation

- [CLI Guide](CLI_GUIDE.md) - Detailed guide for using the CLI interface
- [Data Collector Guide](DATA_COLLECTOR_GUIDE.md) - Information about collecting deprecated package data
- [Parser Summary](PARSER_SUMMARY.md) - Details about dependency parser work 