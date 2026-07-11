"""
Shopee Help Center Assistant — modules package.

Pipeline:
    data_loader → data_processing → (vector store) → query_engine → LLM response
                                                           ↑
                              llm_interface ───────────────┘

Modules:
- data_loader:      Đọc file Markdown từ data/shopee/
- data_processing:  Chunking + tạo/load Vector Store
- llm_interface:    Khởi tạo ChatOllama + Embedding model
- query_engine:     Tạo RAG chain (retriever + prompt + LLM)
"""

from modules.data_loader import load_documents
from modules.data_processing import split_documents, create_vector_store, get_or_create_vector_store
from modules.llm_interface import create_llm, create_embeddings, change_model
from modules.query_engine import create_rag_chain, query
