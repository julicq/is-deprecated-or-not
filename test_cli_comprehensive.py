#!/usr/bin/env python3
"""
Comprehensive test suite for CLI interface.
"""

import subprocess
import json
import yaml
import sys
from pathlib import Path

def run_command(cmd, capture_output=True):
    """Run command and return result."""
    try:
        result = subprocess.run(
            cmd.split(),
            capture_output=capture_output,
            text=True,
            cwd=Path(__file__).parent
        )
        return result
    except Exception as e:
        print(f"Error running command: {e}")
        return None

def test_version():
    """Test version command."""
    print("Testing version command...")
    result = run_command("python utils/cli.py version")
    if result and result.returncode == 0:
        print("Version command works")
        return True
    else:
        print("Version command failed")
        return False

def test_stats():
    """Test stats command."""
    print("Testing stats command...")
    result = run_command("python utils/cli.py stats")
    if result and result.returncode == 0 and "Total packages:" in result.stdout:
        print("Stats command works")
        return True
    else:
        print("Stats command failed")
        return False

def test_search():
    """Test search command."""
    print("Testing search command...")
    result = run_command("python utils/cli.py search requests")
    if result and result.returncode == 0 and "deprecated" in result.stdout:
        print("Search command works")
        return True
    else:
        print("Search command failed")
        return False

def test_list_db():
    """Test list-db command."""
    print("Testing list-db command...")
    result = run_command("python utils/cli.py list-db")
    if result and result.returncode == 0:
        print("List-db command works")
        return True
    else:
        print("List-db command failed")
        return False

def test_validate_db():
    """Test validate-db command."""
    print("Testing validate-db command...")
    result = run_command("python utils/cli.py validate-db")
    if result and result.returncode == 0 and "valid" in result.stdout:
        print("Validate-db command works")
        return True
    else:
        print("Validate-db command failed")
        return False

def test_check_project():
    """Test project checking."""
    print("Testing project check...")
    result = run_command("python utils/cli.py check --path test_project")
    if result and result.returncode == 0:
        print("Project check works")
        return True
    else:
        print("Project check failed")
        return False

def test_export_json():
    """Test JSON export."""
    print("Testing JSON export...")
    result = run_command("python utils/cli.py check --path test_project --export json --output test_export.json")
    if result and result.returncode == 0:
        # Check if file was created
        if Path("test_export.json").exists():
            print("JSON export works")
            return True
        else:
            print("JSON export file not created")
            return False
    else:
        print("JSON export failed")
        return False

def test_export_yaml():
    """Test YAML export."""
    print("Testing YAML export...")
    result = run_command("python utils/cli.py check --path test_project --export yaml --output test_export.yaml")
    if result and result.returncode == 0:
        # Check if file was created
        if Path("test_export.yaml").exists():
            print("YAML export works")
            return True
        else:
            print("YAML export file not created")
            return False
    else:
        print("YAML export failed")
        return False

def test_scheduler():
    """Test scheduler commands."""
    print("Testing scheduler commands...")
    
    # Test status
    result = run_command("python utils/cli.py scheduler status")
    if result and result.returncode == 0:
        print("Scheduler status works")
    else:
        print("Scheduler status failed")
        return False
    
    return True

def test_clear_cache():
    """Test clear-cache command."""
    print("Testing clear-cache command...")
    result = run_command("python utils/cli.py clear-cache")
    if result and result.returncode == 0:
        print("Clear-cache command works")
        return True
    else:
        print("Clear-cache command failed")
        return False

def test_export_db():
    """Test database export."""
    print("Testing database export...")
    result = run_command("python utils/cli.py export-db --format json --output db_export.json")
    if result and result.returncode == 0:
        if Path("db_export.json").exists():
            print("Database export works")
            return True
        else:
            print("Database export file not created")
            return False
    else:
        print("Database export failed")
        return False

def main():
    """Run all tests."""
    print("Starting comprehensive CLI tests...")
    print("=" * 50)
    
    tests = [
        test_version,
        test_stats,
        test_search,
        test_list_db,
        test_validate_db,
        test_check_project,
        test_export_json,
        test_export_yaml,
        test_scheduler,
        test_clear_cache,
        test_export_db
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed!")
        return 0
    else:
        print("Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 