"""
Repository analyzer for collecting dependency information and building dynamic database.
"""

import requests
import yaml
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from datetime import datetime
import logging

from .parser import DependencyParser

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RepositoryAnalyzer:
    """Analyzes repository dependencies and builds dynamic database."""
    
    def __init__(self):
        self.parser = DependencyParser()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'deprecated-checker/1.0'
        })
    
    def analyze_repository(self, project_path: Path) -> Dict[str, Any]:
        """Analyzes repository and builds database for found dependencies."""
        logger.info(f"Analyzing repository: {project_path}")
        
        # Parse all dependencies in the repository
        dependencies_by_file = self.parser.parse_all_files(project_path)
        
        # Extract unique packages
        unique_packages = self._extract_unique_packages(dependencies_by_file)
        logger.info(f"Found {len(unique_packages)} unique packages in repository")
        
        # Build database for these packages
        database = self._build_database_for_packages(unique_packages)
        
        return database
    
    def _extract_unique_packages(self, dependencies_by_file: Dict[str, List[tuple]]) -> Set[str]:
        """Extracts unique package names from all dependency files."""
        unique_packages = set()
        
        for file_name, dependencies in dependencies_by_file.items():
            for package_name, package_version in dependencies:
                unique_packages.add(package_name)
        
        return unique_packages
    
    def _build_database_for_packages(self, packages: Set[str]) -> Dict[str, Any]:
        """Builds database by checking each package for deprecation status."""
        database = {}
        
        for package_name in packages:
            logger.info(f"Checking package: {package_name}")
            
            # Check package on PyPI
            package_info = self._check_package_on_pypi(package_name)
            
            if package_info:
                database[package_name] = package_info
                logger.info(f"Added {package_name} to database")
            else:
                logger.debug(f"Package {package_name} not found or not deprecated")
        
        logger.info(f"Built database with {len(database)} deprecated packages")
        return database
    
    def _check_package_on_pypi(self, package_name: str) -> Optional[Dict[str, Any]]:
        """Checks package on PyPI for deprecation status."""
        try:
            # Get package information from PyPI
            response = self.session.get(
                f"https://pypi.org/pypi/{package_name}/json",
                timeout=10
            )
            
            if response.status_code == 200:
                package_data = response.json()
                
                # Check if package is deprecated
                if self._is_deprecated_package(package_data):
                    alternatives = self._get_alternatives_for_package(package_name)
                    
                    return {
                        "deprecated_since": self._extract_deprecation_date(package_data),
                        "reason": self._extract_deprecation_reason(package_data),
                        "alternatives": alternatives,
                        "source": "pypi_analysis",
                        "last_updated": datetime.now().isoformat(),
                        "package_info": {
                            "latest_version": package_data.get("info", {}).get("version", ""),
                            "summary": package_data.get("info", {}).get("summary", ""),
                            "home_page": package_data.get("info", {}).get("home_page", ""),
                            "project_url": package_data.get("info", {}).get("project_url", "")
                        }
                    }
            
            time.sleep(0.1)  # Don't overload API
            
        except Exception as e:
            logger.warning(f"Error checking package {package_name}: {e}")
        
        return None
    
    def _is_deprecated_package(self, package_data: Dict[str, Any]) -> bool:
        """Checks if package is deprecated based on PyPI data."""
        info = package_data.get("info", {})
        
        # Check different indicators of deprecation
        description = info.get("summary", "")
        keywords = info.get("keywords", "")
        classifiers = info.get("classifiers", [])
        
        # Handle None values
        if description is None:
            description = ""
        if keywords is None:
            keywords = ""
        
        description = description.lower()
        keywords = keywords.lower()
        
        deprecated_indicators = [
            "deprecated", "deprecation", "discontinued", "legacy",
            "outdated", "obsolete", "no longer maintained", "end of life",
            "eol", "sunset", "archived"
        ]
        
        # Check description and keywords
        for indicator in deprecated_indicators:
            if indicator in description or indicator in keywords:
                return True
        
        # Check classifiers for deprecation
        for classifier in classifiers:
            if "deprecated" in classifier.lower() or "end of life" in classifier.lower():
                return True
        
        # Check for specific patterns in description
        if any(pattern in description for pattern in [
            "this package is deprecated",
            "use alternative",
            "no longer supported",
            "moved to",
            "replaced by"
        ]):
            return True
        
        return False
    
    def _extract_deprecation_date(self, package_data: Dict[str, Any]) -> str:
        """Extracts deprecation date from package data."""
        # Try to find deprecation date in description or metadata
        # For now we return approximate date based on latest release
        info = package_data.get("info", {})
        latest_version = info.get("version", "")
        
        # Try to extract date from version or use current date
        if latest_version:
            return f"{datetime.now().year}-01-01"
        
        return datetime.now().strftime("%Y-%m-%d")
    
    def _extract_deprecation_reason(self, package_data: Dict[str, Any]) -> str:
        """Extracts deprecation reason from package data."""
        info = package_data.get("info", {})
        description = info.get("summary", "")
        
        # Handle None values
        if description is None:
            description = ""
        
        # Try to find reason of deprecation in description
        if "deprecated" in description.lower():
            # Extract the sentence containing "deprecated"
            sentences = description.split('.')
            for sentence in sentences:
                if "deprecated" in sentence.lower():
                    return sentence.strip()
        
        # Check for common deprecation patterns
        if "use alternative" in description.lower():
            return "Package deprecated, use alternative"
        elif "no longer supported" in description.lower():
            return "Package no longer supported"
        elif "moved to" in description.lower():
            return "Package moved to alternative"
        elif "replaced by" in description.lower():
            return "Package replaced by alternative"
        
        return "Package marked as deprecated"
    
    def _get_alternatives_for_package(self, package_name: str) -> List[Dict[str, str]]:
        """Gets alternatives for a deprecated package."""
        # Knowledge base of alternatives
        alternatives_db = {
            "urllib3": [
                {
                    "name": "urllib3",
                    "reason": "Update to version 2.0+",
                    "migration_guide": "https://urllib3.readthedocs.io/"
                }
            ],
            "cryptography": [
                {
                    "name": "cryptography",
                    "reason": "Update to version 41.0+",
                    "migration_guide": "https://cryptography.io/"
                }
            ],

            "jinja2": [
                {
                    "name": "jinja2",
                    "reason": "Update to version 3.1+",
                    "migration_guide": "https://jinja.palletsprojects.com/"
                }
            ],
            "flask": [
                {
                    "name": "fastapi",
                    "reason": "Modern async web framework",
                    "migration_guide": "https://fastapi.tiangolo.com/"
                },
                {
                    "name": "starlette",
                    "reason": "Lightweight ASGI framework",
                    "migration_guide": "https://www.starlette.io/"
                }
            ],
            "celery": [
                {
                    "name": "celery",
                    "reason": "Update to version 5.3+",
                    "migration_guide": "https://docs.celeryproject.org/"
                },
                {
                    "name": "rq",
                    "reason": "Simple job queue",
                    "migration_guide": "https://python-rq.org/"
                }
            ],
            "redis": [
                {
                    "name": "redis",
                    "reason": "Update to version 4.5+",
                    "migration_guide": "https://redis.io/"
                }
            ],
            "psycopg2": [
                {
                    "name": "psycopg",
                    "reason": "Modern PostgreSQL adapter",
                    "migration_guide": "https://www.psycopg.org/"
                },
                {
                    "name": "asyncpg",
                    "reason": "Async PostgreSQL driver",
                    "migration_guide": "https://asyncpg.readthedocs.io/"
                }
            ],
            "django-cors-headers": [
                {
                    "name": "django-cors-headers",
                    "reason": "Update to version 4.0+",
                    "migration_guide": "https://github.com/adamchainz/django-cors-headers"
                }
            ]
        }
        
        return alternatives_db.get(package_name, [])
    
    def save_database(self, database: Dict[str, Any], cache_dir: Optional[Path] = None) -> None:
        """Saves the built database to cache."""
        try:
            if cache_dir is None:
                cache_dir = Path(__file__).parent.parent / "cache"
            
            cache_dir.mkdir(exist_ok=True)
            
            cache_file = cache_dir / "repository_database.yaml"
            with open(cache_file, 'w', encoding='utf-8') as f:
                yaml.dump(database, f, default_flow_style=False, allow_unicode=True)
            
            logger.info(f"Saved repository database to cache: {cache_file}")
        except Exception as e:
            logger.error(f"Failed to save repository database: {e}")
    
    def get_statistics(self, database: Dict[str, Any]) -> Dict[str, Any]:
        """Gets statistics about the built database."""
        return {
            "total_packages": len(database),
            "deprecated_packages": len([pkg for pkg in database.values() if pkg.get("deprecated_since")]),
            "sources": list(set(pkg.get("source", "unknown") for pkg in database.values())),
            "last_updated": datetime.now().isoformat()
        } 