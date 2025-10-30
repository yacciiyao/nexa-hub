# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:51
@Desc:
"""
from typing import Dict, Callable

from bots.openai_bot import OpenAIBot
from infrastructure.logger import logger


class ModelRegistry:
    """ 模型注册中心 """

    def __init__(self):
        self._factories: Dict[str, Callable[[], object]] = {}
        self._instances: Dict[str, object] = {}
        self._bootstrap_default()

    def _bootstrap_default(self):
        self.register("openai:gpt-3.5", lambda: OpenAIBot(model_name="gpt-3.5-turbo"))
        self.register("openai:gpt-4o-mini", lambda: OpenAIBot(model_name="gpt-4o-mini"))

    def register(self, name: str, factory: Callable[[], object]) -> None:
        logger.info(f"[ModelRegister] 注册模型: {name}")
        self._factories[name] = factory

    def get_model(self, name: str):
        if name not in self._instances:
            if name not in self._factories:
                raise ValueError(f"未知模型: {name}")

            logger.info(f"[ModelRegister] 初始化模型: {name}")

            self._instances[name] = self._factories[name]()

        return self._instances[name]

    def list_models(self):
        return list(self._factories.keys())

model_registry = ModelRegistry()