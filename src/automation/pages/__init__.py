"""Page objects package"""

from src.automation.pages.registration_page import RegistrationPage
from src.automation.pages.terms_page import TermsPage
from src.automation.pages.wallet_page import WalletPage
from src.automation.pages.extended_info_page import ExtendedInfoPage
from src.automation.pages.document_upload_page import DocumentUploadPage
from src.automation.pages.verification_page import VerificationPage

__all__ = [
    "RegistrationPage",
    "TermsPage",
    "WalletPage",
    "ExtendedInfoPage",
    "DocumentUploadPage",
    "VerificationPage",
]
