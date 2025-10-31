# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:50
@Desc:
"""
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel

from infrastructure.logger import logger
from knowledge.rag_pipeline import rag

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])


@router.post("/upload")
async def upload_and_index(file: UploadFile = File(...), namespace: str = Form(None), admin_token: str = Form(...)):
    """ 仅管理员可用, 上传文件并写入指定 namespace 的向量库 """

    from infrastructure.config_manager import conf
    admin_key = conf().get("rag").get("admin_upload_token", None)
    if admin_token != admin_key:
        return {"ok": False, "error": "权限不足"}

    ns = namespace or conf().get("rag", {}).get("default_namespace", "default")

    # 保存临时文件
    tmp_dir = Path(f"./data/uploads/{file.filename}")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_path = tmp_dir / f"{file.filename}"
    with tmp_path.open("wb") as f:
        f.write(await file.read())

    try:
        chunks = rag.index_file(str(tmp_path), namespace=ns)

        return {"ok": True, "data": {"namespace": ns, "indexed_docs": chunks}, "error": None}

    except Exception as e:
        logger.error(f"[Knowledge] index error: {e}")

        return {"ok": False, "error": str(e)}

    finally:
        try:
            tmp_path.unlink(missing_ok=True)
        except:
            pass


class KnowledgeQuery(BaseModel):
    question: str
    namespace: str | None = None
    top_k: int | None = None
    model: str | None = None


@router.post("/query")
async def query_knowledge(query: KnowledgeQuery):
    if not query.question:
        return {"ok": False, "error": "缺少 question 参数"}
    try:
        answer = rag.query(question=query.question, namespace=query.namespace, model_name=query.model,
                           top_k=query.top_k)

        return {"ok": True, "data": {"answer": answer, "namespace": query.namespace}, "error": None}

    except Exception as e:
        logger.error(f"[Knowledge] query error: {e}")
        return {"ok": False, "error": str(e)}
