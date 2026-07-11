<div align="center">

# Shopee Help Center Assistant

**A local AI assistant and high-performance crawler for Shopee's Knowledge Base.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20UI-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL-1C3C3C)](https://python.langchain.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-000000)](https://ollama.com/)

</div>

Dự án này là một hệ thống AI Assistant nội bộ (chạy local qua Ollama) được thiết kế chuyên biệt để phân tích và hỗ trợ trả lời các câu hỏi dựa trên CSDL (Knowledge Base) của **Trung tâm trợ giúp Shopee (Shopee Help Center)**.

## 📁 Cấu trúc dự án

```
Smart Assistant/
├── config.py                  # Tập trung cấu hình: model, params, prompt, paths
├── app.py                     # Flask entry point (Web UI)
├── modules/                   # Business logic (RAG pipeline)
│   ├── __init__.py            # Export public API
│   ├── data_loader.py         # Đọc Markdown từ data/shopee/
│   ├── data_processing.py     # Chunking + Vector Store (Chroma)
│   ├── llm_interface.py       # ChatOllama + OllamaEmbeddings
│   └── query_engine.py        # RAG chain (retrieve → prompt → LLM)
├── scripts/
│   └── shopee_crawler.py      # Crawler cào dữ liệu Shopee
├── data/shopee/               # 535+ file Markdown Knowledge Base
├── templates/ & static/       # Flask frontend
├── tests/                     # Pytest
└── requirements.txt
```

## 🛠️ Installation

```bash
pip install -r requirements.txt
ollama pull qwen2.5:7b
ollama pull nomic-embed-text
```