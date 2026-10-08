# 西瓜AI部署说明

## 环境要求

- Docker
- Docker Compose
- 8GB+ RAM（推荐）

## 启动方式

```bash
cp .env.example .env
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

## 常见问题

### 1）前端无法访问后端

检查配置中 API 地址是否正确，确保后端端口为 8000。

### 2）Docker 启动失败

确认 Docker 守护进程已开启，并确认端口未被占用。

### 3）任务接口返回错误

确认后端容器已正常启动，并访问 `/health` 验证状态。
