# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:51
@Desc:
"""
from collections import defaultdict
from typing import List, Dict

from infrastructure.logger import logger


class SessionManager:
    """ 进程内会话记忆 """

    def __init__(self, max_turns: int = 6):
        self.sessions: Dict[str, List[Dict[str, str]]] = defaultdict(list)
        self.max_turns = max_turns

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        return self.sessions[session_id]

    def add_message(self, session_id: str, role: str, content: str) -> None:

        history = self.get_history(session_id)

        history.append({"role": role, "content": content})

        if len(history) > 2 * self.max_turns:
            self.sessions[session_id] = history[-2 * self.max_turns :]

        logger.debug(f"[Session] {session_id} <= {role}: {content[:60]}")

    def clear(self, session_id: str) -> None:
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.debug(f"[Session] {session_id} removed")


session_manager = SessionManager()
