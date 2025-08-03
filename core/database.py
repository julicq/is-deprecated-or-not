"""
Database of deprecated packages and their alternatives.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from packaging import version
import importlib.resources as pkg_resources


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
        """Loads database from YAML file."""
        try:
            if self.db_path is None:
                # Load from package data
                import pkg_resources
                try:
                    with pkg_resources.open_text('deprecated_checker', 'data/deprecated_packages.yaml') as f:
                        print(f"Loading from package data using open_text")
                        self.data = yaml.safe_load(f) or {}
                except Exception as e:
                    print(f"Failed to load from package data: {e}")
                    # Fallback to relative path
                    data_file = Path(__file__).parent.parent / "data" / "deprecated_packages.yaml"
                    print(f"Loading from fallback path: {data_file}")
                    with open(data_file, 'r', encoding='utf-8') as f:
                        self.data = yaml.safe_load(f) or {}
            else:
                # Load from file path
                print(f"Loading from file path: {self.db_path}")
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    self.data = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading database: {e}")
            self.data = {}
    
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