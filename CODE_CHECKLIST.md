# Checklist کدهای Python

این لیست تمام فایل‌هایی است که باید از conversation کپی و در پروژه قرار دهید.

## ✅ Configuration Files (آماده در ZIP)
- [x] requirements.txt
- [x] docker-compose.yml
- [x] Dockerfile
- [x] .env.example
- [x] .gitignore
- [x] pytest.ini
- [x] alembic.ini

## 📝 Python Files (باید از conversation کپی شوند)

### Database & Config
- [ ] database.py
- [ ] utils/config.py
- [ ] utils/logger.py
- [ ] utils/__init__.py

### Models
- [ ] models/base.py
- [ ] models/file.py
- [ ] models/analysis.py
- [ ] models/task.py
- [ ] models/__init__.py

### Services
- [ ] services/storage.py
- [ ] services/queue.py
- [ ] services/ai_provider.py
- [ ] services/__init__.py

### Core Modules
- [ ] core/file_handler.py (ماژول 1: دریافت فایل)
- [ ] core/categorizer.py (ماژول 2: دسته‌بندی)
- [ ] core/labeler.py (ماژول 3: لیبل‌گذاری)
- [ ] core/validator.py (ماژول 4: اعتبارسنجی)
- [ ] core/deduplicator.py (ماژول 5: حذف تکراری)
- [ ] core/pattern_finder.py (ماژول 6: الگویابی)
- [ ] core/scraper.py (اسکرپینگ)
- [ ] core/blockchain_analyzer.py (آنالیز بلاکچین)
- [ ] core/__init__.py

### Workers
- [ ] workers/tasks.py
- [ ] workers/__init__.py

### API
- [ ] api/dependencies.py
- [ ] api/main.py
- [ ] api/__init__.py
- [ ] api/routes/upload.py
- [ ] api/routes/analyze.py
- [ ] api/routes/scrape.py
- [ ] api/routes/blockchain.py

### Alembic
- [ ] alembic/env.py
- [ ] alembic/script.py.mako

### Scripts
- [ ] scripts/init_db.py
- [ ] scripts/run_migrations.sh
- [ ] scripts/start_services.sh

### Tests
- [ ] tests/__init__.py
- [ ] tests/conftest.py
- [ ] tests/test_file_handler.py

## 📍 نحوه استفاده:

1. هر فایلی که کپی کردید، تیک بزنید
2. کد را از conversation پیدا کنید (با جستجوی "Location: bigdata/...")
3. فایل را ایجاد کنید
4. کد را کپی کنید
5. ذخیره کنید

## 🎯 بعد از تکمیل:

```bash
# بررسی ساختار
tree bigdata/

# نصب dependencies
pip install -r requirements.txt

# راه‌اندازی
docker-compose up -d
python scripts/init_db.py
uvicorn api.main:app --reload
```

تمام! 🎉
