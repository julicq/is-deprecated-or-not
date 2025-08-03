"""
CLI interface for deprecated dependencies checker.
"""

import sys
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.checker import DeprecatedChecker
from core.data_collector import DataCollector
from core.scheduler import DatabaseScheduler, ManualUpdater, UpdateConfig


app = typer.Typer(
    name="deprecated-checker",
    help="Tool for checking deprecated dependencies in Python projects",
    add_completion=False
)

console = Console()


@app.command()
def check(
    path: Optional[Path] = typer.Option(
        None,
        "--path", "-p",
        help="Path to project for checking (default: current directory)"
    ),
    export: Optional[str] = typer.Option(
        None,
        "--export", "-e",
        help="Export format (json, yaml, text)"
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output", "-o",
        help="File to save report"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Verbose output"
    )
):
    """Checks project for deprecated dependencies."""
    
    # Define project path
    project_path = path or Path.cwd()
    
    if not project_path.exists():
        console.print(f"[red]Error: Path {project_path} does not exist[/red]")
        sys.exit(1)
    
    # Show progress
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Checking dependencies...", total=None)
        
        try:
            # Create checker and check project
            checker = DeprecatedChecker()
            result = checker.check_project(project_path)
            
            progress.update(task, description="Generating report...")
            
            # Determine output format
            format_type = export or "text"
            
            # Generate report
            report = checker.generate_report(result, format_type)
            
            # Output result
            if output:
                with open(output, 'w', encoding='utf-8') as f:
                    f.write(report)
                console.print(f"[green]Report saved to {output}[/green]")
            else:
                if format_type == "text":
                    display_text_report(result, checker, verbose)
                else:
                    console.print(report)
                    
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            if verbose:
                console.print_exception()
            sys.exit(1)


def display_text_report(result, checker, verbose: bool):
    """Displays text report using Rich."""
    
    # Create panel with general statistics
    stats_text = Text()
    stats_text.append(f"Checked files: {', '.join(result.files_checked)}\n")
    stats_text.append(f"Total packages: {result.total_deprecated + result.total_safe}\n")
    stats_text.append(f"Deprecated: {result.total_deprecated}\n")
    stats_text.append(f"Safe: {result.total_safe}")
    
    stats_panel = Panel(
        stats_text,
        title="Statistics",
        border_style="blue"
    )
    console.print(stats_panel)
    console.print()
    
    # Display deprecated packages
    if result.deprecated_packages:
        console.print("[red]Found deprecated packages:[/red]")
        console.print()
        
        for pkg in result.deprecated_packages:
            # Create table for alternatives
            if pkg.alternatives:
                table = Table(
                    title=f"Alternatives for {pkg.name}",
                    show_header=True,
                    header_style="bold magenta"
                )
                table.add_column("Alternative", style="cyan")
                table.add_column("Reason", style="green")
                table.add_column("Action", style="yellow")
                table.add_column("Guide", style="blue")
                
                for alt in pkg.alternatives:
                    action = "Update" if alt["name"].lower() == pkg.name.lower() else "Replace"
                    guide = alt.get("migration_guide", "")
                    table.add_row(
                        alt["name"],
                        alt["reason"],
                        action,
                        guide
                    )
                
                # Package information
                pkg_info = f"""
                [bold red]{pkg.name}[/bold red] (version: {pkg.current_version})
                File: {pkg.file_source}
                Deprecation reason: {pkg.reason}
                Deprecated since: {pkg.deprecated_since}
                """
                console.print(Panel(pkg_info, border_style="red"))
                console.print(table)
                console.print()
    else:
        success_panel = Panel(
            "No deprecated packages found!",
            title="Great job!",
            border_style="green"
        )
        console.print(success_panel)
        console.print()
    
    # Display safe packages (if verbose mode is enabled)
    if verbose and result.safe_packages:
        console.print("[green]Safe packages:[/green]")
        
        safe_table = Table(
            title="Safe packages",
            show_header=True,
            header_style="bold green"
        )
        safe_table.add_column("Package", style="cyan")
        safe_table.add_column("Version", style="green")
        safe_table.add_column("File", style="blue")
        
        for pkg in result.safe_packages:
            safe_table.add_row(
                pkg["name"],
                pkg["version"],
                pkg["file_source"]
            )
        
        console.print(safe_table)
        console.print() 


@app.command()
def list_db():
    """Shows all deprecated packages in the database."""
    checker = DeprecatedChecker()
    db = checker.db
    
    deprecated_packages = db.get_all_deprecated_packages()
    
    if not deprecated_packages:
        console.print("[yellow]Database is empty[/yellow]")
        return
    
    table = Table(
        title="Deprecated packages in database",
        show_header=True,
        header_style="bold magenta"
    )
    table.add_column("Package", style="cyan")
    table.add_column("Deprecated since", style="red")
    table.add_column("Reason", style="yellow")
    table.add_column("Alternatives", style="green")
    
    for package_name in deprecated_packages:
        info = db.get_deprecated_info(package_name)
        alternatives = [alt["name"] for alt in info.get("alternatives", [])]
        
        table.add_row(
            package_name,
            info.get("deprecated_since", "unknown"),
            info.get("reason", "not specified"),
            ", ".join(alternatives) if alternatives else "none"
        )
    
    console.print(table)


@app.command()
def search(
    package: str = typer.Argument(..., help="Name of package to search")
):
    """Finds information about a specific package."""
    checker = DeprecatedChecker()
    db = checker.db
    
    info = db.get_deprecated_info(package)
    
    if not info:
        console.print(f"[green]Package {package} is not deprecated[/green]")
        return
    
    console.print(f"[red]Package {package} is deprecated[/red]")
    console.print(f"Deprecated since: {info.get('deprecated_since', 'unknown')}")
    console.print(f"Reason: {info.get('reason', 'not specified')}")
    
    alternatives = info.get("alternatives", [])
    if alternatives:
        console.print("\n[green]Alternatives:[/green]")
        for alt in alternatives:
            console.print(f"  • {alt['name']}: {alt['reason']}")
            if alt.get('migration_guide'):
                console.print(f"    Guide: {alt['migration_guide']}")


