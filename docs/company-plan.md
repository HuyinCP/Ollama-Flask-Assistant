# Trợ lý CSKH nội bộ tại Tiki

> Tài liệu lập kế hoạch (planning). Xây một trợ lý AI nội bộ hỗ trợ đội Chăm sóc khách hàng. Giai đoạn này tập trung **chuẩn bị dữ liệu nghiệp vụ**. Phần fine-tuning và thiết kế RAG sẽ xử lý ở giai đoạn sau.

## 1. Bối cảnh & mục tiêu

Là thành viên đội CSKH tại **Tiki**, mỗi ngày chúng ta xử lý rất nhiều yêu cầu của khách (đơn hàng, đổi trả, hoàn tiền, sản phẩm lỗi). Trợ lý này giúp đội:

- Phản hồi nhanh và nhất quán theo **đúng chính sách Tiki**.
- Giảm thời gian tra cứu chính sách thủ công.
- Phân loại mức độ cảm xúc để ưu tiên ca gấp.

Vì sao nghiệp vụ này phù hợp để xây trước:

- Use-case CSKH **khớp trực tiếp** với schema hiện tại của trợ lý (`summary`, `sentiment`, `action`, `response`).
- Chính sách của Tiki **rõ ràng, có cấu trúc** → thuận lợi cho RAG.
- Ngữ cảnh tiếng Việt, dễ kiểm chứng nội bộ và mở rộng dần.

## 2. Bài toán

Trợ lý nhận một tin nhắn/khiếu nại của khách hàng và trả về:


| Trường      | Ý nghĩa                                                                         |
| ----------- | ------------------------------------------------------------------------------- |
| `summary`   | Tóm tắt yêu cầu của khách                                                       |
| `sentiment` | Mức độ cảm xúc (0–100)                                                          |
| `action`    | Hành động nội bộ nên thực hiện (tạo C-return, yêu cầu bằng chứng, hoàn tiền...) |
| `response`  | Câu trả lời gửi khách, **bám đúng chính sách Tiki** (nhờ RAG ở giai đoạn sau)   |


## 3. Nguồn dữ liệu (knowledge base cho RAG)

Dữ liệu đã thu thập và lưu trong `data/tiki/` (xem `data/tiki/sources.md` để biết nguồn):

- `chinh-sach-doi-tra.md` — điều kiện và thời hạn đổi trả/bảo hành.
- `thoi-gian-hoan-tien.md` — bảng thời gian hoàn tiền theo phương thức thanh toán.
- `kenh-ho-tro.md` — kênh liên hệ và quy trình khiếu nại C-return.
- `faq.md` — câu hỏi thường gặp.

> [!IMPORTANT]
> Dữ liệu được tổng hợp từ nguồn công khai và **cần đối chiếu lại với trang chính thức của Tiki** trước khi dùng cho môi trường thật. Đây là dữ liệu phục vụ học tập/demo.

## 4. Map dữ liệu vào tình huống

Ví dụ: *"Đơn hàng giao tới bị vỡ, tôi muốn hoàn tiền."*


| Trường      | Kết quả mong muốn                                                                 |
| ----------- | --------------------------------------------------------------------------------- |
| `summary`   | Khách báo sản phẩm bị vỡ, yêu cầu hoàn tiền                                       |
| `sentiment` | ~20/100                                                                           |
| `action`    | Tạo mã khiếu nại C-return; yêu cầu video mở hàng + ảnh tem kiện trong 48h         |
| `response`  | Trả lời theo chính sách lỗi ngoại quan 48h + thời gian hoàn tiền theo phương thức |


## 5. Lộ trình kỹ thuật (giai đoạn sau)

1. **Chuẩn hóa dữ liệu** — làm sạch các file trong `data/tiki/`, chia nhỏ (chunking).
2. **Embeddings + Vector store** — sinh embedding (vd `nomic-embed-text` qua Ollama) và lưu vào Chroma/FAISS.
3. **Retriever** — truy hồi đoạn chính sách liên quan tới câu hỏi.
4. **RAG chain** — chèn ngữ cảnh truy hồi vào prompt trước khi gọi `qwen2.5:7b`.
5. **Trích dẫn nguồn** — đính kèm đoạn chính sách đã dùng để trả lời.
6. **Đánh giá** — bộ câu hỏi mẫu để kiểm độ chính xác trước/sau RAG.

## 6. Trạng thái


| Hạng mục                    | Trạng thái      |
| --------------------------- | --------------- |
| Xác định nghiệp vụ CSKH     | ✅ Đã chốt       |
| Thu thập dữ liệu chính sách | ✅ `data/tiki/`  |
| Thiết kế RAG                | ⏳ Giai đoạn sau |
| Fine-tuning                 | ⏳ Giai đoạn sau |


