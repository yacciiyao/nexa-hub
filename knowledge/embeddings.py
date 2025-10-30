# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:53
@Desc:
"""
from typing import Any

from infrastructure.config_manager import conf
from infrastructure.logger import logger

try:
    from langchain_community.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings

    HAS_SBERT = True

except:
    HAS_SBERT = False

def get_embedding() -> Any:
    rag_cfg = conf().get("rag", {})
    provider = rag_cfg.get("embedding", {}).get("provider", "openai")
    model_name = rag_cfg.get("embedding", {}).get("model", "text-embedding-3-small")

    if provider == "openai":
        api_key = conf().get("openai_api_key")
        base_url = conf().get("openai_base_url")
        logger.info(f"[Embeddings] provider={provider} model={model_name}")
        return OpenAIEmbeddings(api_key=api_key, base_url=base_url, model=model_name)

    elif provider == "sbert":
        if not HAS_SBERT:
            raise RuntimeError(f"未安装 sentence-transformers，请安装依赖或使用其他模型。")

        logger.info(f"[Embeddings] provider={provider} model={model_name}")

    else:
        raise ValueError(f"[Embeddings] provider={provider} model={model_name}")