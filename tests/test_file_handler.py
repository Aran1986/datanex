# Location: datanex/tests/test_file_handler.py

import pytest
from core.file_handler import file_handler
import pandas as pd

@pytest.mark.asyncio
async def test_detect_csv():
    """تست تشخیص فایل CSV"""
    csv_data = b"name,age\nJohn,30\nJane,25"
    file_type, mime = await file_handler.detect_file_type(csv_data)
    assert file_type.value == "csv"

@pytest.mark.asyncio
async def test_load_csv():
    """تست بارگذاری CSV"""
    csv_data = b"name,age\nJohn,30\nJane,25"
    from models.file import FileType
    df = await file_handler.load_data(csv_data, FileType.CSV)
    assert len(df) == 2
    assert list(df.columns) == ['name', 'age']