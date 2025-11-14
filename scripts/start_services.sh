# Location: datanex/scripts/start_services.sh

#!/bin/bash

echo "Starting BigData Analysis Services..."

# Start Docker services
echo "Starting Docker containers..."
docker-compose up -d

# Wait for services
echo "Waiting for services to be ready..."
sleep 10

# Initialize database
echo "Initializing database..."
python scripts/init_db.py

# Start API
echo "Starting API server..."
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload &

# Start Celery worker
echo "Starting Celery worker..."
celery -A workers.tasks worker --loglevel=info &

echo "All services started!"
echo "API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "MinIO Console: http://localhost:9001"