# Quickstart Guide

## Setup

1. **Copy environment file**:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and fill in your credentials.

2. **Start services with Docker**:

   ```bash
   docker-compose up -d
   ```

3. **Check health**:
   ```bash
   curl http://localhost:8000/health
   ```

## Using the CLI

The project includes a CLI tool for local development:

```bash
# Make CLI executable
chmod +x cli.py

# Check system health
./cli.py health

# Initialize database
./cli.py init_db

# Process JSON data to Excel
./cli.py process-data

# Start API server (development)
./cli.py api --reload

# Start worker (development)
./cli.py worker

# Test browser automation
./cli.py test-browser
```

## API Usage

### Create a Job

```bash
curl -X POST "http://localhost:8000/jobs" \
  -H "Content-Type: application/json" \
  -d '{"process_all": true}'
```

### List Jobs

```bash
curl "http://localhost:8000/jobs"
```

### Get Job Status

```bash
curl "http://localhost:8000/jobs/{job_id}"
```

### Get Statistics

```bash
# Job stats
curl "http://localhost:8000/stats/jobs"

# Queue stats
curl "http://localhost:8000/stats/queue"
```

## Input Data

Place your JSON files and license images in the `input/` folder:

```
input/
├── test_data.json
├── ANSH_SURI_front.png
├── ANSH_SURI_back.png
└── ...
```

##Dashboard

Access the API documentation at: **http://localhost:8000/docs**

## Logs

- Job logs: Stored in database (`job_logs` table)
- Application logs: Docker container logs
- Screenshots: `screenshots/` folder

## Troubleshooting

### Database connection issues

```bash
docker-compose logs postgres
```

### Redis connection issues

```bash
docker-compose logs redis
```

### Worker not processing jobs

```bash
docker-compose logs worker
docker-compose restart worker
```
