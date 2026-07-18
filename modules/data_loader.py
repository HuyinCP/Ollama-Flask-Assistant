"""Module for loading raw documents from the Shopee Knowledge Base."""

import os
from typing import List

from langchain_community.document_loaders import DirectoryLoader, TextLoader

import config

def load_documents(data_dir: str = None) -> List:
    """Reads all Markdown files from the data/shopee/ directory.

    Args:
        data_dir: Directory path containing .md files (default: from config).

    Returns:
        List[Document]: List of LangChain Document objects.
    """
    data_dir = data_dir or config.DATA_DIR

    if not os.path.isdir(data_dir):
        return []

    loader = DirectoryLoader(
        data_dir,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )

    documents = loader.load()
    return documents
