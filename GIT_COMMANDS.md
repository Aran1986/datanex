# دستورات Git برای Windows

## مرحله 1: راه‌اندازی اولیه

```bash
# رفتن به پوشه پروژه
cd C:\path\to\bigdata

# راه‌اندازی Git
git init

# اضافه کردن همه فایل‌ها
git add .

# اولین commit
git commit -m "Initial commit: BigData Analysis Service v1.0.0"

# تنظیم branch به main
git branch -M main

# اضافه کردن remote repository
git remote add origin https://github.com/Aran1986/bigdata.git

# Push کردن
git push -u origin main
```

## مرحله 2: آپدیت‌های بعدی

```bash
# دیدن تغییرات
git status

# اضافه کردن فایل‌های جدید/تغییر یافته
git add .

# ایجاد commit
git commit -m "توضیحات تغییرات"

# Push کردن
git push origin main
```

## دستورات مفید

```bash
# دیدن تاریخچه
git log --oneline

# دیدن branch‌ها
git branch

# ایجاد branch جدید
git checkout -b feature/new-feature

# بازگشت به main
git checkout main

# Pull کردن آخرین تغییرات
git pull origin main

# Clone کردن repository
git clone https://github.com/Aran1986/bigdata.git
```

## Gitignore

فایل `.gitignore` از قبل آماده است و از push شدن فایل‌های غیرضروری جلوگیری می‌کند:
- __pycache__
- venv/
- .env
- logs/
- *.pyc

## نکات مهم:

1. هیچ‌وقت `.env` را push نکنید (شامل API keys است)
2. قبل از هر push، `git status` را چک کنید
3. commit message‌ها را واضح و مفید بنویسید
4. برای ویژگی‌های جدید، branch جدید بسازید

## مثال workflow:

```bash
# شروع کار روی ویژگی جدید
git checkout -b feature/ai-enhancement

# تغییرات را اعمال کنید...

# اضافه و commit کردن
git add .
git commit -m "feat: add AI enhancement for better categorization"

# Push به branch جدید
git push origin feature/ai-enhancement

# بعد از review و test، merge به main
git checkout main
git merge feature/ai-enhancement
git push origin main
```

موفق باشید! 🚀
