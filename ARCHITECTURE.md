# 架构设计文档

## 系统架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                      客户端 (Web/Mobile)                       │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTPS
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   API Gateway (Nginx)                         │
│              Rate Limiting / Load Balancing                   │
└────────────────────┬────────────────────────────────────────┘
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
┌──────────────┬──────────────┬──────────────┐
│ FastAPI 1    │ FastAPI 2    │ FastAPI N    │
│   (8001)     │   (8002)     │  (800N)      │
└──────────────┴──────────────┴──────────────┘
      │              │              │
      └──────────────┼──────────────┘
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
┌──────────────┬──────────────┬──────────────┐
│ PostgreSQL   │    Redis     │    MinIO     │
│  (Primary)   │   (Cache)    │   (Storage)  │
└──────────────┴──────────────┴──────────────┘
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
┌──────────────┬──────────────┬──────────────┐
│ Celery Worker│ Celery Worker│ Celery Worker│
│ (AI Service) │ (Video Proc) │ (Publishing) │
└──────────────┴──────────────┴──────────────┘
      │              │              │
      └──────────────┼──────────────┘
                     │
      ┌──────────────┼──────────────────────────────┐
      ▼              ▼                              ▼
┌──────────────┬──────────────┐         ┌──────────────────┐
│ RabbitMQ     │ Redis Queue  │         │  外部服务         │
│  (Message)   │  (Fast Task) │         │ - 豆包API        │
└──────────────┴──────────────┘         │ - 抖音API        │
                                        │ - TTS服务        │
                                        │ - 图片生成        │
                                        └──────────────────┘
```

## 数据流

### 脚本生成流程
```
用户输入
  ▼
[前端] 选择行业/主题/风格
  │
  ├─ 调用 API /content/generate-script
  │
  ▼
[后端] 请求检查 + 参数验证
  │
  ├─ 创建 Task
  │
  ├─ 发送到 Celery 队列
  │
  ▼
[AI Worker] 处理任务
  │
  ├─ 查询热榜数据
  │
  ├─ 调用豆包/Qwen API
  │
  ├─ 生成脚本 + 标题 + 建议
  │
  ├─ 保存到数据库
  │
  └─ 更新 Redis 缓存
  
  ▼
[前端] 实时推送更新
  │
  └─ 显示生成结果
```

### 视频处理流程
```
脚本确认
  ▼
[前端] 点击"生成视频"
  │
  ├─ 选择配音 / 速度 / 效果
  │
  ▼
[后端] 创建视频任务
  │
  ├─ 发送到 Video Worker
  │
  ▼
[Video Worker] 并行处理
  │
  ├─ TTS 配音生成 ──────┐
  ├─ 图片生成处理 ───┬──┤
  ├─ 字幕生成 ────┬──┤
  │               │  │
  └────────────────────┘
  │
  ▼
[FFmpeg] 视频合成
  │
  ├─ 音视频混流
  ├─ 添加字幕
  ├─ 添加效果/转场
  ├─ 导出 MP4
  │
  ▼
[MinIO] 存储视频
  │
  ▼
[前端] 显示预览 + 下载
```

### 发布流程
```
视频确认
  ▼
[前端] 选择平台 + 时间
  │
  ├─ 抖音 / 小红书 / 快手 / B站
  │
  ▼
[后端] 创建发布任务
  │
  ├─ 格式转换（适配各平台）
  ├─ 上传到各平台
  ├─ 获取视频ID
  │
  ▼
[Publisher Worker] 执行发布
  │
  ├─ 调用平台 API
  ├─ 处理上传队列
  ├─ 记录发布状态
  │
  ▼
[数据库] 保存发布信息
  │
  ├─ 视频URL
  ├─ 发布时间
  ├─ 平台标识
  │
  ▼
[前端] 显示发布结果
  │
  └─ 提供平台链接
