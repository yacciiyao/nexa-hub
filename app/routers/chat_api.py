# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:50
@Desc:
"""
from fastapi import APIRouter
from pydantic import BaseModel

from core.bridge_manager import bridge

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    query: str
    model: str = "openai"

@router.post("/")
async def chat_endpoint(request: ChatRequest):
    """ 对接接口: 接收文本输入并返回模型回复 """
    reply = bridge.handle_message(request.query, model_type=request.model)
    return {"reply": reply}

