"""Configuration settings for the Shopee Help Center Assistant."""

import os

# ============================================================
# Ollama Server Settings
# ============================================================
OLLAMA_HOST = "http://localhost:11434"

# ============================================================
# Model Settings
# ============================================================
LLM_MODEL_ID = "qwen2.5:7b"
EMBEDDING_MODEL_ID = "nomic-embed-text"  # Placeholder — sẽ cấu hình sau

# LLM Parameters
LLM_PARAMETERS = {
    "temperature": 0.3,       # Thấp hơn → chính xác hơn cho RAG
    "num_predict": 512,       # Số token tối đa sinh ra
    "top_p": 0.9,
}

# ============================================================
# RAG Pipeline Settings
# ============================================================
# Data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "shopee")

# Chunking
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Retriever
SIMILARITY_TOP_K = 5

# Vector store persistence
VECTOR_STORE_DIR = os.path.join(os.path.dirname(__file__), "vector_store")

# ============================================================
# Prompt Templates
# ============================================================
RAG_PROMPT_TEMPLATE = """Bạn là trợ lý AI chuyên trả lời câu hỏi về chính sách và dịch vụ của Shopee.
Hãy trả lời dựa HOÀN TOÀN vào nội dung tài liệu được cung cấp bên dưới.
Nếu không tìm thấy thông tin trong tài liệu, hãy nói rõ rằng bạn không có thông tin về vấn đề này.
Trả lời bằng tiếng Việt, rõ ràng và có cấu trúc.

Tài liệu tham khảo:
{context}

Câu hỏi: {question}

Trả lời:"""
