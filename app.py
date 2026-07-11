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
