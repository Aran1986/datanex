# Location: datanex/API_GUIDE.md

# API Usage Guide

## Authentication

Currently, the API is open for testing. In production, implement JWT authentication.

## Upload & Analyze File

### 1. Upload File
```bash
curl -X POST "http://localhost:8000/upload/file" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/data.csv"
```

Response:
```json
{
  "file_id": "123e4567-e89b-12d3-a456-426614174000",
  "filename": "data.csv",
  "size": 1024000,
  "status": "uploaded",
  "task_id": "abc123..."
}
```

### 2. Check File Status
```bash
curl -X GET "http://localhost:8000/upload/file/{file_id}"
```

### 3. Start Full Analysis
```bash
curl -X POST "http://localhost:8000/analyze/full" \
  -H "Content-Type: application/json" \
  -d '{"file_id": "123e4567-e89b-12d3-a456-426614174000"}'
```

### 4. Check Analysis Progress
```bash
curl -X GET "http://localhost:8000/analyze/task/{task_id}"
```

## Web Scraping

### Scrape Single URL
```bash
curl -X POST "http://localhost:8000/scrape/url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "method": "requests"
  }'
```

### Scrape Multiple URLs
```bash
curl -X POST "http://localhost:8000/scrape/multiple" \
  -H "Content-Type: application/json" \
  -d '{
    "urls": ["https://example.com", "https://example2.com"],
    "method": "requests",
    "max_concurrent": 3
  }'
```

### Extract Tables
```bash
curl -X POST "http://localhost:8000/scrape/extract-tables?url=https://example.com/table.html"
```

## Blockchain Analysis

### Analyze Address
```bash
curl -X POST "http://localhost:8000/blockchain/analyze-address" \
  -H "Content-Type: application/json" \
  -d '{"address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"}'
```

### Get Transaction
```bash
curl -X POST "http://localhost:8000/blockchain/transaction" \
  -H "Content-Type: application/json" \
  -d '{"tx_hash": "0xabc123..."}'
```

### Get Gas Prices
```bash
curl -X GET "http://localhost:8000/blockchain/gas-prices"
```

## Data Cleaning

### Clean Data
```bash
curl -X POST "http://localhost:8000/analyze/clean" \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "123e4567-e89b-12d3-a456-426614174000",
    "strategy": "drop"
  }'
```

Strategies: `drop`, `fill`, `flag`

### Remove Duplicates
```bash
curl -X POST "http://localhost:8000/analyze/deduplicate" \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "123e4567-e89b-12d3-a456-426614174000",
    "method": "hybrid",
    "keep": "first"
  }'
```

Methods: `exact`, `fuzzy`, `semantic`, `hybrid`
Keep: `first`, `last`, `none`

## Python Client Example
```python
import requests

BASE_URL = "http://localhost:8000"

# Upload file
files = {'file': open('data.csv', 'rb')}
response = requests.post(f"{BASE_URL}/upload/file", files=files)
file_id = response.json()['file_id']

# Start analysis
response = requests.post(
    f"{BASE_URL}/analyze/full",
    json={"file_id": file_id}
)
task_id = response.json()['task_id']

# Check status
import time
while True:
    response = requests.get(f"{BASE_URL}/analyze/task/{task_id}")
    status = response.json()
    
    if status['state'] == 'SUCCESS':
        print("Analysis complete!")
        print(status['result'])
        break
    elif status['state'] == 'FAILURE':
        print("Analysis failed!")
        break
    
    time.sleep(5)
```