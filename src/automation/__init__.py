"""Automation package"""

from src.automation.browser_manager import BrowserManager
from src.automation.registration_workflow import RegistrationWorkflow, run_single_registration

__all__ = [
    "BrowserManager",
    "RegistrationWorkflow",
    "run_single_registration",
]
