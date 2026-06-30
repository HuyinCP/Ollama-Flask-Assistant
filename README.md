# Smart Assistant

Trợ lý AI chạy **cục bộ (local)** bằng [Ollama](https://ollama.com/) + model `**qwen2.5:7b`**, dùng **LangChain (LCEL)** để dựng luồng xử lý và trả về kết quả ở dạng **JSON có cấu trúc**.

---

## 1. Hệ thống làm gì?

Nhận `system_prompt` (vai trò của AI) + `user_prompt` (câu hỏi của người dùng), gọi model qwen2.5 qua Ollama, rồi trả về một JSON gồm 3 trường:


| Trường      | Kiểu  | Ý nghĩa                                     |
| ----------- | ----- | ------------------------------------------- |
| `summary`   | `str` | Tóm tắt câu hỏi của người dùng              |
| `sentiment` | `int` | Điểm cảm xúc, 0 (tiêu cực) → 100 (tích cực) |
| `response`  | `str` | Câu trả lời gợi ý cho người dùng            |


---

## 2. Yêu cầu môi trường

- **Python 3.12** (đang chạy trong `venv`)
- **Ollama** đã cài và đang chạy ở `http://localhost:11434`
- Model đã pull:
  ```bash
  ollama pull qwen2.5:7b
  ollamat   # kiểm tra model đã có lis
  ```
- Thư viện Python:
  ```bash
  pip install langchain-ollama langchain-core pydantic flask
  ```

---

## 3. Cấu trúc dự án

```
Smart Assistant/
├── config.py     # Cấu hình: địa chỉ Ollama, tên model, tham số sinh text
├── model.py      # Lõi AI: dựng chain LangChain, schema JSON, hàm gọi model
├── llm_test.py   # Script test nhanh model.py từ terminal
├── app.py        # Flask API (hiện đang là khung mẫu, chưa nối model)
└── README.md     # Tài liệu này
```

---

## 4. Mô tả từng file

### `config.py` — Cấu hình tập trung

```python
OLLAMA_HOST = "http://localhost:11434"   # Server Ollama local
MODEL_ID    = "qwen2.5:7b"               # Model đang dùng
PARAMETERS  = {                          # Tham số sinh text
    "temperature": 0.7,                  # 0 = ổn định, cao = sáng tạo hơn
    "num_predict": 256,                  # số token tối đa sinh ra
    "top_p": 0.9,
}
```

### `model.py` — Lõi xử lý AI

Các thành phần chính:

1. `**initialize_model()**` — tạo đối tượng `ChatOllama` từ config.
2. `**AIResponse` (Pydantic)** — "khuôn" dữ liệu đầu ra mong muốn (3 trường ở trên).
3. `**json_parser`** — `JsonOutputParser` ép kết quả model về JSON theo khuôn `AIResponse`.
4. `**qwen_template**` — `PromptTemplate` với 3 chỗ trống: `system_prompt`, `user_prompt`, `format_prompt`.
5. `**get_ai_response()**` — dựng và chạy LCEL chain.
6. `**qwen_response()**` — hàm tiện dụng để gọi nhanh.

**Luồng LCEL (cốt lõi):**

```python
chain = template | model | json_parser
#         (1)        (2)        (3)
# (1) Điền dữ liệu vào prompt
# (2) Gửi prompt cho model qwen qua Ollama
# (3) Parse text trả về thành dict JSON
```

> `format_prompt` được sinh tự động bằng `json_parser.get_format_instructions()` — đây là hướng dẫn "hãy trả JSON đúng các field", giúp model biết phải trả đúng định dạng.

### `llm_test.py` — Test nhanh

Gọi `qwen_response()` với một câu hỏi mẫu và in ra `summary`, `sentiment`, `response`.

```bash
python llm_test.py
```

Kết quả mẫu:

```
Summary  : The capital city of Canada is Ottawa.
Sentiment: 85
Response : Ottawa is also known for its beautiful Rideau Canal...
```

### `app.py` — Flask API (khung mẫu)

Hiện có 1 endpoint `POST /generate` nhưng **chưa nối với model** — mới trả về message giả:

```python
@app.route('/generate', methods=['POST'])
def generate():
    return jsonify({"message": "AI response will be generated here"})
```

> Đây là bước tiếp theo cần làm: cho endpoint này gọi `qwen_response()` và trả JSON thật.

---

## 5. Cách chạy

### Chạy thử model (CLI)

```bash
# Bật venv (PowerShell)
.\venv\Scripts\Activate.ps1

# Chạy test
python llm_test.py
```

### Chạy API Flask

```bash
python app.py
# Server chạy ở http://127.0.0.1:5000
```

---

## 6. Sơ đồ luồng dữ liệu

```
[Người dùng]
    │  system_prompt + user_prompt
    ▼
qwen_response()  ──►  get_ai_response()
                          │
                          ▼
            template | model | json_parser   (LCEL chain)
                          │
                          ▼
                 dict JSON: {summary, sentiment, response}
```

---

## 7. Trạng thái hiện tại & bước tiếp theo


| Thành phần                       | Trạng thái                                  |
| -------------------------------- | ------------------------------------------- |
| `config.py`                      | ✅ Xong                                      |
| `model.py` (chain + JSON output) | ✅ Xong, đã test                             |
| `llm_test.py`                    | ✅ Xong, chạy được                           |
| `app.py` (Flask API)             | ⏳ Khung mẫu — cần nối với `qwen_response()` |
| Giao diện web (chat UI)          | ⏳ Chưa làm                                  |


**Bước tiếp theo gợi ý:** nối `app.py` với `model.py` để `/generate` nhận `user_prompt` từ request và trả JSON thật.