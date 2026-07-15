# Kiến trúc Hệ thống: Shopee Help Center Assistant

Tài liệu này cung cấp cái nhìn tổng quan và chi tiết về cấu trúc hệ thống, luồng dữ liệu (Data Flow), và chức năng của từng file trong dự án. Việc nắm rõ kiến trúc này sẽ giúp các lập trình viên dễ dàng bảo trì, gỡ lỗi và phát triển thêm các tính năng mới.

---

## 1. Tổng quan Hệ thống (System Overview)

Dự án là một ứng dụng **RAG (Retrieval-Augmented Generation)** chạy hoàn toàn nội bộ (local). Hệ thống kết hợp các tài liệu từ Shopee Help Center với sức mạnh của LLM cục bộ (thông qua Ollama) để trả lời chính xác các câu hỏi của người dùng dựa trên dữ liệu thực tế.

Kiến trúc hệ thống chia làm 2 pha (phases) chính:
1. **Data Ingestion Phase (Thu thập & Xử lý dữ liệu):** Cào dữ liệu từ Shopee, cắt nhỏ (chunking), tạo embedding và lưu vào Vector Database.
2. **Retrieval & QA Phase (Truy xuất & Hỏi đáp):** Nhận câu hỏi từ người dùng, tìm kiếm các tài liệu liên quan trong Vector DB, và đưa vào LLM để sinh ra câu trả lời cùng trích dẫn nguồn.

---

## 2. Sơ đồ Luồng Hoạt động (Data Flow Diagram)

```mermaid
graph TD
    subgraph 1. Data Ingestion (Offline)
        A[scripts/shopee_crawler.py] -->|Cào dữ liệu API| B[(data/shopee/*.md)]
        B -->|Đọc file| C[modules/data_loader.py]
        C -->|Chia nhỏ Text| D[modules/data_processing.py]
        D -->|Embeddings| E[(Chroma Vector DB)]
    end

    subgraph 2. Retrieval & Generation (Online)
        U[Người dùng hỏi] -->|Gửi API Request| H[app.py / Flask]
        H --> F[modules/query_engine.py]
        E -->|Lấy Top-K Tài liệu tương tự| F
        F -->|Prompt + Context + Câu hỏi| G[modules/llm_interface.py]
        G -->|Sinh câu trả lời| F
        F -->|Trả về JSON (Answer + Sources)| H
        H <--> I[Web UI: HTML/CSS/JS]
    end
```

---

## 3. Giải thích Chức năng Từng File (File-by-File Breakdown)

Mã nguồn được tổ chức theo **Modules Pattern**, tách biệt rõ ràng các khâu của RAG. Việc này giúp dễ dàng bảo trì và thay thế từng thành phần (ví dụ: thay thế vector DB hoặc thay đổi LLM provider) mà không ảnh hưởng đến phần còn lại.

### 🌟 Core Application & Configuration
| File / Thư mục | Giải thích Chức năng |
|---|---|
| **`app.py`** | **Entry point của ứng dụng Web.**<br>- Khởi tạo Flask Server.<br>- Khởi tạo RAG Pipeline (chỉ chạy 1 lần khi server start).<br>- Định nghĩa các HTTP Endpoints (VD: `/api/chat` nhận câu hỏi POST và trả về JSON). Nơi kết nối Web Client và lõi AI. |
| **`config.py`** | **Trung tâm Cấu hình (Single Source of Truth).**<br>- Chứa TẤT CẢ các thiết lập của dự án: cấu hình LLM Host, tham số LLM (temperature), Chunk Size, Top K tài liệu truy xuất, và System Prompt (`RAG_PROMPT_TEMPLATE`).<br>- Giúp developer tinh chỉnh hệ thống tập trung. |
| **`requirements.txt`** | Danh sách các thư viện Python (dependencies) cần thiết để chạy dự án. |

### 🧠 Core RAG Modules (`modules/`)
Thư mục này chứa toàn bộ logic nghiệp vụ xử lý dữ liệu và AI.

