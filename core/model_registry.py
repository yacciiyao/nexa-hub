# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:51
@Desc:
"""
from bots.openai_bot import OpenAIBot
from infrastructure.logger import logger


class ModelRegistry:
    """ 模型注册中心, 统一模型管理与动态加载 """

    _models = {
        "openai": OpenAIBot,
    }

    def __init__(self):
        self.instances = {}

    def get_model(self, model_name: str="openai"):
        """ 获取模型实例 """
        if model_name not in self.instances:
            if model_name not in self._models:
                raise ValueError(f"未知模型: {model_name}")

            logger.info(f"[ModelRegistry] 初始化模型: {model_name}")
            self.instances[model_name] = self._models[model_name]()

        return self.instances[model_name]

# 全局注册模型实例
model_registry = ModelRegistry()
