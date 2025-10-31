# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:50
@Desc:
"""
import uuid

from fastapi import APIRouter, Query
from pydantic import BaseModel

from core.bridge_manager import bridge
from core.dialogue_service import dialog_service
from core.model_registry import model_registry
from core.session_manager import session_manager
from infrastructure.logger import logger

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    user_id: int
    session_id: str = "default"
    model: str = "openai:gpt-3.5"
    query: str

class NewSessionRequest(BaseModel):
    user_id: int
    session_name: str

class ClearRequest(BaseModel):
    user_id: int
    session_id: str

@router.post("/")
async def chat(request: ChatRequest):

    """ 标准聊天接口 """
    reply = bridge.handle_message(
        query=request.query,
        model_name=request.model,
        session_id=request.session_id,
        user_id=request.user_id,
    )

    return {"text": reply.text, "model": reply.model, "session_id": reply.session_id}

@router.post("/start")
async def start(request: NewSessionRequest):
    """ 创建新会话 """
    session_id = str(uuid.uuid4())
    logger.info(f"[ChatAPI] 新会话创建 user={request.user_id}, session={session_id}")

    return {"ok": True, "session_id": session_id, "user_id": request.user_id}

@router.post("/sessions")
async def list_sessions(user_id: int = Query("user_id")):
    """ 获取用户所有会话 """
    sessions = dialog_service.list_sessions(user_id=user_id)
    return {"user_id": user_id, "sessions": sessions}

@router.post("/clear")
async def clear_session(request: ClearRequest):
    session_manager.clear(request.session_id)

    return {"ok": True, "session_id": request.session_id, "error": None}