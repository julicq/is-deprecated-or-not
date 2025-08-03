#!/usr/bin/env python3
"""
Deprecated Checker - Tool for checking deprecated dependencies in Python projects.

Usage:
    python deprecated_checker.py check [--path PATH] [--export FORMAT] [--output FILE] [--verbose]
    python deprecated_checker.py list-db
    python deprecated_checker.py search PACKAGE
"""

import sys
from pathlib import Path

# Add current directory to path for import modules
sys.path.insert(0, str(Path(__file__).parent))

from utils.cli import app


def main():
    """Main function to run CLI."""
    app()


if __name__ == "__main__":
    main() 