# Location: datanex/api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from database import init_db
from utils.logger import log
from utils.config import get_settings
from api.routes import upload, analyze, scrape, blockchain

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """راه‌اندازی و خاموش کردن اپلیکیشن"""
    # Startup
    log.info("Starting BigData Analysis Service...")
    await init_db()
    log.info("Database initialized")
    
    yield
    
    # Shutdown
    log.info("Shutting down BigData Analysis Service...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Data Analysis as a Service - Modular, Scalable, Production-Ready",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # در production باید محدود شود
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router)
app.include_router(analyze.router)
app.include_router(scrape.router)
app.include_router(blockchain.router)

@app.get("/")
async def root():
    """صفحه اصلی"""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "endpoints": {
            "upload": "/upload",
            "analyze": "/analyze",
            "scrape": "/scrape",
            "blockchain": "/blockchain",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """بررسی سلامت سرویس"""
    try:
        from database import engine
        
        # بررسی دیتابیس
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        
        return {
            "status": "healthy",
            "database": "connected",
            "service": settings.APP_NAME
        }
    except Exception as e:
        log.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )

@app.get("/stats")
async def get_stats():
    """آمار کلی سیستم"""
    try:
        from database import async_session
        from sqlalchemy import select, func
        from models import File, Analysis, Task
        
        async with async_session() as session:
            # تعداد فایل‌ها
            file_count = await session.execute(select(func.count(File.id)))
            total_files = file_count.scalar()
            
            # تعداد آنالیزها
            analysis_count = await session.execute(select(func.count(Analysis.id)))
            total_analyses = analysis_count.scalar()
            
            # تعداد taskها
            task_count = await session.execute(select(func.count(Task.id)))
            total_tasks = task_count.scalar()
        
        return {
            "total_files": total_files,
            "total_analyses": total_analyses,
            "total_tasks": total_tasks,
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION
        }
    except Exception as e:
        log.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """مدیریت خطاهای سراسری"""
    log.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An error occurred"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )