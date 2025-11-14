# Location: datanex/workers/tasks.py

from services.queue import celery_app
from services.storage import storage_service
from core.file_handler import file_handler
from core.categorizer import categorizer
from core.labeler import labeler
from core.validator import validator
from core.deduplicator import deduplicator
from core.pattern_finder import pattern_finder
from core.scraper import scraper
from core.blockchain_analyzer import blockchain_analyzer
from utils.logger import log
from models.file import FileStatus
from models.analysis import AnalysisStatus
from database import async_session
from sqlalchemy import select, update
from models import File, Analysis, Task as TaskModel
import asyncio
from typing import Dict, Any
import uuid

@celery_app.task(bind=True)
def process_file_upload(self, file_id: str, file_data: bytes, filename: str):
    """پردازش فایل آپلود شده"""
    try:
        return asyncio.run(_process_file_upload_async(self, file_id, file_data, filename))
    except Exception as e:
        log.error(f"Error processing file upload: {e}")
        return {'status': 'failed', 'error': str(e)}

async def _process_file_upload_async(task, file_id: str, file_data: bytes, filename: str):
    """پردازش async فایل"""
    try:
        # تشخیص نوع فایل
        file_type, mime_type = await file_handler.detect_file_type(file_data)
        
        # استخراج metadata
        metadata = await file_handler.extract_metadata(file_data, file_type)
        
        # بارگذاری به storage
        storage_path = await storage_service.upload_file(file_data, filename, mime_type)
        
        # آپدیت در دیتابیس
        async with async_session() as session:
            result = await session.execute(
                select(File).where(File.id == uuid.UUID(file_id))
            )
            file_record = result.scalar_one_or_none()
            
            if file_record:
                file_record.file_type = file_type
                file_record.mime_type = mime_type
                file_record.storage_path = storage_path
                file_record.metadata = metadata
                file_record.status = FileStatus.PROCESSING
                
                if 'row_count' in metadata:
                    file_record.row_count = metadata['row_count']
                if 'column_count' in metadata:
                    file_record.column_count = metadata['column_count']
                
                await session.commit()
        
        # آغاز آنالیز
        analyze_file_task.delay(file_id)
        
        log.info(f"File {file_id} processed successfully")
        return {'status': 'success', 'file_id': file_id, 'storage_path': storage_path}
        
    except Exception as e:
        log.error(f"Error in file processing: {e}")
        
        # آپدیت وضعیت به failed
        async with async_session() as session:
            await session.execute(
                update(File)
                .where(File.id == uuid.UUID(file_id))
                .values(status=FileStatus.FAILED)
            )
            await session.commit()
        
        raise

@celery_app.task(bind=True)
def analyze_file_task(self, file_id: str):
    """آنالیز کامل فایل"""
    try:
        return asyncio.run(_analyze_file_async(self, file_id))
    except Exception as e:
        log.error(f"Error analyzing file: {e}")
        return {'status': 'failed', 'error': str(e)}

