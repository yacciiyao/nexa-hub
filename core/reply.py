# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:52
@Desc:
"""
from pydantic import BaseModel


class Reply(BaseModel):
    """ 标准的回复输出 """
    user_id: int
    session_id: str
    model: str
    text: str