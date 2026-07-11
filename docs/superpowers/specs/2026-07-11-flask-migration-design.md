# Flask UI Migration Design

## Mục tiêu (Goal)
Chuyển đổi giao diện người dùng từ Gradio sang Flask sử dụng HTML/JS thuần. Yêu cầu giao diện phải đơn giản, dễ đọc code, không màu mè, và không sử dụng Gradio. Cấu trúc cũ của hệ thống AI (Ollama + LangChain) vẫn được giữ nguyên.

## Kiến trúc thay thế (Architecture)

### Backend (Flask)
Sẽ thay thế file `app.py` (hoặc tạo file mới) bằng một ứng dụng Flask cơ bản:
- `GET /`: Trả về trang HTML giao diện chính (`templates/index.html`).
- `POST /api/analyze`: Endpoint nhận JSON payload `{"message": "..."}` từ người dùng. Xử lý qua hàm `qwen_response` hiện tại và trả về kết quả JSON chứa các trường: `summary`, `sentiment`, `action`, `response`, `duration`.

### Frontend
- **HTML (`templates/index.html`)**: Chứa một `<textarea>` để nhập tin nhắn khách hàng và một `<button>` để gửi. Có các `<div id="...">` hoặc `<span>` để hiển thị kết quả phân tích (Tóm tắt, cảm xúc, hành động, câu trả lời gợi ý, thời gian xử lý).
- **CSS (`static/style.css`)**: Sử dụng CSS cơ bản để canh lề, bôi đậm, tạo độ dễ đọc. Không sử dụng thư viện CSS phức tạp hay hiệu ứng màu mè (như yêu cầu).
- **JavaScript (`static/script.js`)**: Lắng nghe sự kiện click nút Submit. Sử dụng `fetch` API gửi dữ liệu đến `/api/analyze`, hiển thị trạng thái "Đang xử lý..." (loading state), và sau đó cập nhật dữ liệu JSON trả về vào các thẻ HTML tương ứng mà không cần tải lại trang.

## Các module cần thay đổi
- [DELETE] Mã Gradio trong `app.py` hiện tại.
- [NEW] Khởi tạo Flask server trong `app.py`.
- [NEW] `templates/index.html` (Giao diện).
- [NEW] `static/style.css` (Style tối giản).
- [NEW] `static/script.js` (Logic fetch dữ liệu).
- [MODIFY] `requirements.txt` (nếu có, thêm `flask`).

## Xử lý lỗi (Error Handling)
- **Frontend**: Nếu request thất bại hoặc timeout, hiển thị dòng cảnh báo màu đỏ nhẹ nhàng trên giao diện báo cho người dùng biết sự cố.
- **Backend**: Bắt lỗi khi gọi LLM và trả về status 500 kèm thông báo lỗi dạng JSON.

## Kế hoạch kiểm thử (Testing)
- Khởi động server `app.py`.
- Mở trình duyệt tại `http://127.0.0.1:5000/`.
- Nhập thử một câu hỏi hỗ trợ khách hàng và kiểm tra xem kết quả có hiện lên đủ 5 trường thông tin nhanh chóng không.
