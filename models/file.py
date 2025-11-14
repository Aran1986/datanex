# Location: datanex/models/file.py

from sqlalchemy import Column, String, Integer, BigInteger, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from .base import Base, TimestampMixin

class FileStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class FileType(str, enum.Enum):
    CSV = "csv"
    EXCEL = "excel"
    JSON = "json"
    XML = "xml"
    PARQUET = "parquet"
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    HTML = "html"
    SQL = "sql"
    UNKNOWN = "unknown"

class File(Base, TimestampMixin):
    __tablename__ = "files"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_type = Column(SQLEnum(FileType), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    mime_type = Column(String(100))
    storage_path = Column(String(500), nullable=False)
    
    status = Column(SQLEnum(FileStatus), default=FileStatus.UPLOADED)
    
    # Metadata extracted from file
    metadata = Column(JSON, default=dict)
    
    # Statistics
    row_count = Column(Integer)
    column_count = Column(Integer)
    
    # Processing results
    categories = Column(JSON, default=list)
    tags = Column(JSON, default=list)
    quality_score = Column(Integer)  # 0-100
    
    def __repr__(self):
        return f"<File {self.original_filename} ({self.file_type})>"