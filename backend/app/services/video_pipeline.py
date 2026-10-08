class VideoPipeline:
    """第一版任务处理器：仅返回结构化脚本与任务状态，方便后续接真实模型和剪辑引擎。"""

    def __init__(self, platform: str = "douyin"):
        self.platform = platform

    def build_hook(self, topic: str) -> str:
        return f"很多人都在做{topic}，但真正能赚到钱的往往不是动作本身，而是方法和节奏。"

    def build_script(self, topic: str, audience: str, style: str, tone: str) -> str:
        script = [
            "开场钩子：" + self.build_hook(topic),
            f"第一段：讲清楚{topic}在{audience}中的真实问题，先制造认知冲突。",
            f"第二段：用{style}的结构，给出3个步骤，语言{tone}，让用户一看就懂。",
            "第三段：给出行动建议，提醒用户先做小动作，再建立系统。",
            "结尾：如果你想把这个方法落地，先用最小动作开始，不要等到一切准备完毕。",
        ]
        return "\n\n".join(script)

    def create_task_payload(self, topic: str, audience: str, style: str, tone: str, duration: int) -> dict:
        return {
            "platform": self.platform,
            "topic": topic,
            "audience": audience,
            "style": style,
            "tone": tone,
            "duration": duration,
            "headline": f"{topic}：{self.platform}爆款脚本模板",
            "script": self.build_script(topic, audience, style, tone),
            "summary": "已完成脚本结构生成，后续可接入 TTS、图像生成和自动剪辑模块。",
        }
