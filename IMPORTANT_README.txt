╔══════════════════════════════════════════════════════════════╗
║              مهم - لطفاً قبل از شروع بخوانید                  ║
╚══════════════════════════════════════════════════════════════╝

این ZIP شامل ساختار کامل پروژه و فایل‌های configuration است.

⚠️ نکته مهم:
کدهای Python اصلی به دلیل محدودیت تعداد tool calls در این ZIP قرار نگرفته‌اند.

✅ آنچه در این ZIP موجود است:
- ساختار کامل پوشه‌ها
- requirements.txt
- docker-compose.yml  
- Dockerfile
- .env.example
- .gitignore
- pytest.ini
- alembic.ini
- README.md
- راهنماها و مستندات

❌ آنچه باید خودتان اضافه کنید:
تمام فایل‌های Python زیر که کدشان در conversation موجود است:

1. database.py
2. utils/config.py
3. utils/logger.py
4. utils/__init__.py
5. models/base.py
6. models/file.py
7. models/analysis.py
8. models/task.py
9. models/__init__.py
10. services/storage.py
11. services/queue.py
12. services/ai_provider.py
13. services/__init__.py
14. core/file_handler.py
15. core/categorizer.py
16. core/labeler.py
17. core/validator.py
18. core/deduplicator.py
19. core/pattern_finder.py
20. core/scraper.py
21. core/blockchain_analyzer.py
22. core/__init__.py
23. workers/tasks.py
24. workers/__init__.py
25. api/dependencies.py
26. api/main.py
27. api/__init__.py
28. api/routes/upload.py
29. api/routes/analyze.py
30. api/routes/scrape.py
31. api/routes/blockchain.py
32. alembic/env.py
33. alembic/script.py.mako
34. scripts/init_db.py
35. tests/conftest.py
36. tests/test_file_handler.py

📋 مراحل کامل:

1. Extract کردن این ZIP
2. کپی کردن تمام کدهای Python از conversation
3. قرار دادن آنها در مکان مناسب طبق STRUCTURE.txt
4. دنبال کردن SETUP_GUIDE_FA.md

🔗 لینک Repository:
https://github.com/Aran1986/bigdata

💡 توصیه:
- ابتدا SETUP_GUIDE_FA.md را بخوانید
- سپس STRUCTURE.txt را برای دیدن ساختار ببینید
- کدها را از conversation کپی کنید
- در نهایت مراحل راه‌اندازی را دنبال کنید

✨ پس از تکمیل:
همه چیز آماده است برای یک سیستم production-ready که:
- کاملاً ماژولار است
- معماری تمیز دارد
- قابل scale است
- مستند کامل دارد

موفق باشید! 🚀
