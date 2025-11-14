# Location: datanex/utils/logger.py

from loguru import logger
import sys
from pathlib import Path

def setup_logger():
    # Remove default handler
    logger.remove()
    
    # Console handler
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level="DEBUG"
    )
    
    # File handler
    log_path = Path("logs")
    log_path.mkdir(exist_ok=True)
    
    logger.add(
        log_path / "bigdata_{time:YYYY-MM-DD}.log",
        rotation="500 MB",
        retention="10 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
        level="INFO"
    )
    
    return logger

log = setup_logger()