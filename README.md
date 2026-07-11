<div align="center">

# Shopee Help Center Assistant 🛍️🤖

**A local AI assistant and high-performance crawler for Shopee's Knowledge Base.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20UI-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![LangChain](https://img.shields.io/badge/LangChain-LCEL-1C3C3C)](https://python.langchain.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-000000)](https://ollama.com/)

</div>

Dự án này là một hệ thống AI Assistant nội bộ (chạy local qua Ollama) được thiết kế chuyên biệt để phân tích và hỗ trợ trả lời các câu hỏi dựa trên CSDL (Knowledge Base) của **Trung tâm trợ giúp Shopee (Shopee Help Center)**. 

Hệ thống bao gồm hai thành phần chính:
1. **Shopee Knowledge Base Crawler**: Một script cào dữ liệu siêu tốc bằng Python, sử dụng các API nội bộ ẩn của Shopee để đệ quy toàn bộ cây danh mục và tải về hàng ngàn bài viết (chuyển đổi HTML sang Markdown) chỉ trong vài chục giây.
2. **Flask AI Assistant**: Giao diện người dùng Web (được nâng cấp từ Gradio sang Flask để linh hoạt hơn) giao tiếp với mô hình ngôn ngữ lớn (LLM) thông qua LangChain và Ollama.

## 🚀 Features

- **High-Speed API Crawler**: Không sử dụng Selenium/Playwright rườm rà. Crawler giao tiếp trực tiếp với nội bộ API của Shopee (`/categories`, `/seo`) để fetch hàng loạt nội dung với tốc độ cực cao.
- **Markdown Conversion**: Toàn bộ dữ liệu thu thập được tự động format sang định dạng Markdown chuẩn, sẵn sàng để đưa vào hệ thống RAG (Retrieval-Augmented Generation).
- **Vanilla JS & Flask UI**: Giao diện chat mượt mà, tốc độ cao được tùy chỉnh bằng CSS Vanilla và JavaScript.
- **100% Local AI**: Mọi truy vấn LLM đều chạy offline tại máy của bạn nhờ **Ollama** và **LangChain**, đảm bảo quyền riêng tư tuyệt đối.

## 🛠️ Installation

1. Cài đặt Python 3.12+ và tạo môi trường ảo (Virtual Environment).
2. Kích hoạt môi trường ảo và cài đặt thư viện:
```bash
pip install -r requirements.txt
```
3. Cài đặt [Ollama](https://ollama.com/) và tải model LLM (mặc định đang dùng Qwen 2.5):
```bash
ollama run qwen2.5:7b
```

## 💻 Usage

### 1. Cập nhật dữ liệu Shopee (Crawler)
Để làm mới Knowledge Base, chạy crawler script:
```bash
python scripts/shopee_crawler.py
```
*Script sẽ tự động quét toàn bộ danh mục và lưu kết quả dưới dạng Markdown vào thư mục `data/shopee/`.*

### 2. Chạy Web Assistant
Khởi động server Flask:
```bash
python app.py
```
Mở trình duyệt và truy cập: `http://127.0.0.1:5000`

## 📁 Cấu trúc thư mục

- `app.py`: Backend Flask xử lý routing và API chat.
- `model.py` & `config.py`: Tích hợp LangChain & Ollama prompt engineering.
- `scripts/shopee_crawler.py`: Script cào dữ liệu Shopee.
- `data/shopee/`: Chứa toàn bộ dữ liệu cào được (Markdown).
- `templates/` & `static/`: HTML, CSS, JS cho giao diện frontend.

---
*Dự án hiện đang trong quá trình chuyển dịch từ một bản Tech-Demo Langchain cơ bản sang một hệ thống RAG thực tế (Real-world RAG Application).*
