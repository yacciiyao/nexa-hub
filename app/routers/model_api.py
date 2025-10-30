# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:51
@Desc:
"""
from fastapi import APIRouter

from core.model_registry import model_registry

router = APIRouter(prefix="/api/models", tags=["model"])

@router.get("/")
async def list_models():
    return {"models": model_registry.list_models()}