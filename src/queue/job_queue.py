"""Job queue manager using RQ and Redis"""

import logging
from typing import Optional, Dict, List
from uuid import UUID
from datetime import datetime

from redis import Redis
from rq import Queue, Worker
from rq.job import Job

from src.config import settings
from src.database.crud import update_job_status, create_job_log
from src.database.models import JobStatus
from src.database.database import get_db_context

logger = logging.getLogger(__name__)


class JobQueue:
    """Manage RQ job queue"""
    
    def __init__(self):
        # Connect to Redis
        self.redis_conn = Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            password=settings.redis_password if settings.redis_password else None,
            decode_responses=False,  # We want bytes for RQ
        )
        
        # Create queue
        self.queue = Queue(
            name='registration',
            connection=self.redis_conn,
            default_timeout='1h',  # 1 hour timeout for jobs
        )
        
        logger.info(f"✓ Connected to Redis at {settings.redis_host}:{settings.redis_port}")
    
    def enqueue_registration(
        self,
        job_id: UUID,
        user_data: Dict,
        upload_folder: str = "./input"
    ) -> Job:
        """
        Enqueue a registration job
        
        Args:
            job_id: Database job ID
            user_data: User information dict
            upload_folder: Folder with license images
        
        Returns:
            RQ Job object
        """
        from src.workers.registration_worker import process_registration_job
        
        logger.info(f"Enqueueing registration job: {job_id}")
        
        # Enqueue job
        rq_job = self.queue.enqueue(
            process_registration_job,
            job_id=str(job_id),
            user_data=user_data,
            upload_folder=upload_folder,
            job_id=f"registration_{job_id}",  # RQ job ID
        )
        
        logger.info(f"✓ Job enqueued: {rq_job.id}")
        
        # Update database
        with get_db_context() as db:
            update_job_status(
                db,
                job_id=job_id,
                status=JobStatus.QUEUED,
                rq_job_id=rq_job.id,
            )
            
            create_job_log(
                db,
                job_id=job_id,
                step_name="ENQUEUED",
                status="SUCCESS",
                message="Job enqueued for processing",
            )
        
        return rq_job
    
    def get_job_status(self, rq_job_id: str) -> Dict:
        """
        Get status of an RQ job
        
        Args:
            rq_job_id: RQ job ID
        
        Returns:
            Status dict
        """
        try:
            job = Job.fetch(rq_job_id, connection=self.redis_conn)
            
            return {
                "id": job.id,
                "status": job.get_status(),
                "created_at": job.created_at.isoformat() if job.created_at else None,
                "started_at": job.started_at.isoformat() if job.started_at else None,
                "ended_at": job.ended_at.isoformat() if job.ended_at else None,
                "result": job.result,
                "exc_info": job.exc_info,
            }
        except Exception as e:
            logger.error(f"Error fetching job {rq_job_id}: {e}")
            return {
                "error": str(e)
            }
    
    def get_queue_stats(self) -> Dict:
        """Get queue statistics"""
        try:
            return {
                "name": self.queue.name,
                "count": len(self.queue),
                "started_jobs": self.queue.started_job_registry.count,
                "finished_jobs": self.queue.finished_job_registry.count,
                "failed_jobs": self.queue.failed_job_registry.count,
                "deferred_jobs": self.queue.deferred_job_registry.count,
                "scheduled_jobs": self.queue.scheduled_job_registry.count,
            }
        except Exception as e:
            logger.error(f"Error getting queue stats: {e}")
            return {"error": str(e)}
    
    def clear_all_jobs(self):
        """Clear all jobs from queue (use with caution!)"""
        logger.warning("Clearing all jobs from queue!")
        self.queue.empty()
        logger.info("✓ Queue cleared")
    
    def cancel_job(self, rq_job_id: str) -> bool:
        """Cancel a job"""
        try:
            job = Job.fetch(rq_job_id, connection=self.redis_conn)
            job.cancel()
            logger.info(f"✓ Job cancelled: {rq_job_id}")
            return True
        except Exception as e:
            logger.error(f"Error cancelling job {rq_job_id}: {e}")
            return False


def start_worker(queue_names: Optional[List[str]] = None):
    """
    Start an RQ worker
    
    Args:
        queue_names: List of queue names to listen to
    """
    if queue_names is None:
        queue_names = ['registration']
    
    redis_conn = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        password=settings.redis_password if settings.redis_password else None,
    )
    
    logger.info(f"Starting worker for queues: {queue_names}")
    
    worker = Worker(
        queues=queue_names,
        connection=redis_conn,
        name=f"worker_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
    )
    
    worker.work(with_scheduler=True)
