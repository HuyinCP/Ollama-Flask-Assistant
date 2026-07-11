# Shopee Crawler Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Viết một script Python để tự động crawl dữ liệu bài viết từ Shopee Help Center và lưu thành định dạng Markdown.

**Architecture:** Sử dụng Playwright để render giao diện Single Page App của Shopee, BeautifulSoup4 để bóc tách thẻ HTML tiêu đề và nội dung, Markdownify để lưu bài viết dưới dạng Markdown.

**Tech Stack:** Python, Playwright, BeautifulSoup4, Markdownify.

## Global Constraints

- Chờ ngẫu nhiên 2-3 giây giữa các request.
- Các file Markdown được lưu tại `data/shopee/`.

---

### Task 1: Thiết lập thư viện và thư mục

**Files:**
- Modify: `requirements.txt`
- Create: `data/shopee/`
- Create: `scripts/`

**Interfaces:**
- Consumes: `requirements.txt`
- Produces: Cài đặt đủ thư viện môi trường để Task 2 sử dụng.

- [ ] **Step 1: Update requirements.txt**

Add to `requirements.txt`:
```text
playwright
beautifulsoup4
markdownify
```

- [ ] **Step 2: Install dependencies**

```bash
.\venv\Scripts\Activate.ps1
pip install playwright beautifulsoup4 markdownify
playwright install chromium
```

- [ ] **Step 3: Tạo thư mục lưu trữ**

```bash
New-Item -ItemType Directory -Force "data\shopee"
New-Item -ItemType Directory -Force "scripts"
```

- [ ] **Step 4: Commit**

```bash
git add requirements.txt
git commit -m "chore: add crawler dependencies"
```

---

### Task 2: Cài đặt logic Crawler

**Files:**
- Create: `scripts/shopee_crawler.py`

**Interfaces:**
- Consumes: Mạng Internet, Playwright library.
- Produces: Các file `.md` trong thư mục `data/shopee/`.

- [ ] **Step 1: Viết script Crawler**

Create `scripts/shopee_crawler.py`:
```python
import os
import time
import random
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from markdownify import markdownify

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'shopee')
os.makedirs(DATA_DIR, exist_ok=True)

def crawl_article(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print(f"Fetching: {url}")
        page.goto(url, wait_until='networkidle')
        
        # Đợi tiêu đề xuất hiện
        try:
            page.wait_for_selector('#hcArticleTitle', timeout=10000)
        except Exception:
            print("Không tìm thấy bài viết hoặc timeout.")
            browser.close()
            return
            
        html_content = page.content()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        title_el = soup.select_one('#hcArticleTitle')
        body_el = soup.select_one('.kb-article-content') or soup.select_one('.quickAnswer')
        
        if not title_el or not body_el:
            print("Thiếu element tiêu đề hoặc nội dung.")
            browser.close()
            return
            
        title = title_el.get_text(strip=True)
        markdown_text = f"# {title}\n\n" + markdownify(str(body_el))
        
        # Tạo tên file an toàn
        safe_title = "".join([c if c.isalnum() else "_" for c in title])
        file_name = f"shopee_article_{safe_title}.md"
        file_path = os.path.join(DATA_DIR, file_name)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
            
        print(f"Đã lưu: {file_name}")
        browser.close()

if __name__ == "__main__":
    # Ví dụ một link cụ thể để test
    test_urls = [
        "https://help.shopee.vn/portal/article/79046"
    ]
    for link in test_urls:
        crawl_article(link)
        time.sleep(random.uniform(2, 4))
```

- [ ] **Step 2: Chạy thử script**

```bash
.\venv\Scripts\Activate.ps1
python scripts/shopee_crawler.py
```

- [ ] **Step 3: Commit**

```bash
git add scripts/shopee_crawler.py
git commit -m "feat: add basic shopee crawler script"
```
