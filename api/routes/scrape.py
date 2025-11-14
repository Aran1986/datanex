# Location: datanex/api/routes/scrape.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from workers.tasks import scrape_url_task
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

router = APIRouter(prefix="/scrape", tags=["scrape"])

class ScrapeUrlRequest(BaseModel):
    url: HttpUrl
    method: str = "requests"  # requests, playwright, scrapy

class ScrapeMultipleRequest(BaseModel):
    urls: List[HttpUrl]
    method: str = "requests"
    max_concurrent: int = 5

class CrawlRequest(BaseModel):
    start_url: HttpUrl
    max_depth: int = 2
    max_pages: int = 100

@router.post("/url")
async def scrape_url(
    request: ScrapeUrlRequest,
    db: AsyncSession = Depends(get_db)
):
    """اسکرپ یک URL"""
    try:
        if request.method not in ['requests', 'playwright', 'scrapy']:
            raise HTTPException(status_code=400, detail="Invalid method")
        
        task = scrape_url_task.delay(str(request.url), request.method)
        
        return {
            "message": "Scraping started",
            "url": str(request.url),
            "method": request.method,
            "task_id": task.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/multiple")
async def scrape_multiple_urls(
    request: ScrapeMultipleRequest,
    db: AsyncSession = Depends(get_db)
):
    """اسکرپ چند URL"""
    try:
        if request.method not in ['requests', 'playwright', 'scrapy']:
            raise HTTPException(status_code=400, detail="Invalid method")
        
        if len(request.urls) > 100:
            raise HTTPException(
                status_code=400,
                detail="Maximum 100 URLs allowed per request"
            )
        
        # ایجاد task برای هر URL
        tasks = []
        for url in request.urls:
            task = scrape_url_task.delay(str(url), request.method)
            tasks.append({
                "url": str(url),
                "task_id": task.id
            })
        
        return {
            "message": f"Scraping started for {len(request.urls)} URLs",
            "tasks": tasks
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/crawl")
async def crawl_website(
    request: CrawlRequest,
    db: AsyncSession = Depends(get_db)
):
    """Crawl کامل یک وبسایت"""
    try:
        from core.scraper import scraper
        
        if request.max_depth > 5:
            raise HTTPException(status_code=400, detail="Max depth cannot exceed 5")
        
        if request.max_pages > 500:
            raise HTTPException(status_code=400, detail="Max pages cannot exceed 500")
        
        # اجرای crawl
        result = await scraper.crawl_website(
            str(request.start_url),
            request.max_depth,
            request.max_pages
        )
        
        return {
            "message": "Crawling completed",
            "start_url": str(request.start_url),
            "pages_crawled": result['pages_crawled'],
            "result": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract-tables")
async def extract_tables_from_url(
    url: HttpUrl,
    db: AsyncSession = Depends(get_db)
):
    """استخراج جداول HTML از URL"""
    try:
        from core.scraper import scraper
        import pandas as pd
        
        tables = await scraper.extract_tables(str(url))
        
        if not tables:
            return {
                "message": "No tables found",
                "url": str(url),
                "table_count": 0
            }
        
        # تبدیل به dict برای response
        tables_data = []
        for i, table in enumerate(tables):
            tables_data.append({
                "table_number": i + 1,
                "rows": len(table),
                "columns": len(table.columns),
                "data": table.to_dict('records')[:100]  # فقط 100 ردیف اول
            })
        
        return {
            "message": "Tables extracted successfully",
            "url": str(url),
            "table_count": len(tables),
            "tables": tables_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api")
async def scrape_api_endpoint(
    api_url: HttpUrl,
    db: AsyncSession = Depends(get_db)
):
    """اسکرپ از API"""
    try:
        from core.scraper import scraper
        
        result = await scraper.scrape_api(str(api_url))
        
        return {
            "message": "API data retrieved",
            "url": str(api_url),
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))