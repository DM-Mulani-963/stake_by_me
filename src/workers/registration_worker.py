"""Registration worker - processes registration jobs from queue"""

import logging
import asyncio
from typing import Dict
from uuid import UUID

from src.automation.registration_workflow import run_single_registration
from src.database.crud import update_job_status, create_job_log
from src.database.models import JobStatus
from src.database.database import get_db_context
from src.config import settings

logger = logging.getLogger(__name__)


def process_registration_job(
    job_id: str,
    user_data: Dict,
    upload_folder: str = "./input"
) -> Dict:
    """
    Process a registration job (RQ worker function)
    
    This function is called by RQ workers and must be synchronous.
    We use asyncio.run() to execute the async registration workflow.
    
    Args:
        job_id: Database job ID (string)
        user_data: User information dict
        upload_folder: Folder with license images
    
    Returns:
        Result dict
    """
    job_uuid = UUID(job_id)
    
    logger.info("=" * 80)
    logger.info(f"WORKER: Processing registration job {job_id}")
    logger.info("=" * 80)
    
    # Update status to IN_PROGRESS
    with get_db_context() as db:
        update_job_status(db, job_uuid, JobStatus.IN_PROGRESS)
        create_job_log(
            db,
            job_id=job_uuid,
            step_name="WORKER_START",
            status="SUCCESS",
            message="Worker started processing job",
        )
    
    try:
        # Run the async registration workflow
        result = asyncio.run(
            run_single_registration(
                job_id=job_uuid,
                user_data=user_data,
                headless=settings.headless,
                upload_folder=upload_folder,
            )
        )
        
        # Update database based on result
        with get_db_context() as db:
            if result["success"]:
                # Success
                update_job_status(
                    db,
                    job_uuid,
                    JobStatus.COMPLETED,
                    verification_status=result["verification_status"],
                    screenshot_path=result["screenshot_path"],
                )
                
                create_job_log(
                    db,
                    job_id=job_uuid,
                    step_name="REGISTRATION_COMPLETE",
                    status="SUCCESS",
                    message=f"Registration completed. Status: {result['verification_status']}",
                    details=result,
                )
                
                logger.info(f"✅ Job {job_id} completed successfully")
            else:
                # Failed
                update_job_status(
                    db,
                    job_uuid,
                    JobStatus.FAILED,
                    error_message=result.get("error"),
                    screenshot_path=result.get("screenshot_path"),
                )
                
                create_job_log(
                    db,
                    job_id=job_uuid,
                    step_name="REGISTRATION_FAILED",
                    status="FAILED",
                    message=f"Registration failed: {result.get('error')}",
                    details=result,
                )
                
                logger.error(f"❌ Job {job_id} failed: {result.get('error')}")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Worker exception for job {job_id}: {e}", exc_info=True)
        
        # Update database to FAILED
        with get_db_context() as db:
            update_job_status(
                db,
                job_uuid,
                JobStatus.FAILED,
                error_message=str(e),
            )
            
            create_job_log(
                db,
                job_id=job_uuid,
                step_name="WORKER_ERROR",
                status="FAILED",
                message=f"Worker error: {str(e)}",
            )
        
        # Re-raise so RQ marks job as failed
        raise


def start_registration_worker():
    """Start the registration worker"""
    from src.queue.job_queue import start_worker
    
    logger.info("Starting registration worker...")
    start_worker(queue_names=['registration'])
