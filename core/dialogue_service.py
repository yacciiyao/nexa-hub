# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 20:12
@Desc:
"""
import time
import uuid
from typing import Dict, List, Optional

from infrastructure.logger import logger


class DialogueService:
    """ 管理多轮对话的上下文缓存 """

    def __init__(self):
        self.user_sessions: Dict[int, Dict[str, Dict]] = {}

    def _ensure_user(self, user_id):
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {}

    def ensure_session_exists(self, user_id: int, session_id: str, default_name: str = "New Chat"):
        self._ensure_user(user_id)
        if session_id not in self.user_sessions[user_id]:
            self.user_sessions[user_id][session_id] = {
                "name": default_name,
                "messages": [],
                "created_at": int(time.time())
            }

    def new_session(self, user_id: int, session_name: str = "New Chat") -> str:
        self._ensure_user(user_id)
        session_id = str(uuid.uuid4())

        self.user_sessions[user_id][session_id] = {"name": session_name, "messages": [], "created_at": int(time.time())}

        return session_id

    def list_sessions(self, user_id: int) -> List[Dict[str, str]]:
        self._ensure_user(user_id)
        sessions = self.user_sessions[user_id]

        result = [
            {
                "session_id": s_id,
                "name": s["name"],
                "created_at": s["created_at"],
            }
            for s_id, s in sessions.items()
        ]

        result.sort(key=lambda x: x["created_at"], reverse=True)

        return result

    def get_session(self, user_id: int, session_id: str) -> Optional[Dict]:
        self._ensure_user(user_id)
        return self.user_sessions[user_id][session_id]

    def get_session_name(self, user_id: int, session_id: str) -> Optional[str]:
        s = self.get_session(user_id, session_id)
        return s["name"] if s else None

    def rename_session(self, user_id: int, session_id: str, new_name: str) -> None:
        self._ensure_user(user_id)
        if session_id in self.user_sessions[user_id]:
            self.user_sessions[user_id][session_id]["name"] = new_name
            logger.info(f"[Dialogue] Cleared session {session_id} for user {user_id}")

    def clear_session(self, user_id: int, session_id: str) -> None:
        self._ensure_user(user_id)
        if session_id in self.user_sessions[user_id]:
            del self.user_sessions[user_id][session_id]
            logger.info(f"[Dialogue] Cleared session {session_id} for user {user_id}")

    def clear_sessions(self, user_id: int) -> None:
        self._ensure_user(user_id)
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]
            logger.info(f"[Dialogue] Cleared all sessions for user {user_id}")

    def append_message(self, user_id: int, session_id: str, role: str, content: str) -> None:
        self._ensure_user(user_id)
        session = self.user_sessions[user_id].get(session_id)
        if not session:
            logger.warning(f"[Dialogue] session not found user={user_id}, id={session_id}, auto-create.")
            self.ensure_session_exists(user_id, session_id)

        self.user_sessions[user_id][session_id]["messages"].append({"role": role, "content": content})

    def get_context(self, user_id: int, session_id: str) -> List[Dict[str, str]]:
        self._ensure_user(user_id)
        session = self.user_sessions[user_id].get(session_id)
        if not session:
            return []

        return session["messages"]

# 单例实例
dialog_service = DialogueService()
