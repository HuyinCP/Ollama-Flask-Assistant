"""Module for interfacing with Ollama LLM and Embedding models."""

import logging

from langchain_ollama import ChatOllama, OllamaEmbeddings

import config

logger = logging.getLogger(__name__)


def create_llm(model_id: str = None, **kwargs) -> ChatOllama:
    """Initialize ChatOllama LLM.

    Args:
        model_id: ID model Ollama (default: from config).
        **kwargs: Additional parameters override config.

    Returns:
        ChatOllama instance.
    """
    model_id = model_id or config.LLM_MODEL_ID
    params = {**config.LLM_PARAMETERS, **kwargs}

    logger.info(f"Initialize LLM: {model_id}")
    return ChatOllama(
        model=model_id,
        base_url=config.OLLAMA_HOST,
        **params,
    )


def create_embeddings(model_id: str = None) -> OllamaEmbeddings:
    """Initialize Embedding model.

    Args:
        model_id: ID embedding model (default: from config).

    Returns:
        OllamaEmbeddings instance.
    """
    model_id = model_id or config.EMBEDDING_MODEL_ID

    logger.info(f"Initialize Embedding model: {model_id}")
    return OllamaEmbeddings(
        model=model_id,
        base_url=config.OLLAMA_HOST,
    )


def change_model(new_model_id: str) -> None:
    """Change current LLM model.

    Args:
        new_model_id: New model ID.
    """
    config.LLM_MODEL_ID = new_model_id
    logger.info(f"Changed LLM model to: {new_model_id}")
