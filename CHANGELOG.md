# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release
- CLI interface with Rich output
- Database of deprecated packages
- Multiple export formats (JSON, YAML, CSV)
- Scheduler for automatic updates
- Comprehensive testing suite
- Complete documentation

## [1.0.1] - 2025-01-03

### Fixed
- Fixed GitHub Actions workflows permissions
- Updated release workflow to use modern action
- Added proper permissions for test and release workflows
- Fixed tag name reference in release workflow

### Technical
- Switched from deprecated `actions/create-release@v1` to `softprops/action-gh-release@v1`
- Added explicit permissions for workflow jobs
- Improved reliability of CI/CD pipeline

### Features
- **CLI Interface**: Beautiful command-line interface with Rich tables and panels
- **Database Management**: Built-in database of deprecated packages with alternatives
- **Export Formats**: Support for JSON, YAML, and CSV exports
- **Scheduler**: Automatic database updates with configurable intervals
- **Search Functionality**: Search for specific packages and their alternatives
- **Project Analysis**: Analyze Python projects for deprecated dependencies
- **Validation**: Database validation and integrity checks

### Commands
- `check` - Check project for deprecated dependencies
- `search` - Search for specific package information
- `stats` - View database statistics
- `list-db` - List all deprecated packages
- `validate-db` - Validate database integrity
- `export-db` - Export database in various formats
- `update-db` - Update database from various sources
- `scheduler` - Manage automatic update scheduler
- `clear-cache` - Clear application cache
- `version` - Show version information

### Documentation
- Complete CLI guide with examples
- Testing guide with comprehensive test scenarios
- Installation and setup instructions
- Troubleshooting guide

## [1.0.0] - 2025-01-03

### Added
- Initial release of Deprecated Dependencies Checker
- Core functionality for checking deprecated packages
- CLI interface with Typer and Rich
- Database system with YAML storage
- Export functionality in multiple formats
- Scheduler for automatic updates
- Comprehensive test suite
- Complete documentation

### Technical Details
- **Python Version**: 3.8+
- **Dependencies**: typer, rich, pyyaml, requests, packaging
- **License**: MIT
- **Repository**: https://github.com/julicq/is-deprecated-or-not

### Installation
```bash
pip install -r requirements.txt
```

### Usage
```bash
# Check project for deprecated dependencies
python utils/cli.py check --path /path/to/project

# Search for specific package
python utils/cli.py search requests

# Export database
python utils/cli.py export-db --format json
``` 