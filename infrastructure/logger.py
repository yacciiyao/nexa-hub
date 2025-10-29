# -*- coding: utf-8 -*-
"""
@Author: yaccii
@Date: 2025-10-29 14:55
@Desc:
"""
import logging


def setup_logger(name: str = "nexa_hub", level=logging.INFO):
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s - %(message)s]', datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)

    return logger

# 全局日志实例
logger = setup_logger()