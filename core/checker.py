"""
Main module for checking deprecated dependencies.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from packaging import version

from .parser import DependencyParser
from .database import DeprecatedPackageDB


@dataclass
class DeprecatedPackage:
    """Information about deprecated package."""
    name: str
    current_version: str
    file_source: str
    deprecated_since: str
    reason: str
    alternatives: List[Dict[str, str]]
    needs_update: bool = False
    required_version: Optional[str] = None


@dataclass
class CheckResult:
    """Result of project check."""
    deprecated_packages: List[DeprecatedPackage]
    safe_packages: List[Dict[str, str]]
    total_deprecated: int
    total_safe: int
    files_checked: List[str]


class DeprecatedChecker:
    """Main class for checking deprecated dependencies."""
    
    def __init__(self, db_path: Optional[Path] = None):
        self.parser = DependencyParser()
        self.db = DeprecatedPackageDB(db_path)
    
    def check_project(self, project_path: Path) -> CheckResult:
        """Checks project for deprecated dependencies."""
        if not project_path.exists():
            raise FileNotFoundError(f"Path {project_path} does not exist")
        
        # Parse all dependency files
        dependencies_by_file = self.parser.parse_all_files(project_path)
        
        deprecated_packages = []
        safe_packages = []
        
        # Check each dependency
        for file_name, dependencies in dependencies_by_file.items():
            for package_name, package_version in dependencies:
                # Extract version from version specification string
                version_str = self._extract_version(package_version)
                
                # Check if package is deprecated
                dep_info = self.db.check_version_compatibility(package_name, version_str)
                
                if dep_info["is_deprecated"]:
                    deprecated_pkg = DeprecatedPackage(
                        name=package_name,
                        current_version=version_str or "not specified",
                        file_source=file_name,
                        deprecated_since=dep_info.get("deprecated_since", "unknown"),
                        reason=dep_info.get("reason", "not specified"),
                        alternatives=dep_info.get("alternatives", []),
                        needs_update=dep_info.get("needs_update", False),
                        required_version=dep_info.get("required_version")
                    )
                    deprecated_packages.append(deprecated_pkg)
                else:
                    safe_packages.append({
                        "name": package_name,
                        "version": version_str or "not specified",
                        "file_source": file_name
                    })
        
        return CheckResult(
            deprecated_packages=deprecated_packages,
            safe_packages=safe_packages,
            total_deprecated=len(deprecated_packages),
            total_safe=len(safe_packages),
            files_checked=list(dependencies_by_file.keys())
        )
    
    def _extract_version(self, version_spec: str) -> str:
        """Extracts version from version specification string."""
        if not version_spec:
            return ""
        
        # Remove comparison operators
        version_str = version_spec.lstrip("<>!=~")
        
        # If version contains range, take minimum
        if "," in version_str:
            parts = version_str.split(",")
            for part in parts:
                part = part.strip()
                if part.startswith(">=") or not part.startswith(("<", ">")):
                    return part.lstrip("<>!=~")
            return parts[0].strip().lstrip("<>!=~")
        
        return version_str
    
    def get_recommendations(self, result: CheckResult) -> List[Dict[str, Any]]:
        """Generates recommendations for updating."""
        recommendations = []
        
        for pkg in result.deprecated_packages:
            rec = {
                "package": pkg.name,
                "current_version": pkg.current_version,
                "file_source": pkg.file_source,
                "reason": pkg.reason,
                "alternatives": []
            }
            
            for alt in pkg.alternatives:
                alt_info = {
                    "name": alt["name"],
                    "reason": alt["reason"],
                    "migration_guide": alt.get("migration_guide", "")
                }
                
                if pkg.needs_update and alt["name"].lower() == pkg.name.lower():
                    alt_info["action"] = f"Update to version {pkg.required_version}+"
                else:
                    alt_info["action"] = "Replace with"
                
                rec["alternatives"].append(alt_info)
            
            recommendations.append(rec)
        
        return recommendations
    
    def generate_report(self, result: CheckResult, format_type: str = "text") -> str:
        """Generates report in specified format."""
        if format_type == "json":
            return self._generate_json_report(result)
        elif format_type == "yaml":
            return self._generate_yaml_report(result)
        else:
            return self._generate_text_report(result)
    
    def _generate_text_report(self, result: CheckResult) -> str:
        """Generates text report."""
        report = []
        report.append("Report on checking deprecated dependencies")
        report.append("=" * 50)
        report.append(f"Checked files: {', '.join(result.files_checked)}")
        report.append(f"Total packages: {result.total_deprecated + result.total_safe}")
        report.append(f"Deprecated: {result.total_deprecated}")
        report.append(f"Safe: {result.total_safe}")
        report.append("")
        
        if result.deprecated_packages:
            report.append("Found deprecated packages:")
            for pkg in result.deprecated_packages:
                report.append(f"  • {pkg.name}=={pkg.current_version} ({pkg.file_source})")
                report.append(f"    Reason: {pkg.reason}")
                if pkg.alternatives:
                    report.append("    Alternatives:")
                    for alt in pkg.alternatives:
                        report.append(f"      - {alt['name']}: {alt['reason']}")
                        if alt.get('migration_guide'):
                            report.append(f"        Guide: {alt['migration_guide']}")
                report.append("")
        else:
            report.append("No deprecated packages found!")
            report.append("")
        
        if result.safe_packages:
            report.append("Safe packages:")
            for pkg in result.safe_packages:
                report.append(f"  • {pkg['name']}=={pkg['version']} ({pkg['file_source']})")
        
        return "\n".join(report)
    
    def _generate_json_report(self, result: CheckResult) -> str:
        """Generates JSON report."""
        import json
        
        report_data = {
            "summary": {
                "total_packages": result.total_deprecated + result.total_safe,
                "deprecated_count": result.total_deprecated,
                "safe_count": result.total_safe,
                "files_checked": result.files_checked
            },
            "deprecated_packages": [
                {
                    "name": pkg.name,
                    "current_version": pkg.current_version,
                    "file_source": pkg.file_source,
                    "deprecated_since": pkg.deprecated_since,
                    "reason": pkg.reason,
                    "alternatives": pkg.alternatives,
                    "needs_update": pkg.needs_update,
                    "required_version": pkg.required_version
                }
                for pkg in result.deprecated_packages
            ],
            "safe_packages": result.safe_packages
        }
        
        return json.dumps(report_data, indent=2, ensure_ascii=False)
    
    def _generate_yaml_report(self, result: CheckResult) -> str:
        """Generates YAML report."""
        import yaml
        
        report_data = {
            "summary": {
                "total_packages": result.total_deprecated + result.total_safe,
                "deprecated_count": result.total_deprecated,
                "safe_count": result.total_safe,
                "files_checked": result.files_checked
            },
            "deprecated_packages": [
                {
                    "name": pkg.name,
                    "current_version": pkg.current_version,
                    "file_source": pkg.file_source,
                    "deprecated_since": pkg.deprecated_since,
                    "reason": pkg.reason,
                    "alternatives": pkg.alternatives,
                    "needs_update": pkg.needs_update,
                    "required_version": pkg.required_version
                }
                for pkg in result.deprecated_packages
            ],
            "safe_packages": result.safe_packages
        }
        
        return yaml.dump(report_data, default_flow_style=False, allow_unicode=True) 