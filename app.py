from flask import Flask, request, jsonify, render_template
from model import qwen_response
from config import SYSTEM_PROMPT
import time

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')  # Trang chat giao diện web


@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    user_message = data.get('message')  # Câu hỏi người dùng gửi lên

    if not user_message:
        return jsonify({"error": "Missing message"}), 400

    start_time = time.time()

    try:
        result = qwen_response(SYSTEM_PROMPT, user_message)  # Gọi model qwen, trả dict JSON
        result['duration'] = round(time.time() - start_time, 2)  # Thêm thời gian xử lý (giây)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
