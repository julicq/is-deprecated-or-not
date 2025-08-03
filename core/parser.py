"""
Parser for different Python project dependency files.
"""

import re
import ast
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import yaml
import toml


class DependencyParser:
    """Parser for Python project dependency files."""
    
    def __init__(self):
        self.requirement_pattern = re.compile(
            r'^([a-zA-Z0-9._-]+)\s*([<>=!~]+)\s*([0-9.]+)$'
        )
    
    def parse_requirements_txt(self, file_path: Path) -> List[Tuple[str, str]]:
        """Parses requirements.txt file."""
        dependencies = []
        
        if not file_path.exists():
            return dependencies
            
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                # Remove comments at the end of the line
                if '#' in line:
                    line = line.split('#')[0].strip()
                
                # Parse dependency
                match = self.requirement_pattern.match(line)
                if match:
                    package_name = match.group(1).lower()
                    version_spec = match.group(2) + match.group(3)
                    dependencies.append((package_name, version_spec))
                else:
                    # Simple dependency without version
                    package_name = line.lower()
                    dependencies.append((package_name, ""))
        
        return dependencies
    
    def parse_setup_py(self, file_path: Path) -> List[Tuple[str, str]]:
        """Parses setup.py file."""
        dependencies = []
        
        if not file_path.exists():
            return dependencies
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST for finding install_requires
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    # Find setup() call
                    if isinstance(node.func, ast.Name) and node.func.id == 'setup':
                        for keyword in node.keywords:
                            if keyword.arg == 'install_requires':
                                if isinstance(keyword.value, ast.List):
                                    for item in keyword.value.elts:
                                        if isinstance(item, ast.Constant):
                                            dep_str = item.value
                                            match = self.requirement_pattern.match(dep_str)
                                            if match:
                                                package_name = match.group(1).lower()
                                                version_spec = match.group(2) + match.group(3)
                                                dependencies.append((package_name, version_spec))
                                            else:
                                                package_name = dep_str.lower()
                                                dependencies.append((package_name, ""))
                                        elif isinstance(item, ast.Str):  # For Python < 3.8
                                            dep_str = item.s
                                            match = self.requirement_pattern.match(dep_str)
                                            if match:
                                                package_name = match.group(1).lower()
                                                version_spec = match.group(2) + match.group(3)
                                                dependencies.append((package_name, version_spec))
                                            else:
                                                package_name = dep_str.lower()
                                                dependencies.append((package_name, ""))
        except Exception as e:
            print(f"Error parsing setup.py: {e}")
        
        return dependencies
    
    def parse_pyproject_toml(self, file_path: Path) -> List[Tuple[str, str]]:
        """Parses pyproject.toml file."""
        dependencies = []
        
        if not file_path.exists():
            return dependencies
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            data = toml.loads(content)
            
            # Check [project.dependencies]
            if 'project' in data and 'dependencies' in data['project']:
                for dep in data['project']['dependencies']:
                    match = self.requirement_pattern.match(dep)
                    if match:
                        package_name = match.group(1).lower()
                        version_spec = match.group(2) + match.group(3)
                        dependencies.append((package_name, version_spec))
                    else:
                        package_name = dep.lower()
                        dependencies.append((package_name, ""))
            
            # Check [tool.poetry.dependencies]
            if 'tool' in data and 'poetry' in data['tool'] and 'dependencies' in data['tool']['poetry']:
                for package_name, version_info in data['tool']['poetry']['dependencies'].items():
                    if isinstance(version_info, str):
                        dependencies.append((package_name.lower(), version_info))
                    else:
                        dependencies.append((package_name.lower(), ""))
                        
        except Exception as e:
            print(f"Error parsing pyproject.toml: {e}")
        
        return dependencies
    
    def parse_all_files(self, project_path: Path) -> Dict[str, List[Tuple[str, str]]]:
        """Parses all dependency files in the project."""
        results = {}
        
        # requirements.txt
        req_file = project_path / "requirements.txt"
        if req_file.exists():
            results["requirements.txt"] = self.parse_requirements_txt(req_file)
        
        # requirements-dev.txt
        req_dev_file = project_path / "requirements-dev.txt"
        if req_dev_file.exists():
            results["requirements-dev.txt"] = self.parse_requirements_txt(req_dev_file)
        
        # setup.py
        setup_file = project_path / "setup.py"
        if setup_file.exists():
            results["setup.py"] = self.parse_setup_py(setup_file)
        
        # pyproject.toml
        pyproject_file = project_path / "pyproject.toml"
        if pyproject_file.exists():
            results["pyproject.toml"] = self.parse_pyproject_toml(pyproject_file)
        
        return results 