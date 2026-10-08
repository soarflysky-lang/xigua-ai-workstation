from pydantic import BaseModel, Field
from typing import Literal, Optional


class TaskCreateRequest(BaseModel):
    topic: str = Field(..., description="短视频主题")
    audience: str = Field(default="商家老板/普通用户", description="目标受众")
    style: str = Field(default="口播式爆款", description="视频风格")
    platform: Literal["douyin", "xiaohongshu", "kuaishou", "bilibili"] = Field(default="douyin")
    duration: int = Field(default=45, ge=15, le=180, description="视频时长（秒）")
    tone: str = Field(default="干净利落，带场景感", description="语气风格")
    industry: Optional[str] = Field(default=None, description="所属行业")


class TaskStatus(BaseModel):
    id: str
    topic: str
    status: str
    platform: str
    duration: int
    created_at: str
    summary: str
    script: str
    headline: str
