import os
import sys
import time
import math
import requests
from markdownify import markdownify

# Fix windows console unicode error
sys.stdout.reconfigure(encoding='utf-8')

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'shopee')
os.makedirs(DATA_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json'
}

def get_leaf_categories():
    """Lấy danh sách ID của tất cả các danh mục lá (không có danh mục con)."""
    url = "https://help.shopee.vn/api/inhouse/hc/mobile/v1/categories?frontend_id=4"
    print("Đang lấy cây danh mục (Category Tree)...")
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    
    leaf_ids = []
    
    def extract_leaves(nodes):
        for node in nodes:
            children = node.get('sub_dir_info', [])
            if not children:
                leaf_ids.append(node['id'])
            else:
                extract_leaves(children)
                
    extract_leaves(data.get('dir_info', []))
    print(f"Tìm thấy {len(leaf_ids)} danh mục lá.")
    return leaf_ids

def get_all_article_ids(category_ids):
    """Lặp qua tất cả danh mục và lấy toàn bộ ID bài viết."""
    all_article_ids = set()
    
    print("\nĐang quét ID bài viết từ các danh mục...")
    for idx, cid in enumerate(category_ids, 1):
        print(f"Quét danh mục {cid} ({idx}/{len(category_ids)})...", end="\r")
        page = 1
        size = 100
        while True:
            url = f"https://help.shopee.vn/api/inhouse/hc/mobile/v1/categories/articles?category_id={cid}&frontend_id=4&page={page}&size={size}"
            try:
                res = requests.get(url, headers=HEADERS)
                res.raise_for_status()
                data = res.json()
                
                articles = data.get('articles', [])
                if not articles:
                    break
                    
                for art in articles:
                    all_article_ids.add(art['id'])
                    
                if len(articles) < size:
                    break
                page += 1
                time.sleep(0.1) # Chống spam API
            except Exception as e:
                print(f"\nLỗi khi lấy bài viết ở category {cid}, page {page}: {e}")
                break
                
    print(f"\nHoàn tất quét! Tổng cộng gom được {len(all_article_ids)} bài viết độc nhất.")
    return list(all_article_ids)

def fetch_and_save_articles(article_ids, batch_size=15):
    """Lấy nội dung chi tiết của các bài viết theo batch và lưu thành Markdown."""
    total = len(article_ids)
    batches = math.ceil(total / batch_size)
    
    print(f"\nBắt đầu tải nội dung {total} bài viết (chia thành {batches} đợt)...")
    
    success_count = 0
    for i in range(batches):
        batch = article_ids[i*batch_size : (i+1)*batch_size]
        url = "https://help.shopee.vn/api/inhouse/hc/mobile/v1/seo?frontend_id=4"
        for aid in batch:
            url += f"&article_ids={aid}"
            
        try:
            res = requests.get(url, headers=HEADERS)
            res.raise_for_status()
            data = res.json()
            
            articles = data.get('articles', []) or data.get('hot_questions', [])
            
            for art in articles:
                art_id = art['id']
                title = art['title']
                content_html = art['content']
                
                markdown_text = f"# {title}\n\n" + markdownify(content_html)
                
                safe_title = "".join([c if c.isalnum() else "_" for c in title])
                # Rút gọn tên file nếu quá dài
                if len(safe_title) > 100:
                    safe_title = safe_title[:100]
                    
                file_name = f"shopee_{art_id}_{safe_title}.md"
                file_path = os.path.join(DATA_DIR, file_name)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_text)
                success_count += 1
                
        except Exception as e:
            print(f"Lỗi tải đợt {i+1}: {e}")
            
        print(f"Đã tải {min((i+1)*batch_size, total)}/{total} bài viết...", end="\r")
        time.sleep(0.5) # Nghỉ xíu tránh rate limit
        
    print(f"\nHoàn thành! Đã tải và lưu {success_count}/{total} bài viết.")

if __name__ == "__main__":
    start_time = time.time()
    
    # Bước 1: Lấy các thư mục
    category_ids = get_leaf_categories()
    
    # Bước 2: Gom ID bài viết
    article_ids = get_all_article_ids(category_ids)
    
    # Bước 3: Tải và lưu nội dung
    if article_ids:
        fetch_and_save_articles(article_ids)
        
    print(f"Tổng thời gian chạy: {round(time.time() - start_time, 2)} giây")
