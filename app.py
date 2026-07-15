"""Flask web interface for the Shopee Help Center Assistant."""

import sys
import time
import logging

# Windows console encoding for Vietnamese
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from flask import Flask, render_template, request, jsonify

from modules.query_engine import create_rag_chain, query

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(stream=sys.stdout)],
)
logger = logging.getLogger(__name__)

# Flask App 
app = Flask(__name__)

# Initialize RAG chain when server starts
logger.info("Initializing RAG chain (may take a few minutes the first time)...")
rag_chain = create_rag_chain()
logger.info("RAG chain is ready!")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """Receive question and answer based on knowledge base."""
    data = request.get_json()
    question = data.get("message", "")

    if not question or not question.strip():
        return jsonify({"error": "Message is empty"}), 400

    start_time = time.time()
    try:
        result = query(rag_chain, question.strip())
    except Exception as e:
        logger.error(f"Query error: {e}")
        return jsonify({"error": str(e)}), 500

    duration = round(time.time() - start_time, 2)

    return jsonify({
        "answer": result["answer"],
        "sources": result["sources"],
        "duration": duration,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
