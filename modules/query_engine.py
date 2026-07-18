"""Module for RAG query: retrieve context from vector store → generate answer via LLM."""

import os

from typing import Any, Dict

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

from modules.llm_interface import create_llm
from modules.data_processing import get_or_create_vector_store
import config

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def _format_docs(docs) -> str:
    """Joins document chunks into a single context string."""
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


def _extract_sources(docs) -> list:
    """Extracts source information from document chunks."""
    seen = set()
    sources = []
    for doc in docs:
        source_path = doc.metadata.get("source", "unknown")
        if source_path not in seen:
            seen.add(source_path)
            # Get file name
            filename = os.path.basename(source_path)
            # Get first line as preview
            preview = doc.page_content[:150].replace("\n", " ").strip()
            sources.append({
                "file": filename,
                "path": source_path,
                "preview": preview,
            })
    return sources


def create_rag_chain(llm=None, vector_store=None) -> tuple:
    """Creates RAG chain + separate retriever.

    Returns:
        Tuple (chain, retriever) — retriever used to retrieve sources.
    """
    llm = llm or create_llm()
    vector_store = vector_store or get_or_create_vector_store()

    retriever = vector_store.as_retriever(
        search_kwargs={"k": config.SIMILARITY_TOP_K}
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", config.CONTEXTUALIZE_Q_SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", config.RAG_SYSTEM_PROMPT),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    return conversational_rag_chain, retriever


def query(chain_and_retriever: tuple, question: str, session_id: str = "default") -> Dict[str, Any]:
    """Send question to RAG chain and receive answer with sources.

    Args:
        chain_and_retriever: Tuple (conversational_rag_chain, retriever).
        question: User's question.
        session_id: Chat session ID to maintain history.

    Returns:
        Dict with keys: answer, sources.
    """
    conversational_rag_chain, retriever = chain_and_retriever

    result = conversational_rag_chain.invoke(
        {"input": question},
        config={"configurable": {"session_id": session_id}}
    )

    docs = result["context"]
    answer = result["answer"]

    # Extract sources
    sources = _extract_sources(docs)

    return {"answer": answer, "sources": sources}
