"""FastAPI web interface for the Shopee Help Center Assistant."""

import sys
import time
import logging

# Windows console encoding for Vietnamese
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

from modules.query_engine import create_rag_chain, query

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(stream=sys.stdout)],
)
logger = logging.getLogger(__name__)

# FastAPI App 
app = FastAPI(title="Shopee Help Center Assistant")

# Mount static files and setup templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize RAG chain when server starts
logger.info("Initializing RAG chain (may take a few minutes the first time)...")
rag_chain = create_rag_chain()
logger.info("RAG chain is ready!")

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/chat")
async def chat(data: ChatRequest):
    """Receive question and answer based on knowledge base."""
    question = data.message

    if not question or not question.strip():
        raise HTTPException(status_code=400, detail="Message is empty")

    start_time = time.time()
    try:
        # Assuming query is synchronous. In a real highly concurrent system, this could be run in a threadpool.
        result = query(rag_chain, question.strip())
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    duration = round(time.time() - start_time, 2)

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "duration": duration,
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
