# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:50
@Desc:
"""
from fastapi import APIRouter, Query
from pydantic import BaseModel

from core.bridge_manager import bridge
from core.dialogue_service import dialog_service
from infrastructure.logger import logger

router = APIRouter(prefix="/api/chat", tags=["Chat"])


# 数据模型定义
class NewSessionRequest(BaseModel):
    user_id: int
    session_name: str | None = None


class ChatRequest(BaseModel):
    user_id: str | int
    session_id: str | None = None
    query: str
    model: str = "openai:gpt-3.5"


class ClearRequest(BaseModel):
    user_id: str | int
    session_id: str


class RenameRequest(BaseModel):
    user_id: str | int
    session_id: str
    new_name: str


@router.post("/start")
async def start(request: NewSessionRequest):
    """ 创建新会话 """

    session_name = request.session_name or "New Chat"
    session_id = dialog_service.new_session(request.user_id, session_name)
    logger.info(f"[ChatAPI] 新会话创建 user={request.user_id}, session={session_id}, name={session_name}")

    return {
        "ok": True,
        "session_id": session_id,
        "session_name": session_name,
        "user_id": request.user_id,
        "error": None
    }


@router.post("/")
async def chat(request: ChatRequest):
    """ 标准聊天接口 """

    session_id = request.session_id or dialog_service.new_session(request.user_id, "New Chat")
    model_name = request.model or "openai:gpt-3.5"

    reply = bridge.handle_message(
        user_id=request.user_id,
        query=request.query,
        model_name=model_name,
        session_id=session_id,
    )

    return {"ok": True, "data": reply.model_dump(), "error": None}


@router.get("/history")
async def get_chat_history(user_id: int = Query(...), session_id: str = Query(...)):
    """ 获取指定用户的会话历史记录 """

    history = dialog_service.get_context(user_id=user_id, session_id=session_id)
    return {"ok": True, "data": {"user_id": user_id, "session_id": session_id, "messages": history}, "error": None}


@router.get("/sessions")
async def list_sessions(user_id: int = Query(..., description="用户ID")):
    """ 获取用户所有会话 """

    sessions = dialog_service.list_sessions(user_id=user_id)
    return {"ok": True, "data": {"user_id": user_id, "sessions": sessions}, "error": None}


@router.post("/clear")
async def clear_session(request: ClearRequest):
    dialog_service.clear_session(request.user_id, request.session_id)
    return {"ok": True, "session_id": request.session_id, "error": None}
