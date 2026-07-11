"""Module for loading raw documents from the Shopee Knowledge Base."""

import os
import logging
from typing import List

from langchain_community.document_loaders import DirectoryLoader, TextLoader

import config

logger = logging.getLogger(__name__)


def load_documents(data_dir: str = None) -> List:
    """Đọc toàn bộ file Markdown từ thư mục data/shopee/.

    Args:
        data_dir: Đường dẫn thư mục chứa file .md (mặc định lấy từ config).

    Returns:
        List[Document]: Danh sách LangChain Document objects.
    """
    data_dir = data_dir or config.DATA_DIR

    if not os.path.isdir(data_dir):
        logger.error(f"Thư mục dữ liệu không tồn tại: {data_dir}")
        return []

    logger.info(f"Đang load tài liệu từ: {data_dir}")

    loader = DirectoryLoader(
        data_dir,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )

    documents = loader.load()
    logger.info(f"Đã load {len(documents)} tài liệu.")
    return documents
