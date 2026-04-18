"""Page object model for document upload"""

import logging
from pathlib import Path
from typing import Optional
from src.automation.browser_manager import BrowserManager

logger = logging.getLogger(__name__)


class DocumentUploadPage:
    """Page object for document upload"""
    
    # Selectors
    DOCUMENT_TYPE_SELECT = "select[name*='document' i], select[name*='type' i]"
    LICENSE_OPTION_VALUE = "driving_license"
    FRONT_IMAGE_INPUT = "input[type='file'][name*='front' i], input[type='file']:nth-of-type(1)"
    BACK_IMAGE_INPUT = "input[type='file'][name*='back' i], input[type='file']:nth-of-type(2)"
    SUBMIT_BUTTON = "button:has-text('Submit'), button:has-text('Upload'), button[type='submit']"
    
    def __init__(self, browser: BrowserManager):
        self.browser = browser
    
    async def select_driving_license(self) -> bool:
        """Select driving license as document type"""
        logger.info("Selecting 'Driving License' as document type...")
        
        if await self.browser.is_visible(self.DOCUMENT_TYPE_SELECT):
            success = await self.browser.select_option(
                self.DOCUMENT_TYPE_SELECT,
                self.LICENSE_OPTION_VALUE
            )
            if success:
                logger.info("✓ Driving License selected")
            return success
        else:
            logger.debug("Document type selector not found, may be pre-selected")
            return True
    
    def find_license_images(self, upload_folder: str, name: str) -> tuple[Optional[Path], Optional[Path]]:
        """
        Find front and back license images for a person
        
        Args:
            upload_folder: Path to upload folder
            name: Full name from license (e.g., "ANSH SURI")
        
        Returns:
            (front_image_path, back_image_path) or (None, None) if not found
        """
        upload_path = Path(upload_folder)
        
        # Normalize name for filename matching
        name_normalized = name.upper().replace(" ", "_")
        
        # Try to find images
        front_pattern = f"{name_normalized}_front.png"
        back_pattern = f"{name_normalized}_back.png"
        
        front_path = upload_path / front_pattern
        back_path = upload_path / back_pattern
        
        if front_path.exists() and back_path.exists():
            logger.info(f"✓ Found license images for {name}")
            logger.debug(f"  Front: {front_path}")
            logger.debug(f"  Back: {back_path}")
            return front_path, back_path
        else:
            logger.warning(f"License images not found for {name}")
            logger.debug(f"  Looked for: {front_pattern}, {back_pattern}")
            return None, None
    
    async def upload_front_image(self, image_path: Path) -> bool:
        """Upload front image of license"""
        logger.info(f"Uploading front image: {image_path.name}")
        success = await self.browser.upload_file(self.FRONT_IMAGE_INPUT, str(image_path))
        if success:
            logger.info("✓ Front image uploaded")
        return success
    
    async def upload_back_image(self, image_path: Path) -> bool:
        """Upload back image of license"""
        logger.info(f"Uploading back image: {image_path.name}")
        success = await self.browser.upload_file(self.BACK_IMAGE_INPUT, str(image_path))
        if success:
            logger.info("✓ Back image uploaded")
        return success
    
    async def click_submit(self) -> bool:
        """Click submit button"""
        logger.info("Clicking 'Submit'...")
        success = await self.browser.click(self.SUBMIT_BUTTON)
        if success:
            logger.info("✓ Submit clicked")
        return success
    
    async def upload_documents(
        self,
        upload_folder: str,
        name: str
    ) -> bool:
        """Complete document upload flow"""
        logger.info("=" * 60)
        logger.info("Document Upload")
        logger.info("=" * 60)
        
        # Step 1: Select document type
        if not await self.select_driving_license():
            logger.error("Failed to select document type")
            return False
        
        # Step 2: Find images
        front_image, back_image = self.find_license_images(upload_folder, name)
        
        if not front_image or not back_image:
            logger.error(f"Missing license images for {name}")
            return False
        
        # Step 3: Upload front image
        if not await self.upload_front_image(front_image):
            logger.error("Failed to upload front image")
            return False
        
        # Step 4: Upload back image
        if not await self.upload_back_image(back_image):
            logger.error("Failed to upload back image")
            return False
        
        # Step 5: Submit
        if not await self.click_submit():
            logger.error("Failed to submit documents")
            return False
        
        logger.info("✓ Document upload completed successfully")
        return True