async def _analyze_file_async(task, file_id: str):
    """آنالیز async فایل"""
    try:
        # دریافت فایل از دیتابیس
        async with async_session() as session:
            result = await session.execute(
                select(File).where(File.id == uuid.UUID(file_id))
            )
            file_record = result.scalar_one_or_none()
            
            if not file_record:
                raise ValueError(f"File {file_id} not found")
            
            # دانلود از storage
            file_data = await storage_service.download_file(file_record.storage_path)
            
            # بارگذاری به DataFrame
            df = await file_handler.load_data(file_data, file_record.file_type)
            
            # 1. دسته‌بندی
            task.update_state(state='PROGRESS', meta={'step': 'categorization', 'progress': 20})
            categories = await categorizer.categorize_columns(df)
            semantic_categories = await categorizer.categorize_data_semantic(df)
            domains = await categorizer.categorize_by_domain(df)
            
            # 2. لیبل‌گذاری
            task.update_state(state='PROGRESS', meta={'step': 'labeling', 'progress': 40})
            labels = await labeler.auto_label_columns(df)
            tags = await labeler.generate_tags(df)
            
            # 3. اعتبارسنجی
            task.update_state(state='PROGRESS', meta={'step': 'validation', 'progress': 60})
            validation_result = await validator.validate_data(df)
            
            # 4. تشخیص تکراری
            task.update_state(state='PROGRESS', meta={'step': 'deduplication', 'progress': 75})
            duplicate_result = await deduplicator.find_duplicates(df, method='hybrid')
            
            # 5. یافتن الگوها
            task.update_state(state='PROGRESS', meta={'step': 'pattern_detection', 'progress': 90})
            patterns = await pattern_finder.find_patterns(df)
            
            # آپدیت فایل
            file_record.status = FileStatus.COMPLETED
            file_record.categories = list(categories.values())
            file_record.tags = tags
            file_record.quality_score = int(validation_result['summary']['quality_score'] * 100)
            
            # ذخیره نتایج آنالیز
            analysis_result = {
                'categorization': {
                    'column_categories': categories,
                    'semantic_categories': semantic_categories,
                    'domains': domains
                },
                'labeling': {
                    'column_labels': labels,
                    'dataset_tags': tags
                },
                'validation': validation_result,
                'deduplication': duplicate_result,
                'patterns': patterns
            }
            
            await session.commit()
        
        task.update_state(state='PROGRESS', meta={'step': 'completed', 'progress': 100})
        
        log.info(f"Analysis completed for file {file_id}")
        return {
            'status': 'success',
            'file_id': file_id,
            'result': analysis_result
        }
        
    except Exception as e:
        log.error(f"Error in file analysis: {e}")
        
        async with async_session() as session:
            await session.execute(
                update(File)
                .where(File.id == uuid.UUID(file_id))
                .values(status=FileStatus.FAILED)
            )
            await session.commit()
        
        raise

@celery_app.task(bind=True)
def scrape_url_task(self, url: str, method: str = 'requests'):
    """اسکرپ URL"""
    try:
        return asyncio.run(_scrape_url_async(self, url, method))
    except Exception as e:
        log.error(f"Error scraping URL: {e}")
        return {'status': 'failed', 'error': str(e)}

async def _scrape_url_async(task, url: str, method: str):
    """اسکرپ async URL"""
    try:
        task.update_state(state='PROGRESS', meta={'step': 'scraping', 'url': url})
        
        result = await scraper.scrape_url(url, method)
        
        log.info(f"Successfully scraped {url}")
        return {'status': 'success', 'url': url, 'data': result}
        
    except Exception as e:
        log.error(f"Error scraping {url}: {e}")
        raise

@celery_app.task(bind=True)
def analyze_blockchain_address_task(self, address: str):
    """آنالیز آدرس blockchain"""
    try:
        return asyncio.run(_analyze_blockchain_address_async(self, address))
    except Exception as e:
        log.error(f"Error analyzing blockchain address: {e}")
        return {'status': 'failed', 'error': str(e)}

async def _analyze_blockchain_address_async(task, address: str):
    """آنالیز async آدرس blockchain"""
    try:
        task.update_state(state='PROGRESS', meta={'step': 'analyzing_address', 'address': address})
        
        # آنالیز آدرس
        address_info = await blockchain_analyzer.analyze_address(address)
        
        # آنالیز تراکنش‌ها
        task.update_state(state='PROGRESS', meta={'step': 'analyzing_transactions'})
        transactions = await blockchain_analyzer.analyze_transactions(address, limit=50)
        
        result = {
            'address_info': address_info,
            'transactions': transactions
        }
        
        log.info(f"Successfully analyzed blockchain address {address}")
        return {'status': 'success', 'address': address, 'data': result}
        
    except Exception as e:
        log.error(f"Error analyzing blockchain address {address}: {e}")
        raise

@celery_app.task(bind=True)
def clean_data_task(self, file_id: str, strategy: str = 'drop'):
    """پاکسازی داده"""
    try:
        return asyncio.run(_clean_data_async(self, file_id, strategy))
    except Exception as e:
        log.error(f"Error cleaning data: {e}")
        return {'status': 'failed', 'error': str(e)}

