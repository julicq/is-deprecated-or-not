# Deprecated Checker

Tool for checking deprecated dependencies in Python projects and suggesting alternatives.

## Features

- **Dynamic Repository Analysis**: Automatically analyzes repository dependencies and builds database based on actual project packages
- **Comprehensive Database Updates**: Updates database with all known deprecated packages from multiple sources
- **Automatic detection of deprecated packages** from requirements.txt, setup.py, pyproject.toml
- **Smart alternatives suggestion** with migration guides
- **Beautiful reports** with Rich library
- **Fast CLI interface** for quick checks
- **Automatic update scheduler** for keeping database current
- **Data export** in JSON, YAML, and CSV formats
- **Cross-Python version compatibility** (3.10, 3.12, 3.12.10)
- **Repository-specific analysis** - only checks packages actually used in your project

## Installation

### From PyPI
```bash
pip install deprecated-checker
```

### From Source
```bash
git clone https://github.com/yourusername/deprecated-checker.git
cd deprecated-checker
pip install -r requirements.txt
```

## Usage

### CLI Interface (Recommended)

```bash
# Check current directory
deprecated-checker check

# Check specific project
deprecated-checker check --path /path/to/project

# Export to JSON
deprecated-checker check --export json --output report.json

# Verbose output
deprecated-checker check --verbose

# View database statistics
deprecated-checker stats

# Search for package information
deprecated-checker search requests

# Update database from all sources
deprecated-checker update-db --source all

# Comprehensive database update (checks hundreds of packages)
deprecated-checker update-db --comprehensive

# Analyze repository dependencies
deprecated-checker analyze-repository

# List all deprecated packages in database
deprecated-checker list-db

# Validate database
deprecated-checker validate-db

# Export database
deprecated-checker export-db --format json --output db_export.json

# Scheduler management
deprecated-checker scheduler start --interval 24
deprecated-checker scheduler status
deprecated-checker scheduler force-update
```

### Repository Analysis

The tool now automatically analyzes your repository's dependencies and builds a dynamic database:

```bash
# Analyze current repository
deprecated-checker analyze-repository

# Analyze specific repository
deprecated-checker analyze-repository --path /path/to/project

# Save analysis results
deprecated-checker analyze-repository --save
```

### Comprehensive Database Updates

Update the database with all known deprecated packages:

```bash
# Update with comprehensive data (may take several minutes)
deprecated-checker update-db --comprehensive
```

This will check hundreds of packages and save results to `data/comprehensive_deprecated_packages.yaml`.

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

### Repository Analysis
```
✓ Analysis complete! Found 3 deprecated packages

┌─────────────┬──────────────────┬─────────────────────┬─────────────────┐
│ Package     │ Deprecated since │ Reason              │ Source          │
├─────────────┼──────────────────┼─────────────────────┼─────────────────┤
│ pycrypto    │ 2020-01-01       │ Package deprecated  │ pypi_analysis   │
│ bottle      │ 2021-01-01       │ Package deprecated  │ pypi_analysis   │
│ six         │ 2022-01-01       │ Package deprecated  │ pypi_analysis   │
└─────────────┴──────────────────┴─────────────────────┴─────────────────┘
```

### Dependency Check
```
Checking deprecated dependencies...

Found deprecated packages:
  • django-cors-headers==3.14.0 → django-cors-headers>=4.0.0
  • requests==2.28.0 → httpx>=0.24.0 (recommended)

Safe packages:
  • fastapi==0.104.0
  • pydantic==2.4.0
```

## Key Features

### Dynamic Repository Analysis
- Automatically detects all dependencies in your project
- Checks each package against PyPI for deprecation status
- Builds database specifically for your project's packages
- Falls back to static database if no deprecated packages found

### Comprehensive Database
- Updates from multiple sources: PyPI, GitHub, security advisories
- Includes hundreds of known deprecated packages
- Regular updates via scheduler
- Export/import capabilities

### Cross-Version Compatibility
- Tested with Python 3.10.0, 3.12.0, and 3.12.10
- Compatible with modern Python packaging standards
- Works with both legacy and modern dependency files

## Project Structure

```
is-deprecated-or-not/
├── core/
│   ├── __init__.py
│   ├── checker.py              # Main checking logic
│   ├── config_manager.py       # Configuration management
│   ├── data_collector.py       # Data collection from multiple sources
│   ├── database.py             # Dynamic database management
│   ├── parser.py               # Dependency file parsing
│   ├── repository_analyzer.py  # Repository analysis engine
│   └── scheduler.py            # Update scheduler
├── data/
│   └── deprecated_packages.yaml
├── utils/
│   ├── __init__.py
│   └── cli.py                  # CLI interface
├── config/
│   └── collector_config.yaml
├── cache/                      # Data cache
├── logs/                       # Logs
├── demo_cli.py                # Demonstration script
├── deprecated_checker.py      # Legacy interface
├── CLI_GUIDE.md              # CLI guide
└── INSTALL.md                # Installation guide
```

## Documentation

- [CLI Guide](CLI_GUIDE.md) - Detailed guide for using the CLI interface
- [Installation Guide](INSTALL.md) - Installation and setup instructions
- [Testing Guide](TESTING_GUIDE.md) - Testing and development information
- [PyPI Publishing Guide](PYPI_PUBLISHING_GUIDE.md) - Publishing to PyPI

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details. 