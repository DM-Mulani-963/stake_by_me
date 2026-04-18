"""Worker entrypoint script"""

import logging
from src.workers.registration_worker import start_registration_worker

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    print("=" * 80)
    print("STARTING REGISTRATION WORKER")
    print("=" * 80)
    start_registration_worker()
