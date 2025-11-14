# Location: datanex/models/analysis.py

from sqlalchemy import Column, String, Integer, JSON, Float, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from .base import Base, TimestampMixin

class AnalysisType(str, enum.Enum):
    CATEGORIZATION = "categorization"
    LABELING = "labeling"
    VALIDATION = "validation"
    DEDUPLICATION = "deduplication"
    PATTERN_DETECTION = "pattern_detection"
    FULL_ANALYSIS = "full_analysis"

class AnalysisStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class Analysis(Base, TimestampMixin):
    __tablename__ = "analyses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id"), nullable=False)
    analysis_type = Column(SQLEnum(AnalysisType), nullable=False)
    status = Column(SQLEnum(AnalysisStatus), default=AnalysisStatus.PENDING)
    
    # Results
    result = Column(JSON, default=dict)
    confidence_score = Column(Float)  # 0.0 - 1.0
    
    # Performance metrics
    processing_time = Column(Float)  # seconds
    rows_processed = Column(Integer)
    
    # Error handling
    error_message = Column(Text)
    
    def __repr__(self):
        return f"<Analysis {self.analysis_type} for File {self.file_id}>"

class AnalysisResult(Base, TimestampMixin):
    __tablename__ = "analysis_results"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("analyses.id"), nullable=False)
    
    # Categorization results
    categories = Column(JSON, default=list)
    
    # Labeling results
    labels = Column(JSON, default=list)
    tags = Column(JSON, default=list)
    
    # Validation results
    invalid_rows = Column(JSON, default=list)
    validation_rules = Column(JSON, default=list)
    
    # Deduplication results
    duplicate_groups = Column(JSON, default=list)
    duplicates_removed = Column(Integer, default=0)
    
    # Pattern detection results
    patterns = Column(JSON, default=list)
    correlations = Column(JSON, default=list)
    anomalies = Column(JSON, default=list)
    
    # Summary statistics
    summary = Column(JSON, default=dict)
    
    def __repr__(self):
        return f"<AnalysisResult for Analysis {self.analysis_id}>"