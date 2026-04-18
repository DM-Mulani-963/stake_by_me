"""Page object model for registration page"""

import logging
from typing import Optional
from src.automation.browser_manager import BrowserManager

logger = logging.getLogger(__name__)


class RegistrationPage:
    """Page object for stake.ac registration form"""
    
    # Selectors (these will need to be updated based on actual site inspection)
    REGISTER_BUTTON = "button:has-text('Register'), a:has-text('Register')"
    EMAIL_INPUT = "input[type='email'], input[name='email']"
    USERNAME_INPUT = "input[name='username'], input[placeholder*='username' i]"
    PASSWORD_INPUT = "input[type='password'], input[name='password']"
    DOB_INPUT = "input[type='date'], input[name='dateOfBirth'], input[name='dob']"
    PHONE_CHECKBOX = "input[type='checkbox'][name*='phone' i]"
    PHONE_INPUT = "input[type='tel'], input[name='phone'], input[name='phoneNumber']"
    NEXT_BUTTON = "button:has-text('Next'), button[type='submit']"
    
    def __init__(self, browser: BrowserManager):
        self.browser = browser
    
    async def click_register(self) -> bool:
        """Click the register button"""
        logger.info("Clicking register button...")
        return await self.browser.click(self.REGISTER_BUTTON)
    
    async def fill_email(self, email: str) -> bool:
        """Fill email field"""
        logger.info(f"Filling email: {email}")
        return await self.browser.fill_input(self.EMAIL_INPUT, email)
    
    async def fill_username(self, username: str) -> bool:
        """Fill username field"""
        logger.info(f"Filling username: {username}")
        return await self.browser.fill_input(self.USERNAME_INPUT, username)
    
    async def fill_password(self, password: str) -> bool:
        """Fill password field"""
        logger.info("Filling password...")
        return await self.browser.fill_input(self.PASSWORD_INPUT, password)
    
    async def fill_dob(self, dob: str) -> bool:
        """Fill date of birth (YYYY-MM-DD format)"""
        logger.info(f"Filling DOB: {dob}")
        return await self.browser.fill_input(self.DOB_INPUT, dob)
    
    async def enable_phone_checkbox(self) -> bool:
        """Enable phone number checkbox if present"""
        logger.info("Enabling phone checkbox...")
        
        # Check if checkbox exists
        if await self.browser.is_visible(self.PHONE_CHECKBOX):
            return await self.browser.check_checkbox(self.PHONE_CHECKBOX)
        else:
            logger.debug("Phone checkbox not found, skipping")
            return True
    
    async def fill_phone(self, phone: str) -> bool:
        """Fill phone number"""
        logger.info(f"Filling phone: {phone}")
        return await self.browser.fill_input(self.PHONE_INPUT, phone)
    
    async def click_next(self) -> bool:
        """Click next/submit button"""
        logger.info("Clicking next button...")
        return await self.browser.click(self.NEXT_BUTTON)
    
    async def fill_registration_form(
        self,
        email: str,
        username: str,
        password: str,
        dob: str,
        phone: str
    ) -> bool:
        """Fill complete registration form"""
        logger.info("=" * 60)
        logger.info("Filling registration form")
        logger.info("=" * 60)
        
        steps = [
            ("Email", self.fill_email(email)),
            ("Username", self.fill_username(username)),
            ("Password", self.fill_password(password)),
            ("Date of Birth", self.fill_dob(dob)),
            ("Phone checkbox", self.enable_phone_checkbox()),
            ("Phone number", self.fill_phone(phone)),
        ]
        
        for step_name, step_coro in steps:
            success = await step_coro
            if not success:
                logger.error(f"Failed at step: {step_name}")
                return False
            logger.info(f"✓ {step_name} completed")
        
        logger.info("✓ Registration form filled successfully")
        return True
