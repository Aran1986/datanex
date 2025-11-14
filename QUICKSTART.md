# ⚡ DataNex - راهنمای سریع راه‌اندازی

## 📦 محتویات این ZIP:

```
DataNex/
├── 🔧 Backend/          # FastAPI, PostgreSQL, Celery
├── 🎨 Frontend/         # React, Vite, TailwindCSS
└── 📚 Documentation/    # راهنماها و مستندات
```

---

## 🚀 راه‌اندازی در 5 دقیقه

### گام 1: Extract کردن

```bash
# Extract در Desktop
cd C:\Users\aran\Desktop
unzip DataNex.zip
cd DataNex
```

---

### گام 2: راه‌اندازی Backend

```bash
# ایجاد virtual environment
python -m venv venv
venv\Scripts\activate

# نصب dependencies
pip install -r requirements.txt

# راه‌اندازی Docker services
docker-compose up -d

# راه‌اندازی database
python scripts/init_db.py

# اجرای API (Terminal 1)
uvicorn api.main:app --reload

# اجرای Celery Worker (Terminal 2)
celery -A workers.tasks worker --loglevel=info
```

✅ **Backend آماده:** http://localhost:8000
📖 **API Docs:** http://localhost:8000/docs

---

### گام 3: راه‌اندازی Frontend

```bash
# Terminal جدید
cd frontend

# نصب dependencies
npm install

# اجرای development server
npm run dev
```

✅ **Frontend آماده:** http://localhost:3000

---

## ⚠️ نکات مهم

### 1️⃣ کدهای Python باید اضافه شوند!

فایل‌های زیر خالی هستند و باید از conversation کپی شوند:

- [ ] `database.py`
- [ ] `utils/config.py`
- [ ] `utils/logger.py`
- [ ] `models/*.py` (4 فایل)
- [ ] `core/*.py` (8 فایل)
- [ ] `services/*.py` (3 فایل)
- [ ] `workers/tasks.py`
- [ ] `api/main.py`
- [ ] `api/dependencies.py`
- [ ] `api/routes/*.py` (4 فایل)

📋 **لیست کامل در:** `CODE_CHECKLIST.md`

### 2️⃣ صفحات Frontend باید اضافه شوند!

فایل‌های زیر باید از راهنما کپی شوند:

- [ ] `frontend/src/pages/FileDetail.jsx`
- [ ] `frontend/src/pages/Scraping.jsx`
- [ ] `frontend/src/pages/Blockchain.jsx`
- [ ] `frontend/src/pages/Settings.jsx`

📋 **کد کامل در:** `frontend/README.md`

---

## 🎯 ترتیب انجام کارها

```
✅ 1. Extract ZIP
✅ 2. نصب Backend dependencies
⚠️ 3. کپی کردن کدهای Python (از conversation)
✅ 4. docker-compose up -d
✅ 5. python scripts/init_db.py
✅ 6. اجرای Backend
✅ 7. نصب Frontend dependencies
⚠️ 8. کپی کردن صفحات Frontend (از راهنما)
✅ 9. اجرای Frontend
✅ 10. تست کامل
```

---

## 📝 دستورات Git

```bash
# راه‌اندازی Git
git init
git add .
git commit -m "Initial commit: DataNex Platform"

# اضافه کردن Remote
git remote add origin https://github.com/YOUR_USERNAME/DataNex.git

# Push
git push -u origin main
```

---

## 🔗 لینک‌های مفید

- 📖 **README کامل:** `README.md`
- 🔧 **راهنمای Backend:** `README_BACKEND.md`
- 📋 **چک‌لیست کدها:** `CODE_CHECKLIST.md`
- 🎨 **راهنمای Frontend:** `frontend/README.md`
- 🌍 **راهنمای فارسی:** `SETUP_GUIDE_FA.md`

---

## 🆘 مشکل داری؟

1. ✅ **Backend run نمیشه؟**
   - بررسی کن Docker services اجرا شدن: `docker-compose ps`
   - بررسی کن Python 3.11+ داری: `python --version`

2. ✅ **Frontend run نمیشه؟**
   - بررسی کن Node.js 18+ داری: `node --version`
   - پاک کن node_modules و دوباره نصب کن

3. ✅ **دیتابیس connect نمیشه؟**
   - بررسی کن PostgreSQL در Docker اجرا شده
   - بررسی کن پورت 5432 باز هست

---

## 🎉 موفق باشی!

هر سوالی داشتی، به فایل‌های راهنما مراجعه کن.

**DataNex Team** 🚀
