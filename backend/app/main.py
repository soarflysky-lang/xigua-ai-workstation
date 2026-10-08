from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers.tasks import router as tasks_router

app = FastAPI(
    title="西瓜AI工作台",
    version="0.1.0",
    description="AI爆款短视频生成工作台，针对抖音内容生产场景。",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_router, prefix="/api")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": settings.app_name,
        "platform": settings.default_platform,
    }


@app.get("/")
def root():
    return {
        "message": "西瓜AI工作台已启动",
        "docs": "/docs",
        "health": "/health",
    }
