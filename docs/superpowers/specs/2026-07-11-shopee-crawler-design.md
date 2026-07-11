# Shopee Help Center Crawler Design

## Mục tiêu (Goal)
Xây dựng một công cụ tự động trích xuất (crawl) các bài viết từ Trung tâm trợ giúp Shopee (Shopee Help Center) để tạo thành một bộ dữ liệu (Knowledge Base) định dạng Markdown, phục vụ cho quá trình xây dựng hệ thống Retrieval-Augmented Generation (RAG) sau này.

## Kiến trúc phần mềm (Architecture)

### Công nghệ sử dụng
- **Ngôn ngữ:** Python 3.12 (đồng bộ với dự án gốc).
- **Thư viện Crawler:** `playwright` (để render JavaScript vì Shopee là Single Page App).
- **Thư viện Parse nội dung:** `beautifulsoup4` (xử lý DOM) và `markdownify` (chuyển HTML sang Markdown).

### Luồng xử lý dữ liệu (Data Flow)
1. **Khởi tạo:**
   - Khởi chạy headless browser thông qua Playwright.
2. **Khám phá liên kết (Link Discovery):**
   - Script sẽ điều hướng qua các danh mục (Categories) của Trung tâm trợ giúp để lấy các URL bài viết (`/portal/article/...`).
3. **Trích xuất nội dung (Content Extraction):**
   - Duyệt qua danh sách URL bài viết.
   - Chờ phần tử tiêu đề bài viết `#hcArticleTitle` xuất hiện.
   - Trích xuất HTML của phần thân bài viết.
4. **Lưu trữ & Làm sạch (Storage & Sanitization):**
   - Chuyển HTML của bài viết sang Markdown bằng `markdownify`.
   - Lưu trữ tại thư mục `data/shopee/` với định dạng tên file: `[id]-tieu-de-bai-viet.md`.

## Cơ chế Xử lý Ngoại lệ (Error Handling & Resilience)
- **Rate Limiting:** Sử dụng `time.sleep()` với thời gian ngẫu nhiên (vd: 2-5 giây) giữa các request để tránh bị hệ thống chặn.
- **Resumption (Lưu tiến độ):** Trạng thái crawl (danh sách các URL đã cào thành công) sẽ được lưu trong file `data/shopee/progress.json` hoặc log file đơn giản. Khi chạy lại, script sẽ bỏ qua các URL đã xử lý.

## Cấu trúc thư mục bổ sung
```text
Ollama-Gradio-Assistant/
├── scripts/
│   └── shopee_crawler.py       # Công cụ crawl chính
├── data/
│   └── shopee/                 # Thư mục lưu trữ kết quả Markdown
```

## Các hạn chế đã biết (Known Limitations)
- Shopee có thể thỉnh thoảng cập nhật cấu trúc DOM (thay đổi CSS class, ID), điều này sẽ yêu cầu bảo trì script bằng cách cập nhật selector (chẳng hạn `#hcArticleTitle`).
- Việc lấy bài viết bằng Playwright mất nhiều thời gian hơn requests thông thường do phải chạy toàn bộ headless browser. Tuy nhiên, nó đảm bảo lấy được dữ liệu đầy đủ 100%.
