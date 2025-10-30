# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:50
@Desc:
"""
from fastapi import APIRouter
from pydantic import BaseModel

from core.bridge_manager import bridge
from core.session_manager import session_manager

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    query: str
    model: str = "openai:gpt-3.5"
    session_id: str = "default"

@router.post("/")
async def chat_endpoint(request: ChatRequest):
    """ 对接接口: 接收文本输入并返回模型回复 """
    reply = bridge.handle_message(request.query, request.model, request.session_id)
    return reply

class ClearRequest(BaseModel):
    session_id: str

@router.post("/clear")
async def clear_session(request: ClearRequest):
    session_manager.clear(request.session_id)

    return {"ok": True, "session_id": request.session_id}