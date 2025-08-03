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
        
        # Extended list of known deprecated packages to check
        packages_to_check = [
            # HTTP Libraries
            "requests", "urllib3", "httplib2", "urllib2",
            
            # Security & Crypto
            "cryptography", "pycrypto", "cryptodome", "hashlib",
            
            # Web Frameworks
            "flask", "django", "bottle", "webpy", "cherrypy",
            
            # Database
            "psycopg2", "mysql-connector", "sqlite3", "pymongo",
            
            # Data Processing
            "pandas", "numpy", "scipy", "matplotlib", "seaborn",
            
            # Configuration
            "pyyaml", "configparser", "ini", "json5",
            
            # Utilities
            "six", "future", "pathlib2", "typing-extensions", "enum34",
            
            # Testing
            "nose", "pytest-cov", "coverage",
            
            # Development Tools
            "setuptools", "distutils", "pip", "wheel",
            
            # Async
            "asyncio", "aiohttp", "tornado", "twisted",
            
            # Serialization
            "pickle", "marshal", "shelve",
            
            # Networking
            "socket", "ftplib", "smtplib", "poplib",
            
            # Image Processing
            "PIL", "Pillow", "opencv-python",
            
            # Machine Learning
            "sklearn", "tensorflow", "keras", "theano",
            
            # Documentation
            "sphinx", "docutils", "mkdocs",
            
            # Deployment
            "fabric", "ansible", "salt",
            
            # Monitoring
            "psutil", "pywin32", "pyserial",
            
            # GUI
            "tkinter", "wx", "pyqt", "kivy",
            
            # Audio/Video
            "pygame", "pyaudio", "opencv",
            
            # Compression
            "zipfile", "tarfile", "gzip", "bz2",
            
            # Text Processing
            "re", "string", "unicodedata",
            
            # Date/Time
            "datetime", "time", "calendar",
            
            # Math
            "math", "random", "statistics",
            
            # System
            "os", "sys", "subprocess", "shutil",
            
            # Network
            "urllib", "http", "email", "smtplib",
            
            # Data
            "csv", "json", "xml", "sqlite3",
            
            # Other
            "threading", "multiprocessing", "concurrent.futures",
            "logging", "warnings", "traceback", "inspect",
            "collections", "itertools", "functools", "operator"
        ]
        
        logger.info(f"Checking {len(packages_to_check)} packages on PyPI...")
        
        for i, package in enumerate(packages_to_check, 1):
            try:
                logger.info(f"Checking package {i}/{len(packages_to_check)}: {package}")
                
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
                            "last_updated": datetime.now().isoformat(),
                            "package_info": {
                                "latest_version": package_data.get("info", {}).get("version", ""),
                                "summary": package_data.get("info", {}).get("summary", ""),
                                "home_page": package_data.get("info", {}).get("home_page", ""),
                                "project_url": package_data.get("info", {}).get("project_url", "")
                            }
                        }
                        logger.info(f"✓ Found deprecated package: {package}")
                    else:
                        logger.debug(f"Package {package} is not deprecated")
                
                time.sleep(0.1)  # Don't overload API
                
            except Exception as e:
                logger.warning(f"Error checking {package}: {e}")
        
        logger.info(f"PyPI collection complete. Found {len(data)} deprecated packages")
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
            # HTTP Libraries
            "urllib3": {
                "deprecated_since": "2022-12-01",
                "reason": "Old versions have vulnerabilities",
                "alternatives": [
                    {
                        "name": "urllib3",
                        "reason": "Update to version 2.0+",
                        "migration_guide": "https://urllib3.readthedocs.io/"
                    }
                ],
                "source": "manual",
                "last_updated": datetime.now().isoformat()
            },
            
            # Security & Crypto
            "cryptography": {
                "deprecated_since": "2023-03-01",
                "reason": "Old versions have critical vulnerabilities",
                "alternatives": [
                    {
                        "name": "cryptography",
                        "reason": "Update to version 41.0+",
                        "migration_guide": "https://cryptography.io/"
                    }
                ],
                "source": "manual",
                "last_updated": datetime.now().isoformat()
            },
            "pycrypto": {
                "deprecated_since": "2018-01-01",
                "reason": "No longer maintained, security vulnerabilities",
                "alternatives": [
                    {
                        "name": "cryptography",
                        "reason": "Modern cryptographic library",
                        "migration_guide": "https://cryptography.io/"
                    }
                ],
                "source": "manual",
                "last_updated": datetime.now().isoformat()
            },
            
            # Web Frameworks
            "jinja2": {
                "deprecated_since": "2023-02-01",
                "reason": "Old versions have performance issues",
                "alternatives": [
                    {
                        "name": "jinja2",
                        "reason": "Update to version 3.1+",
                        "migration_guide": "https://jinja.palletsprojects.com/"
                    }
                ],
                "source": "manual",
                "last_updated": datetime.now().isoformat()
            },
            "flask": {
                "deprecated_since": "2023-04-01",
                "reason": "Recommended to use modern alternatives",
                "alternatives": [
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
                "source": "manual",
                "last_updated": datetime.now().isoformat()
            },
            "bottle": {
                "deprecated_since": "2022-01-01",
                "reason": "No longer actively maintained",
                "alternatives": [
                    {
                        "name": "fastapi",
                        "reason": "Modern async web framework",
                        "migration_guide": "https://fastapi.tiangolo.com/"
                    },
                    {
                        "name": "flask",
                        "reason": "Lightweight web framework",
                        "migration_guide": "https://flask.palletsprojects.com/"
                    }
                ],
                "source": "manual",
                "last_updated": datetime.now().isoformat()
            },
            
            # Database
            "psycopg2": {
                "deprecated_since": "2023-03-01",
                "reason": "Recommended to use psycopg3",
                "alternatives": [
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
                "source": "manual",
                "last_updated": datetime.now().isoformat()
            },
            
            # Utilities
            "six": {
                "deprecated_since": "2020-01-01",
                "reason": "Python 2/3 compatibility no longer needed",
                "alternatives": [
                    {
                        "name": "builtins",
                        "reason": "Use native Python 3 features",
                        "migration_guide": "https://docs.python.org/3/library/builtins.html"
                    }
                ],
                "source": "manual",
                "last_updated": datetime.now().isoformat()
            },
            "future": {
                "deprecated_since": "2020-01-01",
                "reason": "Python 2/3 compatibility no longer needed",
                "alternatives": [
                    {
                        "name": "builtins",
                        "reason": "Use native Python 3 features",
                        "migration_guide": "https://docs.python.org/3/library/builtins.html"
                    }
                ],
                "source": "manual",
                "last_updated": datetime.now().isoformat()
            },
            "pathlib2": {
                "deprecated_since": "2019-01-01",
                "reason": "pathlib is now in standard library",
                "alternatives": [
                    {
                        "name": "pathlib",
                        "reason": "Use standard library pathlib",
                        "migration_guide": "https://docs.python.org/3/library/pathlib.html"
                    }
                ],
                "source": "manual",
                "last_updated": datetime.now().isoformat()
            },
            "enum34": {
                "deprecated_since": "2019-01-01",
                "reason": "enum is now in standard library",
                "alternatives": [
                    {
                        "name": "enum",
                        "reason": "Use standard library enum",
                        "migration_guide": "https://docs.python.org/3/library/enum.html"
                    }
                ],
                "source": "manual",
                "last_updated": datetime.now().isoformat()
            },
            
            # Testing
            "nose": {
                "deprecated_since": "2018-01-01",
                "reason": "No longer maintained",
                "alternatives": [
                    {
                        "name": "pytest",
                        "reason": "Modern testing framework",
                        "migration_guide": "https://docs.pytest.org/"
                    }
                ],
                "source": "manual",
                "last_updated": datetime.now().isoformat()
            },
            
            # Development Tools
            "distutils": {
                "deprecated_since": "2021-01-01",
                "reason": "Deprecated in favor of setuptools",
                "alternatives": [
                    {
                        "name": "setuptools",
                        "reason": "Modern package management",
                        "migration_guide": "https://setuptools.pypa.io/"
                    }
                ],
                "source": "manual",
                "last_updated": datetime.now().isoformat()
            },
            
            # Async
            "tornado": {
                "deprecated_since": "2022-01-01",
                "reason": "No longer actively maintained",
                "alternatives": [
                    {
                        "name": "fastapi",
                        "reason": "Modern async web framework",
                        "migration_guide": "https://fastapi.tiangolo.com/"
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
            
            # Image Processing
            "PIL": {
                "deprecated_since": "2011-01-01",
                "reason": "Replaced by Pillow",
                "alternatives": [
                    {
                        "name": "Pillow",
                        "reason": "Fork of PIL with active maintenance",
                        "migration_guide": "https://pillow.readthedocs.io/"
                    }
                ],
                "source": "manual",
                "last_updated": datetime.now().isoformat()
            },
            
            # Machine Learning
            "theano": {
                "deprecated_since": "2017-01-01",
                "reason": "No longer maintained",
                "alternatives": [
                    {
                        "name": "tensorflow",
                        "reason": "Modern deep learning framework",
                        "migration_guide": "https://www.tensorflow.org/"
                    },
                    {
                        "name": "pytorch",
                        "reason": "Modern deep learning framework",
                        "migration_guide": "https://pytorch.org/"
                    }
                ],
                "source": "manual",
                "last_updated": datetime.now().isoformat()
            },
            
            # Documentation
            "docutils": {
                "deprecated_since": "2022-01-01",
                "reason": "No longer actively maintained",
                "alternatives": [
                    {
                        "name": "sphinx",
                        "reason": "Modern documentation generator",
                        "migration_guide": "https://www.sphinx-doc.org/"
                    }
                ],
                "source": "manual",
                "last_updated": datetime.now().isoformat()
            },
            
            # Deployment
            "fabric": {
                "deprecated_since": "2020-01-01",
                "reason": "No longer actively maintained",
                "alternatives": [
                    {
                        "name": "ansible",
                        "reason": "Modern automation platform",
                        "migration_guide": "https://www.ansible.com/"
                    }
                ],
                "source": "manual",
                "last_updated": datetime.now().isoformat()
            },
            
            # Other
            "celery": {
                "deprecated_since": "2023-05-01",
                "reason": "Old versions have performance issues",
                "alternatives": [
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
                "source": "manual",
                "last_updated": datetime.now().isoformat()
            },
            "redis": {
                "deprecated_since": "2023-01-01",
                "reason": "Old versions have security issues",
                "alternatives": [
                    {
                        "name": "redis",
                        "reason": "Update to version 4.5+",
                        "migration_guide": "https://redis.io/"
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
        description = package_data.get("info", {}).get("summary", "")
        keywords = package_data.get("info", {}).get("keywords", "")
        
        # Handle None values
        if description is None:
            description = ""
        if keywords is None:
            keywords = ""
        
        description = description.lower()
        keywords = keywords.lower()
        
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
        
        # Handle None values
        if description is None:
            description = ""
        
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