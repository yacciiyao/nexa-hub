# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:51
@Desc:
"""
from fastapi import APIRouter

from core.model_registry import get_model_registry

router = APIRouter(prefix="/api/model", tags=["model"])


@router.get("/")
async def list_models():
    registry = get_model_registry()
    models = registry.get_available_models()

    return {"ok": True, "data": {"models": models}, "error": None}
