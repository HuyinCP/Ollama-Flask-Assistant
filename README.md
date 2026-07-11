<div align="center">
  <a href="https://github.com/HuyinCP/Ollama-Flask-Assistant">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset=".github/images/logo-dark.svg">
      <source media="(prefers-color-scheme: light)" srcset=".github/images/logo-light.svg">
      <img alt="Shopee Help Center Assistant Logo" src=".github/images/logo-dark.svg" width="50%">
    </picture>
  </a>
</div>

<div align="center">
  <h3>A local AI assistant and high-performance crawler for Shopee's Knowledge Base.</h3>
</div>

<div align="center">
  <a href="https://www.python.org/" target="_blank"><img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" alt="Python"></a>
  <a href="https://flask.palletsprojects.com/" target="_blank"><img src="https://img.shields.io/badge/Flask-Web%20UI-000000?logo=flask&logoColor=white" alt="Flask"></a>
  <a href="https://python.langchain.com/" target="_blank"><img src="https://img.shields.io/badge/LangChain-LCEL-1C3C3C" alt="LangChain"></a>
  <a href="https://ollama.com/" target="_blank"><img src="https://img.shields.io/badge/Ollama-Local_LLM-000000" alt="Ollama"></a>
</div>

<br>

Dự án này là một hệ thống AI Assistant nội bộ (chạy local qua Ollama) được thiết kế chuyên biệt để phân tích và hỗ trợ trả lời các câu hỏi dựa trên CSDL (Knowledge Base) của **Trung tâm trợ giúp Shopee (Shopee Help Center)**.

> [!TIP]
> Bạn muốn hiểu rõ luồng hoạt động của hệ thống? Hãy xem qua **[Kiến trúc Dự án (ARCHITECTURE.md)](docs/ARCHITECTURE.md)** — tài liệu mô tả chi tiết cách Crawler và AI Assistant kết nối với nhau.

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