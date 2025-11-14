# Location: datanex/README1.md

# BigData Analysis as a Service

A comprehensive, modular data analysis platform supporting file analysis, web scraping, and blockchain data analytics.

## Features

### 1. File Analysis
- ✅ Support for multiple formats (CSV, Excel, JSON, XML, PDF, DOCX, etc.)
- ✅ Automatic categorization
- ✅ Intelligent labeling and tagging
- ✅ Data validation and quality checking
- ✅ Duplicate detection (exact, fuzzy, semantic)
- ✅ Pattern and correlation discovery

### 2. Web Scraping
- ✅ Multiple scraping methods (Requests, Playwright, Scrapy)
- ✅ Concurrent scraping
- ✅ Website crawling
- ✅ Table extraction
- ✅ API scraping

### 3. Blockchain Analytics
- ✅ Ethereum address analysis
- ✅ Transaction tracking
- ✅ Block information
- ✅ Smart contract analysis
- ✅ Real-time monitoring

## Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL
- Redis
- MinIO

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Aran1986/bigdata.git
cd bigdata
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Start services:
```bash
docker-compose up -d
```

6. Initialize database:
```bash
python scripts/init_db.py
```

7. Start API:
```bash
uvicorn api.main:app --reload
```

8. Start Celery worker:
```bash
celery -A workers.tasks worker --loglevel=info
```

## API Documentation

API docs available at: `http://localhost:8000/docs`

### Endpoints

#### Upload
- `POST /upload/file` - Upload file
- `GET /upload/file/{file_id}` - Get file info
- `GET /upload/files` - List files
- `DELETE /upload/file/{file_id}` - Delete file

#### Analysis
- `POST /analyze/full` - Full analysis
- `POST /analyze/clean` - Clean data
- `POST /analyze/deduplicate` - Remove duplicates
- `GET /analyze/task/{task_id}` - Get task status

#### Scraping
- `POST /scrape/url` - Scrape URL
- `POST /scrape/multiple` - Scrape multiple URLs
- `POST /scrape/crawl` - Crawl website
- `POST /scrape/extract-tables` - Extract tables

#### Blockchain
- `POST /blockchain/analyze-address` - Analyze address
- `POST /blockchain/transaction` - Get transaction
- `POST /blockchain/block` - Get block
- `GET /blockchain/gas-prices` - Get gas prices

## Architecture
```
bigdata/
├── api/              # FastAPI endpoints
├── core/             # Business logic modules
├── models/           # Database models
├── services/         # External services
├── workers/          # Celery tasks
├── utils/            # Utilities
├── tests/            # Test suite
└── scripts/          # Helper scripts
```

## Technology Stack

- **Backend**: FastAPI, Python 3.11
- **Database**: PostgreSQL
- **Cache/Queue**: Redis, Celery
- **Storage**: MinIO (S3-compatible)
- **ML/AI**: Scikit-learn, Sentence-Transformers
- **Scraping**: Scrapy, Playwright, BeautifulSoup
- **Blockchain**: Web3.py

## License

MIT License