# 🚀 راهنمای استفاده از DataNex Launcher

## 📦 فایل‌های موجود:

1. **START_DATANEX.bat** - راه‌اندازی خودکار برنامه
2. **STOP_DATANEX.bat** - خاموش کردن برنامه

---

## ✅ **پیش‌نیازها (فقط یکبار نصب کن):**

### 1️⃣ Python 3.11+
- دانلود: https://www.python.org/downloads/
- ⚠️ **مهم:** حتما "Add Python to PATH" رو تیک بزن!

### 2️⃣ Node.js 18+
- دانلود: https://nodejs.org/
- نسخه LTS رو دانلود کن

### 3️⃣ Docker Desktop
- دانلود: https://www.docker.com/products/docker-desktop/
- بعد از نصب، Docker Desktop رو باز کن و اجرا کن

---

## 🚀 **نحوه استفاده:**

### ▶️ راه‌اندازی DataNex:

```
1. کپی کن START_DATANEX.bat به: C:\Users\aran\Desktop\DataNex\

2. دابل کلیک روی START_DATANEX.bat

3. صبر کن تا برنامه بالا بیاد (10-15 ثانیه)

4. مرورگر خودکار باز میشه با http://localhost:3000
```

---

### 🎯 **چی اتفاق می‌افته؟**

فایل START_DATANEX.bat این کارها رو انجام میده:

```
1. ✅ چک می‌کنه Python نصب هست یا نه
2. ✅ چک می‌کنه Node.js نصب هست یا نه  
3. ✅ چک می‌کنه Docker اجرا شده یا نه
4. ✅ اگه virtual environment نیست، می‌سازه
5. ✅ اگه Python dependencies نصب نیست، نصب می‌کنه
6. ✅ اگه Frontend dependencies نصب نیست، نصب می‌کنه
7. ✅ Docker services رو start می‌کنه (PostgreSQL, Redis, MinIO)
8. ✅ Backend رو start می‌کنه در یک terminal جدید
9. ✅ Frontend رو start می‌کنه در یک terminal جدید
10. ✅ مرورگر رو باز می‌کنه با http://localhost:3000
```

---

### 🛑 **خاموش کردن DataNex:**

```
1. دابل کلیک روی STOP_DATANEX.bat

2. همه services خاموش میشن
```

---

## 📺 **بعد از اجرا:**

### دو تا terminal window باز میشه:

1. **DataNex Backend** - API Server
   - URL: http://localhost:8000
   - API Docs: http://localhost:8000/docs

2. **DataNex Frontend** - UI Server
   - URL: http://localhost:3000

⚠️ **این دو تا terminal رو نبند!** تا وقتی می‌خوای با DataNex کار کنی باید باز باشن.

---

## 🔧 **مشکلات احتمالی:**

### ❌ "Python is not installed"
```
راه حل:
1. نصب کن Python از: https://www.python.org/downloads/
2. حتما تیک بزن "Add Python to PATH"
3. بعد از نصب، restart کن کامپیوتر
```

### ❌ "Node.js is not installed"
```
راه حل:
1. نصب کن Node.js از: https://nodejs.org/
2. نسخه LTS رو دانلود کن
3. بعد از نصب، restart کن کامپیوتر
```

### ❌ "Docker is not installed or not running"
```
راه حل:
1. نصب کن Docker Desktop از: https://www.docker.com/products/docker-desktop/
2. باز کن Docker Desktop
3. صبر کن تا Docker start بشه (آیکونش در system tray سبز میشه)
4. دوباره دابل کلیک کن START_DATANEX.bat
```

### ❌ Port 3000 یا 8000 اشغاله
```
راه حل:
1. ببند تمام برنامه‌هایی که روی این پورت‌ها هستن
2. اجرا کن: netstat -ano | findstr :3000
3. kill کن process: taskkill /PID [شماره PID] /F
```

---

## 📝 **نکات مهم:**

✅ **اولین بار:** نصب dependencies کمی طول می‌کشه (5-10 دقیقه)

✅ **دفعات بعدی:** خیلی سریع start میشه (10-15 ثانیه)

✅ **همیشه:** Docker Desktop باید اجرا باشه قبل از START

✅ **بعد از کار:** STOP_DATANEX.bat رو اجرا کن تا همه چی خاموش بشه

---

## 🎊 **موفق باشی!**

حالا با یک دابل کلیک، DataNex آماده استفاده است! 🚀

---

## 🔗 **دستورات دستی (اگه لازم شد):**

### راه‌اندازی دستی Backend:
```cmd
cd C:\Users\aran\Desktop\DataNex
venv\Scripts\activate
uvicorn api.main:app --reload
```

### راه‌اندازی دستی Frontend:
```cmd
cd C:\Users\aran\Desktop\DataNex\frontend
npm run dev
```

### راه‌اندازی دستی Docker:
```cmd
cd C:\Users\aran\Desktop\DataNex
docker-compose up -d
```

---

**DataNex Team** 💎
