"""Page object model for terms and conditions"""

import logging
from src.automation.browser_manager import BrowserManager

logger = logging.getLogger(__name__)


class TermsPage:
    """Page object for terms and conditions"""
    
    # Selectors
    TERMS_CONTAINER = ".terms-container, #terms, [class*='terms' i]"
    AGREEMENT_CHECKBOX = "input[type='checkbox'][name*='agree' i], input[type='checkbox'][name*='terms' i]"
    CREATE_ACCOUNT_BUTTON = "button:has-text('Create Account'), button:has-text('Accept'), button[type='submit']"
    
    def __init__(self, browser: BrowserManager):
        self.browser = browser
    
    async def scroll_terms(self) -> bool:
        """Scroll terms and conditions to bottom"""
        logger.info("Scrolling terms and conditions...")
        
        # Try to find and scroll the terms container
        if await self.browser.is_visible(self.TERMS_CONTAINER):
            success = await self.browser.scroll_to_bottom(self.TERMS_CONTAINER)
        else:
            # If no specific container, scroll the whole page
            logger.debug("Terms container not found, scrolling page")
            success = await self.browser.scroll_to_bottom()
        
        if success:
            logger.info("✓ Scrolled to bottom of terms")
        return success
    
    async def accept_terms(self) -> bool:
        """Check the agreement checkbox"""
        logger.info("Accepting terms and conditions...")
        success = await self.browser.check_checkbox(self.AGREEMENT_CHECKBOX)
        if success:
            logger.info("✓ Terms accepted")
        return success
    
    async def click_create_account(self) -> bool:
        """Click create account button"""
        logger.info("Clicking 'Create Account'...")
        success = await self.browser.click(self.CREATE_ACCOUNT_BUTTON)
        if success:
            logger.info("✓ Create Account clicked")
        return success
    
    async def complete_terms_flow(self) -> bool:
        """Complete entire terms and conditions flow"""
        logger.info("=" * 60)
        logger.info("Completing Terms & Conditions")
        logger.info("=" * 60)
        
        steps = [
            ("Scroll terms", self.scroll_terms()),
            ("Accept checkbox", self.accept_terms()),
            ("Create account", self.click_create_account()),
        ]
        
        for step_name, step_coro in steps:
            success = await step_coro
            if not success:
                logger.error(f"Failed at step: {step_name}")
                return False
        
        logger.info("✓ Terms flow completed successfully")
        return True
