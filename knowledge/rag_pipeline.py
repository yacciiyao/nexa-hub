# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:53
@Desc:
"""
from typing import Optional

from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_community.chat_models import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate

from infrastructure.config_manager import conf
from infrastructure.logger import logger
from knowledge.embeddings import get_embedding
from knowledge.loader import load_documents
from knowledge.splitter import get_text_splitter
from knowledge.vector_store import vectorstore


class RagPipeline:
    """ RAG: 文档入库 + 检索增强问答"""

    def __init__(self):
        cfg = conf().get("rag", {})
        self.default_namespace = cfg.get("default_namespace", "default")
        self.available_namespaces = cfg.get("available_namespaces", [])
        self.top_k = cfg.get("top_k", 5)

    def index_file(self, file_path: str, namespace: Optional[str] = None) -> int:
        """ 索引构建 """
        ns = namespace or self.default_namespace
        docs = load_documents(file_path)
        splitter = get_text_splitter()
        chunks = splitter.split_documents(docs)
        embedding = get_embedding()

        # 载入已有库或新建
        vs = vectorstore.load(ns, embedding)
        if vs is None:
            vs = FAISS.from_documents(chunks, embedding)

        else:
            vs.add_documents(chunks)

        vectorstore.save(vs, ns)

        logger.info(f"[RAG] indexed {len(chunks)} documents into namespace {ns}")
        return len(chunks)

    def query(self, question: str, namespace: Optional[str] = None, model: Optional[str] = None,
              top_k: Optional[int] = None) -> str:
        ns = namespace or self.default_namespace
        k = top_k or self.top_k

        embedding = get_embedding()

        if self.available_namespaces and ns not in self.available_namespaces:
            return f"知识库 `{ns}` 未授权访问"

        vs = vectorstore.load(ns, embedding)
        if vs is None:
            return f"知识库 `{ns}` 不存在, 请联系管理员先上传文档"

        retriever = vs.as_retriever(search_kwargs={"k": k})

        # 可以从 ModelRegistry 动态获取模型, 这里先用 OpenAI
        llm_model = model or conf().get("default_model", "gpt-3.5-turbo")

        api_key = conf().get("openai_api_key")
        base_url = conf().get("openai_base_url")

        llm = ChatOpenAI(api_key=api_key, base_url=base_url, model=llm_model, temperature=0)

        template = (
            "你是企业内部知识助手。请基于给定【上下文】回答用户问题。"
            "若上下文不足以回答，请明确说无法回答，不要编造内容。\n\n"
            "【上下文】:\n{context}\n\n"
            "【问题】:\n{question}\n\n"
            "【要求】:\n- 用中文简洁准确作答\n- 如使用了上下文信息，请在答案末尾给出要点小结"
        )

        prompt = PromptTemplate(template=template, input_variables=["context", "question"])

        qa = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": prompt},
        )

        answer = qa.run(query=question)

        return answer


rag = RagPipeline()