```

## 服务拆分

### 1. API 服务 (FastAPI)
**职责**: 处理 HTTP 请求，业务逻辑，数据验证

**包含模块**:
- 认证授权
- 内容管理
- 任务调度
- 平台管理
- 分析统计

### 2. AI Worker (Celery)
**职责**: 处理 AI 相关的异步任务

**任务类型**:
- 脚本生成
- 标题建议
- 热点分析
- 图片生成

### 3. Video Worker (Celery)
**职责**: 处理视频处理相关任务

**任务类型**:
- TTS 生成
- 视频剪辑
- 字幕合成
- 格式转换

### 4. Publisher Worker (Celery)
**职责**: 处理多平台发布

**任务类型**:
- 抖音上传
- 小红书发布
- 快手上传
- B站投稿
- 定时发布

## 数据库设计

### 核心表结构

**users** - 用户表
```sql
- id (UUID)
- email (UNIQUE)
- username
- password_hash
- role (ADMIN/TEAM_LEAD/MEMBER)
- status (ACTIVE/INACTIVE)
- created_at
- updated_at
```

**teams** - 团队表
```sql
- id (UUID)
- name
- owner_id (FK users)
- description
- settings (JSONB)
- created_at
```

**content_scripts** - 内容表
```sql
- id (UUID)
- team_id (FK teams)
- creator_id (FK users)
- topic
- industry
- style
- script_content (TEXT)
- headlines (JSONB)
- status (DRAFT/PUBLISHED)
- created_at
- updated_at
```

**videos** - 视频表
```sql
- id (UUID)
- script_id (FK content_scripts)
- team_id (FK teams)
- video_url
- thumbnail_url
- duration
- status (PROCESSING/READY/PUBLISHED)
- metadata (JSONB)
- created_at
```

**published_videos** - 发布记录
```sql
- id (UUID)
- video_id (FK videos)
- platform (DOUYIN/XIAOHONGSHU/KUAISHOU/BILIBILI)
- platform_video_id
- publish_time
- status (SCHEDULED/PUBLISHED/FAILED)
- metrics (JSONB - 播放数/评论数等)
- created_at
```

**analytics** - 分析数据
```sql
- id (UUID)
- video_id (FK videos)
- platform
- date
- views
- likes
- comments
- shares
- completion_rate
- updated_at
```

## 缓存策略

### Redis 缓存

**1. 会话缓存**
```
key: session:{user_id}:{token}
value: { user_id, permissions, timestamp }
ttl: 24 hours
```

**2. 热点数据缓存**
```
key: hot_topics:{platform}:{date}
value: [{ topic, popularity, trend }, ...]
ttl: 6 hours
```

**3. 模板缓存**
```
key: templates:{industry}:{type}
value: [{ id, name, content }, ...]
ttl: 24 hours
```

**4. 任务队列**
```
key: task_queue:{worker_type}
value: task_id (使用 RabbitMQ 主要处理)
```

**5. 分析数据缓存**
```
key: analytics:{video_id}
value: { views, likes, comments, ... }
ttl: 1 hour (自动刷新)
```

## 消息队列设计

### RabbitMQ 队列

**1. AI 处理队列**
```
queue: ai_tasks
worker: AI Worker
priority: HIGH
exchange: task.ai
```

**2. 视频处理队列**
```
queue: video_tasks
worker: Video Worker
priority: MEDIUM
exchange: task.video
```

**3. 发布队列**
```
queue: publish_tasks
worker: Publisher Worker
priority: MEDIUM
exchange: task.publish
```

**4. 通知队列**
```
queue: notifications
worker: Notification Service
priority: LOW
exchange: notifications
```

## 认证授权

### JWT 令牌
```
Header: {
  "alg": "HS256",
  "typ": "JWT"
}

Payload: {
  "sub": "user_id",
  "team_id": "team_id",
  "role": "MEMBER",
  "permissions": ["read:content", "write:content"],
  "iat": 1234567890,
  "exp": 1234571490
}
```

### 权限模型
```
ROLES:
- ADMIN: 系统管理
- TEAM_LEAD: 团队管理
- MEMBER: 普通成员

PERMISSIONS:
- read:content
- write:content
- publish:content
- manage:team
- view:analytics
- manage:settings
```

## 监控告警

### Prometheus 指标

**1. API 性能**
```
http_request_duration_seconds (histogram)
http_request_total (counter)
http_request_errors_total (counter)
```

**2. 任务处理**
```
celery_task_duration_seconds (histogram)
celery_task_total (counter)
celery_task_failure_total (counter)
celery_task_queue_length (gauge)
```

**3. 数据库**
```
db_connection_pool_size (gauge)
db_query_duration_seconds (histogram)
db_query_errors_total (counter)
```

**4. 系统资源**
```
process_cpu_seconds_total (counter)
process_resident_memory_bytes (gauge)
container_memory_usage_bytes (gauge)
```

### 告警规则
- API 错误率 > 1%
- 任务处理耗时 > 30s
- 数据库连接数 > 80%
- 磁盘使用率 > 85%

## 部署拓扑

### 单机部署
```
Single Server
├── Docker
│   ├── FastAPI
│   ├── PostgreSQL
│   ├── Redis
│   ├── RabbitMQ
│   └── Celery Workers (多个)
```

### 多机部署
```
Load Balancer (Nginx)
├── API Server 1 (FastAPI)
├── API Server 2 (FastAPI)
├── API Server 3 (FastAPI)
├── Database Cluster (PostgreSQL)
├── Cache Cluster (Redis)
├── Message Queue (RabbitMQ)
├── Worker Pool 1 (AI)
├── Worker Pool 2 (Video)
└── Worker Pool 3 (Publisher)
```

### Kubernetes 部署
```
K8s Cluster
├── Ingress (Nginx)
├── FastAPI Deployment (3 replicas)
├── Celery Deployment (多个 Worker)
├── PostgreSQL StatefulSet
├── Redis StatefulSet
├── RabbitMQ StatefulSet
├── Persistent Volume (MinIO)
└── Monitoring (Prometheus/Grafana)
```

## 安全考虑

### 网络安全
- TLS/SSL 加密传输
- VPC 隔离
- WAF 防护
- DDoS 防护

### 数据安全
- 数据库加密
- 敏感信息加密存储
- 备份加密
- 定期备份恢复演练

### 应用安全
- SQL 注入防护
- XSS 防护
- CSRF 防护
- 速率限制
- API 认证

## 性能优化

### 缓存策略
- 多层缓存 (CDN/Redis/应用)
- 缓存预热
- 缓存失效管理

### 数据库优化
- 索引优化
- 查询优化
- 分区表
- 主从复制

### 队列优化
- 任务优先级
- 批量处理
- 异步处理

### 代码优化
- 连接池
- 对象池
- 内存管理
- 垃圾回收调优
