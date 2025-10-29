# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:51
@Desc:
"""
from core.model_registry import model_registry
from infrastructure.logger import logger


class BridgeManager:
    """ 请求调度中心 """

    def __init__(self):
        self.models = model_registry

    def handle_message(self, query: str, model_type: str="openai"):
        logger.info(f"[BridgeManager] 处理请求: {query} ({model_type})")

        bot = self.models.get_model(model_type)

        return bot.reply(query)

bridge = BridgeManager()