async def _clean_data_async(task, file_id: str, strategy: str):
    """پاکسازی async داده"""
    try:
        # دریافت فایل
        async with async_session() as session:
            result = await session.execute(
                select(File).where(File.id == uuid.UUID(file_id))
            )
            file_record = result.scalar_one_or_none()
            
            if not file_record:
                raise ValueError(f"File {file_id} not found")
            
            # دانلود و بارگذاری
            file_data = await storage_service.download_file(file_record.storage_path)
            df = await file_handler.load_data(file_data, file_record.file_type)
            
            # اعتبارسنجی
            task.update_state(state='PROGRESS', meta={'step': 'validating'})
            validation_result = await validator.validate_data(df)
            
            # پاکسازی
            task.update_state(state='PROGRESS', meta={'step': 'cleaning'})
            cleaned_df = await validator.clean_data(df, validation_result, strategy)
            
            # ذخیره فایل تمیز شده
            # تبدیل به CSV
            import io
            csv_buffer = io.BytesIO()
            cleaned_df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            
            cleaned_filename = f"cleaned_{file_record.original_filename}"
            storage_path = await storage_service.upload_file(
                csv_data,
                cleaned_filename,
                'text/csv'
            )
            
            # ایجاد رکورد جدید
            new_file = File(
                filename=cleaned_filename,
                original_filename=cleaned_filename,
                file_type=file_record.file_type,
                file_size=len(csv_data),
                mime_type='text/csv',
                storage_path=storage_path,
                status=FileStatus.COMPLETED,
                row_count=len(cleaned_df),
                column_count=len(cleaned_df.columns)
            )
            
            session.add(new_file)
            await session.commit()
            
            new_file_id = str(new_file.id)
        
        log.info(f"Successfully cleaned file {file_id}, new file: {new_file_id}")
        return {
            'status': 'success',
            'original_file_id': file_id,
            'cleaned_file_id': new_file_id,
            'removed_rows': len(df) - len(cleaned_df)
        }
        
    except Exception as e:
        log.error(f"Error cleaning data: {e}")
        raise

@celery_app.task(bind=True)
def remove_duplicates_task(self, file_id: str, method: str = 'hybrid', keep: str = 'first'):
    """حذف تکراری‌ها"""
    try:
        return asyncio.run(_remove_duplicates_async(self, file_id, method, keep))
    except Exception as e:
        log.error(f"Error removing duplicates: {e}")
        return {'status': 'failed', 'error': str(e)}

async def _remove_duplicates_async(task, file_id: str, method: str, keep: str):
    """حذف async تکراری‌ها"""
    try:
        async with async_session() as session:
            result = await session.execute(
                select(File).where(File.id == uuid.UUID(file_id))
            )
            file_record = result.scalar_one_or_none()
            
            if not file_record:
                raise ValueError(f"File {file_id} not found")
            
            # دانلود و بارگذاری
            file_data = await storage_service.download_file(file_record.storage_path)
            df = await file_handler.load_data(file_data, file_record.file_type)
            
            # یافتن تکراری‌ها
            task.update_state(state='PROGRESS', meta={'step': 'finding_duplicates'})
            duplicate_result = await deduplicator.find_duplicates(df, method=method)
            
            # حذف تکراری‌ها
            task.update_state(state='PROGRESS', meta={'step': 'removing_duplicates'})
            cleaned_df = await deduplicator.remove_duplicates(df, duplicate_result, keep=keep)
            
            # ذخیره
            import io
            csv_buffer = io.BytesIO()
            cleaned_df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            
            deduped_filename = f"deduped_{file_record.original_filename}"
            storage_path = await storage_service.upload_file(
                csv_data,
                deduped_filename,
                'text/csv'
            )
            
            new_file = File(
                filename=deduped_filename,
                original_filename=deduped_filename,
                file_type=file_record.file_type,
                file_size=len(csv_data),
                mime_type='text/csv',
                storage_path=storage_path,
                status=FileStatus.COMPLETED,
                row_count=len(cleaned_df),
                column_count=len(cleaned_df.columns)
            )
            
            session.add(new_file)
            await session.commit()
            
            new_file_id = str(new_file.id)
        
        log.info(f"Successfully removed duplicates from {file_id}, new file: {new_file_id}")
        return {
            'status': 'success',
            'original_file_id': file_id,
            'deduped_file_id': new_file_id,
            'duplicates_removed': len(df) - len(cleaned_df),
            'duplicate_groups': len(duplicate_result['duplicate_groups'])
        }
        
    except Exception as e:
        log.error(f"Error removing duplicates: {e}")
        raise