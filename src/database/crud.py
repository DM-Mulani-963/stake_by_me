"""CRUD operations for database models"""

from typing import List, Optional
from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

from src.database.models import (
    Job, JobLog, SystemHealth, WorkerHeartbeat, ErrorLog,
    JobStatus, VerificationStatus
)


# ==================== JOB CRUD ====================

def create_job(
    db: Session,
    json_filename: str,
    excel_filename: Optional[str] = None,
    email: Optional[str] = None,
    username: Optional[str] = None,
    name: Optional[str] = None,
) -> Job:
    """Create a new job"""
    job = Job(
        json_filename=json_filename,
        excel_filename=excel_filename,
        email=email,
        username=username,
        name=name,
        status=JobStatus.PENDING,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def get_job(db: Session, job_id: UUID) -> Optional[Job]:
    """Get job by ID"""
    return db.query(Job).filter(Job.id == job_id).first()


def get_jobs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[JobStatus] = None,
) -> List[Job]:
    """Get all jobs with optional filtering"""
    query = db.query(Job)
    if status:
        query = query.filter(Job.status == status)
    return query.order_by(desc(Job.created_at)).offset(skip).limit(limit).all()


def update_job_status(
    db: Session,
    job_id: UUID,
    status: JobStatus,
    error_message: Optional[str] = None,
    last_error_step: Optional[str] = None,
) -> Optional[Job]:
    """Update job status"""
    job = get_job(db, job_id)
    if job:
        job.status = status
        if status == JobStatus.RUNNING and not job.started_at:
            job.started_at = datetime.utcnow()
        elif status in [JobStatus.COMPLETED, JobStatus.FAILED]:
            job.completed_at = datetime.utcnow()
        
        if error_message:
            job.error_message = error_message
        if last_error_step:
            job.last_error_step = last_error_step
        
        if status == JobStatus.RETRY:
            job.retry_count += 1
        
        db.commit()
        db.refresh(job)
    return job


def update_job_verification(
    db: Session,
    job_id: UUID,
    verification_status: VerificationStatus,
    screenshot_path: Optional[str] = None,
    html_content: Optional[str] = None,
) -> Optional[Job]:
    """Update job verification status"""
    job = get_job(db, job_id)
    if job:
        job.verification_status = verification_status
        if screenshot_path:
            job.verification_screenshot = screenshot_path
        if html_content:
            job.verification_html = html_content
        db.commit()
        db.refresh(job)
    return job


def delete_job(db: Session, job_id: UUID) -> bool:
    """Delete a job"""
    job = get_job(db, job_id)
    if job:
        db.delete(job)
        db.commit()
        return True
    return False


def get_jobs_by_status(db: Session, status: JobStatus) -> List[Job]:
    """Get all jobs with a specific status"""
    return db.query(Job).filter(Job.status == status).all()


def get_jobs_for_recovery(db: Session) -> List[Job]:
    """Get jobs that need recovery (stuck in RUNNING state)"""
    return db.query(Job).filter(Job.status == JobStatus.RUNNING).all()


# ==================== JOB LOG CRUD ====================

def create_job_log(
    db: Session,
    job_id: UUID,
    step_name: str,
    action: str,
    status: str,
    step_number: Optional[int] = None,
    duration_ms: Optional[int] = None,
    error_message: Optional[str] = None,
    metadata: Optional[str] = None,
) -> JobLog:
    """Create a job log entry"""
    log = JobLog(
        job_id=job_id,
        step_name=step_name,
        step_number=step_number,
        action=action,
        status=status,
        duration_ms=duration_ms,
        error_message=error_message,
        metadata=metadata,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_job_logs(db: Session, job_id: UUID) -> List[JobLog]:
    """Get all logs for a specific job"""
    return db.query(JobLog).filter(JobLog.job_id == job_id).order_by(JobLog.timestamp).all()


def get_recent_logs(db: Session, limit: int = 100) -> List[JobLog]:
    """Get recent logs across all jobs"""
    return db.query(JobLog).order_by(desc(JobLog.timestamp)).limit(limit).all()


# ==================== SYSTEM HEALTH CRUD ====================

def create_system_health(
    db: Session,
    cpu_usage: Optional[float] = None,
    ram_usage: Optional[float] = None,
    disk_usage: Optional[float] = None,
    queue_size: int = 0,
    active_jobs: int = 0,
    pending_jobs: int = 0,
    worker_status: Optional[str] = None,
) -> SystemHealth:
    """Create system health snapshot"""
    health = SystemHealth(
        cpu_usage_percent=cpu_usage,
        ram_usage_percent=ram_usage,
        disk_usage_percent=disk_usage,
        queue_size=queue_size,
        active_jobs=active_jobs,
        pending_jobs=pending_jobs,
        worker_status=worker_status,
    )
    db.add(health)
    db.commit()
    db.refresh(health)
    return health


def get_latest_system_health(db: Session) -> Optional[SystemHealth]:
    """Get latest system health snapshot"""
    return db.query(SystemHealth).order_by(desc(SystemHealth.timestamp)).first()


def get_system_health_history(db: Session, hours: int = 24) -> List[SystemHealth]:
    """Get system health history for the last N hours"""
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    return db.query(SystemHealth).filter(
        SystemHealth.timestamp >= cutoff_time
    ).order_by(SystemHealth.timestamp).all()


# ==================== WORKER HEARTBEAT CRUD ====================

def update_worker_heartbeat(
    db: Session,
    worker_name: str,
    current_job_id: Optional[UUID] = None,
    metadata: Optional[str] = None,
) -> WorkerHeartbeat:
    """Update worker heartbeat"""
    heartbeat = WorkerHeartbeat(
        worker_name=worker_name,
        current_job_id=current_job_id,
        metadata=metadata,
    )
    db.add(heartbeat)
    db.commit()
    db.refresh(heartbeat)
    return heartbeat


def get_latest_worker_heartbeat(db: Session, worker_name: str) -> Optional[WorkerHeartbeat]:
    """Get latest heartbeat for a worker"""
    return db.query(WorkerHeartbeat).filter(
        WorkerHeartbeat.worker_name == worker_name
    ).order_by(desc(WorkerHeartbeat.timestamp)).first()


# ==================== ERROR LOG CRUD ====================

def create_error_log(
    db: Session,
    level: str,
    message: str,
    module: Optional[str] = None,
    function: Optional[str] = None,
    job_id: Optional[UUID] = None,
    stack_trace: Optional[str] = None,
    metadata: Optional[str] = None,
) -> ErrorLog:
    """Create an error log entry"""
    error = ErrorLog(
        level=level,
        message=message,
        module=module,
        function=function,
        job_id=job_id,
        stack_trace=stack_trace,
        metadata=metadata,
    )
    db.add(error)
    db.commit()
    db.refresh(error)
    return error


def get_recent_errors(db: Session, limit: int = 50) -> List[ErrorLog]:
    """Get recent error logs"""
    return db.query(ErrorLog).order_by(desc(ErrorLog.timestamp)).limit(limit).all()


# Import timedelta for time calculations
from datetime import timedelta
