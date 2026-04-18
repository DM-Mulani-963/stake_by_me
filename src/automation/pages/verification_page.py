"""Page object model for verification status page"""

import logging
from pathlib import Path
from typing import Optional, Dict
from src.automation.browser_manager import BrowserManager

logger = logging.getLogger(__name__)


class VerificationPage:
    """Page object for verification status page"""
    
    # URL
    VERIFICATION_URL = "https://stake.ac/settings/verification"
    
    # Selectors (will need to be updated based on actual site)
    STATUS_CONTAINER = ".verification-status, #verification, [class*='verification' i]"
    STATUS_TEXT = ".status, .verification-status-text, [class*='status' i]"
    
    # Status keywords
    STATUS_KEYWORDS = {
        "verified": ["verified", "approved", "complete", "success"],
        "pending": ["pending", "in progress", "processing", "reviewing"],
        "submitted": ["submitted", "sent", "uploaded"],
        "rejected": ["rejected", "denied", "failed", "declined"],
    }
    
    def __init__(self, browser: BrowserManager):
        self.browser = browser
    
    async def navigate_to_verification(self) -> bool:
        """Navigate to verification page"""
        logger.info(f"Navigating to verification page: {self.VERIFICATION_URL}")
        success = await self.browser.goto(self.VERIFICATION_URL)
        if success:
            logger.info("✓ Verification page loaded")
        return success
    
    async def capture_screenshot(self, filepath: str) -> bool:
        """Capture screenshot of verification page"""
        logger.info(f"Capturing screenshot: {filepath}")
        return await self.browser.screenshot(filepath, full_page=True)
    
    async def save_html(self, filepath: str) -> bool:
        """Save HTML of verification page"""
        logger.info(f"Saving HTML: {filepath}")
        return await self.browser.save_html(filepath)
    
    async def extract_verification_status(self) -> str:
        """
        Extract verification status from page
        
        Returns:
            Status string: VERIFIED, PENDING, SUBMITTED, REJECTED, or ERROR
        """
        logger.info("Extracting verification status...")
        
        try:
            # Get text from status elements
            status_text = await self.browser.get_text(self.STATUS_TEXT)
            
            if not status_text:
                # Try getting from container
                status_text = await self.browser.get_text(self.STATUS_CONTAINER)
            
            if not status_text:
                # Try getting from page body
                status_text = await self.browser.get_text("body")
            
            if not status_text:
                logger.error("Could not extract status text")
                return "ERROR"
            
            # Normalize text
            status_text_lower = status_text.lower()
            
            # Check for each status
            for status, keywords in self.STATUS_KEYWORDS.items():
                for keyword in keywords:
                    if keyword in status_text_lower:
                        status_upper = status.upper()
                        logger.info(f"✓ Status detected: {status_upper}")
                        return status_upper
            
            # If no keyword matched
            logger.warning(f"Could not determine status from text: {status_text[:100]}")
            return "PENDING"  # Default to pending if unclear
            
        except Exception as e:
            logger.error(f"Error extracting status: {e}")
            return "ERROR"
    
    async def capture_verification_status(
        self,
        job_id: str,
        screenshots_folder: str = "./screenshots"
    ) -> Dict:
        """
        Complete verification capture flow
        
        Returns:
            Dict with status, screenshot_path, html_path
        """
        logger.info("=" * 60)
        logger.info("Verification Status Capture")
        logger.info("=" * 60)
        
        # Navigate to verification page
        if not await self.navigate_to_verification():
            logger.error("Failed to navigate to verification page")
            return {
                "status": "ERROR",
                "screenshot_path": None,
                "html_path": None,
            }
        
        # Wait a bit for page to settle
        import asyncio
        await asyncio.sleep(2)
        
        # Create paths
        screenshots_path = Path(screenshots_folder)
        screenshots_path.mkdir(parents=True, exist_ok=True)
        
        screenshot_file = screenshots_path / f"{job_id}_verification.png"
        html_file = screenshots_path / f"{job_id}_verification.html"
        
        # Capture screenshot
        screenshot_success = await self.capture_screenshot(str(screenshot_file))
        
        # Save HTML
        html_success = await self.save_html(str(html_file))
        
        # Extract status
        status = await self.extract_verification_status()
        
        result = {
            "status": status,
            "screenshot_path": str(screenshot_file) if screenshot_success else None,
            "html_path": str(html_file) if html_success else None,
        }
        
        logger.info("=" * 60)
        logger.info(f"Verification Status: {status}")
        logger.info(f"Screenshot: {screenshot_file if screenshot_success else 'Failed'}")
        logger.info(f"HTML: {html_file if html_success else 'Failed'}")
        logger.info("=" * 60)
        
        return result
