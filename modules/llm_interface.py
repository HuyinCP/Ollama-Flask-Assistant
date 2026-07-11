"""Module for interfacing with Ollama LLM and Embedding models."""

import logging

from langchain_ollama import ChatOllama, OllamaEmbeddings

import config

logger = logging.getLogger(__name__)


def create_llm(model_id: str = None, **kwargs) -> ChatOllama:
    """Khởi tạo ChatOllama LLM.

    Args:
        model_id: ID model Ollama (mặc định lấy từ config).
        **kwargs: Tham số bổ sung ghi đè config.

    Returns:
        ChatOllama instance.
    """
    model_id = model_id or config.LLM_MODEL_ID
    params = {**config.LLM_PARAMETERS, **kwargs}

    logger.info(f"Khởi tạo LLM: {model_id}")
    return ChatOllama(
        model=model_id,
        base_url=config.OLLAMA_HOST,
        **params,
    )


def create_embeddings(model_id: str = None) -> OllamaEmbeddings:
    """Khởi tạo Embedding model.

    Args:
        model_id: ID embedding model (mặc định lấy từ config).

    Returns:
        OllamaEmbeddings instance.
    """
    model_id = model_id or config.EMBEDDING_MODEL_ID

    logger.info(f"Khởi tạo Embedding model: {model_id}")
    return OllamaEmbeddings(
        model=model_id,
        base_url=config.OLLAMA_HOST,
    )


def change_model(new_model_id: str) -> None:
    """Đổi model LLM đang dùng.

    Args:
        new_model_id: ID model mới.
    """
    config.LLM_MODEL_ID = new_model_id
    logger.info(f"Đã đổi LLM model sang: {new_model_id}")
