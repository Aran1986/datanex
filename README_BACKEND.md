# BigData Analysis as a Service

یک پلتفرم جامع و ماژولار برای آنالیز داده که از فرمت‌های متنوع، اسکرپینگ وب و آنالیز بلاکچین پشتیبانی می‌کند.

## ویژگی‌ها

### 1. آنالیز فایل
- ✅ پشتیبانی از فرمت‌های مختلف (CSV, Excel, JSON, XML, PDF, DOCX و...)
- ✅ دسته‌بندی خودکار
- ✅ لیبل‌گذاری هوشمند
- ✅ اعتبارسنجی و بررسی کیفیت
- ✅ تشخیص تکراری (exact, fuzzy, semantic)
- ✅ کشف الگو و همبستگی

### 2. اسکرپینگ وب
- ✅ روش‌های متنوع اسکرپ (Requests, Playwright, Scrapy)
- ✅ اسکرپ همزمان
- ✅ Crawling وبسایت
- ✅ استخراج جداول
- ✅ اسکرپ API

### 3. آنالیز بلاکچین
- ✅ آنالیز آدرس Ethereum
- ✅ ردیابی تراکنش‌ها
- ✅ اطلاعات بلاک
- ✅ آنالیز Smart Contract
- ✅ نظارت Real-time

## نصب سریع

### پیش‌نیازها
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL
- Redis
- MinIO

### مراحل نصب

1. کلون repository:
```bash
git clone https://github.com/Aran1986/bigdata.git
cd bigdata
```

2. ایجاد virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. نصب dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

4. تنظیم environment:
```bash
cp .env.example .env
# ویرایش .env با تنظیمات خود
```

5. راه‌اندازی سرویس‌ها:
```bash
docker-compose up -d
```

6. راه‌اندازی دیتابیس:
```bash
python scripts/init_db.py
```

7. اجرای API:
```bash
uvicorn api.main:app --reload
```

8. اجرای Celery worker:
```bash
celery -A workers.tasks worker --loglevel=info
```

## مستندات API

مستندات در: `http://localhost:8000/docs`

## معماری

```
bigdata/
├── api/              # FastAPI endpoints
├── core/             # ماژول‌های اصلی
├── models/           # مدل‌های دیتابیس
├── services/         # سرویس‌های خارجی
├── workers/          # Celery tasks
├── utils/            # ابزارها
├── tests/            # تست‌ها
└── scripts/          # اسکریپت‌های کمکی
```

## تکنولوژی‌ها

- **Backend**: FastAPI, Python 3.11
- **Database**: PostgreSQL
- **Cache/Queue**: Redis, Celery
- **Storage**: MinIO (S3-compatible)
- **ML/AI**: Scikit-learn, Sentence-Transformers
- **Scraping**: Scrapy, Playwright, BeautifulSoup
- **Blockchain**: Web3.py

## لایسنس

MIT License
