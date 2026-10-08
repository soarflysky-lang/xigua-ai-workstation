# 西瓜AI工作台

西瓜AI 是一个面向抖音短视频爆款生产的 AI 工作台，帮助普通人、商家老板、创业者和转行者，在不懂剪辑、不懂运营、不懂脚本创作的前提下，快速生成爆款短视频内容。

它不是单个 AI 工具，而是一个完整的内容生产系统：
- 选题
- 标题
- 脚本
- 口播文案
- 知识库能力
- 任务执行记录
- 可私有化部署的工作台

## 1. 产品定位

### 目标用户
- 商家老板：希望用短视频提升门店/品牌曝光
- 转行者：想通过抖音做副业赚钱
- 创业者：需要快速搭建内容生产闭环
- 内容团队：想要标准化脚本与知识库

### 目标场景
- 抖音短视频爆款脚本生成
- 商业知识拆解视频
- 口播型短视频生成
- 知识库 + 标题模板 + 选题库
- 私有化部署，给客户独立工作台

### 营销定位

西瓜AI 不是卖“AI工具”，而是卖“自动化内容生产能力”。
客户不需要懂剪辑、不需要懂运营、不需要会写稿，只要输入行业和主题，系统就能输出脚本和任务结构，帮助客户更快做视频。

---

## 2. 产品卖点

### 核心卖点
1. 零基础也能做短视频
2. 抖音优先，适合普通人和商家
3. 知识库驱动内容生产
4. 可私有化部署，适合客户预付费+交付
5. 适合做成“工作台 + 销售工具 + 课程内容”三位一体

### 商业模式建议
- 一次性交付：客户先付费，您部署独立实例
- 技术支持：维护、优化、升级
- 知识库升级：按行业增加模板
- 私域流量：做客户内容运营服务

---

## 3. 第一版 MVP 功能

### 已实现
- 后端 API：创建任务、查询任务状态
- 工作台前端：输入主题并生成脚本内容
- 知识库：抖音算法、头标题模板
- Docker 部署脚本

### 计划增强
- 真正接入 AI 大模型 API（豆包 / DeepSeek / OpenAI / Qwen）
- TTS 配音生成
- 视频封面与动态字幕
- 自动剪辑与导出短视频
- 多平台发布
- 用户角色与权限管理

---

## 4. 技术架构

- 后端：FastAPI + Python
- 前端：原生 HTML/CSS/JS，适合快速演示
- 知识库：Markdown / JSON
- 部署：Docker + Docker Compose
- 目标：让产品快速落地、便于二次开发和客户演示

---

## 5. 目录结构

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
│   ├── viral_title_templates.json
│   └── hot_topics.md
├── scripts/
│   └── deploy.sh
├── docs/
│   ├── deployment.md
│   └── sales_pitch.md
└── data/
    └── example_tasks.json
```

---

## 6. 快速开始

### 本地启动后端

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 本地启动前端

```bash
cd frontend
python -m http.server 8080
```

访问：
- 后端文档：http://localhost:8000/docs
- 前端页面：http://localhost:8080

### Docker 启动

```bash
cp .env.example .env
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

---

## 7. 默认接口

- GET /health
- POST /api/tasks
- GET /api/tasks
- GET /api/tasks/{task_id}

---

## 8. 业务说明

第一版先追求“可卖和可演示”，而不是一上来就做全套自媒体管理系统。
核心目标是：
- 用户只需要输入主题
- 系统给出脚本结构、标题和任务状态
- 形成“AI内容生产工作台”的基本雏形

这种形式非常适合以下场景：
- 给客户演示
- 作为私有化部署样机
- 作为自媒体培训和交付内容模板

---

## 9. 未来迭代路线

### v1.1：增强体验
- 接入真实大模型
- 任务列表页
- 历史任务归档
- 更清晰的脚本结构输出

### v1.2：抖音闭环
- TTS 配音
- 自动封面图
- 字幕生成
- 批量脚本生成

### v1.3：商业化交付
- 用户角色与CRM
- 客户独立部署
- 高级模板市场
- 私域运营知识库

---

## 10. 售前话术示例

> 西瓜AI 不是一个简单的聊天工具，而是一个面向短视频创作者的 AI 工作台。它能帮助商家和转行者在不懂剪辑、不懂运营的情况下，快速生成有价值的短视频脚本与内容结构，降低内容创业门槛。
>
> 我们的目标不是卖一个功能，而是卖一套“从零到一做爆款视频”的内容生产能力。

---

## 11. 版权与使用说明

本仓库适合二次开发、客户演示、私有化部署和商业交付使用。
建议保留品牌信息，并按客户需要进行定制化开发。

---

## 12. 结论

西瓜AI 可以作为“AI 自媒体工作台”的第一版样机，适合继续迭代成：
- 客户端工作台
- 知识库 + 培训产品
- 私有化部署交付
- 课程/服务/工具三位一体的卖点

这是一个值得继续做，并且很适合商业化推进的方向。
