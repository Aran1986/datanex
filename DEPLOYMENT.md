# Location: datanex/DEPLOYMENT.md

# Deployment Guide

## Production Deployment

### 1. Environment Setup

Create production `.env`:
```bash
# Application
DEBUG=false

# Database (use managed PostgreSQL)
DATABASE_URL=postgresql+asyncpg://user:pass@prod-db-host:5432/bigdata

# Redis (use managed Redis)
REDIS_URL=redis://prod-redis-host:6379/0

# MinIO (use AWS S3 or managed MinIO)
MINIO_ENDPOINT=s3.amazonaws.com
MINIO_ACCESS_KEY=your_access_key
MINIO_SECRET_KEY=your_secret_key
MINIO_BUCKET=bigdata-prod
MINIO_SECURE=true

# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
INFURA_API_KEY=...
```

### 2. Docker Production Build
```bash
# Build production image
docker build -t bigdata:production -f Dockerfile.prod .

# Tag for registry
docker tag bigdata:production your-registry/bigdata:1.0.0

# Push to registry
docker push your-registry/bigdata:1.0.0
```

### 3. Deploy with Docker Compose
```bash
# Production docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

### 4. Deploy to Kubernetes
```bash
# Apply configurations
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Check status
kubectl get pods -n bigdata
```

### 5. Setup Monitoring
```bash
# Prometheus
kubectl apply -f k8s/monitoring/prometheus.yaml

# Grafana
kubectl apply -f k8s/monitoring/grafana.yaml
```

## Security Checklist

- [ ] Change all default passwords
- [ ] Enable HTTPS/TLS
- [ ] Implement JWT authentication
- [ ] Set up firewall rules
- [ ] Enable rate limiting
- [ ] Configure CORS properly
- [ ] Use secrets management (Vault, AWS Secrets Manager)
- [ ] Enable logging and monitoring
- [ ] Set up backup strategy
- [ ] Implement disaster recovery plan

## Scaling

### Horizontal Scaling
```yaml
# Scale API
kubectl scale deployment bigdata-api --replicas=5

# Scale Celery workers
kubectl scale deployment bigdata-worker --replicas=10
```

### Auto-scaling
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: bigdata-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: bigdata-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Backup Strategy

### Database Backup
```bash
# Daily backup
pg_dump -h db-host -U user bigdata > backup_$(date +%Y%m%d).sql

# Automated backup
0 2 * * * /usr/local/bin/backup-db.sh
```

### File Storage Backup
```bash
# Sync MinIO to S3
aws s3 sync s3://bigdata-files s3://bigdata-backup/$(date +%Y%m%d)/
```

## Monitoring

### Health Endpoints

- API: `http://api-host/health`
- Database: Check connection pool
- Redis: Check memory usage
- Celery: Monitor queue length

### Alerts

Set up alerts for:
- API response time > 2s
- Error rate > 1%
- Database connections > 80%
- Redis memory > 90%
- Disk usage > 85%
- Worker queue length > 1000

## Performance Optimization

1. **Database Indexing**
   - Add indexes on frequently queried columns
   - Use connection pooling

2. **Caching**
   - Cache frequently accessed data in Redis
   - Implement CDN for static assets

3. **API Optimization**
   - Enable compression
   - Implement pagination
   - Use async operations

4. **Worker Optimization**
   - Tune Celery worker count
   - Set task time limits
   - Use result backend efficiently