"""Page object model for wallet setup"""

import logging
from src.automation.browser_manager import BrowserManager

logger = logging.getLogger(__name__)


class WalletPage:
    """Page object for wallet setup"""
    
    # Selectors
    WALLET_POPUP = ".modal, .popup, [role='dialog']"
    SETUP_WALLET_BUTTON = "button:has-text('Setup Wallet'), button:has-text('Create Wallet')"
    OTP_INPUT = "input[type='text'][name*='otp' i], input[placeholder*='otp' i], input[name='code']"
    OTP_SUBMIT_BUTTON = "button:has-text('Submit'), button:has-text('Verify'), button[type='submit']"
    
    def __init__(self, browser: BrowserManager):
        self.browser = browser
    
    async def wait_for_wallet_popup(self, timeout: int = 10000) -> bool:
        """Wait for wallet popup to appear"""
        logger.info("Waiting for wallet popup...")
        success = await self.browser.wait_for_selector(self.WALLET_POPUP, timeout=timeout)
        if success:
            logger.info("✓ Wallet popup appeared")
        return success
    
    async def click_setup_wallet(self) -> bool:
        """Click setup wallet button"""
        logger.info("Clicking 'Setup Wallet'...")
        success = await self.browser.click(self.SETUP_WALLET_BUTTON)
        if success:
            logger.info("✓ Setup Wallet clicked")
        return success
    
    async def wait_for_otp_input(self, timeout: int = 10000) -> bool:
        """Wait for OTP input field to appear"""
        logger.info("Waiting for OTP input field...")
        success = await self.browser.wait_for_selector(self.OTP_INPUT, timeout=timeout)
        if success:
            logger.info("✓ OTP input field appeared")
        return success
    
    async def request_otp_from_user(self) -> str:
        """Request OTP from user via terminal"""
        logger.info("=" * 60)
        logger.info("OTP REQUIRED")
        logger.info("=" * 60)
        
        print("\n" + "=" * 60)
        print("🔐 OTP VERIFICATION REQUIRED")
        print("=" * 60)
        print("Please check your email/phone for the OTP code.")
        print("Enter the OTP below:")
        print("=" * 60)
        
        otp = input("OTP: ").strip()
        
        logger.info(f"OTP received from user (length: {len(otp)})")
        return otp
    
    async def submit_otp(self, otp: str) -> bool:
        """Submit OTP code"""
        logger.info("Submitting OTP...")
        
        # Fill OTP input
        success = await self.browser.fill_input(self.OTP_INPUT, otp)
        if not success:
            return False
        
        # Click submit
        success = await self.browser.click(self.OTP_SUBMIT_BUTTON)
        if success:
            logger.info("✓ OTP submitted")
        
        return success
    
    async def complete_wallet_setup_with_otp(self) -> bool:
        """Complete wallet setup with OTP verification"""
        logger.info("=" * 60)
        logger.info("Wallet Setup with OTP")
        logger.info("=" * 60)
        
        # Wait for popup
        if not await self.wait_for_wallet_popup():
            logger.error("Wallet popup did not appear")
            return False
        
        # Click setup wallet
        if not await self.click_setup_wallet():
            logger.error("Failed to click setup wallet")
            return False
        
        # Wait for OTP input
        if not await self.wait_for_otp_input():
            logger.error("OTP input did not appear")
            return False
        
        # Request OTP from user
        otp = await self.request_otp_from_user()
        
        if not otp:
            logger.error("No OTP provided")
            return False
        
        # Submit OTP
        if not await self.submit_otp(otp):
            logger.error("Failed to submit OTP")
            return False
        
        logger.info("✓ Wallet setup completed successfully")
        return True
