# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:51
@Desc:
"""
from core.model_registry import model_registry
from core.reply import Reply
from core.session_manager import session_manager
from infrastructure.logger import logger


class BridgeManager:
    """ 请求调度中心 """

    def __init__(self):
        self.models = model_registry

    def handle_message(self, query: str, model_key: str, session_id: str) -> Reply:
        logger.info(f"[BridgeManager] query={query[:40]}, model={model_key}, session={session_id}")

        bot = self.models.get_model(model_key)

        history = session_manager.get_history(session_id)

        # 拼接上下文
        messages = history + [{"role": "user", "content": query}]
        answer = bot.reply_with_context(messages)

        # 写入会话
        session_manager.add_message(session_id, "user", query)
        session_manager.add_message(session_id, "assistant", answer)

        return Reply(text=answer, model=model_key, session_id=session_id)

bridge = BridgeManager()