"""
Data collector for deprecated packages from various sources.
"""

import requests
import yaml
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PackageInfo:
    """Information about a deprecated package."""
    name: str
    deprecated_since: str
    reason: str
    alternatives: List[Dict[str, str]]
    source: str
    last_updated: str


class DataCollector:
    """Collects data about deprecated packages from various sources."""
    
    def __init__(self, cache_dir: Optional[Path] = None):
        if cache_dir is None:
            cache_dir = Path(__file__).parent.parent / "cache"
        
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)
        
        # Data sources
        self.sources = {
            "pypi": self._collect_from_pypi,
            "github": self._collect_from_github,
            "manual": self._collect_manual_data,
            "security_advisories": self._collect_security_advisories
        }
    
    def collect_all_data(self) -> Dict[str, Any]:
        """Collects data from all sources."""
        all_data = {}
        
        for source_name, collector_func in self.sources.items():
            try:
                logger.info(f"Collecting data from {source_name}...")
                data = collector_func()
                if data:
                    all_data.update(data)
                    logger.info(f"Collected {len(data)} packages from {source_name}")
            except Exception as e:
                logger.error(f"Error collecting from {source_name}: {e}")
        
        return all_data
    
    def _collect_from_pypi(self) -> Dict[str, Any]:
        """Collects deprecated packages from PyPI API."""
        data = {}
        
        # List of known deprecated packages to check
        packages_to_check = [
            "requests", "urllib3", "cryptography", "pyyaml", "jinja2",
            "flask", "celery", "redis", "psycopg2", "django-cors-headers",
            "six", "future", "configparser", "pathlib2", "typing-extensions"
        ]
        
        for package in packages_to_check:
            try:
                # Get package information from PyPI
                response = requests.get(
                    f"https://pypi.org/pypi/{package}/json",
                    timeout=10
                )
                
                if response.status_code == 200:
                    package_data = response.json()
                    
                    # Check if there is information about deprecation
                    if self._is_deprecated_package(package_data):
                        alternatives = self._get_alternatives(package)
                        data[package] = {
                            "deprecated_since": self._extract_deprecation_date(package_data),
                            "reason": self._extract_deprecation_reason(package_data),
                            "alternatives": alternatives,
                            "source": "pypi",
                            "last_updated": datetime.now().isoformat()
                        }
                
                time.sleep(0.1)  # Don't overload API
                
            except Exception as e:
                logger.warning(f"Error checking {package}: {e}")
        
        return data
    
    def _collect_from_github(self) -> Dict[str, Any]:
        """Collects deprecated packages from GitHub repositories."""
        data = {}
        
        # GitHub API endpoints to search deprecated packages
        search_queries = [
            "deprecated python package",
            "python package deprecated",
            "deprecated dependency",
            "python security vulnerability deprecated"
        ]
        
        for query in search_queries:
            try:
                # Here you can use GitHub API to search deprecated packages
                # For now we use static data
                pass
            except Exception as e:
                logger.warning(f"Error searching GitHub: {e}")
        
        return data
    
    def _collect_manual_data(self) -> Dict[str, Any]:
        """Collects manually curated data about deprecated packages."""
        return {
            "requests": {
                "deprecated_since": "2023-01-01",
                "reason": "Recommended to use httpx for better performance and async support",
                "alternatives": [
                    {
                        "name": "httpx",
                        "reason": "Modern HTTP library with async/await support",
                        "migration_guide": "https://www.python-httpx.org/migration/"
                    },
                    {
                        "name": "aiohttp",
                        "reason": "Async HTTP library",
                        "migration_guide": "https://docs.aiohttp.org/"
                    }
                ],
                "source": "manual",
                "last_updated": datetime.now().isoformat()
            },
            "django-cors-headers": {
                "deprecated_since": "2023-06-01",
                "reason": "Old versions have security issues",
                "alternatives": [
                    {
                        "name": "django-cors-headers",
                        "reason": "Update to version 4.0+",
                        "migration_guide": "https://github.com/adamchainz/django-cors-headers"
                    }
                ],
                "source": "manual",
                "last_updated": datetime.now().isoformat()
            }
        }
    
    def _collect_security_advisories(self) -> Dict[str, Any]:
        """Collects data from security advisories."""
        data = {}
        
        # Security advisories sources
        advisory_sources = [
            "https://github.com/advisories",
            "https://nvd.nist.gov/vuln",
            "https://security.snyk.io"
        ]
        
        # Here you can add logic to parse security advisories
        # For now we return empty dictionary
        
        return data
    
    def _is_deprecated_package(self, package_data: Dict[str, Any]) -> bool:
        """Checks if package is deprecated based on PyPI data."""
        # Check different indicators of deprecation
        description = package_data.get("info", {}).get("summary", "").lower()
        keywords = package_data.get("info", {}).get("keywords", "").lower()
        
        deprecated_indicators = [
            "deprecated", "deprecation", "discontinued", "legacy",
            "outdated", "obsolete", "no longer maintained"
        ]
        
        for indicator in deprecated_indicators:
            if indicator in description or indicator in keywords:
                return True
        
        return False
    
    def _extract_deprecation_date(self, package_data: Dict[str, Any]) -> str:
        """Extracts deprecation date from package data."""
        # Try to find deprecation date in description or metadata
        # For now we return approximate date
        return "2023-01-01"
    
    def _extract_deprecation_reason(self, package_data: Dict[str, Any]) -> str:
        """Extracts deprecation reason from package data."""
        description = package_data.get("info", {}).get("summary", "")
        
        # Try to find reason of deprecation in description
        if "deprecated" in description.lower():
            return description
        
        return "Package marked as deprecated"
    
    def _get_alternatives(self, package_name: str) -> List[Dict[str, str]]:
        """Gets alternatives for a deprecated package."""
        # Knowledge base of alternatives
        alternatives_db = {
            "requests": [
                {
                    "name": "httpx",
                    "reason": "Modern HTTP library with async/await support",
                    "migration_guide": "https://www.python-httpx.org/migration/"
                },
                {
                    "name": "aiohttp",
                    "reason": "Async HTTP library",
                    "migration_guide": "https://docs.aiohttp.org/"
                }
            ],
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
            ]
        }
        
        return alternatives_db.get(package_name, [])
    
    def update_database(self, output_path: Optional[Path] = None) -> None:
        """Updates the deprecated packages database."""
        if output_path is None:
            output_path = Path(__file__).parent.parent / "data" / "deprecated_packages.yaml"
        
        # Collect data
        logger.info("Starting data collection...")
        new_data = self.collect_all_data()
        
        # Load existing data
        existing_data = {}
        if output_path.exists():
            with open(output_path, 'r', encoding='utf-8') as f:
                existing_data = yaml.safe_load(f) or {}
        
        # Merge data
        merged_data = self._merge_data(existing_data, new_data)
        
        # Save updated database
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(merged_data, f, default_flow_style=False, allow_unicode=True)
        
        logger.info(f"Database updated with {len(merged_data)} packages")
    
    def _merge_data(self, existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
        """Merges existing and new data."""
        merged = existing.copy()
        
        for package_name, package_data in new.items():
            if package_name in merged:
                # Update existing data
                existing_package = merged[package_name]
                existing_package.update(package_data)
                existing_package["last_updated"] = datetime.now().isoformat()
            else:
                # Add new data
                merged[package_name] = package_data
        
        return merged
    
    def get_statistics(self) -> Dict[str, Any]:
        """Gets statistics about the collected data."""
        db_path = Path(__file__).parent.parent / "data" / "deprecated_packages.yaml"
        
        if not db_path.exists():
            return {"total_packages": 0, "sources": {}}
        
        with open(db_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        
        sources = {}
        for package_data in data.values():
            source = package_data.get("source", "unknown")
            sources[source] = sources.get(source, 0) + 1
        
        return {
            "total_packages": len(data),
            "sources": sources,
            "last_updated": max(
                (pkg.get("last_updated", "1970-01-01") for pkg in data.values()),
                default="unknown"
            )
        } 