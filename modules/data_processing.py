"""Module for processing documents: chunking + vector store creation."""

import os
import logging
from typing import List, Optional

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from modules.data_loader import load_documents
from modules.llm_interface import create_embeddings
import config

logger = logging.getLogger(__name__)


def split_documents(documents: List) -> List:
    """Chia nhỏ documents thành các chunks.

    Args:
        documents: Danh sách LangChain Document objects.

    Returns:
        List[Document]: Danh sách các chunks đã chia nhỏ.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " ", ""],
    )

    chunks = splitter.split_documents(documents)
    logger.info(f"Đã chia {len(documents)} tài liệu thành {len(chunks)} chunks.")
    return chunks


def create_vector_store(chunks: List, persist_dir: str = None) -> Chroma:
    """Tạo vector store từ danh sách chunks (xử lý theo batch).

    Args:
        chunks: Danh sách document chunks.
        persist_dir: Thư mục lưu vector store (mặc định lấy từ config).

    Returns:
        Chroma vector store.
    """
    persist_dir = persist_dir or config.VECTOR_STORE_DIR
    embedding_model = create_embeddings()

    batch_size = 50  # Tránh gửi quá nhiều chunks cùng lúc đến Ollama
    logger.info(f"Đang tạo vector store với {len(chunks)} chunks (batch_size={batch_size})...")

    # Tạo vector store với batch đầu tiên
    vector_store = Chroma.from_documents(
        documents=chunks[:batch_size],
        embedding=embedding_model,
        persist_directory=persist_dir,
    )

    # Thêm các batch tiếp theo
    for i in range(batch_size, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        vector_store.add_documents(batch)
        logger.info(f"  Đã xử lý {min(i + batch_size, len(chunks))}/{len(chunks)} chunks...")

    logger.info(f"Vector store đã lưu tại: {persist_dir}")
    return vector_store


def get_or_create_vector_store(persist_dir: str = None) -> Chroma:
    """Load vector store từ disk nếu đã có, nếu chưa thì build mới.

    Args:
        persist_dir: Thư mục lưu vector store.

    Returns:
        Chroma vector store.
    """
    persist_dir = persist_dir or config.VECTOR_STORE_DIR
    embedding_model = create_embeddings()

    # Nếu đã có vector store trên disk → load lại
    if os.path.isdir(persist_dir) and os.listdir(persist_dir):
        logger.info(f"Đang load vector store có sẵn từ: {persist_dir}")
        return Chroma(
            persist_directory=persist_dir,
            embedding_function=embedding_model,
        )

    # Nếu chưa có → build từ đầu
    logger.info("Chưa có vector store. Đang build mới...")
    documents = load_documents()
    chunks = split_documents(documents)
    return create_vector_store(chunks, persist_dir)
