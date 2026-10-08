# 西瓜AI 企业级完整产品

一站式短视频内容生产工作台，集成AI脚本生成、配音、配图、自动剪辑、多平台发布、数据分析。

## 🎯 核心功能

### 1. 内容生成
- ✅ AI智能脚本生成（基于豆包/Qwen/GPT）
- ✅ 爆款标题建议（基于热榜分析）
- ✅ 自动口播文案
- ✅ 100+行业模板库
- ✅ 热点实时监测

### 2. 视频制作
- ✅ TTS自动配音（支持多音色）
- ✅ AI生成配图（Stable Diffusion）
- ✅ 自动字幕生成（Whisper）
- ✅ 智能剪辑（关键帧提取）
- ✅ 动态转场效果

### 3. 多平台发布
- ✅ 抖音自动发布
- ✅ 小红书同步
- ✅ 快手上传
- ✅ B站/微博支持
- ✅ 定时/批量发布

### 4. 数据分析
- ✅ 实时播放数据
- ✅ 互动率分析
- ✅ 爆款预测
- ✅ 对标分析
- ✅ ROI追踪

### 5. 团队协作
- ✅ 多用户管理
- ✅ 角色权限控制
- ✅ 团队内容库共享
- ✅ 审核流程
- ✅ 内容版本管理

### 6. 知识库
- ✅ 自媒体运营指南
- ✅ 行业最佳实践
- ✅ 案例库
- ✅ 爆款选题库
- ✅ 平台算法说明

---

## 📦 技术栈

### 后端
- **框架**: FastAPI + Python 3.11+
- **数据库**: PostgreSQL + Redis
- **消息队列**: Celery + RabbitMQ
- **存储**: MinIO / AWS S3
- **AI服务**: 
  - 大模型API (豆包/Qwen/GPT)
  - TTS服务 (Edge-TTS/阿里云)
  - 图片生成 (Stable Diffusion)
  - 视频处理 (FFmpeg)
  - 字幕识别 (Whisper)

### 前端
- **框架**: React 18 + TypeScript
- **UI库**: Ant Design 5
- **状态管理**: Zustand
- **编辑器**: Draft.js / Slate
- **图表**: ECharts
- **视频播放**: HLS.js

### 基础设施
- **容器化**: Docker + Docker Compose
- **编排**: Kubernetes Ready
- **监控**: Prometheus + Grafana
- **日志**: ELK Stack
- **CI/CD**: GitHub Actions

---

## 🏗️ 项目结构

```
xigua-ai-enterprise/
├── backend/
│   ├── app/
│   │   ├── main.py                    # 应用入口
│   │   ├── config.py                  # 配置管理
│   │   ├── models/                    # 数据模型
│   │   │   ├── user.py
│   │   │   ├── content.py
│   │   │   ├── task.py
│   │   │   └── analytics.py
│   │   ├── schemas/                   # 请求/响应模型
│   │   ├── routers/                   # API路由
│   │   │   ├── auth.py
│   │   │   ├── content.py
│   │   │   ├── tasks.py
│   │   │   ├── platforms.py
│   │   │   ├── analytics.py
│   │   │   └── knowledge.py
│   │   ├── services/                  # 业务逻辑
│   │   │   ├── ai_service.py          # AI生成
│   │   │   ├── video_processor.py     # 视频处理
│   │   │   ├── platform_service.py    # 平台发布
│   │   │   ├── hot_topics.py          # 热点监测
│   │   │   └── analytics_service.py   # 数据分析
│   │   ├── utils/                     # 工具函数
│   │   ├── middleware/                # 中间件
│   │   └── dependencies.py            # 依赖注入
│   ├── requirements.txt
│   ├── Dockerfile
│   └── alembic/                       # 数据库迁移
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── ContentGenerator.tsx
│   │   │   ├── VideoEditor.tsx
│   │   │   ├── Publishing.tsx
│   │   │   ├── Analytics.tsx
│   │   │   ├── KnowledgeBase.tsx
│   │   │   └── TeamManagement.tsx
│   │   ├── components/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── store/
│   │   ├── styles/
│   │   └── App.tsx
│   ├── package.json
│   └── Dockerfile
│
├── services/
│   ├── ai-worker/                     # AI处理服务
│   │   ├── script_generator.py
│   │   ├── title_suggester.py
│   │   └── image_generator.py
│   ├── video-worker/                  # 视频处理服务
│   │   ├── ffmpeg_processor.py
│   │   ├── tts_engine.py
│   │   └── video_merger.py
│   └── publisher-worker/              # 发布服务
│       └── platform_uploader.py
│
├── knowledge_base/
│   ├── templates/
│   │   ├── scripts/                   # 脚本模板
│   │   ├── titles/                    # 标题模板
│   │   └── industries/                # 行业指南
│   ├── guides/
│   │   ├── douyin_algorithm.md
│   │   ├── xiaohongshu_guide.md
│   │   ├── kuaishou_guide.md
│   │   └── bilibili_guide.md
│   └── cases/                         # 案例库
│
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
├── README.md
├── DEPLOYMENT.md
└── ARCHITECTURE.md
```

