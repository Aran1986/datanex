# 🚀 DataNex - Next-Gen Data Analysis Platform

<div align="center">

![DataNex Logo](frontend/public/logo.svg)

**DataNex** is a comprehensive, modular data analysis platform powered by AI

[Features](#features) • [Quick Start](#quick-start) • [Documentation](#documentation) • [License](#license)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**DataNex** is a complete data analysis ecosystem that combines:
- **Powerful Backend API** (FastAPI + PostgreSQL + Celery)
- **Modern Frontend UI** (React + Vite + TailwindCSS)
- **AI-Powered Analysis** (Pattern detection, categorization, deduplication)
- **Web Scraping** (Extract data from websites)
- **Blockchain Analytics** (Ethereum address and transaction analysis)

---

## ✨ Features

### 📊 Data Analysis
- ✅ Multi-format support (CSV, Excel, JSON, XML, PDF, DOCX, etc.)
- ✅ Automatic categorization and labeling
- ✅ Data quality validation
- ✅ Smart duplicate detection (exact, fuzzy, semantic)
- ✅ Pattern and correlation discovery
- ✅ Anomaly detection

### 🌐 Web Scraping
- ✅ Multiple scraping methods (Requests, Playwright, Scrapy)
- ✅ Concurrent scraping
- ✅ Website crawling
- ✅ Table extraction from HTML

### ⛓️ Blockchain Analytics
- ✅ Ethereum address analysis
- ✅ Transaction tracking
- ✅ Block information
- ✅ Smart contract analysis
- ✅ Gas price monitoring

### 🎨 Modern UI
- ✅ Beautiful gradient design
- ✅ Drag & drop file upload
- ✅ Real-time progress tracking
- ✅ Interactive charts and visualizations
- ✅ Responsive design (mobile, tablet, desktop)

---

## 🏗️ Architecture

```
DataNex/
├── 🔧 Backend (FastAPI)
│   ├── api/              # API endpoints
│   ├── core/             # Business logic (8 modules)
│   ├── models/           # Database models
│   ├── services/         # External services
│   └── workers/          # Celery tasks
│
├── 🎨 Frontend (React)
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── pages/        # Application pages
│   │   ├── services/     # API integration
│   │   └── store/        # State management
│   └── public/           # Static assets
│
└── 📚 Documentation
    └── Comprehensive guides
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL
- Redis

### Backend Setup

```bash
# 1. Navigate to project root
cd DataNex

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Start Docker services
docker-compose up -d

# 5. Initialize database
python scripts/init_db.py

# 6. Start API server
uvicorn api.main:app --reload

# 7. Start Celery worker (in another terminal)
celery -A workers.tasks worker --loglevel=info
```

**Backend will be available at:** `http://localhost:8000`
**API Documentation:** `http://localhost:8000/docs`

### Frontend Setup

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
```

**Frontend will be available at:** `http://localhost:3000`

---

## 📁 Project Structure

```
DataNex/
├── 📦 Backend
│   ├── api/
│   │   ├── main.py                 # FastAPI app
│   │   ├── dependencies.py         # Dependencies
│   │   └── routes/
│   │       ├── upload.py           # File upload endpoints
│   │       ├── analyze.py          # Analysis endpoints
│   │       ├── scrape.py           # Scraping endpoints
│   │       └── blockchain.py       # Blockchain endpoints
│   │
│   ├── core/
│   │   ├── file_handler.py         # Module 1: File processing
│   │   ├── categorizer.py          # Module 2: Categorization
│   │   ├── labeler.py              # Module 3: Labeling
│   │   ├── validator.py            # Module 4: Validation
│   │   ├── deduplicator.py         # Module 5: Deduplication
│   │   ├── pattern_finder.py       # Module 6: Pattern detection
│   │   ├── scraper.py              # Module 7: Web scraping
│   │   └── blockchain_analyzer.py  # Module 8: Blockchain analysis
│   │
│   ├── models/
│   │   ├── base.py                 # Base models
│   │   ├── file.py                 # File model
│   │   ├── analysis.py             # Analysis model
│   │   └── task.py                 # Task model
│   │
│   ├── services/
│   │   ├── storage.py              # MinIO storage
│   │   ├── queue.py                # Celery queue
│   │   └── ai_provider.py          # AI integration
│   │
│   ├── workers/
│   │   └── tasks.py                # Background tasks
│   │
│   ├── utils/
│   │   ├── config.py               # Configuration
│   │   └── logger.py               # Logging
│   │
│   └── tests/                      # Test suite
│
├── 🎨 Frontend
│   ├── src/
│   │   ├── components/
│   │   │   └── Layout/
│   │   │       ├── Layout.jsx
│   │   │       ├── Sidebar.jsx
│   │   │       └── Navbar.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx       # Main dashboard
│   │   │   ├── Upload.jsx          # File upload
│   │   │   ├── FileDetail.jsx      # File details
│   │   │   ├── Scraping.jsx        # Web scraping
│   │   │   ├── Blockchain.jsx      # Blockchain analysis
│   │   │   └── Settings.jsx        # Settings
│   │   │
│   │   ├── services/
│   │   │   └── api.js              # API client
│   │   │
│   │   └── store/
│   │       └── index.js            # State management
│   │
│   └── public/
│       └── logo.svg                # DataNex logo
│
└── 📚 Documentation
    ├── README.md                   # This file
    ├── README_BACKEND.md           # Backend documentation
    ├── SETUP_GUIDE_FA.md           # Persian setup guide
    ├── CODE_CHECKLIST.md           # Code checklist
    └── GIT_COMMANDS.md             # Git commands
```

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **Redis** - Cache and message broker
- **Celery** - Background task processing
- **MinIO** - Object storage (S3-compatible)
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations

### Data Processing
- **Pandas** - Data manipulation
- **Scikit-learn** - Machine learning
- **Sentence-Transformers** - Semantic similarity
- **Great Expectations** - Data validation

### Web Scraping
- **Scrapy** - Web crawling framework
- **Playwright** - Browser automation
- **BeautifulSoup** - HTML parsing

### Blockchain
- **Web3.py** - Ethereum integration
- **Solana.py** - Solana integration

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **TailwindCSS** - Styling framework
- **Recharts** - Data visualization
- **Zustand** - State management
- **React Router** - Routing
- **Axios** - HTTP client

---

## 📚 Documentation

### Setup Guides
- [English Setup Guide](README_BACKEND.md)
- [راهنمای فارسی](SETUP_GUIDE_FA.md)

### Code Documentation
- [Code Checklist](CODE_CHECKLIST.md)
- [Project Structure](STRUCTURE.txt)

### Deployment
- [Git Commands](GIT_COMMANDS.md)
- Docker Compose included

---

## 🔧 Configuration

### Backend (.env)
```env
DATABASE_URL=postgresql+asyncpg://admin:admin123@localhost:5432/datanex
REDIS_URL=redis://localhost:6379/0
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

---

## 📊 API Endpoints

### File Upload
- `POST /upload/file` - Upload file
- `GET /upload/files` - List files
- `GET /upload/file/{file_id}` - Get file info
- `DELETE /upload/file/{file_id}` - Delete file

### Analysis
- `POST /analyze/full` - Full analysis
- `POST /analyze/clean` - Clean data
- `POST /analyze/deduplicate` - Remove duplicates
- `GET /analyze/task/{task_id}` - Get task status

### Scraping
- `POST /scrape/url` - Scrape URL
- `POST /scrape/multiple` - Scrape multiple URLs
- `POST /scrape/crawl` - Crawl website
- `POST /scrape/extract-tables` - Extract tables

### Blockchain
- `POST /blockchain/analyze-address` - Analyze address
- `POST /blockchain/transaction` - Get transaction
- `POST /blockchain/block` - Get block info
- `GET /blockchain/gas-prices` - Get gas prices

---

## 🎨 Branding

### Colors
- **Primary (Indigo)**: #6366f1 - Technology, Power
- **Secondary (Purple)**: #8b5cf6 - Creativity, AI
- **Accent (Cyan)**: #06b6d4 - Data, Digital

### Logo
- Hexagon shape = Structure, Architecture
- Connected nodes = Data network
- Gradient = Modern, Advanced

---

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines.

---

## 📄 License

MIT License

Copyright (c) 2024 DataNex

---

## 🆘 Support

- **Documentation**: Check the docs folder
- **Issues**: Open an issue on GitHub
- **Email**: support@datanex.io

---

## 🎯 Roadmap

- [x] Core data analysis features
- [x] Web scraping
- [x] Blockchain analytics
- [x] Modern UI/UX
- [ ] Advanced ML models
- [ ] Real-time collaboration
- [ ] API authentication
- [ ] Cloud deployment guides

---

<div align="center">

Made with ❤️ by DataNex Team

**[Website](#) • [Documentation](#) • [GitHub](#)**

</div>
