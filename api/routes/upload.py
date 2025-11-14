# Location: datanex/api/routes/upload.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import File as FileModel
from models.file import FileStatus, FileType
from workers.tasks import process_file_upload
from utils.logger import log
from utils.config import get_settings
import uuid

settings = get_settings()
router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/file")
async def upload_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """آپلود فایل جدید"""
    try:
        # بررسی سایز
        file_data = await file.read()
        file_size = len(file_data)
        
        if file_size > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE} bytes"
            )
        
        # بررسی پسوند
        file_extension = file.filename.split('.')[-1].lower()
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        # ایجاد رکورد در دیتابیس
        file_id = uuid.uuid4()
        db_file = FileModel(
            id=file_id,
            filename=str(file_id),
            original_filename=file.filename,
            file_type=FileType.UNKNOWN,
            file_size=file_size,
            storage_path="",
            status=FileStatus.UPLOADED
        )
        
        db.add(db_file)
        await db.commit()
        await db.refresh(db_file)
        
        # ارسال به Celery برای پردازش
        task = process_file_upload.delay(
            str(file_id),
            file_data,
            file.filename
        )
        
        log.info(f"File uploaded: {file.filename}, ID: {file_id}")
        
        return {
            "file_id": str(file_id),
            "filename": file.filename,
            "size": file_size,
            "status": "uploaded",
            "task_id": task.id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/file/{file_id}")
async def get_file_info(
    file_id: str,
    db: AsyncSession = Depends(get_db)
):
    """دریافت اطلاعات فایل"""
    try:
        from sqlalchemy import select
        
        result = await db.execute(
            select(FileModel).where(FileModel.id == uuid.UUID(file_id))
        )
        file = result.scalar_one_or_none()
        
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        
        return {
            "file_id": str(file.id),
            "filename": file.original_filename,
            "file_type": file.file_type.value,
            "file_size": file.file_size,
            "status": file.status.value,
            "row_count": file.row_count,
            "column_count": file.column_count,
            "categories": file.categories,
            "tags": file.tags,
            "quality_score": file.quality_score,
            "created_at": file.created_at.isoformat(),
            "metadata": file.metadata
        }
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error getting file info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/files")
async def list_files(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """لیست فایل‌ها"""
    try:
        from sqlalchemy import select
        
        result = await db.execute(
            select(FileModel)
            .order_by(FileModel.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        files = result.scalars().all()
        
        return {
            "total": len(files),
            "skip": skip,
            "limit": limit,
            "files": [
                {
                    "file_id": str(f.id),
                    "filename": f.original_filename,
                    "file_type": f.file_type.value,
                    "status": f.status.value,
                    "created_at": f.created_at.isoformat()
                }
                for f in files
            ]
        }
        
    except Exception as e:
        log.error(f"Error listing files: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/file/{file_id}")
async def delete_file(
    file_id: str,
    db: AsyncSession = Depends(get_db)
):
    """حذف فایل"""
    try:
        from sqlalchemy import select, delete
        from services.storage import storage_service
        
        result = await db.execute(
            select(FileModel).where(FileModel.id == uuid.UUID(file_id))
        )
        file = result.scalar_one_or_none()
        
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        
        # حذف از storage
        if file.storage_path:
            await storage_service.delete_file(file.storage_path)
        
        # حذف از دیتابیس
        await db.execute(
            delete(FileModel).where(FileModel.id == uuid.UUID(file_id))
        )
        await db.commit()
        
        log.info(f"File deleted: {file_id}")
        
        return {"message": "File deleted successfully", "file_id": file_id}
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error deleting file: {e}")
        raise HTTPException(status_code=500, detail=str(e))