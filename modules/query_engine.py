"""Module for RAG query: retrieve context from vector store → generate answer via LLM."""

import logging
from typing import Any

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from modules.llm_interface import create_llm
from modules.data_processing import get_or_create_vector_store
import config

logger = logging.getLogger(__name__)


def _format_docs(docs) -> str:
    """Nối các document chunks thành 1 chuỗi context."""
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


def create_rag_chain(llm=None, vector_store=None) -> Any:
    """Tạo RAG chain: retriever → prompt → LLM → output.

    Args:
        llm: ChatOllama instance (mặc định tạo mới từ config).
        vector_store: Chroma vector store (mặc định load/tạo từ config).

    Returns:
        LangChain Runnable chain.
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

    # LCEL chain: retrieve → format → prompt → LLM → parse string
    chain = (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    logger.info("RAG chain đã sẵn sàng.")
    return chain


def query(chain, question: str) -> str:
    """Gửi câu hỏi đến RAG chain và nhận câu trả lời.

    Args:
        chain: RAG chain (tạo bởi create_rag_chain).
        question: Câu hỏi của người dùng.

    Returns:
        Câu trả lời dạng string.
    """
    logger.info(f"Query: {question[:80]}...")
    answer = chain.invoke(question)
    return answer
