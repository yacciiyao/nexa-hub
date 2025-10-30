# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:52
@Desc:
"""
from pydantic import BaseModel, Field


class Message(BaseModel):
    query: str = Field(..., description="用户输入")
    model: str = Field(default="openai:gpt-3.5", description="模型标识")
    session_id: str = Field(default="default", description="会话ID, 用于上下文记忆")