---

## 🚀 快速开始

### 本地开发

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/xigua-ai-enterprise.git
cd xigua-ai-enterprise

# 2. 配置环境
cp .env.example .env
# 编辑 .env 填入 API 密钥

# 3. 启动开发环境
docker-compose up -d

# 4. 初始化数据库
docker exec xigua-backend alembic upgrade head

# 5. 访问应用
# 前端: http://localhost:3000
# 后端API: http://localhost:8000
# API文档: http://localhost:8000/docs
```

### 生产部署

```bash
# 使用生产配置
docker-compose -f docker-compose.prod.yml up -d

# 自动化脚本部署
chmod +x scripts/deploy.sh
./scripts/deploy.sh prod
```

---

## 📊 核心API

### 内容生成
```bash
POST /api/v1/content/generate-script
POST /api/v1/content/generate-title
POST /api/v1/content/suggest-topics
```

### 视频处理
```bash
POST /api/v1/video/generate-tts
POST /api/v1/video/process
POST /api/v1/video/merge
```

### 平台发布
```bash
POST /api/v1/platform/publish
GET /api/v1/platform/status/{task_id}
GET /api/v1/platform/analytics/{video_id}
```

### 团队管理
```bash
POST /api/v1/team/create
POST /api/v1/team/add-member
GET /api/v1/team/members
```

---

## 🔐 安全特性

- ✅ JWT身份认证
- ✅ 角色权限控制 (RBAC)
- ✅ API速率限制
- ✅ 请求加密
- ✅ 审计日志
- ✅ 数据加密存储
- ✅ HTTPS强制
- ✅ SQL注入防护
- ✅ XSS防护
- ✅ CSRF保护

---

## 📈 扩展性

### 水平扩展
- 多实例负载均衡
- 数据库主从复制
- Redis集群
- 消息队列集群

### 功能扩展
- 插件系统支持
- 自定义工作流
- 第三方集成
- 模型切换能力

---

## 🔧 配置示例

### 豆包 API 配置
```env
DOUBAO_API_KEY=your_key_here
DOUBAO_MODEL=doubao-pro-32k
```

### TTS 配置
```env
TTS_PROVIDER=edge-tts  # edge-tts, aliyun, azure
TTS_VOICE=zh-CN-YunyangNeural
```

### 视频处理
```env
FFMPEG_PATH=/usr/bin/ffmpeg
VIDEO_OUTPUT_FORMAT=mp4
VIDEO_QUALITY=1080p
```

### 平台密钥
```env
DOUYIN_CLIENT_ID=xxx
DOUYIN_CLIENT_SECRET=xxx
XIAOHONGSHU_TOKEN=xxx
```

---

## 📝 开发指南

- [后端开发指南](./docs/BACKEND_DEV.md)
- [前端开发指南](./docs/FRONTEND_DEV.md)
- [API文档](./docs/API.md)
- [数据库设计](./docs/DATABASE.md)
- [部署指南](./DEPLOYMENT.md)
- [架构设计](./ARCHITECTURE.md)

---

## 📦 集成的开源项目

- [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) - 短视频生成引擎
- [ViralMint](https://github.com/openclaw-easy/ViralMint) - 爆款分析系统
- [FFmpeg](https://github.com/FFmpeg/FFmpeg) - 视频处理
- [Whisper](https://github.com/openai/whisper) - 字幕生成
- [Stable Diffusion](https://github.com/CompVis/stable-diffusion) - 图片生成

---

## 💼 商业部署

### 私有化部署
- 完整代码交付
- 专业部署支持
- 长期技术支持
- 源代码访问

### SaaS 托管
- 云端部署运营
- 自动备份升级
- 7x24 技术支持
- 99.9% 可用性保证

### 混合部署
- 灵活部署选择
- 数据隐私保护
- 成本优化

---

## 📄 许可证

MIT License - 适合商用部署和二次开发

---

## 🤝 支持与合作

- 企业级部署咨询
- 定制功能开发
- 行业解决方案
- 技术培训服务

---

**西瓜AI - 让普通人也能做爆款短视频**
