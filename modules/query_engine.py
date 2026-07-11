"""Module for RAG query: retrieve context from vector store → generate answer via LLM."""

import os
import logging
from typing import Any, Dict

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from modules.llm_interface import create_llm
from modules.data_processing import get_or_create_vector_store
import config

logger = logging.getLogger(__name__)


def _format_docs(docs) -> str:
    """Nối các document chunks thành 1 chuỗi context."""
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


def _extract_sources(docs) -> list:
    """Trích xuất thông tin nguồn từ các document chunks."""
    seen = set()
    sources = []
    for doc in docs:
        source_path = doc.metadata.get("source", "unknown")
        if source_path not in seen:
            seen.add(source_path)
            # Lấy tên file đẹp hơn
            filename = os.path.basename(source_path)
            # Trích dòng đầu tiên làm preview
            preview = doc.page_content[:150].replace("\n", " ").strip()
            sources.append({
                "file": filename,
                "path": source_path,
                "preview": preview,
            })
    return sources


def create_rag_chain(llm=None, vector_store=None) -> tuple:
    """Tạo RAG chain + retriever riêng biệt.

    Returns:
        Tuple (chain, retriever) — retriever dùng để lấy sources.
    """
    llm = llm or create_llm()
    vector_store = vector_store or get_or_create_vector_store()

    retriever = vector_store.as_retriever(
        search_kwargs={"k": config.SIMILARITY_TOP_K}
    )

    prompt = PromptTemplate(
        template=config.RAG_PROMPT_TEMPLATE,
        input_variables=["context", "question"],
    )

    # LCEL chain: format context → prompt → LLM → parse string
    generate_chain = prompt | llm | StrOutputParser()

    logger.info("RAG chain đã sẵn sàng.")
    return generate_chain, retriever


def query(chain_and_retriever: tuple, question: str) -> Dict[str, Any]:
    """Gửi câu hỏi đến RAG chain và nhận câu trả lời kèm sources.

    Args:
        chain_and_retriever: Tuple (generate_chain, retriever).
        question: Câu hỏi của người dùng.

    Returns:
        Dict với keys: answer, sources.
    """
    generate_chain, retriever = chain_and_retriever
    logger.info(f"Query: {question[:80]}...")

    # Bước 1: Retrieve documents
    docs = retriever.invoke(question)

    # Bước 2: Generate answer
    context = _format_docs(docs)
    answer = generate_chain.invoke({"context": context, "question": question})

    # Bước 3: Trích xuất sources
    sources = _extract_sources(docs)

    return {"answer": answer, "sources": sources}
