"""FastAPI application - REST API for registration automation"""

import logging
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, BackgroundTask
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.config import settings
from src.database.database import get_db, engine, Base, check_db_connection
from src.database import crud
from src.database.models import JobStatus
from src.queue.job_queue import JobQueue
from src.processors.pipeline import DataPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Stake By Me - Registration Automation API",
    description="Automated registration and data processing system",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize job queue
job_queue = JobQueue()


# Pydantic models for API
class JobCreate(BaseModel):
    """Request model for creating a new job"""
    json_filename: Optional[str] = None
    process_all: bool = Field(default=False, description="Process all JSON files in input folder")


class JobResponse(BaseModel):
    """Response model for job"""
    id: str
    json_filename: Optional[str]
    status: str
    verification_status: Optional[str]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    error_message: Optional[str]
    screenshot_path: Optional[str]
    rq_job_id: Optional[str]
    
    class Config:
        from_attributes = True


class JobStats(BaseModel):
    """Job statistics"""
    total: int
    pending: int
    queued: int
    in_progress: int
    completed: int
    failed: int


class QueueStats(BaseModel):
    """Queue statistics"""
    queue_name: str
    queued_jobs: int
    started_jobs: int
    finished_jobs: int
    failed_jobs: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    database: str
    redis: str
    timestamp: datetime


# Startup and shutdown events
@app.on_event("startup")
async def startup():
    """Initialize database and services on startup"""
    logger.info("Starting up application...")
    
    # Create database tables
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Check database connection
    if check_db_connection():
        logger.info("✓ Database connection successful")
    else:
        logger.error("✗ Database connection failed")
    
    logger.info("✓ Application startup complete")


@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown"""
    logger.info("Shutting down application...")


# API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Stake By Me - Registration Automation API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    
    # Check database
    db_status = "healthy" if check_db_connection() else "unhealthy"
    
    # Check Redis
    try:
        job_queue.redis_conn.ping()
        redis_status = "healthy"
    except:
        redis_status = "unhealthy"
    
    overall_status = "healthy" if db_status == "healthy" and redis_status == "healthy" else "unhealthy"
    
    return {
        "status": overall_status,
        "database": db_status,
        "redis": redis_status,
        "timestamp": datetime.now(),
    }


@app.post("/jobs", response_model=JobResponse, tags=["Jobs"])
async def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new registration job
    
    - Processes JSON data from input folder
    - Generates Excel file
    - Enqueues registration workflow
    """
    logger.info("Creating new job...")
    
    try:
        # Process data
        pipeline = DataPipeline()
        excel_path, records = pipeline.process()
        
        if not records:
            raise HTTPException(status_code=400, detail="No valid records found in input files")
        
        # Create database job for each record
        jobs_created = []
        
        for record in records:
            # Create job in database
            job = crud.create_job(
                db,
                json_filename=record.get("source_file", "unknown"),
                status=JobStatus.PENDING,
            )
            
            # Enqueue for processing
            job_queue.enqueue_registration(
                job_id=job.id,
                user_data=record,
                upload_folder="./input",
            )
            
            jobs_created.append(job)
            logger.info(f"✓ Created and enqueued job: {job.id}")
        
        # Return first job (or could return all)
        return jobs_created[0]
        
    except Exception as e:
        logger.error(f"Error creating job: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/jobs", response_model=List[JobResponse], tags=["Jobs"])
async def list_jobs(
    status: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all jobs"""
    
    if status:
        try:
            status_enum = JobStatus[status.upper()]
            jobs = crud.get_jobs_by_status(db, status_enum, limit=limit)
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    else:
        jobs = db.query(crud.Job).order_by(crud.Job.created_at.desc()).limit(limit).all()
    
    return jobs


@app.get("/jobs/{job_id}", response_model=JobResponse, tags=["Jobs"])
async def get_job(job_id: UUID, db: Session = Depends(get_db)):
    """Get a specific job"""
    
    job = crud.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job


@app.delete("/jobs/{job_id}", tags=["Jobs"])
async def cancel_job(job_id: UUID, db: Session = Depends(get_db)):
    """Cancel a job"""
    
    job = crud.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Cancel in RQ if has RQ job ID
    if job.rq_job_id:
        job_queue.cancel_job(job.rq_job_id)
    
    # Update database
    crud.update_job_status(db, job_id, JobStatus.FAILED, error_message="Cancelled by user")
    
    return {"message": "Job cancelled"}


@app.get("/jobs/{job_id}/logs", tags=["Jobs"])
async def get_job_logs(job_id: UUID, db: Session = Depends(get_db)):
    """Get logs for a specific job"""
    
    job = crud.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    logs = crud.get_job_logs(db, job_id)
    return logs


@app.get("/stats/jobs", response_model=JobStats, tags=["Statistics"])
async def get_job_stats(db: Session = Depends(get_db)):
    """Get job statistics"""
    
    from sqlalchemy import func
    
    stats = db.query(
        func.count(crud.Job.id).label("total"),
        func.sum(crud.Job.status == JobStatus.PENDING).label("pending"),
        func.sum(crud.Job.status == JobStatus.QUEUED).label("queued"),
        func.sum(crud.Job.status == JobStatus.IN_PROGRESS).label("in_progress"),
        func.sum(crud.Job.status == JobStatus.COMPLETED).label("completed"),
        func.sum(crud.Job.status == JobStatus.FAILED).label("failed"),
    ).first()
    
    return {
        "total": stats.total or 0,
        "pending": stats.pending or 0,
        "queued": stats.queued or 0,
        "in_progress": stats.in_progress or 0,
        "completed": stats.completed or 0,
        "failed": stats.failed or 0,
    }


@app.get("/stats/queue", response_model=QueueStats, tags=["Statistics"])
async def get_queue_stats():
    """Get queue statistics"""
    
    stats = job_queue.get_queue_stats()
    
    return {
        "queue_name": stats.get("name", "registration"),
        "queued_jobs": stats.get("count", 0),
        "started_jobs": stats.get("started_jobs", 0),
        "finished_jobs": stats.get("finished_jobs", 0),
        "failed_jobs": stats.get("failed_jobs", 0),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
