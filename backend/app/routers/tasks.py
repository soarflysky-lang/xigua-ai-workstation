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

    hook = (
        f"很多人都在做{payload.topic}，但真正能赚到钱的不是动作本身，"
        "而是方法、节奏和用户代入感。"
    )

    script = (
        f"开场钩子：{hook}\n\n"
        f"第一段：讲清楚{payload.topic}在{payload.audience}中的真实问题，让用户立刻有代入感。\n\n"
        f"第二段：用{payload.style}的节奏，拆解3个关键步骤，语言保持{payload.tone}，让用户一看就懂。\n\n"
        "第三段：给出实际行动方案，告诉用户：先做最小动作，不要等完全准备好。\n\n"
        "结尾：如果你想真正把内容做成生意，先把结构做清楚，再用系统输出。"
    )

    task = {
        "id": task_id,
        "topic": payload.topic,
        "audience": payload.audience,
        "style": payload.style,
        "platform": payload.platform,
        "duration": payload.duration,
        "tone": payload.tone,
        "industry": payload.industry,
        "status": "generated",
        "created_at": now,
        "summary": (
            f"已完成{payload.platform}短视频脚本生成，主题为{payload.topic}，适合{payload.audience}观看。"
        ),
        "headline": f"{payload.topic}：{payload.platform}爆款脚本模板",
        "script": script,
    }

    TASK_STORE[task_id] = task
    return task


@router.get("/{task_id}")
def get_task(task_id: str):
    task = TASK_STORE.get(task_id)
    if not task:
        return {"detail": "task not found"}
    return task
