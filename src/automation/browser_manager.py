"""Browser automation manager using Playwright"""

import asyncio
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Playwright
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from src.config import config, settings

logger = logging.getLogger(__name__)


class BrowserManager:
    """Manage Playwright browser instances"""
    
    def __init__(self):
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
        # Configuration
        self.headless = settings.headless
        self.timeout = config.browser.timeout
        self.slow_mo = config.browser.slow_mo
        self.viewport = config.browser.viewport
    
    async def start(self, headless: Optional[bool] = None):
        """Initialize Playwright and launch browser"""
        if headless is not None:
            self.headless = headless
        
        logger.info(f"Starting browser (headless={self.headless})...")
        
        try:
            self.playwright = await async_playwright().start()
            
            # Launch Chromium
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                slow_mo=self.slow_mo,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                ]
            )
            
            # Create context with options
            self.context = await self.browser.new_context(
                viewport=self.viewport,
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='en-US',
                timezone_id='Asia/Kolkata',
            )
            
            # Set default timeout
            self.context.set_default_timeout(self.timeout)
            
            # Create page
            self.page = await self.context.new_page()
            
            # Enable console logging if configured
            if config.features.enable_console_logging:
                self.page.on("console", lambda msg: logger.debug(f"Browser console: {msg.text}"))
            
            # Enable error logging
            self.page.on("pageerror", lambda err: logger.error(f"Browser error: {err}"))
            
            logger.info("✓ Browser started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            await self.cleanup()
            raise
    
    async def goto(self, url: str, wait_until: str = "networkidle") -> bool:
        """Navigate to URL"""
        try:
            logger.info(f"Navigating to: {url}")
            await self.page.goto(url, wait_until=wait_until)
            logger.info("✓ Page loaded")
            return True
        except PlaywrightTimeoutError:
            logger.error(f"Timeout loading page: {url}")
            return False
        except Exception as e:
            logger.error(f"Error navigating to {url}: {e}")
            return False
    
    async def screenshot(self, filepath: str, full_page: bool = True) -> bool:
        """Take screenshot"""
        try:
            screenshot_path = Path(filepath)
            screenshot_path.parent.mkdir(parents=True, exist_ok=True)
            
            await self.page.screenshot(
                path=str(screenshot_path),
                full_page=full_page
            )
            logger.info(f"✓ Screenshot saved: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return False
    
    async def save_html(self, filepath: str) -> bool:
        """Save page HTML"""
        try:
            html = await self.page.content()
            
            html_path = Path(filepath)
            html_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html)
            
            logger.info(f"✓ HTML saved: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving HTML: {e}")
            return False
    
    async def wait_for_selector(
        self,
        selector: str,
        timeout: Optional[int] = None,
        state: str = "visible"
    ) -> bool:
        """Wait for element to be ready"""
        try:
            await self.page.wait_for_selector(
                selector,
                timeout=timeout or self.timeout,
                state=state
            )
            return True
        except PlaywrightTimeoutError:
            logger.warning(f"Timeout waiting for selector: {selector}")
            return False
        except Exception as e:
            logger.error(f"Error waiting for selector {selector}: {e}")
            return False
    
    async def fill_input(self, selector: str, value: str, delay: int = 50) -> bool:
        """Fill input field with typing delay"""
        try:
            await self.page.fill(selector, "")  # Clear first
            await self.page.type(selector, value, delay=delay)
            logger.debug(f"✓ Filled {selector}")
            return True
        except Exception as e:
            logger.error(f"Error filling {selector}: {e}")
            return False
    
    async def click(self, selector: str, delay: int = 100) -> bool:
        """Click element"""
        try:
            await self.page.click(selector)
            await asyncio.sleep(delay / 1000)  # Small delay after click
            logger.debug(f"✓ Clicked {selector}")
            return True
        except Exception as e:
            logger.error(f"Error clicking {selector}: {e}")
            return False
    
    async def scroll_to_bottom(self, container_selector: Optional[str] = None) -> bool:
        """Scroll to bottom of page or container"""
        try:
            if container_selector:
                # Scroll specific container
                await self.page.eval_on_selector(
                    container_selector,
                    "el => el.scrollTop = el.scrollHeight"
                )
            else:
                # Scroll page
                await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            
            await asyncio.sleep(1)  # Wait for scroll to complete
            logger.debug("✓ Scrolled to bottom")
            return True
        except Exception as e:
            logger.error(f"Error scrolling: {e}")
            return False
    
    async def check_checkbox(self, selector: str) -> bool:
        """Check a checkbox"""
        try:
            await self.page.check(selector)
            logger.debug(f"✓ Checked {selector}")
            return True
        except Exception as e:
            logger.error(f"Error checking {selector}: {e}")
            return False
    
    async def select_option(self, selector: str, value: str) -> bool:
        """Select dropdown option"""
        try:
            await self.page.select_option(selector, value)
            logger.debug(f"✓ Selected {value} in {selector}")
            return True
        except Exception as e:
            logger.error(f"Error selecting option in {selector}: {e}")
            return False
    
    async def upload_file(self, selector: str, filepath: str) -> bool:
        """Upload file"""
        try:
            file_path = Path(filepath)
            if not file_path.exists():
                logger.error(f"File not found: {filepath}")
                return False
            
            await self.page.set_input_files(selector, str(file_path))
            logger.debug(f"✓ Uploaded {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            return False
    
    async def wait_for_navigation(self, timeout: Optional[int] = None):
        """Wait for navigation"""
        try:
            await self.page.wait_for_load_state("networkidle", timeout=timeout)
            return True
        except Exception as e:
            logger.error(f"Error waiting for navigation: {e}")
            return False
    
    async def get_text(self, selector: str) -> Optional[str]:
        """Get text content from element"""
        try:
            element = await self.page.query_selector(selector)
            if element:
                return await element.text_content()
            return None
        except Exception as e:
            logger.error(f"Error getting text from {selector}: {e}")
            return None
    
    async def is_visible(self, selector: str) -> bool:
        """Check if element is visible"""
        try:
            return await self.page.is_visible(selector)
        except Exception as e:
            return False
    
    async def cleanup(self):
        """Clean up browser resources"""
        logger.info("Cleaning up browser resources...")
        
        try:
            if self.page:
                await self.page.close()
                self.page = None
            
            if self.context:
                await self.context.close()
                self.context = None
            
            if self.browser:
                await self.browser.close()
                self.browser = None
            
            if self.playwright:
                await self.playwright.stop()
                self.playwright = None
            
            logger.info("✓ Browser cleanup complete")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    async def __aenter__(self):
        """Context manager entry"""
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        await self.cleanup()
