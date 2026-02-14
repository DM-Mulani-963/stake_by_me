-- Initial database setup for Stake By Me
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- Create custom types
DO $$ BEGIN CREATE TYPE job_status AS ENUM (
    'PENDING',
    'RUNNING',
    'COMPLETED',
    'FAILED',
    'RETRY',
    'FAILED_RECOVERED'
);
EXCEPTION
WHEN duplicate_object THEN null;
END $$;
DO $$ BEGIN CREATE TYPE verification_status AS ENUM (
    'VERIFIED',
    'PENDING',
    'SUBMITTED',
    'REJECTED',
    'ERROR'
);
EXCEPTION
WHEN duplicate_object THEN null;
END $$;
-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_created_at ON jobs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_job_logs_job_id ON job_logs(job_id);
CREATE INDEX IF NOT EXISTS idx_job_logs_timestamp ON job_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_system_health_timestamp ON system_health(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_worker_heartbeats_timestamp ON worker_heartbeats(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_error_logs_timestamp ON error_logs(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_error_logs_job_id ON error_logs(job_id);
-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO stake_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO stake_user;