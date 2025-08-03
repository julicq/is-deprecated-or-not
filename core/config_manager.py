"""
Configuration manager for the data collector.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class CollectorConfig:
    """Configuration for data collector."""
    pypi_enabled: bool = True
    pypi_packages: list = None
    pypi_timeout: int = 10
    pypi_rate_limit: float = 0.1
    
    github_enabled: bool = True
    github_queries: list = None
    github_token: Optional[str] = None
    
    security_enabled: bool = True
    security_sources: list = None
    
    manual_enabled: bool = True
    manual_data_file: str = "data/manual_packages.yaml"


@dataclass
class SchedulerConfig:
    """Configuration for scheduler."""
    enabled: bool = True
    interval_hours: int = 24
    retry_attempts: int = 3
    retry_delay_minutes: int = 30
    backup_before_update: bool = True
    notify_on_failure: bool = True


@dataclass
class DatabaseConfig:
    """Configuration for database."""
    output_path: str = "data/deprecated_packages.yaml"
    backup_dir: str = "cache/backups"
    max_backups: int = 10


@dataclass
class LoggingConfig:
    """Configuration for logging."""
    level: str = "INFO"
    file: str = "logs/collector.log"
    max_size_mb: int = 10
    backup_count: int = 5


class ConfigManager:
    """Manages configuration for the data collector."""
    
    def __init__(self, config_path: Optional[Path] = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "collector_config.yaml"
        
        self.config_path = config_path
        self.config_data = self._load_config()
        
        # Initialize configurations
        self.collector = self._parse_collector_config()
        self.scheduler = self._parse_scheduler_config()
        self.database = self._parse_database_config()
        self.logging = self._parse_logging_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Loads configuration from file."""
        if not self.config_path.exists():
            return {}
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}
    
    def _parse_collector_config(self) -> CollectorConfig:
        """Parses collector configuration."""
        collector_data = self.config_data.get("collector", {})
        sources = collector_data.get("sources", {})
        
        return CollectorConfig(
            pypi_enabled=sources.get("pypi", {}).get("enabled", True),
            pypi_packages=sources.get("pypi", {}).get("packages_to_check", []),
            pypi_timeout=sources.get("pypi", {}).get("timeout", 10),
            pypi_rate_limit=sources.get("pypi", {}).get("rate_limit", 0.1),
            
            github_enabled=sources.get("github", {}).get("enabled", True),
            github_queries=sources.get("github", {}).get("search_queries", []),
            github_token=sources.get("github", {}).get("api_token"),
            
            security_enabled=sources.get("security_advisories", {}).get("enabled", True),
            security_sources=sources.get("security_advisories", {}).get("sources", []),
            
            manual_enabled=sources.get("manual", {}).get("enabled", True),
            manual_data_file=sources.get("manual", {}).get("data_file", "data/manual_packages.yaml")
        )
    
    def _parse_scheduler_config(self) -> SchedulerConfig:
        """Parses scheduler configuration."""
        scheduler_data = self.config_data.get("scheduler", {})
        
        return SchedulerConfig(
            enabled=scheduler_data.get("enabled", True),
            interval_hours=scheduler_data.get("interval_hours", 24),
            retry_attempts=scheduler_data.get("retry_attempts", 3),
            retry_delay_minutes=scheduler_data.get("retry_delay_minutes", 30),
            backup_before_update=scheduler_data.get("backup_before_update", True),
            notify_on_failure=scheduler_data.get("notify_on_failure", True)
        )
    
    def _parse_database_config(self) -> DatabaseConfig:
        """Parses database configuration."""
        db_data = self.config_data.get("database", {})
        
        return DatabaseConfig(
            output_path=db_data.get("output_path", "data/deprecated_packages.yaml"),
            backup_dir=db_data.get("backup_dir", "cache/backups"),
            max_backups=db_data.get("max_backups", 10)
        )
    
    def _parse_logging_config(self) -> LoggingConfig:
        """Parses logging configuration."""
        logging_data = self.config_data.get("logging", {})
        
        return LoggingConfig(
            level=logging_data.get("level", "INFO"),
            file=logging_data.get("file", "logs/collector.log"),
            max_size_mb=logging_data.get("max_size_mb", 10),
            backup_count=logging_data.get("backup_count", 5)
        )
    
    def get_alternatives_db(self) -> Dict[str, list]:
        """Gets alternatives database from config."""
        return self.config_data.get("alternatives", {})
    
    def save_config(self) -> None:
        """Saves current configuration to file."""
        try:
            self.config_path.parent.mkdir(exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config_data, f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def update_config(self, section: str, key: str, value: Any) -> None:
        """Updates configuration value."""
        if section not in self.config_data:
            self.config_data[section] = {}
        
        if isinstance(key, str) and "." in key:
            # Handle nested keys like "sources.pypi.enabled"
            keys = key.split(".")
            current = self.config_data[section]
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]
            current[keys[-1]] = value
        else:
            self.config_data[section][key] = value
    
    def get_config_value(self, section: str, key: str, default: Any = None) -> Any:
        """Gets configuration value."""
        section_data = self.config_data.get(section, {})
        
        if isinstance(key, str) and "." in key:
            # Handle nested keys
            keys = key.split(".")
            current = section_data
            for k in keys:
                if isinstance(current, dict) and k in current:
                    current = current[k]
                else:
                    return default
            return current
        else:
            return section_data.get(key, default) 