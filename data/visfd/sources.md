# Nguồn dữ liệu — UIT-ViSFD

Dataset bình luận người dùng về sản phẩm (điện thoại) trên một sàn thương mại điện tử lớn ở Việt Nam, đã được gán nhãn aspect-based sentiment. Dùng cho mục đích **học tập / nghiên cứu / huấn luyện** trợ lý CSKH.

## Nguồn

- HuggingFace: <https://huggingface.co/datasets/visolex/ViSFD>
- GitHub gốc: <https://github.com/LuongPhan/UIT-ViSFD>
- Paper: Phan et al. (2021), *"SA2SL: From Aspect-Based Sentiment Analysis to Social Listening System for Business Intelligence"* — Springer KSEM 2021: <https://link.springer.com/chapter/10.1007/978-3-030-82147-0_53>
- Tác giả: Luong Luc Phan et al., University of Information Technology – VNUHCM.

> [!IMPORTANT]
> Dataset **miễn phí cho mục đích nghiên cứu**. Nếu sử dụng, vui lòng **trích dẫn paper gốc** ở trên. Đây là dữ liệu thu thập từ bình luận công khai, không phải tài liệu của Tiki.

## File

| File | Mô tả |
|---|---|
| `ViSFD.csv` | 11.122 bình luận đã gộp các split (train/dev/test) |
| `HF_README.md` | README gốc từ HuggingFace (mô tả + giấy phép) |

## Cấu trúc cột (`ViSFD.csv`)

| Cột | Kiểu | Mô tả |
|---|---|---|
| `dataset` | string | Luôn là `ViSFD` (nguồn gốc) |
| `type` | string | Split: `train` / `validation` / `test` |
| `index` | int | Số thứ tự bản ghi |
| `comment` | string | Nội dung bình luận (tiếng Việt) |
| `n_star` | int | Số sao người dùng đánh giá (1–5) |
| `date_time` | string | Thời điểm đăng bình luận |
| `label` | string | JSON map từ 10 aspect → nhãn `{negative, neutral, positive}` |

Tổng: **11.122 bình luận** (Train 7.786 / Dev 1.112 / Test 2.224).

## 10 aspect categories

SCREEN, CAMERA, FEATURES, BATTERY, PERFORMANCE, STORAGE, DESIGN, PRICE, GENERAL, SER&ACC (dịch vụ & phụ kiện).

## Ghi chú cho giai đoạn sau

- Cột `comment` + `label` dùng để huấn luyện/đánh giá phân tích cảm xúc theo khía cạnh.
- Có thể dùng `comment` làm đầu vào thử cho trợ lý hiện tại (`summary`/`sentiment`/`action`/`response`).
- `n_star` là tín hiệu tốt để đối chiếu với `sentiment` model dự đoán.
