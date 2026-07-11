# Kiến trúc Dự án: Shopee Help Center Assistant

Tài liệu này giải thích cấu trúc và luồng dữ liệu (Data Flow) của dự án, giúp các developer mới dễ dàng hiểu cách hệ thống hoạt động và cách bảo trì/phát triển thêm tính năng.

## 1. Tổng quan (Overview)

Dự án là một ứng dụng **RAG (Retrieval-Augmented Generation)** chạy hoàn toàn local, được thiết kế để hỏi đáp về các chính sách, quy định của Shopee.
Hệ thống kết hợp **Flask** làm Backend/UI, **LangChain** để xây dựng RAG pipeline, và **Ollama** để chạy các Local LLMs.

### 1.1 Sơ đồ luồng hoạt động (Architecture Diagram)

```mermaid
graph TD
    subgraph Dữ liệu (Offline)
        A[scripts/shopee_crawler.py] -->|Cào dữ liệu Shopee API| B[(data/shopee/*.md)]
    end

    subgraph RAG Pipeline (modules/)
        B -->|load_documents| C[modules/data_loader.py]
        C -->|split_documents| D[modules/data_processing.py]
        D -->|embed_documents| E[(Chroma Vector DB)]
        
        U[User Question] --> F[modules/query_engine.py]
        E -->|retriever| F
        F -->|Prompt Context + Question| G[modules/llm_interface.py]
        G -->|ChatOllama qwen2.5:7b| F
    end

    subgraph Web UI
        F -->|JSON Response + Sources| H[app.py / Flask API]
        H <--> I[templates/index.html & static/script.js]
    end
```

---

## 2. Giải thích cấu trúc thư mục (Directory Structure)

Kiến trúc mã nguồn áp dụng **Modules Pattern** (lấy cảm hứng từ khóa học Icebreaker của IBM/Coursera) để tách biệt rõ ràng từng khâu của RAG.

| File / Folder | Chức năng (Purpose) |
|---|---|
| **`config.py`** | Nơi duy nhất chứa TẤT CẢ cấu hình: Model parameters, System Prompts, Chunk Size, Paths. Thay vì sửa code rải rác, dev chỉ cần sửa file này. |
| **`app.py`** | Entry point của Flask. Chứa các HTTP Endpoints (VD: `/api/chat`) để giao tiếp với client. Nó gọi trực tiếp vào `query_engine.py`. |
| **`modules/`** | Core RAG business logic. Được chia nhỏ để dễ test và thay thế (VD: nếu muốn đổi Chroma sang FAISS, chỉ cần sửa đúng 1 file). |
| `modules/data_loader.py` | Hàm load hàng loạt file `.md` thành các object `Document` của Langchain. |
| `modules/data_processing.py`| Nhận Document thô, thực hiện Text Chunking (chia nhỏ) và nhúng vào `Chroma Vector Store` thông qua batching để tối ưu hiệu suất. |
| `modules/llm_interface.py`  | Giao tiếp với Ollama. Khởi tạo Chat LLM và Embedding Model. Mọi thay đổi về provider (VD: đổi từ Ollama sang OpenAI) sẽ làm ở đây. |
| `modules/query_engine.py`   | Trái tim của ứng dụng: Dùng `LCEL` (LangChain Expression Language) để nối Retriever, Prompt, và LLM lại thành một chuỗi hỏi đáp hoàn chỉnh. Nó cũng có chức năng trích xuất "Nguồn tham khảo" (citations). |
| **`scripts/`** | Chứa các script chạy độc lập. Hiện có `shopee_crawler.py` dùng API nội bộ ẩn của Shopee để cào hàng ngàn bài viết rất nhanh. |

---

## 3. Hướng dẫn Debug và Mở rộng

### 3.1 Dữ liệu không cập nhật
- **Vấn đề:** Ứng dụng trả lời sai so với chính sách hiện tại của Shopee.
- **Giải pháp:** Xóa thư mục `vector_store/`, chạy `python scripts/shopee_crawler.py` để lấy dữ liệu mới nhất, sau đó chạy lại `python app.py` để ứng dụng build lại vector store.

### 3.2 Tinh chỉnh (Tuning) chất lượng câu trả lời
- **Bước 1:** Vào `config.py`.
- **Bước 2:** Chỉnh `CHUNK_SIZE` và `CHUNK_OVERLAP` để kiểm soát độ lớn của đoạn văn bản cung cấp cho LLM.
- **Bước 3:** Chỉnh `SIMILARITY_TOP_K` (số lượng tài liệu được lấy ra) nếu LLM đang thiếu thông tin.
- **Bước 4:** Sửa đổi `RAG_PROMPT_TEMPLATE` để ép model trả lời theo đúng tone giọng mong muốn.

### 3.3 Hiểu cách Citations (Trích dẫn nguồn) hoạt động
Mỗi khi trả lời, hệ thống sẽ trả về **`sources`**. Chức năng này được định nghĩa ở hàm `_extract_sources` trong file `modules/query_engine.py`. Nó lọc trùng lặp đường dẫn và lấy tên file gốc để hiển thị trên UI. Nếu bạn muốn hiển thị thêm thông tin (VD: nội dung chi tiết của source), hãy sửa hàm này.

---

## 4. Công nghệ sử dụng (Tech Stack)

- **Backend:** Flask, Python 3.12
- **Frontend:** Vanilla HTML/CSS/JS (Không cần node_modules)
- **AI Framework:** LangChain (LCEL format), ChromaDB (Vector Search)
- **Models:** Ollama (qwen2.5:7b cho logic, nomic-embed-text cho embeddings)
