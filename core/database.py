"""
Dynamic database of deprecated packages and their alternatives.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from packaging import version
import importlib.resources as pkg_resources
from .data_collector import DataCollector
# from .repository_analyzer import RepositoryAnalyzer  # Not used in current logic
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DeprecatedPackageDB:
    """Database of deprecated packages."""
    
    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            # Always try to load from package data first
            self.db_path = None  # Will load from package
        else:
            self.db_path = db_path
        
        self._load_database()
    
    def _load_database(self):
        """Loads database from static file by default."""
        try:
            if self.db_path is None:
                # Try to load from static file first (fallback)
                static_data = self._load_static_database()
                
                # Use static data by default, only analyze repository if explicitly requested
                if static_data:
                    self.data = static_data
                    logger.info(f"Using static data with {len(static_data)} packages")
                else:
                    logger.warning("No static data found, database will be empty")
                    self.data = {}
            else:
                # Load from specified file path
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    self.data = yaml.safe_load(f) or {}
                    logger.info(f"Successfully loaded database from specified path: {self.db_path}")
        except Exception as e:
            logger.error(f"Error loading database: {e}")
            self.data = {}
    
    def _load_static_database(self) -> Dict[str, Any]:
        """Loads static database from YAML file as fallback."""
        try:
            # Method 1: Try importlib.resources with correct package structure
            try:
                import importlib.resources as resources
                with resources.open_text('core', 'deprecated_packages.yaml') as f:
                    data = yaml.safe_load(f) or {}
                    logger.info("Successfully loaded static database using importlib.resources from core")
                    return data
            except Exception as e:
                logger.debug(f"Failed to load static database using importlib.resources: {e}")
            
            # Method 2: Try to load from core directory
            try:
                import core
                core_dir = Path(core.__file__).parent
                data_file = core_dir / "deprecated_packages.yaml"
                if data_file.exists():
                    with open(data_file, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f) or {}
                        logger.info(f"Successfully loaded static database from core directory: {data_file}")
                        return data
                else:
                    logger.debug(f"Static database file not found at: {data_file}")
            except Exception as e:
                logger.debug(f"Failed to load static database from core directory: {e}")
            
            # Method 3: Fallback to relative path
            try:
                data_file = Path(__file__).parent / "deprecated_packages.yaml"
                if data_file.exists():
                    with open(data_file, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f) or {}
                        logger.info(f"Successfully loaded static database from relative path: {data_file}")
                        return data
                else:
                    logger.debug(f"Static database file not found at: {data_file}")
            except Exception as e:
                logger.debug(f"Failed to load static database from relative path: {e}")
            
            # Method 4: Try data directory
            try:
                data_file = Path(__file__).parent.parent / "data" / "deprecated_packages.yaml"
                if data_file.exists():
                    with open(data_file, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f) or {}
                        logger.info(f"Successfully loaded static database from data directory: {data_file}")
                        return data
                else:
                    logger.debug(f"Static database file not found at: {data_file}")
            except Exception as e:
                logger.debug(f"Failed to load static database from data directory: {e}")
            
            logger.warning("No static database file found in any location")
            return {}
        except Exception as e:
            logger.error(f"Error loading static database: {e}")
            return {}
    
    def _should_collect_fresh_data(self) -> bool:
        """Determines if we should collect fresh data."""
        # For now, use static data by default
        # In the future, this could check cache age, user preference, etc.
        return False
    
    def _save_dynamic_data(self, data: Dict[str, Any]) -> None:
        """Saves dynamically collected data to cache."""
        try:
            cache_dir = Path(__file__).parent.parent / "cache"
            cache_dir.mkdir(exist_ok=True)
            
            cache_file = cache_dir / "dynamic_database.yaml"
            with open(cache_file, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            
            logger.info(f"Saved dynamic data to cache: {cache_file}")
        except Exception as e:
            logger.error(f"Failed to save dynamic data: {e}")
    
    def is_deprecated(self, package_name: str, package_version: str = "") -> bool:
        """Checks if package is deprecated."""
        package_name = package_name.lower()
        return package_name in self.data
    
    def get_deprecated_info(self, package_name: str) -> Optional[Dict[str, Any]]:
        """Gets information about deprecated package."""
        package_name = package_name.lower()
        return self.data.get(package_name)
    
    def get_alternatives(self, package_name: str) -> List[Dict[str, str]]:
        """Gets list of alternatives for deprecated package."""
        info = self.get_deprecated_info(package_name)
        if info and 'alternatives' in info:
            return info['alternatives']
        return []
    
    def check_version_compatibility(self, package_name: str, current_version: str) -> Dict[str, Any]:
        """Checks version compatibility of package."""
        package_name = package_name.lower()
        info = self.get_deprecated_info(package_name)
        
        if not info:
            return {"is_deprecated": False}
        
        result = {
            "is_deprecated": True,
            "deprecated_since": info.get("deprecated_since"),
            "reason": info.get("reason"),
            "alternatives": info.get("alternatives", []),
            "current_version": current_version,
            "needs_update": False
        }
        
        # Check if package needs update
        if current_version and "alternatives" in info:
            for alt in info["alternatives"]:
                if alt["name"].lower() == package_name:
                    # This is update of the same package
                    if "version" in alt:
                        try:
                            current_ver = version.parse(current_version)
                            required_ver = version.parse(alt["version"])
                            if current_ver < required_ver:
                                result["needs_update"] = True
                                result["required_version"] = alt["version"]
                        except version.InvalidVersion:
                            pass
                    break
        
        return result
    
    def get_all_deprecated_packages(self) -> List[str]:
        """Returns list of all deprecated packages."""
        return list(self.data.keys())
    
    def search_alternatives(self, package_name: str) -> List[Dict[str, str]]:
        """Searches alternatives for package."""
        return self.get_alternatives(package_name)
    
    def get_migration_guide(self, package_name: str, alternative_name: str) -> Optional[str]:
        """Gets link to migration guide."""
        alternatives = self.get_alternatives(package_name)
        for alt in alternatives:
            if alt["name"].lower() == alternative_name.lower():
                return alt.get("migration_guide")
        return None
    
    def export_to_json(self) -> str:
        """Exports database to JSON format."""
        import json
        return json.dumps(self.data, indent=2, ensure_ascii=False)
    
    def export_to_yaml(self) -> str:
        """Exports database to YAML format."""
        return yaml.dump(self.data, default_flow_style=False, allow_unicode=True)
    
    def export_to_csv(self) -> str:
        """Exports database to CSV format."""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(["Package", "Deprecated Since", "Reason", "Alternatives"])
        
        # Write data
        for package_name, info in self.data.items():
            deprecated_since = info.get("deprecated_since", "")
            reason = info.get("reason", "")
            alternatives = ", ".join([alt["name"] for alt in info.get("alternatives", [])])
            
            writer.writerow([package_name, deprecated_since, reason, alternatives])
        
        return output.getvalue() 