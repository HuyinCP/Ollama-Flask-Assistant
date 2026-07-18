"""Module for processing documents: chunking + vector store creation."""

import os
from typing import List, Optional

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from modules.data_loader import load_documents
from modules.llm_interface import create_embeddings
import config


def split_documents(documents: List) -> List:
    """Splits documents into chunks.

    Args:
        documents: List of LangChain Document objects.

    Returns:
        List[Document]: List of chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " ", ""],
    )

    chunks = splitter.split_documents(documents)
    return chunks


def create_vector_store(chunks: List, persist_dir: str = None) -> Chroma:
    """Creates vector store from list of chunks (batch processing).

    Args:
        chunks: List of document chunks.
        persist_dir: Directory to save vector store (default: from config).

    Returns:
        Chroma vector store.
    """
    persist_dir = persist_dir or config.VECTOR_STORE_DIR
    embedding_model = create_embeddings()

    batch_size = 50  # Avoid sending too many chunks to Ollama at once

    # Create vector store with the first batch
    vector_store = Chroma.from_documents(
        documents=chunks[:batch_size],
        embedding=embedding_model,
        persist_directory=persist_dir,
    )

    # Add next batches
    for i in range(batch_size, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        vector_store.add_documents(batch)

    return vector_store


def get_or_create_vector_store(persist_dir: str = None) -> Chroma:
    """Load vector store from disk if exists, otherwise build new one.

    Args:
        persist_dir: Directory to save vector store.

    Returns:
        Chroma vector store.
    """
    persist_dir = persist_dir or config.VECTOR_STORE_DIR
    embedding_model = create_embeddings()

    # If vector store already exists on disk -> load it
    if os.path.isdir(persist_dir) and os.listdir(persist_dir):
        return Chroma(
            persist_directory=persist_dir,
            embedding_function=embedding_model,
        )

    # If vector store doesn't exist yet -> build new one
    documents = load_documents()
    chunks = split_documents(documents)
    return create_vector_store(chunks, persist_dir)
