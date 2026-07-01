# Nguồn dữ liệu — Tiki

Dữ liệu trong thư mục này được tổng hợp từ các nguồn công khai (tháng 6/2026) phục vụ mục đích **học tập / demo RAG**.

> [!IMPORTANT]
> Đây KHÔNG phải tài liệu chính thức của Tiki. Trước khi dùng cho môi trường thật, cần **đối chiếu lại với trang chính thức** của Tiki vì chính sách có thể thay đổi.

## Nguồn tham khảo

- Học viện Tiki — Câu hỏi thường gặp về xử lý đổi – trả – bảo hành: https://hocvien.tiki.vn/faq/cau-hoi-thuong-gap-ve-xu-ly-doi-tra-bao-hanh/
- Tiki Blog — Chương trình Đổi Trả 365 (1 đổi 1 trong 365 ngày): https://tiki.vn/blog/chuong-trinh-doi-tra-365/
- Hướng dẫn Tiki — FAQ chính sách đổi trả hàng hóa: https://huongdantiki.com/cac-cau-hoi-thuong-gap-ve-chinh-sach-doi-tra-hang-hoa/
- Gửi yêu cầu hỗ trợ Tiki: https://tiki.vn/lien-he/gui-yeu-cau
- Hotline TikiCare: 19006035 (8h – 21h)

## Danh sách file dữ liệu

| File | Nội dung |
|---|---|
| `chinh-sach-doi-tra.md` | Điều kiện, thời hạn đổi trả/bảo hành, bằng chứng cần cung cấp |
| `thoi-gian-hoan-tien.md` | Bảng thời gian hoàn tiền theo phương thức thanh toán |
| `kenh-ho-tro.md` | Kênh liên hệ, quy trình khiếu nại C-return, action gợi ý |
| `faq.md` | Câu hỏi thường gặp |

## Ghi chú cho giai đoạn RAG

- Các file ở định dạng Markdown, dễ chunk theo heading.
- Nên gắn metadata (nguồn, ngày cập nhật) khi ingest.
- Cân nhắc tách bảng (thời gian hoàn tiền) thành chunk riêng để truy hồi chính xác.
