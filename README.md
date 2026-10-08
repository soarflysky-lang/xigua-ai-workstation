# 西瓜AI工作台

西瓜AI 是一个面向抖音短视频爆款生产的 AI 工作台，目标是帮助转行者、商家老板和创业者在不懂剪辑、不懂运营的前提下，用 AI 自动生成高质量短视频内容，并通过知识库、脚本模板、短视频生产流水线降低内容创作门槛。

## 产品定位

- 面向客户：商家老板、转行者、创业者、内容团队
- 目标场景：爆款短视频制作、脚本生成、配音、AI剪辑、知识库辅导
- 支持平台：抖音优先，后续扩展小红书/快手/B站
- 商业模式：私有化部署 + 客户预付费 + 维护升级

## 第一版目标

- 用户输入主题/行业/目标用户
- AI 自动生成短视频脚本
- 可自动生成口播文案和推荐标题
- 生成目标视频状态、任务日志和执行记录
- 提供知识库：爆款脚本模板、选题指南、抖音算法基础知识
- 可用一键部署到服务器

## 技术架构

- 后端：FastAPI + Python
- 前端：HTML / CSS / JavaScript 轻量前端
- 任务系统：内存任务队列（第一版）
- 知识库：Markdown / JSON 文档
- 部署：Docker + Docker Compose

## 目录结构

```text
xigua-ai-workstation/
├── README.md
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── models/
│       │   └── schemas.py
│       ├── routers/
│       │   └── tasks.py
│       └── services/
│           ├── video_pipeline.py
│           └── douyin.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── knowledge_base/
│   ├── README.md
│   ├── douyin_algorithm.md
│   └── viral_title_templates.json
├── scripts/
│   └── deploy.sh
└── docs/
    └── deployment.md
```

## 快速开始

### 1）本地启动后端

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2）本地启动前端

```bash
cd frontend
python -m http.server 8080
```

然后访问：
- 后端：http://localhost:8000/docs
- 前端：http://localhost:8080

### 3）使用 Docker 启动

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

## 默认接口

- GET /health
- POST /api/tasks
- GET /api/tasks
- GET /api/tasks/{task_id}

## 业务说明

第一版不追求大而全，而是先做好“最可卖的结果”：

- 用户输入行业/主题
- 系统输出脚本、口播文案、标题
- 生成短视频任务状态和结果记录
- 面向抖音用户提供高质量内容流程

## 未来演进

后续版本可以继续扩展：

- 接入真实 AI 模型 API（豆包 / OpenAI / Qwen / DeepSeek）
- 接入 TTS 配音能力
- 自动生成静态画面或视频封面
- 结合真实抖音平台 API 发布
- 增加多团队权限和数据统计
- 增加营销/客户知识库模块

## 版权说明

本仓库用于二次开发和私有化部署，适合为客户定制 AI 自媒体工作台。建议保留品牌和版权信息，以便后续进行商用部署。

## 备注

这是一个“可演示、可部署、可继续迭代”的第一版，适合作为客户展示原型和售前演示基础。
