import os
import sys
import time
import json
import random
import urllib.request
from bs4 import BeautifulSoup
from markdownify import markdownify

# Fix windows console unicode error
sys.stdout.reconfigure(encoding='utf-8')

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'shopee')
os.makedirs(DATA_DIR, exist_ok=True)

def crawl_article(url):
    print(f"Fetching: {url}")
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Lỗi tải trang: {e}")
        return

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Tìm thẻ script chứa dữ liệu
    script_tag = soup.find('script', id='ScriptForHydrate')
    if not script_tag:
        print("Không tìm thấy dữ liệu bài viết (ScriptForHydrate missing).")
        return
        
    script_text = script_tag.string
    if not script_text:
        print("ScriptForHydrate rỗng.")
        return
        
    # Extract JSON string from window["FORGE_SSR_DATA_MAP"] = {...};
    try:
        start_idx = script_text.find('window["FORGE_SSR_DATA_MAP"] = ')
        if start_idx == -1:
            raise ValueError("Không tìm thấy biến FORGE_SSR_DATA_MAP")
            
        start_idx += len('window["FORGE_SSR_DATA_MAP"] = ')
        
        # Tìm vị trí kết thúc bằng cách tìm chuỗi ';\n'
        end_idx = script_text.find(';\n', start_idx)
        if end_idx != -1:
            json_str = script_text[start_idx:end_idx]
        else:
            json_str = script_text[start_idx:]
            
        data_map = json.loads(json_str)
        
        # Article data thường nằm ở key '4' hoặc lặp qua các keys
        article_data = data_map.get('4')
        if not article_data or 'title' not in article_data:
            for k, v in data_map.items():
                if isinstance(v, dict) and 'title' in v and 'content' in v:
                    article_data = v
                    break
                    
        if not article_data:
            print("Không tìm thấy article_data trong JSON.")
            return
            
        title = article_data['title']
        content_html = article_data['content']
        
        markdown_text = f"# {title}\n\n" + markdownify(content_html)
        
        safe_title = "".join([c if c.isalnum() else "_" for c in title])
        file_name = f"shopee_article_{safe_title}.md"
        file_path = os.path.join(DATA_DIR, file_name)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
            
        print(f"Đã lưu thành công: {file_name}")
        
    except Exception as e:
        print(f"Lỗi parse dữ liệu: {e}")

if __name__ == "__main__":
    test_urls = [
        "https://help.shopee.vn/portal/article/79046"
    ]
    for link in test_urls:
        crawl_article(link)
        time.sleep(random.uniform(1, 2))