| File | Giải thích Chức năng |
|---|---|
| **`__init__.py`** | Khai báo thư mục `modules` là một package, export các hàm quan trọng. |
| **`data_loader.py`** | **Chịu trách nhiệm load dữ liệu gốc.**<br>- Quét thư mục `data/shopee/` để đọc toàn bộ các file `.md`.<br>- Chuyển đổi nội dung text thô thành đối tượng `Document` của LangChain (kèm metadata nguồn gốc). |
| **`data_processing.py`** | **Xử lý Text và lưu trữ Vector.**<br>- Nhận các Document từ `data_loader.py`.<br>- Cắt văn bản dài thành các đoạn (chunks) nhỏ thông qua `RecursiveCharacterTextSplitter`.<br>- Quản lý việc lưu các vector (embeddings) vào hệ thống file thông qua `ChromaDB`. |
| **`llm_interface.py`** | **Cầu nối với các AI Models (LLM Provider).**<br>- Khởi tạo module Chat (`ChatOllama`) và module Embeddings (`OllamaEmbeddings`).<br>- Cô lập logic gọi API LLM ở một nơi duy nhất. |
| **`query_engine.py`** | **Trái tim của RAG Pipeline.**<br>- Dùng `LCEL` (LangChain Expression Language) để nối chuỗi: `Retriever` ➜ `Prompt` ➜ `LLM`.<br>- Hàm `query()` thực thi toàn bộ luồng hỏi đáp.<br>- Hàm `_extract_sources()` chịu trách nhiệm phân tích metadata để trả về danh sách các tài liệu tham khảo cho người dùng. |

### 🕸️ Data Ingestion (`scripts/` & Storage)
| File / Thư mục | Giải thích Chức năng |
|---|---|
| **`scripts/shopee_crawler.py`** | Script chạy offline. Gọi API của Shopee Help Center để cào bài viết, chuyển đổi HTML sang file `.md` rồi lưu lại. |
| **`data/shopee/`** | Thư mục chứa kho dữ liệu tĩnh (tài liệu Markdown) tạo ra bởi crawler. Đóng vai trò là Knowledge Base. |
| **`vector_store/`** | Thư mục sinh tự động bởi ChromaDB. Chứa dữ liệu text đã mã hóa thành vector số. Nhờ lưu sẵn tại đây, hệ thống không phải xử lý (embed) lại hàng trăm file Markdown mỗi khi khởi động. |

### 💻 Giao diện Người dùng (Frontend)
| File / Thư mục | Giải thích Chức năng |
|---|---|
| **`templates/index.html`** | Giao diện chính của ứng dụng (khung chat, bố cục hiển thị). |
| **`static/`** | Thư mục chứa tài nguyên tĩnh của Frontend. Bao gồm file `.css` (định dạng màu sắc, giao diện) và file `.js` (gửi AJAX request đến server, xử lý animation loading). |

---

## 4. Hướng dẫn Bảo trì & Tinh chỉnh

### 4.1. Làm sao để cập nhật dữ liệu mới từ Shopee?
Nếu Shopee thay đổi chính sách, hệ thống AI sẽ không biết trừ khi bạn cập nhật dữ liệu:
1. **Xóa Vector DB cũ:** Xóa hoàn toàn thư mục `vector_store/`.
2. **Cập nhật Markdown:** Chạy lệnh `python scripts/shopee_crawler.py` để hệ thống kéo về bộ dữ liệu mới nhất.
3. **Build lại DB:** Chạy `python app.py`. Lúc khởi động, hệ thống sẽ thấy thiếu vector store nên sẽ tự động đọc lại các file `.md` mới và tạo embeddings lại từ đầu.

### 4.2. Tinh chỉnh (Tuning) Chất lượng Câu trả lời
Tất cả các tham số nằm gọn trong `config.py`:
- **Đổi giọng văn (Tone):** Chỉnh sửa biến `RAG_PROMPT_TEMPLATE`. Ép model luôn trả lời bằng Tiếng Việt hoặc yêu cầu trình bày theo từng bước cụ thể.
- **Ngữ cảnh bị thiếu:** Nếu AI trả lời thiếu ý, thử tăng tham số `SIMILARITY_TOP_K` (số tài liệu lấy ra).
- **Tối ưu Chunking:** Nếu văn bản bị cắt ngang làm mất ngữ nghĩa, hãy điều chỉnh `CHUNK_SIZE` và `CHUNK_OVERLAP` để các chunk bao hàm trọn vẹn thông tin hơn.
- **Độ dài câu trả lời:** Chỉnh thông số `num_predict` trong `LLM_PARAMETERS` (tăng lên nếu đáp án bị cắt ngang).
