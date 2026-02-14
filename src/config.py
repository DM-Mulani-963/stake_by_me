"""Configuration management module"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class BrowserConfig(BaseModel):
    """Browser automation configuration"""
    headless: bool = True
    timeout: int = 30000
    slow_mo: int = 0
    viewport: Dict[str, int] = {"width": 1920, "height": 1080}


class PathsConfig(BaseModel):
    """File paths configuration"""
    input_folder: str = "./data"
    upload_folder: str = "./input"
    output_folder: str = "./output"
    logs_folder: str = "./logs"
    screenshots_folder: str = "./screenshots"


class LoggingConfig(BaseModel):
    """Logging configuration"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    max_log_size_mb: int = 100
    backup_count: int = 5


class JobsConfig(BaseModel):
    """Job processing configuration"""
    max_retries: int = 3
    retry_delay_seconds: int = 60
    exponential_backoff: bool = True
    job_timeout_minutes: int = 30
    otp_timeout_minutes: int = 5


class RateLimitConfig(BaseModel):
    """Rate limiting configuration"""
    enabled: bool = True
    max_jobs_per_hour: int = 20
    delay_between_jobs_seconds: int = 30


class DatabaseConfig(BaseModel):
    """Database configuration"""
    host: str = "postgres"
    port: int = 5432
    name: str = "stake_db"
    pool_size: int = 10
    max_overflow: int = 20


class RedisConfig(BaseModel):
    """Redis configuration"""
    host: str = "redis"
    port: int = 6379
    db: int = 0
    queue_name: str = "stake_jobs"


class WorkerConfig(BaseModel):
    """Worker configuration"""
    processes: int = 1
    heartbeat_interval_seconds: int = 30
    restart_interval_hours: int = 24


class MonitoringConfig(BaseModel):
    """Monitoring configuration"""
    health_check_interval_seconds: int = 30
    cpu_threshold_percent: int = 80
    ram_threshold_percent: int = 80
    disk_threshold_percent: int = 90


class CleanupConfig(BaseModel):
    """Cleanup tasks configuration"""
    archive_logs_after_days: int = 7
    delete_old_jobs_after_days: int = 30
    cleanup_cron: str = "0 2 * * *"


class APIConfig(BaseModel):
    """API configuration"""
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    cors_origins: list[str] = ["http://localhost", "http://localhost:8000"]


class SecurityConfig(BaseModel):
    """Security configuration"""
    enable_auth: bool = True
    session_timeout_minutes: int = 60


class WorkflowConfig(BaseModel):
    """Workflow configuration"""
    target_url: str = "https://stake.ac"
    verification_url: str = "https://stake.ac/settings/verification"


class Config(BaseModel):
    """Main configuration model"""
    browser: BrowserConfig = Field(default_factory=BrowserConfig)
    paths: PathsConfig = Field(default_factory=PathsConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    jobs: JobsConfig = Field(default_factory=JobsConfig)
    rate_limit: RateLimitConfig = Field(default_factory=RateLimitConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    worker: WorkerConfig = Field(default_factory=WorkerConfig)
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig)
    cleanup: CleanupConfig = Field(default_factory=CleanupConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    workflow: WorkflowConfig = Field(default_factory=WorkflowConfig)


class Settings(BaseSettings):
    """Environment settings"""
    # Application
    app_name: str = "stake_by_me"
    app_env: str = "production"
    debug: bool = False
    
    # Database
    postgres_user: str = "stake_user"
    postgres_password: str = "changeme"
    postgres_db: str = "stake_db"
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    database_url: Optional[str] = None
    
    # Redis
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    redis_url: Optional[str] = None
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_secret_key: str = "changeme"
    
    # Authentication
    api_username: str = "admin"
    api_password: str = "changeme"
    jwt_secret_key: str = "changeme"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    
    # Browser
    headless: bool = True
    browser_timeout: int = 30000
    
    # Logging
    log_level: str = "INFO"
    
    # Worker
    worker_processes: int = 1
    worker_name: str = "stake_worker"
    
    # Rate Limiting
    max_jobs_per_hour: int = 20
    
    class Config:
        env_file = ".env"
        case_sensitive = False


def load_config(config_path: str = "config/config.yaml") -> Config:
    """Load configuration from YAML file"""
    config_file = Path(config_path)
    
    if not config_file.exists():
        print(f"Warning: Config file {config_path} not found, using defaults")
        return Config()
    
    with open(config_file, 'r') as f:
        config_data = yaml.safe_load(f)
    
    return Config(**config_data)


def load_settings() -> Settings:
    """Load settings from environment variables"""
    return Settings()


# Global instances
config = load_config()
settings = load_settings()

# Build database URL if not provided
if not settings.database_url:
    settings.database_url = (
        f"postgresql://{settings.postgres_user}:{settings.postgres_password}"
        f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
    )

# Build Redis URL if not provided
if not settings.redis_url:
    settings.redis_url = f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}"
