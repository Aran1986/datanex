# Location: datanex/api/routes/analyze.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import File as FileModel
from workers.tasks import (
    analyze_file_task,
    clean_data_task,
    remove_duplicates_task
)
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter(prefix="/analyze", tags=["analyze"])

class AnalyzeRequest(BaseModel):
    file_id: str

class CleanDataRequest(BaseModel):
    file_id: str
    strategy: str = "drop"  # drop, fill, flag

class DeduplicateRequest(BaseModel):
    file_id: str
    method: str = "hybrid"  # exact, fuzzy, semantic, hybrid
    keep: str = "first"  # first, last, none

@router.post("/full")
async def analyze_full(
    request: AnalyzeRequest,
    db: AsyncSession = Depends(get_db)
):
    """آنالیز کامل فایل"""
    try:
        from sqlalchemy import select
        
        result = await db.execute(
            select(FileModel).where(FileModel.id == uuid.UUID(request.file_id))
        )
        file = result.scalar_one_or_none()
        
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        
        # شروع آنالیز
        task = analyze_file_task.delay(request.file_id)
        
        return {
            "message": "Analysis started",
            "file_id": request.file_id,
            "task_id": task.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clean")
async def clean_data(
    request: CleanDataRequest,
    db: AsyncSession = Depends(get_db)
):
    """پاکسازی داده"""
    try:
        from sqlalchemy import select
        
        result = await db.execute(
            select(FileModel).where(FileModel.id == uuid.UUID(request.file_id))
        )
        file = result.scalar_one_or_none()
        
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        
        if request.strategy not in ['drop', 'fill', 'flag']:
            raise HTTPException(status_code=400, detail="Invalid strategy")
        
        task = clean_data_task.delay(request.file_id, request.strategy)
        
        return {
            "message": "Data cleaning started",
            "file_id": request.file_id,
            "strategy": request.strategy,
            "task_id": task.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/deduplicate")
async def deduplicate_data(
    request: DeduplicateRequest,
    db: AsyncSession = Depends(get_db)
):
    """حذف تکراری‌ها"""
    try:
        from sqlalchemy import select
        
        result = await db.execute(
            select(FileModel).where(FileModel.id == uuid.UUID(request.file_id))
        )
        file = result.scalar_one_or_none()
        
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        
        if request.method not in ['exact', 'fuzzy', 'semantic', 'hybrid']:
            raise HTTPException(status_code=400, detail="Invalid method")
        
        if request.keep not in ['first', 'last', 'none']:
            raise HTTPException(status_code=400, detail="Invalid keep parameter")
        
        task = remove_duplicates_task.delay(
            request.file_id,
            request.method,
            request.keep
        )
        
        return {
            "message": "Deduplication started",
            "file_id": request.file_id,
            "method": request.method,
            "keep": request.keep,
            "task_id": task.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """دریافت وضعیت task"""
    try:
        from celery.result import AsyncResult
        
        task = AsyncResult(task_id)
        
        if task.state == 'PENDING':
            response = {
                'state': task.state,
                'status': 'Task is waiting to be executed'
            }
        elif task.state == 'PROGRESS':
            response = {
                'state': task.state,
                'current': task.info.get('step', ''),
                'progress': task.info.get('progress', 0),
                'status': task.info.get('status', '')
            }
        elif task.state == 'SUCCESS':
            response = {
                'state': task.state,
                'result': task.result
            }
        else:
            response = {
                'state': task.state,
                'status': str(task.info)
            }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))