#!/usr/bin/env python3
"""
Stake By Me - Standalone CLI Tool
Complete registration automation without Docker
"""

import sys
import asyncio
import logging
from pathlib import Path
from typing import Optional
import argparse
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.processors.pipeline import DataPipeline
from src.automation.registration_workflow import run_single_registration
from src.config import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('cli/stake_cli.log')
    ]
)
logger = logging.getLogger(__name__)


class StakeCLI:
    """Standalone CLI for complete registration workflow"""
    
    def __init__(self):
        self.config = config
        
    def process_data(self, input_file: Optional[str] = None):
        """Process JSON data to Excel"""
        print("\n" + "="*80)
        print("📊 PROCESSING DATA")
        print("="*80)
        
        try:
            pipeline = DataPipeline()
            excel_path, records = pipeline.process()
            
            if excel_path and records:
                print(f"\n✅ Success!")
                print(f"   📄 Excel file: {excel_path}")
                print(f"   📝 Records: {len(records)}")
                return excel_path, records
            else:
                print("\n❌ No data found to process")
                return None, []
                
        except Exception as e:
            logger.error(f"Data processing failed: {e}", exc_info=True)
            print(f"\n❌ Error: {e}")
            return None, []
    
    async def run_registration(self, user_data: dict, headless: bool = True):
        """Run single registration workflow"""
        print("\n" + "="*80)
        print(f"🚀 REGISTRATION: {user_data.get('username', 'Unknown')}")
        print("="*80)
        
        try:
            result = await run_single_registration(
                job_id=None,
                user_data=user_data,
                headless=headless
            )
            
            if result.get('success'):
                print(f"\n✅ Registration successful!")
                print(f"   Status: {result.get('verification_status', 'Unknown')}")
                if result.get('screenshot_path'):
                    print(f"   Screenshot: {result['screenshot_path']}")
            else:
                print(f"\n❌ Registration failed: {result.get('error', 'Unknown error')}")
                
            return result
            
        except Exception as e:
            logger.error(f"Registration failed: {e}", exc_info=True)
            print(f"\n❌ Error: {e}")
            return {"success": False, "error": str(e)}
    
    async def process_and_register(self, headless: bool = True):
        """Complete workflow: process data and run registrations"""
        print("\n" + "🎯"*40)
        print("COMPLETE REGISTRATION WORKFLOW")
        print("🎯"*40)
        
        # Step 1: Process data
        excel_path, records = self.process_data()
        
        if not records:
            print("\n❌ No records to process. Exiting.")
            return
        
        # Step 2: Run registrations
        print(f"\n📋 Processing {len(records)} registrations...")
        results = []
        
        for idx, record in enumerate(records, 1):
            print(f"\n{'─'*80}")
            print(f"Registration {idx}/{len(records)}")
            print(f"{'─'*80}")
            
            result = await self.run_registration(record, headless=headless)
            results.append({
                'user': record.get('username'),
                'success': result.get('success'),
                'status': result.get('verification_status'),
                'error': result.get('error')
            })
            
            # Small delay between registrations
            if idx < len(records):
                await asyncio.sleep(5)
        
        # Step 3: Summary
        self.print_summary(results)
        
        return results
    
    def print_summary(self, results: list):
        """Print execution summary"""
        print("\n" + "="*80)
        print("📊 EXECUTION SUMMARY")
        print("="*80)
        
        total = len(results)
        successful = sum(1 for r in results if r['success'])
        failed = total - successful
        
        print(f"\n📈 Statistics:")
        print(f"   Total:      {total}")
        print(f"   ✅ Success: {successful}")
        print(f"   ❌ Failed:  {failed}")
        print(f"   Success Rate: {(successful/total*100):.1f}%")
        
        if failed > 0:
            print(f"\n❌ Failed registrations:")
            for r in results:
                if not r['success']:
                    print(f"   • {r['user']}: {r.get('error', 'Unknown error')}")
        
        print(f"\n📁 Output Location:")
        print(f"   Excel: {config.paths.output_folder}/")
        print(f"   Screenshots: {config.paths.screenshots_folder}/")
        print(f"   Logs: cli/stake_cli.log")
        print()
    
    def test_browser(self, headless: bool = False):
        """Test browser automation"""
        print("\n" + "="*80)
        print("🌐 BROWSER TEST")
        print("="*80)
        
        async def _test():
            from src.automation.browser_manager import BrowserManager
            
            try:
                async with BrowserManager(headless=headless) as browser:
                    page = await browser.new_page()
                    await page.goto("https://stake.ac")
                    print(f"\n✅ Browser test successful!")
                    print(f"   Title: {await page.title()}")
                    await asyncio.sleep(3)
                    
            except Exception as e:
                logger.error(f"Browser test failed: {e}", exc_info=True)
                print(f"\n❌ Browser test failed: {e}")
        
        asyncio.run(_test())
    
    def check_dependencies(self):
        """Check if all dependencies are installed"""
        print("\n" + "="*80)
        print("🔍 CHECKING DEPENDENCIES")
        print("="*80)
        
        dependencies = {
            'openpyxl': 'Excel generation',
            'pandas': 'Data processing',
            'faker': 'Synthetic data',
            'playwright': 'Browser automation',
            'pydantic': 'Configuration',
        }
        
        missing = []
        for package, purpose in dependencies.items():
            try:
                __import__(package)
                print(f"   ✅ {package:15s} - {purpose}")
            except ImportError:
                print(f"   ❌ {package:15s} - {purpose} (MISSING)")
                missing.append(package)
        
        if missing:
            print(f"\n⚠️  Missing packages: {', '.join(missing)}")
            print(f"\n📦 Install with: pip install {' '.join(missing)}")
            return False
        else:
            print(f"\n✅ All dependencies installed!")
            return True
    
    def install_playwright(self):
        """Install Playwright browsers"""
        print("\n" + "="*80)
        print("📦 INSTALLING PLAYWRIGHT BROWSERS")
        print("="*80)
        
        import subprocess
        try:
            subprocess.run(['playwright', 'install', 'chromium'], check=True)
            print("\n✅ Playwright browsers installed!")
        except Exception as e:
            print(f"\n❌ Failed to install Playwright: {e}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Stake By Me - Complete Registration Automation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process JSON data to Excel
  %(prog)s process

  # Run complete workflow (process + register)
  %(prog)s run

  # Run with visible browser
  %(prog)s run --no-headless

  # Test browser automation
  %(prog)s test-browser

  # Check dependencies
  %(prog)s check

  # Install Playwright browsers
  %(prog)s install-playwright
        """
    )
    
    parser.add_argument(
        'command',
        choices=['process', 'run', 'test-browser', 'check', 'install-playwright'],
        help='Command to execute'
    )
    
    parser.add_argument(
        '--no-headless',
        action='store_true',
        help='Show browser window (default: headless)'
    )
    
    args = parser.parse_args()
    
    cli = StakeCLI()
    
    try:
        if args.command == 'check':
            cli.check_dependencies()
            
        elif args.command == 'install-playwright':
            cli.install_playwright()
            
        elif args.command == 'process':
            cli.process_data()
            
        elif args.command == 'test-browser':
            cli.test_browser(headless=not args.no_headless)
            
        elif args.command == 'run':
            asyncio.run(cli.process_and_register(headless=not args.no_headless))
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
