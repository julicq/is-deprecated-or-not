#!/usr/bin/env python3
"""
Tests for Deprecated Checker.
"""

import unittest
from pathlib import Path
import tempfile
import shutil
import yaml

from core.checker import DeprecatedChecker
from core.parser import DependencyParser
from core.database import DeprecatedPackageDB


class TestDeprecatedChecker(unittest.TestCase):
    """Tests for main functionality."""
    
    def setUp(self):
        """Setup tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
        
        # Create test database
        self.test_db_data = {
            "requests": {
                "deprecated_since": "2023-01-01",
                "reason": "Test reason",
                "alternatives": [
                    {
                        "name": "httpx",
                        "reason": "Better alternative",
                        "migration_guide": "https://example.com"
                    }
                ]
            }
        }
        
        # Create temporary database
        self.db_path = self.project_path / "test_db.yaml"
        with open(self.db_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.test_db_data, f)
        
        self.checker = DeprecatedChecker(self.db_path)
    
    def tearDown(self):
        """Cleanup after tests."""
        shutil.rmtree(self.temp_dir)
    
    def test_parse_requirements_txt(self):
        """Test parsing requirements.txt."""
        # Create test requirements.txt
        req_file = self.project_path / "requirements.txt"
        with open(req_file, 'w', encoding='utf-8') as f:
            f.write("requests==2.31.0\n")
            f.write("fastapi==0.104.0\n")
            f.write("# Comment\n")
            f.write("pydantic>=2.0.0\n")
        
        parser = DependencyParser()
        deps = parser.parse_requirements_txt(req_file)
        
        self.assertEqual(len(deps), 3)
        self.assertIn(("requests", "==2.31.0"), deps)
        self.assertIn(("fastapi", "==0.104.0"), deps)
        self.assertIn(("pydantic", ">=2.0.0"), deps)
    
    def test_check_deprecated_package(self):
        """Test checking deprecated package."""
        # Create requirements.txt with deprecated package
        req_file = self.project_path / "requirements.txt"
        with open(req_file, 'w', encoding='utf-8') as f:
            f.write("requests==2.31.0\n")
            f.write("fastapi==0.104.0\n")
        
        result = self.checker.check_project(self.project_path)
        
        self.assertEqual(result.total_deprecated, 1)
        self.assertEqual(result.total_safe, 1)
        self.assertEqual(result.deprecated_packages[0].name, "requests")
        self.assertEqual(result.safe_packages[0]["name"], "fastapi")
    
    def test_extract_version(self):
        """Test extracting version."""
        checker = DeprecatedChecker()
        
        self.assertEqual(checker._extract_version("==2.31.0"), "2.31.0")
        self.assertEqual(checker._extract_version(">=2.0.0"), "2.0.0")
        self.assertEqual(checker._extract_version("~=1.0"), "1.0")
        self.assertEqual(checker._extract_version(""), "")
    
    def test_generate_report(self):
        """Test generating report."""
        # Create test data
        req_file = self.project_path / "requirements.txt"
        with open(req_file, 'w', encoding='utf-8') as f:
            f.write("requests==2.31.0\n")
        
        result = self.checker.check_project(self.project_path)
        
        # Test text report
        text_report = self.checker.generate_report(result, "text")
        self.assertIn("requests", text_report)
        self.assertIn("deprecated", text_report)
        
        # Test JSON report
        json_report = self.checker.generate_report(result, "json")
        self.assertIn("requests", json_report)
        self.assertIn("deprecated_packages", json_report)
        
        # Test YAML report
        yaml_report = self.checker.generate_report(result, "yaml")
        self.assertIn("requests", yaml_report)


class TestDatabase(unittest.TestCase):
    """Tests for database."""
    
    def setUp(self):
        """Setup tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test_db.yaml"
        
        # Create test database
        test_data = {
            "requests": {
                "deprecated_since": "2023-01-01",
                "reason": "Test reason",
                "alternatives": [
                    {
                        "name": "httpx",
                        "reason": "Better alternative",
                        "migration_guide": "https://example.com"
                    }
                ]
            }
        }
        
        with open(self.db_path, 'w', encoding='utf-8') as f:
            yaml.dump(test_data, f)
        
        self.db = DeprecatedPackageDB(self.db_path)
    
    def tearDown(self):
        """Cleanup after tests."""
        shutil.rmtree(self.temp_dir)
    
    def test_is_deprecated(self):
        """Test checking deprecated package."""
        self.assertTrue(self.db.is_deprecated("requests"))
        self.assertFalse(self.db.is_deprecated("fastapi"))
    
    def test_get_alternatives(self):
        """Test getting alternatives."""
        alternatives = self.db.get_alternatives("requests")
        self.assertEqual(len(alternatives), 1)
        self.assertEqual(alternatives[0]["name"], "httpx")
    
    def test_get_migration_guide(self):
        """Test getting migration guide."""
        guide = self.db.get_migration_guide("requests", "httpx")
        self.assertEqual(guide, "https://example.com")
    
    def test_get_all_deprecated_packages(self):
        """Test getting all deprecated packages."""
        packages = self.db.get_all_deprecated_packages()
        self.assertEqual(len(packages), 1)
        self.assertIn("requests", packages)


class TestParser(unittest.TestCase):
    """Tests for parser."""
    
    def setUp(self):
        """Setup tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir)
        self.parser = DependencyParser()
    
    def tearDown(self):
        """Cleanup after tests."""
        shutil.rmtree(self.temp_dir)
    
    def test_parse_all_files(self):
        """Test parsing all files."""
        # Create requirements.txt
        req_file = self.project_path / "requirements.txt"
        with open(req_file, 'w', encoding='utf-8') as f:
            f.write("requests==2.31.0\n")
        
        # Create setup.py
        setup_file = self.project_path / "setup.py"
        with open(setup_file, 'w', encoding='utf-8') as f:
            f.write("""
from setuptools import setup

setup(
    name="test-package",
    install_requires=[
        "fastapi==0.104.0",
        "pydantic>=2.0.0"
    ]
)
""")
        
        results = self.parser.parse_all_files(self.project_path)
        
        self.assertIn("requirements.txt", results)
        self.assertIn("setup.py", results)
        self.assertEqual(len(results["requirements.txt"]), 1)
        self.assertEqual(len(results["setup.py"]), 2)


if __name__ == "__main__":
    unittest.main() 