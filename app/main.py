# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:49
@Desc: 主服务入口
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.routers import chat_api, model_api, knowledge_api
from infrastructure.config_manager import config
from infrastructure.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ 生命周期管理: 启动与关闭事件 """

    # 启动阶段
    config.load()
    logger.info("Nexa-Hub 服务启动...")

    yield

    logger.info("Nexa-Hub 服务关闭...")

def create_app() -> FastAPI:
    """ 创建并初始化 Nexa-Hub 应用 """
    app = FastAPI(title="Nexa-Hub", version="1.1.0", lifespan=lifespan,)

    origins = [
        "http://localhost",
        "http://localhost:3000",
        "http://127.0.0.1:8000",
        "http://localhost:7979",
        "http://127.0.0.1:7979",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(chat_api.router)
    app.include_router(model_api.router)
    app.include_router(knowledge_api.router)

    @app.get("/")
    async def index():
        return JSONResponse({
            "service": "Nexa-Hub",
            "docs": "/docs",
            "endpoints": ["/api/chat/", "/api/chat/clear", "/api/models/"]
        })

    return app

app = create_app()