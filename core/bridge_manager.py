# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:51
@Desc: 模型桥接与对话调度
"""
from core.dialogue_service import dialog_service
from core.model_registry import get_model_registry
from core.reply import Reply
from infrastructure.logger import logger


class BridgeManager:
    """ 请求调度中心 """

    def __init__(self):
        self.models = get_model_registry()
        print(self.models)
    def handle_message(self, query: str, model_name: str, session_id: str, user_id: int) -> Reply:

        logger.info(f"[BridgeManager] query={query[:40]}, model={model_name}, session={session_id}")

        dialog_service.ensure_session_exists(user_id, session_id)

        bot = self.models.get_model(model_name)
        if not bot:
            raise ValueError(f"模型不存在 {model_name}")

        # 从 Dialogue 获取上下文
        history = dialog_service.get_context(user_id=user_id, session_id=session_id)
        is_first = len(history) == 0
        message = history + [{"role": "user", "content": query}]

        # 模型生成回复
        answer = bot.reply_with_context(message)

        # 将消息写入 Dialogue
        dialog_service.append_message(user_id=user_id, session_id=session_id, role="user", content=query)
        dialog_service.append_message(user_id=user_id, session_id=session_id, role="assistant", content=answer)

        if is_first:
            try:
                title_prompt = f"请用10个字以内总结以下对话主题（不要带问号和标点）：{query}"
                title = bot.reply(title_prompt).strip()
                if title:
                    dialog_service.rename_session(user_id=user_id, session_id=session_id, new_name=title)

            except:
                logger.warning(f"[Bridge] 自动命名失败")

        return Reply(text=answer, model=model_name, user_id=user_id, session_id=session_id)


bridge = BridgeManager()
