# 🎯 Stake By Me - Automated Registration & Data Processing

> **Internal 24/7 Monitoring & Automation System**

## 📋 Overview

Stake By Me is an automated registration and data processing workflow system designed for internal use. It processes JSON files, generates Excel spreadsheets, automates web-based registration workflows, handles OTP verification, uploads documents, and verifies submission status.

## 🏗️ Architecture

### Tech Stack

- **Backend:** FastAPI (Python)
- **Automation:** Playwright (Python)
- **Database:** PostgreSQL
- **Queue System:** RQ (Redis Queue)
- **Cache/Broker:** Redis
- **Deployment:** Docker Compose

### Design Philosophy

- **24/7 Stability:** Built for continuous operation with crash recovery
- **Job Queueing:** Background job processing for reliable execution
- **Monitoring:** Comprehensive logging and system health tracking
- **Dark Neo-Tech UI:** Modern dashboard for operational control

## 📁 Project Structure

```
stake_by_me/
├── config/             # Configuration files
├── data/               # Input JSON files
├── input/              # Document images (driving licenses)
├── logs/               # Execution logs
├── output/             # Generated Excel files
├── screenshots/        # Verification screenshots
├── src/                # Source code
│   ├── api/           # FastAPI application
│   ├── automation/    # Playwright workflows
│   ├── database/      # Database models and migrations
│   ├── processors/    # Data processing modules
│   └── ui/            # Dashboard frontend
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.10+
- 4GB RAM minimum (8GB recommended for parallel jobs)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repo-url>
   cd stake_by_me
   ```

2. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start with Docker Compose**

   ```bash
   docker-compose up -d
   ```

4. **Access the dashboard**
   ```
   http://localhost:8000
   ```

## 🔧 Configuration

Edit `config/config.yaml`:

```yaml
headless: true # Run browser in headless mode
input_folder: ./data
upload_folder: ./uploads
log_level: INFO
max_retries: 3
timeout: 30000 # milliseconds
```

## 📊 Features

### ✅ Data Processing

- JSON file parsing and validation
- Synthetic data generation for missing fields
- Excel file generation with structured data
- Country-city-postal code consistency

### ✅ Browser Automation

- Cloudflare CAPTCHA handling (where legally authorized)
- Multi-step registration workflow
- OTP manual entry via terminal
- Document upload automation
- Verification status capture

### ✅ Job Queue System

- Background job processing with RQ
- Retry mechanism with exponential backoff
- Crash recovery on startup
- Job status tracking

### ✅ Monitoring Dashboard

- Real-time job monitoring
- System health metrics (CPU, RAM, Disk)
- Live process logs
- Error tracking and analytics

## 🔐 Security

- VPN/local access only (not exposed publicly)
- Basic authentication
- Environment variable secrets
- No OTP/password logging
- Input sanitization

## 📝 Usage

### Adding Jobs

1. Place JSON files in the `data/` folder
2. Place driving license images in `input/` folder with naming format:
   - `FIRSTNAME_LASTNAME_front.png`
   - `FIRSTNAME_LASTNAME_back.png`
3. Jobs will be automatically picked up and processed

### Monitoring

Access the dashboard at `http://localhost:8000` to:

- View job status
- Monitor system health
- Review logs
- Manage failed jobs

## 🧪 Testing

```bash
# Run unit tests
pytest tests/unit

# Run integration tests
pytest tests/integration

# Run all tests
pytest
```

## 📚 Documentation

- [PRD](sources/prd.md) - Product Requirements Document
- [Tech Stack](sources/tech-stack.md) - Technical architecture details
- [Design Doc](sources/design-doc.md) - UI/UX design specifications
- [TODO](TODO.md) - Implementation task list

## ⚠️ Important Notes

### Legal & Compliance

This tool is designed for:

- **Authorized environments only**
- **Explicit written platform permission**
- **Internal QA or testing use cases**

**DO NOT USE** for:

- Security bypass without authorization
- Platform policy violations
- Unauthorized automation
- Identity falsification

### Performance Expectations

- **Memory:** ~200-400MB per browser instance
- **Runtime:** Continuous 24/7 operation supported
- **Cleanup:** Browser restarts after each job
- **Monitoring:** Health checks every 30 seconds

## 🐛 Troubleshooting

### Common Issues

**Browser crashes:**

- Check available memory
- Review browser console logs in `logs/{job_id}/browser_console.log`
- Ensure headless mode is configured correctly

**Job stuck in RUNNING:**

- Restart worker service
- Check crash recovery logs
- Review job timeout settings

**Database connection errors:**

- Verify PostgreSQL container is running
- Check database credentials in `.env`
- Review connection pool settings

## 🔄 Maintenance

### Daily Tasks

- Review failed jobs
- Check system health metrics
- Monitor disk space

### Weekly Tasks

- Archive old logs
- Clean up completed jobs
- Review error patterns

### Monthly Tasks

- Database vacuum
- Update dependencies
- Performance optimization review

## 📞 Support

For issues or questions:

- Check logs in `logs/` directory
- Review dashboard error panel
- Check system health metrics

## 📄 License

Internal use only - Not for redistribution

---

**Built with ❤️ for reliability and stability**
# stake_by_me
