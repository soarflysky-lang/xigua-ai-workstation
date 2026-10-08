# 部署指南

## 系统要求

### 开发环境
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### 生产环境
- CPU: 4+ cores
- RAM: 16GB+
- 存储: 500GB+ (视频存储)
- 网络: 100Mbps+
- 操作系统: Ubuntu 22.04 LTS 或 CentOS 8+

---

## 快速开始 (本地开发)

### 1. 环境准备

```bash
# 克隆项目
git clone https://github.com/yourusername/xigua-ai-enterprise.git
cd xigua-ai-enterprise

# 复制环境配置
cp .env.example .env

# 编辑 .env 文件（填入 API 密钥等）
vim .env
```

### 2. 启动开发环境

```bash
# 启动所有服务（Docker Compose）
docker-compose up -d

# 查看日志
docker-compose logs -f

# 初始化数据库
docker-compose exec backend python -m alembic upgrade head

# 创建超级管理员
docker-compose exec backend python scripts/create_admin.py
```

### 3. 访问应用

```
前端: http://localhost:3000
后端API: http://localhost:8000
API文档: http://localhost:8000/docs
Redis: localhost:6379
PostgreSQL: localhost:5432
RabbitMQ: http://localhost:15672 (guest/guest)
```

---

## Docker Compose 配置

### 基本配置 (docker-compose.yml)

```yaml
version: '3.8'

services:
  # PostgreSQL 数据库
  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: xigua_ai
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - xigua_network

  # Redis 缓存
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - xigua_network

  # RabbitMQ 消息队列
  rabbitmq:
    image: rabbitmq:3.12-management-alpine
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: guest
      RABBITMQ_DEFAULT_PASS: guest
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    networks:
      - xigua_network

  # MinIO 存储
  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio_data:/minio_data
    command: server /minio_data --console-address ":9001"
    networks:
      - xigua_network

  # 后端 API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/xigua_ai
      REDIS_URL: redis://redis:6379/0
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672/
      MINIO_URL: minio:9000
    depends_on:
      - postgres
      - redis
      - rabbitmq
      - minio
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    networks:
      - xigua_network

  # Celery Worker (AI)
  ai_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/xigua_ai
      REDIS_URL: redis://redis:6379/0
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672/
    depends_on:
      - postgres
      - redis
      - rabbitmq
    volumes:
      - ./backend:/app
    command: celery -A app.tasks worker -l info -Q ai_tasks -c 4
    networks:
      - xigua_network

  # Celery Worker (Video)
  video_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/xigua_ai
      REDIS_URL: redis://redis:6379/0
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672/
    depends_on:
      - postgres
      - redis
      - rabbitmq
      - minio
    volumes:
      - ./backend:/app
    command: celery -A app.tasks worker -l info -Q video_tasks -c 2
    networks:
      - xigua_network

  # Celery Worker (Publisher)
  publisher_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/xigua_ai
      REDIS_URL: redis://redis:6379/0
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672/
    depends_on:
      - postgres
      - redis
      - rabbitmq
    volumes:
      - ./backend:/app
    command: celery -A app.tasks worker -l info -Q publish_tasks -c 2
    networks:
      - xigua_network

  # 前端
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://localhost:8000
    depends_on:
      - backend
    networks:
      - xigua_network

volumes:
  postgres_data:
  redis_data:
  rabbitmq_data:
  minio_data:

networks:
  xigua_network:
    driver: bridge
```

---

## 生产环境部署

### 1. 服务器准备

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装基础工具
sudo apt install -y curl wget git vim htop

# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 启用 Docker 服务
sudo systemctl enable docker
sudo systemctl start docker

# 将用户添加到 docker 组
sudo usermod -aG docker $USER
```

### 2. 应用部署

```bash
# 创建部署目录
mkdir -p /opt/xigua-ai
cd /opt/xigua-ai

# 克隆项目
git clone https://github.com/yourusername/xigua-ai-enterprise.git .

# 切换到生产配置
cp .env.example .env
vim .env  # 编辑环境变量

# 使用生产配置启动
docker-compose -f docker-compose.prod.yml up -d

# 初始化数据库
docker-compose -f docker-compose.prod.yml exec backend python -m alembic upgrade head

# 检查状态
docker-compose -f docker-compose.prod.yml ps
```

### 3. Nginx 反向代理

```nginx
# /etc/nginx/sites-available/xigua-ai
upstream api_backend {
    server localhost:8000;
}

upstream frontend {
    server localhost:3000;
}

server {
    listen 80;
    server_name xigua-ai.example.com;
    
    # 重定向到 HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name xigua-ai.example.com;
    
    # SSL 证书
    ssl_certificate /etc/letsencrypt/live/xigua-ai.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/xigua-ai.example.com/privkey.pem;
    
    # 安全头
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    # API 代理
    location /api {
        proxy_pass http://api_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
    }
    
    # WebSocket 支持
    location /ws {
        proxy_pass http://api_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
    }
    
    # 前端代理
    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_buffering off;
    }
}
```

### 4. SSL 证书配置

```bash
# 使用 Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d xigua-ai.example.com

# 自动更新
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### 5. 监控和日志

```bash
# 查看日志
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f ai_worker

# 系统监控
docker stats

# 备份数据
cd /opt/xigua-ai
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U postgres xigua_ai > backup_$(date +%Y%m%d).sql

# 定时备份（crontab）
0 2 * * * cd /opt/xigua-ai && docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U postgres xigua_ai > backups/backup_$(date +\%Y\%m\%d).sql
```

---

## Kubernetes 部署 (高级)

### 1. 创建命名空间

```bash
kubectl create namespace xigua-ai
kubectl config set-context --current --namespace=xigua-ai
```

### 2. 部署 ConfigMap 和 Secret

```bash
kubectl create configmap xigua-config --from-file=.env
kubectl create secret generic xigua-secrets --from-literal=db_password=xxx
```

### 3. 部署应用

```bash
# 应用 Kubernetes 配置
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/rabbitmq.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/workers.yaml
kubectl apply -f k8s/frontend.yaml

# 查看部署状态
kubectl get pods
kubectl get services
```

---

## 常见问题

### Q: 如何重启服务？
```bash
docker-compose -f docker-compose.prod.yml restart backend
```

### Q: 如何查看数据库？
```bash
docker-compose -f docker-compose.prod.yml exec postgres psql -U postgres -d xigua_ai
```

### Q: 如何清理旧容器？
```bash
docker system prune -a
```

### Q: 如何扩展 Worker？
```bash
# 在 docker-compose.prod.yml 中增加 worker 副本
docker-compose -f docker-compose.prod.yml up -d --scale ai_worker=4
```

---

## 性能优化

### 数据库优化
```sql
-- 创建索引
CREATE INDEX idx_content_team_id ON content_scripts(team_id);
CREATE INDEX idx_videos_status ON videos(status);

-- 启用 pg_stat_statements
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
```

### Redis 优化
```bash
# 调整最大内存
redis-cli CONFIG SET maxmemory 2gb
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

### Worker 优化
```bash
# 增加 Worker 并发数
celery -A app.tasks worker -l info -Q ai_tasks -c 8
```

---

**需要帮助？** 查看完整文档或联系技术支持
