# Flask UI Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Chuyển đổi giao diện ứng dụng từ Gradio sang một ứng dụng Flask HTML/JS tĩnh đơn giản.

**Architecture:** Sử dụng Flask làm API backend, HTML/CSS tĩnh, và Javascript Vanilla để thực hiện fetch request đến server thay vì reload trang.

**Tech Stack:** Flask, HTML, CSS, Vanilla JS.

## Global Constraints

Giao diện đơn giản, dễ đọc code, không màu mè, không sử dụng Gradio. Cấu trúc AI LangChain giữ nguyên.

---

### Task 1: Thiết lập giao diện Frontend (HTML & CSS)

**Files:**
- Create: `templates/index.html`
- Create: `static/style.css`

**Interfaces:**
- Consumes: User input từ giao diện.
- Produces: Form HTML chuẩn bị cho Task 2 để gắn JS.

- [ ] **Step 1: Write HTML Structure**

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ollama Assistant</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <h1>Customer Inquiry Analyzer</h1>
        <p>Local AI assistant powered by <strong>Qwen 2.5 7B</strong> via Ollama + LangChain LCEL.</p>
        
        <div class="input-group">
            <label for="message">Customer message</label>
            <textarea id="message" rows="4" placeholder="Enter a customer inquiry..."></textarea>
        </div>
        <button id="analyze-btn">Analyze</button>

        <div id="results" class="hidden">
            <div class="result-row">
                <div class="result-box">
                    <label>Summary</label>
                    <div id="out-summary" class="output"></div>
                </div>
                <div class="result-box">
                    <label>Sentiment (0–100)</label>
                    <div id="out-sentiment" class="output"></div>
                </div>
            </div>
            <div class="result-box">
                <label>Recommended action</label>
                <div id="out-action" class="output"></div>
            </div>
            <div class="result-box">
                <label>Suggested response</label>
                <div id="out-response" class="output"></div>
            </div>
            <div class="result-box">
                <label>Duration (seconds)</label>
                <div id="out-duration" class="output"></div>
            </div>
        </div>
    </div>
    <script src="/static/script.js"></script>
</body>
</html>
```

- [ ] **Step 2: Write basic CSS style**

```css
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 20px;
    background-color: #f9f9f9;
    color: #333;
}
.container {
    max-width: 800px;
    margin: 0 auto;
    background: #fff;
    padding: 20px;
    border-radius: 4px;
    border: 1px solid #ddd;
}
.input-group, .result-box {
    margin-bottom: 15px;
}
label {
    display: block;
    font-weight: bold;
    margin-bottom: 5px;
}
textarea {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
    font-family: inherit;
}
button {
    background: #007bff;
    color: white;
    border: none;
    padding: 10px 15px;
    cursor: pointer;
    border-radius: 4px;
}
button:disabled {
    background: #aaa;
}
.output {
    min-height: 20px;
    padding: 10px;
    background: #f1f1f1;
    border: 1px solid #ccc;
    border-radius: 4px;
    white-space: pre-wrap;
}
.result-row {
    display: flex;
    gap: 15px;
}
.result-row .result-box {
    flex: 1;
}
.hidden {
    display: none;
}
```

- [ ] **Step 3: Commit**

```bash
git add templates/index.html static/style.css
git commit -m "feat: add html and css templates for flask UI"
```

---

### Task 2: Cài đặt logic Javascript (Frontend)

**Files:**
- Create: `static/script.js`

**Interfaces:**
- Consumes: ID từ HTML trong Task 1, API backend `/api/analyze`.
- Produces: Cập nhật DOM.

- [ ] **Step 1: Write Vanilla JS fetch logic**

```javascript
document.getElementById('analyze-btn').addEventListener('click', async () => {
    const message = document.getElementById('message').value;
    if (!message.trim()) return;

    const btn = document.getElementById('analyze-btn');
    btn.disabled = true;
    btn.textContent = 'Analyzing...';
    
    document.getElementById('results').classList.remove('hidden');
    const outputs = ['summary', 'sentiment', 'action', 'response', 'duration'];
    outputs.forEach(id => document.getElementById(`out-${id}`).textContent = '...');

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        
        if (!response.ok) throw new Error('API request failed');
        
        const data = await response.json();
        
        document.getElementById('out-summary').textContent = data.summary || '';
        document.getElementById('out-sentiment').textContent = data.sentiment || '';
        document.getElementById('out-action').textContent = data.action || '';
        document.getElementById('out-response').textContent = data.response || '';
        document.getElementById('out-duration').textContent = data.duration || '';
    } catch (error) {
        alert('An error occurred during analysis.');
        console.error(error);
    } finally {
        btn.disabled = false;
        btn.textContent = 'Analyze';
    }
});
```

- [ ] **Step 2: Commit**

```bash
git add static/script.js
git commit -m "feat: add vanilla js client logic"
```

---

### Task 3: Backend Flask API & Testing

**Files:**
- Modify: `app.py`
- Modify: `requirements.txt`
- Create: `tests/test_app.py`

**Interfaces:**
- Consumes: `qwen_response` function từ `model.py`.
- Produces: Endpoint `POST /api/analyze` trả về JSON, và `GET /` render HTML.

- [ ] **Step 1: Write failing API test**

Create `tests/test_app.py`:
```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_api_analyze_empty(client):
    response = client.post('/api/analyze', json={'message': '   '})
    assert response.status_code == 400
```

- [ ] **Step 2: Thêm requirements**

Nếu chưa có `requirements.txt`, hãy tạo nó. Thêm dòng:
```text
flask
pytest
```
Chạy `pip install flask pytest`.

- [ ] **Step 3: Update `app.py` for Flask**

Replace `app.py` with:
```python
import time
from flask import Flask, render_template, request, jsonify

from config import SYSTEM_PROMPT
from model import qwen_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    message = data.get('message', '')
    
    if not message or not message.strip():
        return jsonify({"error": "Message is empty"}), 400

    start_time = time.time()
    try:
        result = qwen_response(SYSTEM_PROMPT, message)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
    duration = round(time.time() - start_time, 2)
    
    return jsonify({
        "summary": result.get("summary", ""),
        "sentiment": result.get("sentiment", ""),
        "action": result.get("action", ""),
        "response": result.get("response", ""),
        "duration": duration
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

- [ ] **Step 4: Run test to verify passes**

```bash
python -m pytest tests/test_app.py -v
```

- [ ] **Step 5: Commit**

```bash
git add app.py tests/test_app.py requirements.txt
git commit -m "feat: setup flask app and api endpoint"
```
