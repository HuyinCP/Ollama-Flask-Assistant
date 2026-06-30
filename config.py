OLLAMA_HOST = "http://localhost:11434"

MODEL_ID = "qwen2.5:7b"

PARAMETERS = {
    "temperature": 0.5,   # 0: ổn định/chính xác, 1: sáng tạo hơn
    "num_predict": 256,   # số token tối đa sinh ra
    "top_p": 0.9,
}

# System prompt — điều khiển vai trò, ngôn ngữ và định dạng đầu ra của Agent
SYSTEM_PROMPT = (
    "You are an AI assistant helping with customer inquiries. "
    "Summarize the user's message, rate its sentiment from 0 to 100, "
    "recommend the next action to take, "
    "and provide a helpful and concise response. "
    "IMPORTANT: Always write ALL output fields (summary, action, response) in English, "
    "even if the user writes in another language. Never respond in Vietnamese, Chinese, or any other language."
)
