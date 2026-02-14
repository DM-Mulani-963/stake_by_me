"""Database models for Stake By Me system"""

from datetime import datetime
from typing import Optional
from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class JobStatus(str, PyEnum):
    """Job status enumeration"""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRY = "RETRY"
    FAILED_RECOVERED = "FAILED_RECOVERED"


class VerificationStatus(str, PyEnum):
    """Verification status enumeration"""
    VERIFIED = "VERIFIED"
    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    REJECTED = "REJECTED"
    ERROR = "ERROR"


class Job(Base):
    """Job model for tracking registration jobs"""
    __tablename__ = "jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    json_filename = Column(String(255), nullable=False)
    excel_filename = Column(String(255))
    
    # User information
    email = Column(String(255))
    username = Column(String(255))
    name = Column(String(255))
    
    # Job status
    status = Column(Enum(JobStatus), default=JobStatus.PENDING, nullable=False)
    retry_count = Column(Integer, default=0)
    
    # Verification
    verification_status = Column(Enum(VerificationStatus))
    verification_screenshot = Column(String(512))
    verification_html = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Error tracking
    error_message = Column(Text)
    last_error_step = Column(String(100))
    
    # Relationship to logs
    logs = relationship("JobLog", back_populates="job", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Job {self.id} - {self.status}>"
    
    @property
    def duration_seconds(self) -> Optional[float]:
        """Calculate job duration in seconds"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None


class JobLog(Base):
    """Job log model for tracking individual steps"""
    __tablename__ = "job_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    
    # Step information
    step_name = Column(String(100), nullable=False)
    step_number = Column(Integer)
    action = Column(String(500), nullable=False)
    status = Column(String(50), nullable=False)  # SUCCESS, FAILED, RUNNING
    
    # Timing
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    duration_ms = Column(Integer)
    
    # Error info
    error_message = Column(Text)
    stack_trace = Column(Text)
    
    # Additional context
    metadata = Column(Text)  # JSON string for additional data
    
    # Relationship
    job = relationship("Job", back_populates="logs")
    
    def __repr__(self):
        return f"<JobLog {self.id} - {self.job_id} - {self.step_name}>"


class SystemHealth(Base):
    """System health metrics model"""
    __tablename__ = "system_health"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Resource metrics
    cpu_usage_percent = Column(Float)
    ram_usage_percent = Column(Float)
    disk_usage_percent = Column(Float)
    
    # Queue metrics
    queue_size = Column(Integer, default=0)
    active_jobs = Column(Integer, default=0)
    pending_jobs = Column(Integer, default=0)
    
    # Worker status
    worker_status = Column(String(50))  # ONLINE, OFFLINE, DEGRADED
    worker_heartbeat = Column(DateTime)
    
    # Database status
    db_connection_pool_size = Column(Integer)
    db_active_connections = Column(Integer)
    
    # Redis status
    redis_status = Column(String(50))  # CONNECTED, DISCONNECTED
    redis_memory_usage_mb = Column(Float)
    
    # Browser metrics
    active_browser_instances = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<SystemHealth {self.timestamp} - CPU: {self.cpu_usage_percent}%>"


class WorkerHeartbeat(Base):
    """Worker heartbeat tracking"""
    __tablename__ = "worker_heartbeats"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    worker_name = Column(String(100), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    status = Column(String(50), default="ALIVE")
    current_job_id = Column(UUID(as_uuid=True))
    metadata = Column(Text)  # JSON string for additional info
    
    def __repr__(self):
        return f"<WorkerHeartbeat {self.worker_name} - {self.timestamp}>"


class ErrorLog(Base):
    """Global error logging"""
    __tablename__ = "error_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Error details
    level = Column(String(20), nullable=False)  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    module = Column(String(100))
    function = Column(String(100))
    
    # Job association (if applicable)
    job_id = Column(UUID(as_uuid=True))
    
    # Error content
    message = Column(Text, nullable=False)
    stack_trace = Column(Text)
    metadata = Column(Text)  # JSON string
    
    def __repr__(self):
        return f"<ErrorLog {self.id} - {self.level} - {self.message[:50]}>"
