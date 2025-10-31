# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 20:12
@Desc:
"""
from typing import Dict, List


class DialogueService:
    """ 管理多轮对话的上下文缓存 """

    def __init__(self):
        self.sessions: Dict[str, List[Dict[str, str]]] = {}

    def get_context(self, session_id: str) -> List[Dict[str, str]]:
        """ 获取当前对话的上下文 """
        return self.sessions.get(session_id, [])

    def append_message(self, session_id: str, role: str, content: str):
        """ 添加消息 """
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append({"role": role, "content": content})

    def clear_session(self, session_id: str):
        """ 清空指定 session """
        if session_id not in self.sessions:
            del self.sessions[session_id]

    def list_sessions(self):
        """ 列出所有 session_id """
        return list(self.sessions.keys())


# 单例实例
dialog_service = DialogueService()
