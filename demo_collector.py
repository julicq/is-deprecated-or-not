#!/usr/bin/env python3
"""
Demo of data parser for deprecated packages.
"""

import sys
from pathlib import Path
import time

# Add current directory to path for import modules
sys.path.insert(0, str(Path(__file__).parent))

from core.data_collector import DataCollector
from core.scheduler import DatabaseScheduler, ManualUpdater, UpdateConfig
from core.config_manager import ConfigManager
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def demo_data_collection():
    """Demonstrates data collection from different sources."""
    console.print(Panel("🔍 Demonstration of data collection for deprecated packages", style="bold blue"))
    
    # Create data collector
    collector = DataCollector()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        # Demonstrate collection from PyPI
        task1 = progress.add_task("Collection from PyPI...", total=None)
        time.sleep(2)  # Simulate work
        progress.update(task1, description="✅ Data from PyPI collected")
        
        # Demonstrate collection from GitHub
        task2 = progress.add_task("Collection from GitHub...", total=None)
        time.sleep(1.5)
        progress.update(task2, description="✅ Data from GitHub collected")
        
        # Demonstrate collection from security advisories
        task3 = progress.add_task("Collection from security advisories...", total=None)
        time.sleep(1)
        progress.update(task3, description="✅ Data from security advisories collected")
    
    console.print("\n📊 Data collection statistics:")
    
    # Show statistics
    stats = collector.get_statistics()
    table = Table(title="Database statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Total packages", str(stats["total_packages"]))
    for source, count in stats["sources"].items():
        table.add_row(f"Source: {source}", str(count))
    table.add_row("Last update", stats.get("last_updated", "Unknown"))
    
    console.print(table)


def demo_scheduler():
    """Demonstrates scheduler functionality."""
    console.print(Panel("⏰ Demonstration of update scheduler", style="bold green"))
    
    # Create scheduler
    config = UpdateConfig(interval_hours=1)  # Short interval for demo
    scheduler = DatabaseScheduler(config)
    
    # Show status
    status = scheduler.get_status()
    
    table = Table(title="Scheduler status")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Running", "✅ Yes" if status["is_running"] else "❌ No")
    table.add_row("Interval", f"{status['config']['interval_hours']} hours")
    table.add_row("Retry attempts", str(status['config']['retry_attempts']))
    table.add_row("Last update", status.get('last_update', 'Never'))
    table.add_row("Next update", status.get('next_update', 'Unknown'))
    
    console.print(table)
    
    # Demonstrate forced update
    console.print("\n⚡ Demonstration of forced update...")
    if scheduler.force_update():
        console.print("✅ Forced update completed successfully")
    else:
        console.print("❌ Forced update failed")


def demo_manual_updater():
    """Demonstrates manual update."""
    console.print(Panel("🔧 Demonstration of manual update", style="bold yellow"))
    
    updater = ManualUpdater()
    
    # Show database validation
    console.print("🔍 Database validation...")
    validation = updater.validate_database()
    
    if validation["valid"]:
        console.print("✅ Database is valid")
        console.print(f"📦 Total packages: {validation['total_packages']}")
        
        # Show sources
        sources_table = Table(title="Data sources")
        sources_table.add_column("Source", style="cyan")
        sources_table.add_column("Packages", style="green")
        
        for source, count in validation["sources"].items():
            sources_table.add_row(source, str(count))
        
        console.print(sources_table)
    else:
        console.print("❌ Database is invalid")
        console.print(f"Error: {validation.get('error', 'Unknown error')}")


def demo_config_manager():
    """Demonstrates configuration management."""
    console.print(Panel("⚙️ Demonstration of configuration management", style="bold magenta"))
    
    config_manager = ConfigManager()
    
    # Show current configuration
    console.print("📋 Current configuration:")
    
    config_table = Table(title="Collector settings")
    config_table.add_column("Parameter", style="cyan")
    config_table.add_column("Value", style="green")
    
    config_table.add_row("PyPI enabled", "✅ Yes" if config_manager.collector.pypi_enabled else "❌ No")
    config_table.add_row("GitHub enabled", "✅ Yes" if config_manager.collector.github_enabled else "❌ No")
    config_table.add_row("Security advisories enabled", "✅ Yes" if config_manager.collector.security_enabled else "❌ No")
    config_table.add_row("Manual enabled", "✅ Yes" if config_manager.collector.manual_enabled else "❌ No")
    config_table.add_row("Timeout PyPI", str(config_manager.collector.pypi_timeout))
    config_table.add_row("Rate limit PyPI", str(config_manager.collector.pypi_rate_limit))
    
    console.print(config_table)
    
    # Show alternatives
    alternatives = config_manager.get_alternatives_db()
    if alternatives:
        console.print("\n🔄 Alternatives database:")
        for package, alts in alternatives.items():
            console.print(f"  • {package}: {len(alts)} alternatives")


def main():
    """Main demonstration function."""
    console.print(Panel.fit(
        "🚀 Demonstration of data parser for deprecated packages",
        style="bold red"
    ))
    
    try:
        # Demonstrate data collection
        demo_data_collection()
        console.print("\n" + "="*60 + "\n")
        
        # Demonstrate scheduler
        demo_scheduler()
        console.print("\n" + "="*60 + "\n")
        
        # Demonstrate manual update
        demo_manual_updater()
        console.print("\n" + "="*60 + "\n")
        
        # Demonstrate configuration management
        demo_config_manager()
        
        console.print("\n" + "="*60)
        console.print(Panel(
            "✅ Demonstration completed successfully!\n\n"
            "Now you can use commands:\n"
            "• python deprecated_checker.py update-db --source manual\n"
            "• python deprecated_checker.py scheduler status\n"
            "• python deprecated_checker.py stats\n"
            "• python deprecated_checker.py validate-db",
            style="bold green"
        ))
        
    except Exception as e:
        console.print(f"[red]❌ Error in demonstration: {e}[/red]")


if __name__ == "__main__":
    main() 