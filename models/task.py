# Location: datanex/models/task.py

from sqlalchemy import Column, String, Integer, JSON, Enum as SQLEnum, ForeignKey, Text, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from .base import Base, TimestampMixin

class TaskType(str, enum.Enum):
    FILE_UPLOAD = "file_upload"
    DATA_ANALYSIS = "data_analysis"
    WEB_SCRAPING = "web_scraping"
    BLOCKCHAIN_ANALYSIS = "blockchain_analysis"
    DATA_MIGRATION = "data_migration"

class TaskStatus(str, enum.Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Task(Base, TimestampMixin):
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_type = Column(SQLEnum(TaskType), nullable=False)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.QUEUED)
    
    # Task details
    params = Column(JSON, default=dict)
    result = Column(JSON, default=dict)
    
    # Progress tracking
    progress = Column(Float, default=0.0)  # 0.0 - 100.0
    
    # Error handling
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    
    # Celery task ID
    celery_task_id = Column(String(255))
    
    def __repr__(self):
        return f"<Task {self.task_type} ({self.status})>"