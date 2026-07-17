"""Configuration settings for the Shopee Help Center Assistant."""

import os

# Ollama Server Settings
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

# Model Settings
LLM_MODEL_ID = "qwen2.5:7b"
EMBEDDING_MODEL_ID = "nomic-embed-text"

# LLM Parameters
LLM_PARAMETERS = {
    "temperature": 0.3,       # Temperature more high -> model more creative, less logic
    "num_predict": 512,       # Max number of tokens to generate
    "top_p": 0.9,
}

# Data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "shopee")

# Chunking
CHUNK_SIZE = 500 # How many tokens to split the text into
CHUNK_OVERLAP = 50 # How many tokens to overlap between chunks

# Retriever
SIMILARITY_TOP_K = 5 # How many chunks to retrieve

# Vector store persistence
VECTOR_STORE_DIR = os.path.join(os.path.dirname(__file__), "vector_store")

# Prompt Templates
RAG_PROMPT_TEMPLATE = """Bạn là trợ lý AI chuyên trả lời câu hỏi về chính sách và dịch vụ của Shopee.
Hãy trả lời dựa HOÀN TOÀN vào nội dung tài liệu được cung cấp bên dưới.
Nếu không tìm thấy thông tin trong tài liệu, hãy nói rõ rằng bạn không có thông tin về vấn đề này.

QUAN TRỌNG:
1. Trả lời bằng tiếng Việt, rõ ràng và chia thành các bước (nếu có).
2. GIỮ NGUYÊN các đường dẫn (hyperlink) và tên các nút bấm, mục menu chính xác như trong tài liệu (ví dụ: "vào mục Tôi > chọn thẻ Chờ giao hàng"). KHÔNG tự ý tóm tắt làm mất các bước thao tác cụ thể này.

Tài liệu tham khảo:
{context}

Câu hỏi: {question}

Trả lời:"""