@app.command()
def update_db(
    source: Optional[str] = typer.Option(
        None,
        "--source", "-s",
        help="Source to update from (pypi, manual, github, security_advisories, all)"
    ),
    force: bool = typer.Option(
        False,
        "--force", "-f",
        help="Force immediate update"
    )
):
    """Updates the deprecated packages database."""
    
    if source and source not in ["pypi", "manual", "github", "security_advisories", "all"]:
        console.print(f"[red]Unknown source: {source}[/red]")
        console.print("Available sources: pypi, manual, github, security_advisories, all")
        return
    
    if source == "all" or source is None:
        # Update from all sources
        console.print("Updating database from all sources...")
        collector = DataCollector()
        collector.update_database()
        console.print("[green]Database updated successfully[/green]")
    else:
        # Update from specific source
        console.print(f"Updating database from {source}...")
        updater = ManualUpdater()
        if updater.update_from_source(source):
            console.print(f"[green]Database updated from {source}[/green]")
        else:
            console.print(f"[red]Failed to update from {source}[/red]")


@app.command()
def scheduler(
    action: str = typer.Argument(..., help="Action (start, stop, status, force-update)"),
    interval: Optional[int] = typer.Option(
        24,
        "--interval", "-i",
        help="Update interval in hours"
    )
):
    """Manages the automatic database update scheduler."""
    
    config = UpdateConfig(interval_hours=interval)
    scheduler = DatabaseScheduler(config)
    
    if action == "start":
        console.print("Starting scheduler...")
        scheduler.start()
        console.print("[green]Scheduler started[/green]")
        console.print(f"Updates will run every {interval} hours")
        
    elif action == "stop":
        console.print("Stopping scheduler...")
        scheduler.stop()
        console.print("[green]Scheduler stopped[/green]")
        
    elif action == "status":
        status = scheduler.get_status()
        console.print("Scheduler Status:")
        console.print(f"  Running: {'Yes' if status['is_running'] else 'No'}")
        console.print(f"  Last Update: {status.get('last_update', 'Never')}")
        console.print(f"  Next Update: {status.get('next_update', 'Unknown')}")
        console.print(f"  Interval: {status['config']['interval_hours']} hours")
        
    elif action == "force-update":
        console.print("Forcing immediate update...")
        if scheduler.force_update():
            console.print("[green]Force update completed[/green]")
        else:
            console.print("[red]Force update failed[/red]")
            
    else:
        console.print(f"[red]Unknown action: {action}[/red]")
        console.print("Available actions: start, stop, status, force-update")


@app.command()
def validate_db():
    """Validates the current database."""
    console.print("Validating database...")
    
    updater = ManualUpdater()
    result = updater.validate_database()
    
    if result["valid"]:
        console.print("[green]Database is valid[/green]")
        console.print(f"Total packages: {result['total_packages']}")
        console.print("Sources:")
        for source, count in result["sources"].items():
            console.print(f"  {source}: {count} packages")
    else:
        console.print("[red]Database validation failed[/red]")
        console.print(f"Error: {result.get('error', 'Unknown error')}")
        if "errors" in result:
            console.print("Details:")
            for error in result["errors"]:
                console.print(f"  • {error}")


@app.command()
def stats():
    """Shows database statistics."""
    console.print("Database Statistics:")
    
    collector = DataCollector()
    stats = collector.get_statistics()
    
    console.print(f"Total packages: {stats['total_packages']}")
    console.print("Sources:")
    for source, count in stats["sources"].items():
        console.print(f"  {source}: {count} packages")
    console.print(f"Last updated: {stats.get('last_updated', 'Unknown')}")


@app.command()
def export_db(
    format: str = typer.Option(
        "json",
        "--format", "-f",
        help="Export format (json, yaml, csv)"
    ),
    output: Path = typer.Option(
        None,
        "--output", "-o",
        help="Output file path"
    )
):
    """Exports the deprecated packages database."""
    console.print("Exporting database...")
    
    checker = DeprecatedChecker()
    db = checker.db
    
    if format == "json":
        data = db.export_to_json()
        ext = ".json"
    elif format == "yaml":
        data = db.export_to_yaml()
        ext = ".yaml"
    elif format == "csv":
        data = db.export_to_csv()
        ext = ".csv"
    else:
        console.print(f"[red]Unsupported format: {format}[/red]")
        return
    
    if output is None:
        output = Path(f"deprecated_packages{ext}")
    
    try:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(data)
        console.print(f"[green]Database exported to {output}[/green]")
    except Exception as e:
        console.print(f"[red]Export failed: {e}[/red]")


@app.command()
def clear_cache():
    """Clears the cache directory."""
    import shutil
    
    cache_dir = Path("cache")
    if cache_dir.exists():
        try:
            shutil.rmtree(cache_dir)
            cache_dir.mkdir(exist_ok=True)
            console.print("[green]Cache cleared successfully[/green]")
        except Exception as e:
            console.print(f"[red]Failed to clear cache: {e}[/red]")
    else:
        console.print("[yellow]Cache directory does not exist[/yellow]")


@app.command()
def version():
    """Shows the version of the tool."""
    console.print("Deprecated Dependencies Checker")
    console.print("Version: 1.0.1")
    console.print("Author: Iulian Pavlov")
    console.print("License: MIT")


if __name__ == "__main__":
    app() 