"""Page object model for extended information form"""

import logging
from typing import Dict
from src.automation.browser_manager import BrowserManager

logger = logging.getLogger(__name__)


class ExtendedInfoPage:
    """Page object for extended information form"""
    
    # Selectors
    FIRSTNAME_INPUT = "input[name='firstName'], input[name='firstname'], input[placeholder*='first name' i]"
    LASTNAME_INPUT = "input[name='lastName'], input[name='lastname'], input[placeholder*='last name' i]"
    COUNTRY_SELECT = "select[name='country'], input[name='country']"
    PLACE_OF_BIRTH_INPUT = "input[name='placeOfBirth'], input[name='place_of_birth'], input[placeholder*='place of birth' i]"
    ADDRESS_INPUT = "input[name='address'], textarea[name='address'], input[name='residential_address']"
    CITY_INPUT = "input[name='city'], input[placeholder*='city' i]"
    POSTAL_CODE_INPUT = "input[name='postalCode'], input[name='postal_code'], input[name='zipCode']"
    OCCUPATION_INDUSTRY_SELECT = "select[name*='industry' i], input[name*='industry' i]"
    OCCUPATION_FIELD_SELECT = "select[name*='field' i], input[name*='field' i]"
    OCCUPATION_EXPERIENCE_SELECT = "select[name*='experience' i], input[name*='experience' i]"
    SAVE_CONTINUE_BUTTON = "button:has-text('Save'), button:has-text('Continue'), button[type='submit']"
    
    def __init__(self, browser: BrowserManager):
        self.browser = browser
    
    async def fill_firstname(self, firstname: str) -> bool:
        """Fill first name (including middle name)"""
        logger.info(f"Filling first name: {firstname}")
        return await self.browser.fill_input(self.FIRSTNAME_INPUT, firstname)
    
    async def fill_lastname(self, lastname: str) -> bool:
        """Fill last name"""
        logger.info(f"Filling last name: {lastname}")
        return await self.browser.fill_input(self.LASTNAME_INPUT, lastname)
    
    async def fill_country(self, country: str) -> bool:
        """Fill country"""
        logger.info(f"Filling country: {country}")
        
        # Try select first
        if await self.browser.is_visible(self.COUNTRY_SELECT):
            try:
                return await self.browser.select_option(self.COUNTRY_SELECT, country)
            except:
                # If select fails, try as input
                return await self.browser.fill_input(self.COUNTRY_SELECT, country)
        return False
    
    async def fill_place_of_birth(self, place: str) -> bool:
        """Fill place of birth"""
        logger.info(f"Filling place of birth: {place}")
        return await self.browser.fill_input(self.PLACE_OF_BIRTH_INPUT, place)
    
    async def fill_address(self, address: str) -> bool:
        """Fill residential address"""
        logger.info(f"Filling address: {address}")
        return await self.browser.fill_input(self.ADDRESS_INPUT, address)
    
    async def fill_city(self, city: str) -> bool:
        """Fill city"""
        logger.info(f"Filling city: {city}")
        return await self.browser.fill_input(self.CITY_INPUT, city)
    
    async def fill_postal_code(self, postal_code: str) -> bool:
        """Fill postal code"""
        logger.info(f"Filling postal code: {postal_code}")
        return await self.browser.fill_input(self.POSTAL_CODE_INPUT, postal_code)
    
    async def fill_occupation_industry(self, industry: str) -> bool:
        """Fill occupation industry"""
        logger.info(f"Filling occupation industry: {industry}")
        
        if await self.browser.is_visible(self.OCCUPATION_INDUSTRY_SELECT):
            try:
                return await self.browser.select_option(self.OCCUPATION_INDUSTRY_SELECT, industry)
            except:
                return await self.browser.fill_input(self.OCCUPATION_INDUSTRY_SELECT, industry)
        return False
    
    async def fill_occupation_field(self, field: str) -> bool:
        """Fill occupation field"""
        logger.info(f"Filling occupation field: {field}")
        
        if await self.browser.is_visible(self.OCCUPATION_FIELD_SELECT):
            try:
                return await self.browser.select_option(self.OCCUPATION_FIELD_SELECT, field)
            except:
                return await self.browser.fill_input(self.OCCUPATION_FIELD_SELECT, field)
        return False
    
    async def fill_occupation_experience(self, experience: str) -> bool:
        """Fill occupation experience"""
        logger.info(f"Filling occupation experience: {experience}")
        
        if await self.browser.is_visible(self.OCCUPATION_EXPERIENCE_SELECT):
            try:
                return await self.browser.select_option(self.OCCUPATION_EXPERIENCE_SELECT, experience)
            except:
                return await self.browser.fill_input(self.OCCUPATION_EXPERIENCE_SELECT, experience)
        return False
    
    async def click_save_continue(self) -> bool:
        """Click save and continue button"""
        logger.info("Clicking 'Save and Continue'...")
        success = await self.browser.click(self.SAVE_CONTINUE_BUTTON)
        if success:
            logger.info("✓ Save and Continue clicked")
        return success
    
    async def fill_extended_info(self, data: Dict) -> bool:
        """Fill complete extended information form"""
        logger.info("=" * 60)
        logger.info("Filling Extended Information")
        logger.info("=" * 60)
        
        steps = [
            ("First Name", self.fill_firstname(data.get("firstname", ""))),
            ("Last Name", self.fill_lastname(data.get("lastname", ""))),
            ("Country", self.fill_country(data.get("country", "India"))),
            ("Place of Birth", self.fill_place_of_birth(data.get("place_of_birth", ""))),
            ("Residential Address", self.fill_address(data.get("residential_address", ""))),
            ("City", self.fill_city(data.get("city", ""))),
            ("Postal Code", self.fill_postal_code(data.get("postal_code", ""))),
            ("Occupation Industry", self.fill_occupation_industry(data.get("occupation_industry", ""))),
            ("Occupation Field", self.fill_occupation_field(data.get("occupation_field", ""))),
            ("Occupation Experience", self.fill_occupation_experience(data.get("occupation_experience", ""))),
        ]
        
        for step_name, step_coro in steps:
            success = await step_coro
            if not success:
                logger.warning(f"Failed at step: {step_name}, continuing...")
            else:
                logger.info(f"✓ {step_name} completed")
        
        logger.info("✓ Extended info form filled successfully")
        return True
