# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:50
@Desc:
"""
from fastapi import APIRouter
from pydantic import BaseModel

from core.bridge_manager import bridge
from core.dialogue_service import dialog_service
from core.model_registry import model_registry
from core.session_manager import session_manager

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    query: str
    model: str = "openai:gpt-3.5"
    session_id: str = "default"

@router.post("/")
async def chat(request: ChatRequest):
    """ 对接接口: 接收文本输入并返回模型回复 """
    model = model_registry.get_model(request.model)
    if not model:
        return {"ok": False, "error": f"模型 {request.model} 未注册", "data": None}

    # 获取上下文
    context = dialog_service.get_context(request.session_id)
    context.append({"role": "user", "content": request.query})

    # 调用模型回复
    reply = model.reply_with_context(context)

    # 保存对话
    dialog_service.append_message(request.session_id, "user", request.query)
    dialog_service.append_message(request.session_id, "assistant", reply)

    return {
        "ok": True,
        "data": {
            "text": reply,
            "session_id": request.session_id,
            "model": request.model
        },
        "error": None
    }

class ClearRequest(BaseModel):
    session_id: str

@router.post("/clear")
async def clear_session(request: ClearRequest):
    session_manager.clear(request.session_id)

    return {"ok": True, "session_id": request.session_id, "error": None}