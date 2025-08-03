#!/usr/bin/env python3
"""
Script for building and publishing the deprecated-checker package to PyPI.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, check=True):
    """Run command and return result."""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"STDERR: {result.stderr}")
        if check and result.returncode != 0:
            print(f"Command failed with exit code {result.returncode}")
            return False
        return True
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def clean_build():
    """Clean previous build artifacts."""
    print("Cleaning previous build artifacts...")
    commands = [
        "rm -rf build/",
        "rm -rf dist/",
        "rm -rf *.egg-info/",
        "find . -name '*.pyc' -delete",
        "find . -name '__pycache__' -type d -exec rm -rf {} +"
    ]
    
    for cmd in commands:
        if not run_command(cmd, check=False):
            print(f"Warning: {cmd} failed")

def build_package():
    """Build the package."""
    print("Building package...")
    return run_command("python -m build")

def check_package():
    """Check the built package."""
    print("Checking built package...")
    return run_command("python -m twine check dist/*")

def upload_to_testpypi():
    """Upload to TestPyPI."""
    print("Uploading to TestPyPI...")
    return run_command("python -m twine upload --repository testpypi dist/*")

def upload_to_pypi():
    """Upload to PyPI."""
    print("Uploading to PyPI...")
    return run_command("python -m twine upload dist/*")

def install_dev_dependencies():
    """Install development dependencies."""
    print("Installing development dependencies...")
    return run_command("pip install build twine")

def main():
    """Main function."""
    print("Starting package build and publish process...")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("Error: pyproject.toml not found. Are you in the project root?")
        return 1
    
    # Install dev dependencies
    if not install_dev_dependencies():
        print("Failed to install development dependencies")
        return 1
    
    # Clean previous builds
    clean_build()
    
    # Build package
    if not build_package():
        print("Failed to build package")
        return 1
    
    # Check package
    if not check_package():
        print("Package check failed")
        return 1
    
    print("Package built and checked successfully!")
    print()
    print("Package files created:")
    for file in Path("dist").glob("*"):
        print(f"  - {file}")
    print()
    
    # Ask user what to do next
    print("What would you like to do?")
    print("1. Upload to TestPyPI (recommended for testing)")
    print("2. Upload to PyPI (production)")
    print("3. Exit without uploading")
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == "1":
        if upload_to_testpypi():
            print("Successfully uploaded to TestPyPI!")
            print("TestPyPI URL: https://test.pypi.org/project/deprecated-checker/")
        else:
            print("Failed to upload to TestPyPI")
            return 1
    elif choice == "2":
        print("Warning: This will upload to production PyPI!")
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        if confirm == "yes":
            if upload_to_pypi():
                print("Successfully uploaded to PyPI!")
                print("PyPI URL: https://pypi.org/project/deprecated-checker/")
            else:
                print("Failed to upload to PyPI")
                return 1
        else:
            print("Upload cancelled")
    else:
        print("Upload cancelled")
    
    print()
    print("Build process completed!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 