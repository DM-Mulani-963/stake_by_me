#!/usr/bin/env python3
"""CLI management script for Stake By Me automation"""

import click
import asyncio
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@click.group()
def cli():
    """Stake By Me - Registration Automation CLI"""
    pass


@cli.command()
@click.option('--host', default='0.0.0.0', help='API host')
@click.option('--port', default=8000, help='API port')
@click.option('--reload', is_flag=True, help='Enable auto-reload')
def api(host, port, reload):
    """Start the FastAPI server"""
    import uvicorn
    
    click.echo("=" * 80)
    click.echo("Starting FastAPI Server")
    click.echo("=" * 80)
    click.echo(f"Host: {host}")
    click.echo(f"Port: {port}")
    click.echo(f"Docs: http://{host}:{port}/docs")
    click.echo("=" * 80)
    
    uvicorn.run(
        "src.api.main:app",
        host=host,
        port=port,
        reload=reload,
    )


@cli.command()
def worker():
    """Start the RQ worker"""
    from src.workers.registration_worker import start_registration_worker
    
    click.echo("=" * 80)
    click.echo("Starting RQ Worker")
    click.echo("=" * 80)
    
    start_registration_worker()


@cli.command()
def init_db():
    """Initialize the database"""
    from src.database.database import init_db
    
    click.echo("=" * 80)
    click.echo("Initializing Database")
    click.echo("=" * 80)
    
    try:
        init_db()
        click.echo("✓ Database initialized successfully")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise


@cli.command()
def process_data():
    """Process JSON data and generate Excel"""
    from src.processors.pipeline import DataPipeline
    
    click.echo("=" * 80)
    click.echo("Processing Data")
    click.echo("=" * 80)
    
    try:
        pipeline = DataPipeline()
        excel_path, records = pipeline.process()
        
        click.echo(f"✓ Processed {len(records)} records")
        click.echo(f"✓ Excel saved to: {excel_path}")
    except Exception as e:
        click.echo(f"✗ Error: {e}", err=True)
        raise


@cli.command()
@click.option('--headless/--no-headless', default=True, help='Run browser in headless mode')
def test_browser(headless):
    """Test browser automation"""
    from src.automation.browser_manager import BrowserManager
    
    async def test():
        click.echo("=" * 80)
        click.echo("Testing Browser")
        click.echo("=" * 80)
        
        async with BrowserManager() as browser:
            await browser.start(headless=headless)
            
            click.echo("✓ Browser started")
            
            # Test navigation
            await browser.goto("https://stake.ac")
            click.echo("✓ Navigation successful")
            
            # Take screenshot
            screenshot_path = Path("./screenshots/test.png")
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            await browser.screenshot(str(screenshot_path))
            click.echo(f"✓ Screenshot saved: {screenshot_path}")
        
        click.echo("✓ Browser test complete")
    
    asyncio.run(test())


@cli.command()
@click.option('--job-id', required=True, help='Job ID to run')
@click.option('--headless/--no-headless', default=True, help='Run browser in headless mode')
def run_job(job_id, headless):
    """Run a single registration job manually"""
    from uuid import UUID
    from src.database.database import get_db_context
    from src.database.crud import get_job
    from src.automation.registration_workflow import run_single_registration
    
    async def run():
        click.echo("=" * 80)
        click.echo(f"Running Job: {job_id}")
        click.echo("=" * 80)
        
        # Get job from database
        job_uuid = UUID(job_id)
        
        with get_db_context() as db:
            job = get_job(db, job_uuid)
            if not job:
                click.echo(f"✗ Job not found: {job_id}", err=True)
                return
        
        # Get user data (you would need to fetch this from processed data)
        # For now, this is a placeholder
        click.echo("✗ Manual job running not fully implemented")
        click.echo("  Use the API to create and run jobs")
    
    asyncio.run(run())


@cli.command()
def health():
    """Check system health"""
    from src.database.database import check_db_connection
    from src.queue.job_queue import JobQueue
    
    click.echo("=" * 80)
    click.echo("System Health Check")
    click.echo("=" * 80)
    
    # Check database
    db_ok = check_db_connection()
    click.echo(f"Database: {'✓ Healthy' if db_ok else '✗ Unhealthy'}")
    
    # Check Redis
    try:
        queue = JobQueue()
        queue.redis_conn.ping()
        redis_ok = True
    except:
        redis_ok = False
    
    click.echo(f"Redis: {'✓ Healthy' if redis_ok else '✗ Unhealthy'}")
    
    # Overall
    overall = db_ok and redis_ok
    click.echo("=" * 80)
    click.echo(f"Overall: {'✓ All systems healthy' if overall else '✗ Some systems unhealthy'}")


if __name__ == '__main__':
    cli()
