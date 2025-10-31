# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:53
@Desc:
"""
from pathlib import Path
from typing import Optional

from langchain_community.vectorstores import FAISS

from infrastructure.config_manager import conf
from infrastructure.logger import logger


class VectorStoreManager:
    """ 按 namespace 管理多个 FAISS 向量库 """

    def __init__(self):
        rag_cfg = conf().get("rag", {})
        self.store_dir = Path(rag_cfg.get("store_dir", "./data/vector_stores"))
        self.store_dir.mkdir(parents=True, exist_ok=True)

    def _ns_path(self, namespace: str) -> Path:
        return self.store_dir / namespace

    def save(self, vs: FAISS, namespace: str):
        ns_path = self._ns_path(namespace)
        ns_path.mkdir(parents=True, exist_ok=True)

        vs.save_local(str(ns_path))

        logger.info(f"[VectorStore] Saved {ns_path}")

    def load(self, namespace: str, embeddings) -> Optional[FAISS]:
        ns_path = self._ns_path(namespace)
        if not ns_path.exists():
            return None

        try:
            vs = FAISS.load_local(str(ns_path), embeddings=embeddings, allow_dangerous_deserialization=True)
            logger.info(f"[VectorStore] Loaded {ns_path}")
            return vs

        except Exception as e:
            logger.error(f"[VectorStore] Failed to load {ns_path}, {e}")

            return None


vectorstore = VectorStoreManager()
