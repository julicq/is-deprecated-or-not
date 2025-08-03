#!/usr/bin/env python3
"""
CLI interface demonstration for deprecated dependencies checker.
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd):
    """Runs command and outputs result."""
    print(f"\nExecuting command: {cmd}")
    print("=" * 50)
    
    try:
        result = subprocess.run(
            cmd.split(),
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"Errors: {result.stderr}")
            
        return result.returncode == 0
    except Exception as e:
        print(f"Command execution error: {e}")
        return False

def main():
    """Main demonstration function."""
    print("CLI Interface Demonstration for Deprecated Dependencies Checker")
    print("=" * 60)
    
    # Show version
    print("\n1. Version information:")
    run_command("python utils/cli.py version")
    
    # Show help
    print("\n2. Command help:")
    run_command("python utils/cli.py --help")
    
    # Check database statistics
    print("\n3. Database statistics:")
    run_command("python utils/cli.py stats")
    
    # Show list of packages in database
    print("\n4. List of deprecated packages in database:")
    run_command("python utils/cli.py list-db")
    
    # Check specific package
    print("\n5. Search for information about 'requests' package:")
    run_command("python utils/cli.py search requests")
    
    # Validate database
    print("\n6. Database validation:")
    run_command("python utils/cli.py validate-db")
    
    # Show scheduler status
    print("\n7. Scheduler status:")
    run_command("python utils/cli.py scheduler status")
    
    print("\nDemonstration completed!")
    print("\nTo check a project use:")
    print("  python utils/cli.py check --path /path/to/project")
    print("\nTo update database:")
    print("  python utils/cli.py update-db --source all")

if __name__ == "__main__":
    main() 