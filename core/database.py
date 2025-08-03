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
                # Method 1: Try importlib.resources with correct package structure
                try:
                    import importlib.resources as resources
                    # Try to load from the core module
                    try:
                        with resources.open_text('core', 'deprecated_packages.yaml') as f:
                            self.data = yaml.safe_load(f) or {}
                            print(f"Successfully loaded database using importlib.resources from core")
                            return
                    except Exception as e:
                        print(f"Failed to load from core using importlib.resources: {e}")
                        
                        # Try alternative approach - load from the core directory
                        try:
                            import core
                            core_dir = Path(core.__file__).parent
                            data_file = core_dir / "deprecated_packages.yaml"
                            if data_file.exists():
                                with open(data_file, 'r', encoding='utf-8') as f:
                                    self.data = yaml.safe_load(f) or {}
                                    print(f"Successfully loaded database from core directory: {data_file}")
                                    return
                        except Exception as e:
                            print(f"Failed to load from core directory: {e}")
                            
                except ImportError:
                    print("importlib.resources not available")
                
                # Method 2: Try pkg_resources (for older Python versions)
                try:
                    import pkg_resources
                    try:
                        dist = pkg_resources.get_distribution('deprecated-checker')
                        data_content = pkg_resources.resource_string('deprecated-checker', 'data/deprecated_packages.yaml')
                        self.data = yaml.safe_load(data_content) or {}
                        print("Successfully loaded database using pkg_resources.get_distribution")
                        return
                    except Exception as e:
                        print(f"Failed to load using pkg_resources.get_distribution: {e}")
                        
                        # Try alternative package names with pkg_resources
                        package_names = ['deprecated_checker', 'core']
                        for package_name in package_names:
                            try:
                                with pkg_resources.resource_stream(package_name, 'data/deprecated_packages.yaml') as f:
                                    self.data = yaml.safe_load(f) or {}
                                    print(f"Successfully loaded database using pkg_resources from {package_name}")
                                    return
                            except Exception as e:
                                print(f"Failed to load from {package_name} using pkg_resources: {e}")
                                continue
                except ImportError:
                    print("pkg_resources not available")
                
                # Method 3: Try to find the file in the installed package location
                try:
                    import sys
                    for path in sys.path:
                        if 'site-packages' in path or 'dist-packages' in path:
                            # Look for the package directory
                            package_dir = Path(path) / "deprecated_checker"
                            if package_dir.exists():
                                data_file = package_dir / "data" / "deprecated_packages.yaml"
                                if data_file.exists():
                                    with open(data_file, 'r', encoding='utf-8') as f:
                                        self.data = yaml.safe_load(f) or {}
                                        print(f"Successfully loaded database from installed package: {data_file}")
                                        return
                except Exception as e:
                    print(f"Failed to load from installed package: {e}")
                
                # Method 4: Fallback to relative path (for development)
                try:
                    data_file = Path(__file__).parent.parent / "data" / "deprecated_packages.yaml"
                    with open(data_file, 'r', encoding='utf-8') as f:
                        self.data = yaml.safe_load(f) or {}
                        print(f"Successfully loaded database from relative path: {data_file}")
                        return
                except Exception as e:
                    print(f"Failed to load from relative path: {e}")
                
                # Method 5: Try to find the file in site-packages
                try:
                    import site
                    for site_dir in site.getsitepackages():
                        data_file = Path(site_dir) / "data" / "deprecated_packages.yaml"
                        if data_file.exists():
                            with open(data_file, 'r', encoding='utf-8') as f:
                                self.data = yaml.safe_load(f) or {}
                                print(f"Successfully loaded database from site-packages: {data_file}")
                                return
                except Exception as e:
                    print(f"Failed to load from site-packages: {e}")
                
                # If all methods fail, create empty database
                print("All loading methods failed, creating empty database")
                self.data = {}
            else:
                # Load from file path
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    self.data = yaml.safe_load(f) or {}
                    print(f"Successfully loaded database from specified path: {self.db_path}")
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