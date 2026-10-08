class DouyinOptimizer:
    """抖音业务优化建议，第一版用于知识库和提示词增强。"""

    def __init__(self):
        self.algorithm_rules = [
            "开头 3 秒必须抓住注意力，强烈钩子比信息量更重要。",
            "视频内容最好围绕单一问题展开，不要一开始堆叠太多概念。",
            "结尾留行动呼吁，提升关注、评论和转化。",
            "搭配真实场景、痛点和收益，增强代入感。",
            "适当使用停顿、字幕和情绪表达提升停留时长。",
        ]

    def generate_prompt(self, topic: str, audience: str) -> str:
        return (
            f"请基于主题【{topic}】为【{audience}】生成一段抖音爆款短视频脚本，"
            "要求：开头强钩子、节奏清晰、解决痛点、用简单语言、留行动呼吁。"
        )
