from fastapi import APIRouter
from uuid import uuid4
from datetime import datetime

from app.models.schemas import TaskCreateRequest

router = APIRouter(prefix="/tasks", tags=["tasks"])

TASK_STORE = {}


@router.get("")
def list_tasks():
    return {"tasks": list(TASK_STORE.values())}


@router.post("")
def create_task(payload: TaskCreateRequest):
    task_id = uuid4().hex[:8]
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    task = {
        "id": task_id,
        "topic": payload.topic,
        "audience": payload.audience,
        "style": payload.style,
        "platform": payload.platform,
        "duration": payload.duration,
        "tone": payload.tone,
        "industry": payload.industry,
        "status": "queued",
        "created_at": now,
        "summary": f"已接收主题：{payload.topic}，平台：{payload.platform}，将生成爆款短视频脚本与结构化任务。",
        "headline": f"{payload.topic}：抖音爆款脚本模板",
        "script": (
            "开场钩子：这个方法，很多人都忽略了，但它真的能改变结果。\n\n"
            "第一段：讲清楚问题和痛点，让用户立刻有代入感。\n"
            "第二段：给出具体操作步骤，结合真实场景，保持节奏。\n"
            "第三段：总结收益，给出行动呼吁，提升留存和转化。"
        ),
    }

    TASK_STORE[task_id] = task
    return task


@router.get("/{task_id}")
def get_task(task_id: str):
    task = TASK_STORE.get(task_id)
    if not task:
        return {"detail": "task not found"}
    return task
