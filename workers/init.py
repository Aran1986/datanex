# Location: datanex/workers/__init__.py

from .tasks import (
    process_file_upload,
    analyze_file_task,
    scrape_url_task,
    analyze_blockchain_address_task,
    clean_data_task,
    remove_duplicates_task
)

__all__ = [
    "process_file_upload",
    "analyze_file_task",
    "scrape_url_task",
    "analyze_blockchain_address_task",
    "clean_data_task",
    "remove_duplicates_task"
]