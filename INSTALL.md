# Location: datanex/INSTALL.md

# Installation Guide

## System Requirements

- OS: Linux (Ubuntu 20.04+), macOS, or Windows 10/11
- RAM: 8GB minimum, 16GB recommended
- Storage: 20GB free space
- Python: 3.11 or higher
- Docker: 20.10+
- Docker Compose: 2.0+

## Step-by-Step Installation

### 1. Install Python 3.11

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

#### macOS
```bash
brew install python@3.11
```

#### Windows
Download from: https://www.python.org/downloads/

### 2. Install Docker

#### Ubuntu
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

#### macOS/Windows
Download Docker Desktop from: https://www.docker.com/products/docker-desktop/

### 3. Clone Repository
```bash
git clone https://github.com/Aran1986/bigdata.git
cd bigdata
```

### 4. Create Virtual Environment
```bash
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 5. Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Install Playwright Browsers
```bash
playwright install chromium
```

### 7. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` and set your configuration:
- Database credentials
- Redis URL
- MinIO credentials
- API keys (OpenAI, Anthropic, Infura, etc.)

### 8. Start Docker Services
```bash
docker-compose up -d
```

Verify services:
```bash
docker-compose ps
```

### 9. Initialize Database
```bash
python scripts/init_db.py
```

### 10. Run Migrations
```bash
alembic upgrade head
```

### 11. Start Services

Open 3 terminals:

**Terminal 1 - API:**
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Celery Worker:**
```bash
celery -A workers.tasks worker --loglevel=info
```

**Terminal 3 - Celery Beat (optional):**
```bash
celery -A workers.tasks beat --loglevel=info
```

### 12. Verify Installation

Open browser: http://localhost:8000/docs

You should see the API documentation.

## Troubleshooting

### Port Already in Use
```bash
# Linux/Mac
sudo lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Database Connection Error
```bash
# Check PostgreSQL
docker-compose logs postgres

# Restart services
docker-compose restart postgres
```

### Redis Connection Error
```bash
# Check Redis
docker-compose logs redis

# Restart Redis
docker-compose restart redis
```

## Next Steps

1. Read API Documentation: http://localhost:8000/docs
2. Run tests: `pytest tests/`
3. Check logs: `tail -f logs/bigdata_*.log`