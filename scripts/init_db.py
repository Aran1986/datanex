# Location: datanex/scripts/init_db.py

"""
اسکریپت راه‌اندازی اولیه دیتابیس
"""

import asyncio
from database import init_db
from utils.logger import log

async def main():
    log.info("Initializing database...")
    await init_db()
    log.info("Database initialized successfully!")

if __name__ == "__main__":
    asyncio.run(main())