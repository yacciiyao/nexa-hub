# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:52
@Desc: OpenAI 聊天接口
"""
from openai import OpenAI

from infrastructure.config_manager import conf
from infrastructure.logger import logger


class OpenAIBot:
    def __init__(self):
        api_key = conf().get('openai_api_key')
        base_url = conf().get('openai_base_url')
        if not api_key:
            raise Exception('OpenAI API key not found.')

        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def reply(self, query: str, context=None):
        """ 核心对话方法 """
        logger.info(f"[OpenAIBot] 接收到消息: {query}")
        try:
            response = self.client.chat.completions.create(
                model=conf().get('openai_model', "gpt-3.5-turbo"),
                messages=[{"role": "user", "content": query}],
            )

            content = response.choices[0].message.content
            logger.info(f"[OpenAIBot] 回复: {content}")
            return content

        except Exception as e:
            logger.error(f"[OpenAIBot] 调用失败: {e}")
            return f"调用模型出错: {e}"

