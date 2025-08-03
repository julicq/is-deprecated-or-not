"""
Scheduler for automatic database updates.
"""

import schedule
import time
import threading
from pathlib import Path
from typing import Optional, Callable
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass

from .data_collector import DataCollector

logger = logging.getLogger(__name__)


@dataclass
class UpdateConfig:
    """Configuration for database updates."""
    enabled: bool = True
    interval_hours: int = 24  # Update every 24 hours
    retry_attempts: int = 3
    retry_delay_minutes: int = 30
    backup_before_update: bool = True
    notify_on_failure: bool = True


class DatabaseScheduler:
    """Scheduler for automatic database updates."""
    
    def __init__(self, config: Optional[UpdateConfig] = None):
        self.config = config or UpdateConfig()
        self.collector = DataCollector()
        self.is_running = False
        self.last_update = None
        self.update_thread = None
        
        # Path to file with information about last update
        self.status_file = Path(__file__).parent.parent / "cache" / "update_status.json"
        self.status_file.parent.mkdir(exist_ok=True)
    
    def start(self) -> None:
        """Starts the scheduler."""
        if self.is_running:
            logger.warning("Scheduler is already running")
            return
        
        self.is_running = True
        
        # Setup schedule
        schedule.every(self.config.interval_hours).hours.do(self._update_database)
        
        # Start in separate thread
        self.update_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.update_thread.start()
        
        logger.info(f"Scheduler started with {self.config.interval_hours}h interval")
    
    def stop(self) -> None:
        """Stops the scheduler."""
        self.is_running = False
        schedule.clear()
        logger.info("Scheduler stopped")
    
    def _run_scheduler(self) -> None:
        """Runs the scheduler loop."""
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def _update_database(self) -> None:
        """Performs database update with error handling."""
        logger.info("Starting scheduled database update...")
        
        # Create backup
        if self.config.backup_before_update:
            self._create_backup()
        
        # Try to update database
        for attempt in range(self.config.retry_attempts):
            try:
                self.collector.update_database()
                self._update_status(success=True)
                logger.info("Database update completed successfully")
                return
                
            except Exception as e:
                logger.error(f"Database update attempt {attempt + 1} failed: {e}")
                
                if attempt < self.config.retry_attempts - 1:
                    logger.info(f"Retrying in {self.config.retry_delay_minutes} minutes...")
                    time.sleep(self.config.retry_delay_minutes * 60)
                else:
                    self._update_status(success=False, error=str(e))
                    if self.config.notify_on_failure:
                        self._notify_failure(str(e))
    
    def _create_backup(self) -> None:
        """Creates a backup of the current database."""
        db_path = Path(__file__).parent.parent / "data" / "deprecated_packages.yaml"
        if db_path.exists():
            backup_path = Path(__file__).parent.parent / "cache" / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
            backup_path.parent.mkdir(exist_ok=True)
            
            import shutil
            shutil.copy2(db_path, backup_path)
            logger.info(f"Backup created: {backup_path}")
    
    def _update_status(self, success: bool, error: Optional[str] = None) -> None:
        """Updates the status file."""
        status = {
            "last_update": datetime.now().isoformat(),
            "success": success,
            "error": error,
            "next_update": (datetime.now() + timedelta(hours=self.config.interval_hours)).isoformat()
        }
        
        import json
        with open(self.status_file, 'w') as f:
            json.dump(status, f, indent=2)
        
        self.last_update = datetime.now()
    
    def _notify_failure(self, error: str) -> None:
        """Notifies about update failure."""
        # Here you can add notifications (email, Slack, etc.)
        logger.error(f"Database update failed: {error}")
    
    def force_update(self) -> bool:
        """Forces immediate database update."""
        logger.info("Forcing immediate database update...")
        
        try:
            self.collector.update_database()
            self._update_status(success=True)
            logger.info("Forced update completed successfully")
            return True
        except Exception as e:
            logger.error(f"Forced update failed: {e}")
            self._update_status(success=False, error=str(e))
            return False
    
    def get_status(self) -> dict:
        """Gets the current scheduler status."""
        status = {
            "is_running": self.is_running,
            "config": {
                "enabled": self.config.enabled,
                "interval_hours": self.config.interval_hours,
                "retry_attempts": self.config.retry_attempts
            },
            "last_update": self.last_update.isoformat() if self.last_update else None,
            "next_update": None
        }
        
        # Load information from status file
        if self.status_file.exists():
            import json
            try:
                with open(self.status_file, 'r') as f:
                    file_status = json.load(f)
                    status.update(file_status)
            except Exception as e:
                logger.warning(f"Error reading status file: {e}")
        
        return status
    
    def get_statistics(self) -> dict:
        """Gets statistics about the database."""
        return self.collector.get_statistics()


class ManualUpdater:
    """Manual updater for one-time database updates."""
    
    def __init__(self):
        self.collector = DataCollector()
    
    def update_from_source(self, source: str) -> bool:
        """Updates database from a specific source."""
        logger.info(f"Updating database from source: {source}")
        
        try:
            if source == "pypi":
                data = self.collector._collect_from_pypi()
            elif source == "manual":
                data = self.collector._collect_manual_data()
            elif source == "github":
                data = self.collector._collect_from_github()
            elif source == "security_advisories":
                data = self.collector._collect_security_advisories()
            else:
                logger.error(f"Unknown source: {source}")
                return False
            
            # Update database only with data from specified source
            db_path = Path(__file__).parent.parent / "data" / "deprecated_packages.yaml"
            existing_data = {}
            
            if db_path.exists():
                import yaml
                with open(db_path, 'r', encoding='utf-8') as f:
                    existing_data = yaml.safe_load(f) or {}
            
            # Update database only with data from specified source
            for package_name, package_data in data.items():
                package_data["source"] = source
                package_data["last_updated"] = datetime.now().isoformat()
                existing_data[package_name] = package_data
            
            # Save updated database
            with open(db_path, 'w', encoding='utf-8') as f:
                yaml.dump(existing_data, f, default_flow_style=False, allow_unicode=True)
            
            logger.info(f"Updated {len(data)} packages from {source}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating from {source}: {e}")
            return False
    
    def validate_database(self) -> dict:
        """Validates the current database."""
        db_path = Path(__file__).parent.parent / "data" / "deprecated_packages.yaml"
        
        if not db_path.exists():
            return {"valid": False, "error": "Database file not found"}
        
        try:
            import yaml
            with open(db_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            validation_result = {
                "valid": True,
                "total_packages": len(data),
                "sources": {},
                "errors": []
            }
            
            for package_name, package_data in data.items():
                # Check required fields
                required_fields = ["deprecated_since", "reason", "alternatives"]
                for field in required_fields:
                    if field not in package_data:
                        validation_result["errors"].append(
                            f"Package {package_name} missing required field: {field}"
                        )
                        validation_result["valid"] = False
                
                # Count sources
                source = package_data.get("source", "unknown")
                validation_result["sources"][source] = validation_result["sources"].get(source, 0) + 1
            
            return validation_result
            
        except Exception as e:
            return {"valid": False, "error": str(e)} 