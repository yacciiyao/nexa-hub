# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:50
@Desc:
"""
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel

from infrastructure.config_manager import conf
from infrastructure.logger import logger
from knowledge.rag_pipeline import rag

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])

@router.post("/upload")
async def upload_and_index(file: UploadFile = File(...), namespace: str = Form(None)):
    """ 上传文件并写入指定 namespace 的向量库 """
    ns = namespace or conf().get("rag", {}).get("default_namespace", "default")

    # 保存临时文件
    tmp_dir = Path("./data/uploads")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_path = tmp_dir / f"{file.filename}"
    with tmp_path.open("wb") as f:
        f.write(await file.read())

    try:
        chunks = rag.index_file(str(tmp_path), namespace=ns)

        return {"ok": True, "namespace": ns, "chunks": chunks, "filename": file.filename}

    except Exception as e:
        logger.error(f"[Knowledge] index error: {e}")

        return {"ok": False, "error": str(e)}

    finally:
        pass

class KnowledgeQuery(BaseModel):
    question: str
    namespace: str | None = None
    top_k : int | None = None
    model: str | None = None

@router.post("/query")
async def query_knowledge(query: KnowledgeQuery):
    answer = rag.query(question=query.question, namespace=query.namespace, model_name=query.model, top_k=query.top_k)

    return {"answer": answer, "namespace": query.namespace or conf().get("rag", {}).get("default_namespace", "default")}