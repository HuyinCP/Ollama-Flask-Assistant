FROM python:3.10-slim

# Đặt thư mục làm việc trong container
WORKDIR /app

# Cài đặt các thư viện hệ thống cần thiết (nếu có cho chromadb v.v.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt trước để tận dụng Docker cache
COPY requirements.txt .

# Cài đặt các thư viện Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . .

# Mở port 5000
EXPOSE 5000

# Lệnh khởi chạy ứng dụng
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
