"""Module for loading raw documents from the Shopee Knowledge Base."""

import os
import logging
from typing import List

from langchain_community.document_loaders import DirectoryLoader, TextLoader

import config

logger = logging.getLogger(__name__)


def load_documents(data_dir: str = None) -> List:
    """Reads all Markdown files from the data/shopee/ directory.

    Args:
        data_dir: Directory path containing .md files (default: from config).

    Returns:
        List[Document]: List of LangChain Document objects.
    """
    data_dir = data_dir or config.DATA_DIR

    if not os.path.isdir(data_dir):
        logger.error(f"Data directory does not exist: {data_dir}")
        return []

    logger.info(f"Loading documents from: {data_dir}")

    loader = DirectoryLoader(
        data_dir,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )

    documents = loader.load()
    logger.info(f"Loaded {len(documents)} documents.")
    return documents
