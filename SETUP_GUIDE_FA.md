# راهنمای راه‌اندازی کامل پروژه BigData

## مرحله 1: دانلود و آماده‌سازی

1. این ZIP را extract کنید
2. وارد پوشه شوید: `cd bigdata`

## مرحله 2: ایجاد فایل‌های کد Python

تمام کدهای Python در طول conversation نوشته شدند. شما باید آنها را کپی کنید:

### فایل‌هایی که باید ایجاد شوند:

1. **database.py** - کدش در conversation است
2. **utils/config.py** - کدش در conversation است  
3. **utils/logger.py** - کدش در conversation است
4. **models/base.py** - کدش در conversation است
5. **models/file.py** - کدش در conversation است
6. **models/analysis.py** - کدش در conversation است
7. **models/task.py** - کدش در conversation است
8. **services/storage.py** - کدش در conversation است
9. **core/file_handler.py** - کدش در conversation است
10. **core/categorizer.py** - کدش در conversation است
11. **core/labeler.py** - کدش در conversation است
12. **core/validator.py** - کدش در conversation است
13. **core/deduplicator.py** - کدش در conversation است
14. **core/pattern_finder.py** - کدش در conversation است
15. **core/scraper.py** - کدش در conversation است
16. **core/blockchain_analyzer.py** - کدش در conversation است
17. **services/queue.py** - کدش در conversation است
18. **services/ai_provider.py** - کدش در conversation است
19. **workers/tasks.py** - کدش در conversation است
20. **api/dependencies.py** - کدش در conversation است
21. **api/routes/upload.py** - کدش در conversation است
22. **api/routes/analyze.py** - کدش در conversation است
23. **api/routes/scrape.py** - کدش در conversation است
24. **api/routes/blockchain.py** - کدش در conversation است
25. **api/main.py** - کدش در conversation است
26. **alembic/env.py** - کدش در conversation است
27. **scripts/init_db.py** - کدش در conversation است

و تمام فایل‌های __init__.py

## مرحله 3: ایجاد Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# یا
venv\Scripts\activate  # Windows
```

## مرحله 4: نصب Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
```

## مرحله 5: راه‌اندازی Docker Services

```bash
docker-compose up -d
```

## مرحله 6: تنظیم Environment

```bash
cp .env.example .env
# ویرایش .env با تنظیمات خود
```

## مرحله 7: راه‌اندازی Database

```bash
python scripts/init_db.py
```

## مرحله 8: اجرای برنامه

### Terminal 1 - API:
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Terminal 2 - Celery Worker:
```bash
celery -A workers.tasks worker --loglevel=info
```

## مرحله 9: تست

مرورگر را باز کنید: http://localhost:8000/docs

## نکات مهم:

1. همه کدهای Python در conversation هستند - کپی کنید
2. ساختار پوشه‌ها از قبل ساخته شده
3. فایل‌های config آماده هستند
4. فقط کدهای Python را باید اضافه کنید

## Push به GitHub:

```bash
git init
git add .
git commit -m "Initial commit: BigData Analysis Service"
git branch -M main
git remote add origin https://github.com/Aran1986/bigdata.git
git push -u origin main
```

## سوالات متداول:

**Q: چرا کدهای Python در ZIP نیستند؟**
A: بخاطر محدودیت تعداد tool calls. همه کدها در conversation هستند و شما باید کپی کنید.

**Q: آیا می‌توانم بعداً بخش‌های دیگر را اضافه کنم؟**
A: بله! معماری کاملاً ماژولار است.

**Q: چگونه به production deploy کنم؟**
A: فایل DEPLOYMENT.md را ببینید.
