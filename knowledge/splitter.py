# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-30 12:22
@Desc:
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter

from infrastructure.config_manager import conf


def get_text_splitter():
    cfg = conf().get("rag", {})

    chunk_size = cfg.get("chunk_size", 800)
    chunk_overlap = cfg.get("chunk_overlap", 150)

    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n", "\n\n", ".", "。", "!", "?", "！", "，"]
    )