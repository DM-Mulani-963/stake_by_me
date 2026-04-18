"""Complete registration workflow orchestrator"""

import logging
import asyncio
from typing import Dict, Optional
from pathlib import Path
from uuid import UUID

from src.automation.browser_manager import BrowserManager
from src.automation.pages import (
    RegistrationPage,
    TermsPage,
    WalletPage,
    ExtendedInfoPage,
    DocumentUploadPage,
    VerificationPage,
)
from src.config import config

logger = logging.getLogger(__name__)


class RegistrationWorkflow:
    """Complete registration workflow automation"""
    
    # Site URL
    SITE_URL = "https://stake.ac"
    
    def __init__(self):
        self.browser: Optional[BrowserManager] = None
        
        # Page objects (initialized after browser)
        self.registration_page: Optional[RegistrationPage] = None
        self.terms_page: Optional[TermsPage] = None
        self.wallet_page: Optional[WalletPage] = None
        self.extended_info_page: Optional[ExtendedInfoPage] = None
        self.document_upload_page: Optional[DocumentUploadPage] = None
        self.verification_page: Optional[VerificationPage] = None
    
    async def initialize(self, headless: bool = True):
        """Initialize browser and page objects"""
        logger.info("Initializing registration workflow...")
        
        self.browser = BrowserManager()
        await self.browser.start(headless=headless)
        
        # Initialize page objects
        self.registration_page = RegistrationPage(self.browser)
        self.terms_page = TermsPage(self.browser)
        self.wallet_page = WalletPage(self.browser)
        self.extended_info_page = ExtendedInfoPage(self.browser)
        self.document_upload_page = DocumentUploadPage(self.browser)
        self.verification_page = VerificationPage(self.browser)
        
        logger.info("✓ Workflow initialized")
    
    async def cleanup(self):
        """Clean up browser resources"""
        if self.browser:
            await self.browser.cleanup()
    
    async def run_registration(
        self,
        job_id: UUID,
        user_data: Dict,
        upload_folder: str = "./input"
    ) -> Dict:
        """
        Execute complete registration workflow
        
        Args:
            job_id: Unique job identifier
            user_data: User information from processed data
            upload_folder: Folder containing license images
        
        Returns:
            Result dict with status and verification info
        """
        logger.info("=" * 80)
        logger.info(f"STARTING REGISTRATION WORKFLOW - Job ID: {job_id}")
        logger.info("=" * 80)
        
        result = {
            "success": False,
            "job_id": str(job_id),
            "verification_status": "ERROR",
            "screenshot_path": None,
            "html_path": None,
            "error": None,
        }
        
        try:
            # Step 1: Navigate to site
            logger.info(f"\n📍 STEP 1: Navigate to {self.SITE_URL}")
            if not await self.browser.goto(self.SITE_URL):
                raise Exception(f"Failed to load {self.SITE_URL}")
            
            await asyncio.sleep(2)  # Wait for page to load
            
            # Step 2: Click register button
            logger.info("\n📍 STEP 2: Click Register")
            if not await self.registration_page.click_register():
                raise Exception("Failed to click register button")
            
            await asyncio.sleep(2)
            
            # Step 3: Fill registration form
            logger.info("\n📍 STEP 3: Fill Registration Form")
            if not await self.registration_page.fill_registration_form(
                email=user_data.get("email"),
                username=user_data.get("username"),
                password=user_data.get("password"),
                dob=user_data.get("dateofbirth"),  # YYYY-MM-DD
                phone=user_data.get("phone_number"),
            ):
                raise Exception("Failed to fill registration form")
            
            # Step 4: Submit registration
            logger.info("\n📍 STEP 4: Submit Registration")
            if not await self.registration_page.click_next():
                raise Exception("Failed to submit registration")
            
            await asyncio.sleep(3)
            
            # Step 5: Handle CAPTCHA (manual intervention may be needed)
            logger.info("\n📍 STEP 5: CAPTCHA Handling")
            logger.warning("⚠️  CAPTCHA may be present - waiting 10 seconds...")
            print("\n" + "=" * 80)
            print("⚠️  If CAPTCHA appears, please solve it manually")
            print("=" * 80)
            await asyncio.sleep(10)
            
            # Step 6: Terms and conditions
            logger.info("\n📍 STEP 6: Terms & Conditions")
            if not await self.terms_page.complete_terms_flow():
                raise Exception("Failed to complete terms flow")
            
            await asyncio.sleep(3)
            
            # Step 7: Wallet setup with OTP
            logger.info("\n📍 STEP 7: Wallet Setup (OTP Required)")
            if not await self.wallet_page.complete_wallet_setup_with_otp():
                raise Exception("Failed to complete wallet setup")
            
            await asyncio.sleep(3)
            
            # Step 8: Extended information
            logger.info("\n📍 STEP 8: Extended Information")
            if not await self.extended_info_page.fill_extended_info(user_data):
                logger.warning("Some extended info fields failed, continuing...")
            
            if not await self.extended_info_page.click_save_continue():
                raise Exception("Failed to save extended info")
            
            await asyncio.sleep(3)
            
            # Step 9: Document upload
            logger.info("\n📍 STEP 9: Document Upload")
            
            # Get full name from data for image lookup
            full_name = f"{user_data.get('firstname', '')} {user_data.get('lastname', '')}".strip()
            
            if not await self.document_upload_page.upload_documents(
                upload_folder=upload_folder,
                name=full_name,
            ):
                raise Exception("Failed to upload documents")
            
            await asyncio.sleep(5)  # Wait for upload processing
            
            # Step 10: Capture verification status
            logger.info("\n📍 STEP 10: Capture Verification Status")
            verification_result = await self.verification_page.capture_verification_status(
                job_id=str(job_id),
                screenshots_folder=config.paths.screenshots,
            )
            
            # Update result
            result["success"] = True
            result["verification_status"] = verification_result["status"]
            result["screenshot_path"] = verification_result["screenshot_path"]
            result["html_path"] = verification_result["html_path"]
            
            logger.info("\n" + "=" * 80)
            logger.info("✅ REGISTRATION WORKFLOW COMPLETED SUCCESSFULLY")
            logger.info("=" * 80)
            logger.info(f"Verification Status: {result['verification_status']}")
            logger.info(f"Screenshot: {result['screenshot_path']}")
            logger.info("=" * 80)
            
        except Exception as e:
            logger.error(f"\n❌ REGISTRATION WORKFLOW FAILED: {e}")
            result["error"] = str(e)
            
            # Try to capture screenshot on error
            try:
                error_screenshot = Path(config.paths.screenshots) / f"{job_id}_error.png"
                await self.browser.screenshot(str(error_screenshot))
                result["screenshot_path"] = str(error_screenshot)
            except:
                pass
        
        return result
    
    async def __aenter__(self):
        """Context manager entry"""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        await self.cleanup()


async def run_single_registration(
    job_id: UUID,
    user_data: Dict,
    headless: bool = True,
    upload_folder: str = "./input"
) -> Dict:
    """
    Convenience function to run a single registration
    
    Args:
        job_id: Unique job identifier
        user_data: User information
        headless: Run browser in headless mode
        upload_folder: Folder with license images
    
    Returns:
        Result dict
    """
    async with RegistrationWorkflow() as workflow:
        await workflow.initialize(headless=headless)
        return await workflow.run_registration(
            job_id=job_id,
            user_data=user_data,
            upload_folder=upload_folder
        )
