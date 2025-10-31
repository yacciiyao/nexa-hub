# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:51
@Desc:
"""
from core.dialogue_service import dialog_service
from core.model_registry import model_registry
from core.reply import Reply
from infrastructure.logger import logger


class BridgeManager:
    """ 请求调度中心 """

    def __init__(self):
        self.models = model_registry

    def handle_message(self, query: str, model_name: str, session_id: str) -> Reply:
        logger.info(f"[BridgeManager] query={query[:40]}, model={model_name}, session={session_id}")

        bot = self.models.get_model(model_name)
        if not bot:
            return Reply(
                text=f"模型 {model_name} 未注册",
                model=model_name,
                session_id=session_id
            )

        # 从 Dialogue 获取上下文
        history = dialog_service.get_context(session_id)
        message = history + [{"role": "user", "content": query}]

        # 模型生成回复
        answer = bot.reply_with_context(message)

        # 将消息写入 Dialogue
        dialog_service.append_message(session_id, "user", query)
        dialog_service.append_message(session_id, "assistant", answer)

        return Reply(text=answer, model=model_name, session_id=session_id)


bridge = BridgeManager()
